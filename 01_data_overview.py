"""
Project 13: DataCo Supply Chain Delivery Delay Prediction
Module: 01_data_overview.py - Khám phá và Kiểm toán Chất lượng Dữ liệu Thô (Data Overview & Initial Audit)

"""

import os
import sys
from pathlib import Path

# Cấu hình UTF-8 cho console Windows
if sys.platform == "win32":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# =============================================================================
# CẤU HÌNH HẰNG SỐ & TIÊU CHUẨN SCHEMA
# =============================================================================
EXPECTED_ROWS = 180519
EXPECTED_COLS = 53

# Danh sách thuộc tính định danh cá nhân nhạy cảm (PII) cần bảo vệ nghiêm ngặt
PII_COLUMNS = [
    "Customer Email",
    "Customer Password",
    "Customer Fname",
    "Customer Lname",
    "Customer Street"
]

# Ký hiệu khuyết thiếu và nhiễu phổ biến cần kiểm toán
SUSPICIOUS_SYMBOLS = ["?", "-", "nan", "None", "unknown", "-1", "9999", "chÆ°a rÃµ"]


def get_safe_display_df(df: pd.DataFrame, n: int = 5) -> pd.DataFrame:
    """Tạo bản sao DataFrame với các cột PII được ẩn danh hóa (che giấu) để hiển thị an toàn."""
    df_safe = df.head(n).copy()
    for col in PII_COLUMNS:
        if col in df_safe.columns:
            df_safe[col] = "***MASKED_PII***"
    return df_safe


def load_raw_data(file_path: Path) -> pd.DataFrame:
    """
    Đọc dữ liệu CSV an toàn, tự động thử nghiệm danh sách encoding phổ biến.
    Không chỉnh sửa hoặc ghi đè lên dữ liệu gốc.
    """
    print(f"\n[BƯỚC 1] Bắt đầu đọc file dữ liệu: {file_path}")
    if not file_path.exists():
        # Thử tìm ở thư mục gốc nếu chưa có thư mục con
        fallback_path = Path("7_PJ13_2521001054_Nguyễn Lê Nhật Hạ.csv")
        if fallback_path.exists():
            print(f"-> Chuyển hướng sang file tại thư mục gốc: {fallback_path}")
            file_path = fallback_path
        else:
            raise FileNotFoundError(
                f"[LỖI NGHIÊM TRỌNG] Không tìm thấy file dữ liệu tại '{file_path}'. "
                f"Vui lòng đảm bảo file tồn tại trong thư mục data/raw/ hoặc thư mục làm việc."
            )

    encodings_to_try = ["utf-8-sig", "utf-8", "latin1", "cp1252"]
    df = None
    used_encoding = None

    for enc in encodings_to_try:
        try:
            print(f"-> Đang thử encoding: {enc}...")
            # Đọc ban đầu với dtype='string' để bảo toàn nguyên vẹn mọi ký tự nhiễu thô
            df = pd.read_csv(file_path, encoding=enc, low_memory=False, dtype="string")
            used_encoding = enc
            print(f"-> [THÀNH CÔNG] Đọc file thành công với encoding: '{enc}'")
            break
        except UnicodeDecodeError:
            continue
        except Exception as e:
            print(f"-> Thử {enc} thất bại do: {e}")
            continue

    if df is None:
        raise ValueError("[LỖI] Không thể đọc file bằng bất kỳ encoding nào trong danh sách hỗ trợ.")

    return df


def validate_schema(df: pd.DataFrame) -> dict:
    """
    Kiểm tra số dòng, số cột và đối chiếu với cấu trúc chuẩn của DataCo (180.519 dòng x 53 cột).
    """
    print("\n[BƯỚC 2] Kiểm tra và đối chiếu Schema chuẩn:")
    actual_rows, actual_cols = df.shape
    print(f"-> Kích thước thực tế: {actual_rows:,} dòng x {actual_cols} cột")
    print(f"-> Kích thước chuẩn:   {EXPECTED_ROWS:,} dòng x {EXPECTED_COLS} cột")

    row_match = (actual_rows == EXPECTED_ROWS)
    col_match = (actual_cols == EXPECTED_COLS)

    if row_match and col_match:
        print("-> [XÁC NHẬN] Dữ liệu khớp 100% với cấu trúc quy chuẩn DataCo Supply Chain.")
    else:
        print(f"-> [CẢNH BÁO] Dữ liệu có sự sai lệch kích thước (Dòng khớp: {row_match}, Cột khớp: {col_match}).")

    return {
        "actual_rows": actual_rows,
        "actual_cols": actual_cols,
        "row_match": row_match,
        "col_match": col_match
    }


def inspect_data_structure(df: pd.DataFrame):
    """In cấu trúc dữ liệu, 5 dòng đầu an toàn và thông tin kiểu dữ liệu."""
    print("\n[BƯỚC 3] Khám phá cấu trúc dữ liệu tổng quan:")
    print("--- 5 DÒNG ĐẦU TIÊN (ĐÃ ẨN DANH HÓA THÔNG TIN CÁ NHÂN PII) ---")
    safe_head = get_safe_display_df(df, 5)
    print(safe_head.iloc[:, :8].to_string())
    print("\n--- THỐNG KÊ CÁC KIỂU DỮ LIỆU BAN ĐẦU (DTYPES) ---")
    dtype_counts = df.dtypes.value_counts()
    for dt, count in dtype_counts.items():
        print(f"  + Kiểu {dt}: {count} cột")


def audit_missing_and_suspicious_symbols(df: pd.DataFrame) -> pd.DataFrame:
    """
    Thống kê giá trị Null và các ký hiệu nghi vấn: '?', '-', 'nan', 'None', 'unknown', '-1', '9999'.
    Tính tỷ lệ phần trăm từng ký hiệu theo từng cột và trên toàn bộ dữ liệu.
    """
    print("\n[BƯỚC 4] Kiểm toán giá trị thiếu (Missing) và ký hiệu nhiễu:")
    total_cells = df.shape[0] * df.shape[1]
    
    # 1. Thống kê cấp độ toàn bộ dataset
    standard_nulls = df.isna().sum().sum()
    print(f"-> Tổng số ô giá trị NaN tiêu chuẩn: {standard_nulls:,} ô ({standard_nulls / total_cells * 100:.2f}%)")

    audit_records = []
    
    for col in df.columns:
        s = df[col].astype("string").str.strip()
        col_null_count = s.isna().sum()
        col_null_pct = (col_null_count / len(df)) * 100
        
        # Đếm các ký hiệu nhiễu
        symbol_counts = {}
        for sym in SUSPICIOUS_SYMBOLS:
            cnt = int(s.str.lower().eq(sym.lower()).fillna(False).sum())
            symbol_counts[sym] = cnt
            
        total_suspicious = sum(symbol_counts.values())
        total_dirty = col_null_count + total_suspicious
        total_dirty_pct = (total_dirty / len(df)) * 100
        
        rec = {
            "Tên Cột (Column Name)": col,
            "Số Lượng Null": col_null_count,
            "Tỷ Lệ Null (%)": round(col_null_pct, 2),
            "Ký hiệu '?'": symbol_counts["?"],
            "Ký hiệu '-'": symbol_counts["-"],
            "Ký hiệu 'unknown'": symbol_counts["unknown"],
            "Ký hiệu '-1'": symbol_counts["-1"],
            "Ký hiệu '9999'": symbol_counts["9999"],
            "Tổng Lượng Bất Thường": total_dirty,
            "Tỷ Lệ Bất Thường Tổng (%)": round(total_dirty_pct, 2)
        }
        audit_records.append(rec)
        
    audit_df = pd.DataFrame(audit_records)
    
    # In Top 10 cột có tỷ lệ giá trị thiếu/nhiễu cao nhất
    top_dirty = audit_df.sort_values(by="Tỷ Lệ Bất Thường Tổng (%)", ascending=False).head(10)
    print("\n--- TOP 10 CỘT CÓ TỶ LỆ DỮ LIỆU THIẾU / NHIỄU CAO NHẤT ---")
    print(top_dirty[["Tên Cột (Column Name)", "Số Lượng Null", "Tỷ Lệ Null (%)", "Tổng Lượng Bất Thường", "Tỷ Lệ Bất Thường Tổng (%)"]].to_string(index=False))
    
    return audit_df


def audit_duplicates_and_keys(df: pd.DataFrame) -> dict:
    """
    Kiểm tra số dòng trùng hoàn toàn, trùng Order Id, trùng Order Item Id.
    Phân tích quan hệ khóa chính và đơn vị quan sát.
    """
    print("\n[BƯỚC 5] Kiểm toán tính trùng lặp và các khóa thực thể:")
    exact_duplicates = int(df.duplicated().sum())
    print(f"-> Số dòng trùng lặp 100% hoàn toàn: {exact_duplicates:,} dòng")

    order_id_unique = df["Order Id"].nunique(dropna=True) if "Order Id" in df.columns else None
    order_id_dups = df["Order Id"].duplicated().sum() if "Order Id" in df.columns else None
    
    item_id_unique = df["Order Item Id"].nunique(dropna=True) if "Order Item Id" in df.columns else None
    item_id_dups = df["Order Item Id"].duplicated().sum() if "Order Item Id" in df.columns else None
    
    print(f"-> Khóa 'Order Id':      {order_id_unique:,} giá trị duy nhất | {order_id_dups:,} lần xuất hiện lặp lại")
    print(f"-> Khóa 'Order Item Id': {item_id_unique:,} giá trị duy nhất | {item_id_dups:,} dòng trùng lặp")
    
    print("-> [GHI CHÚ NGHIỆP VỤ] Đơn vị quan sát của DataCo là một dòng mục hàng (Order Item Transaction).")
    print("   Việc 'Order Id' lặp lại là hoàn toàn tự nhiên vì một đơn hàng thường bao gồm nhiều sản phẩm con.")
    print("   Ngược lại, 'Order Item Id' đóng vai trò khóa chính kỹ thuật và phải mang tính duy nhất.")

    return {
        "exact_duplicates": exact_duplicates,
        "order_id_unique": order_id_unique,
        "order_id_dups": order_id_dups,
        "item_id_unique": item_id_unique,
        "item_id_dups": item_id_dups
    }


def analyze_target_and_core_features(df: pd.DataFrame):
    """
    Phân tích sơ bộ phân bố biến mục tiêu Late_delivery_risk và các biến nghiệp vụ cốt lõi:
    Shipping Mode, Order Region, Market.
    """
    print("\n[BƯỚC 6] Khảo sát Biến mục tiêu & Biến nghiệp vụ cốt lõi:")
    
    # 1. Biến mục tiêu Late_delivery_risk
    if "Late_delivery_risk" in df.columns:
        target_s = df["Late_delivery_risk"].astype("string").str.strip()
        val_counts = target_s.value_counts(dropna=False)
        print("--- PHÂN BỐ GIÁ TRỊ THÔ CỦA 'Late_delivery_risk' ---")
        print(val_counts.to_string())
        
        # Đếm các nhãn hợp lệ (0, 1) và nhãn dơ (nhiễu đơn vị VND, USD, ?, v.v.)
        valid_0 = int(target_s.eq("0").sum())
        valid_1 = int(target_s.eq("1").sum())
        invalid_or_missing = len(df) - (valid_0 + valid_1)
        
        total_valid = valid_0 + valid_1
        print(f"-> Nhãn hợp lệ '0' (Đúng hạn): {valid_0:,} ({valid_0 / total_valid * 100:.2f}%)" if total_valid > 0 else "")
        print(f"-> Nhãn hợp lệ '1' (Trễ hạn):  {valid_1:,} ({valid_1 / total_valid * 100:.2f}%)" if total_valid > 0 else "")
        print(f"-> Nhãn nhiễu / khuyết:         {invalid_or_missing:,} ({invalid_or_missing / len(df) * 100:.2f}%)")

    # 2. Phân bố Shipping Mode
    if "Shipping Mode" in df.columns:
        print("\n--- PHÂN BỐ PHƯƠNG THỨC VẬN CHUYỂN ('Shipping Mode') ---")
        sm_counts = df["Shipping Mode"].value_counts(dropna=False)
        print(sm_counts.to_string())

    # 3. Phân bố Market
    if "Market" in df.columns:
        print("\n--- PHÂN BỐ THỊ TRƯỜNG ('Market') ---")
        m_counts = df["Market"].value_counts(dropna=False)
        print(m_counts.to_string())


def audit_privacy_pii(df: pd.DataFrame) -> pd.DataFrame:
    """
    Kiểm tra bảo mật PII: Chỉ xuất thông tin tổng hợp, tuyệt đối không xuất giá trị cụ thể.
    """
    print("\n[BƯỚC 7] Kiểm toán Bảo vệ Quyền riêng tư (Data Privacy & PII Compliance):")
    pii_records = []
    
    for col in PII_COLUMNS:
        if col in df.columns:
            s = df[col].astype("string")
            rec = {
                "Thuộc Tính PII": col,
                "Kiểu Dữ Liệu": str(df[col].dtype),
                "Số Lượng Khuyết": int(s.isna().sum()),
                "Tỷ Lệ Khuyết (%)": round(s.isna().mean() * 100, 2),
                "Số Giá Trị Độc Nhất (Cardinality)": int(s.nunique(dropna=True)),
                "Tuân Thủ GDPR/Bảo Mật": "Cần Loại Bỏ Khỏi Không Gian Đặc Trưng"
            }
            pii_records.append(rec)
            
    pii_df = pd.DataFrame(pii_records)
    print(pii_df.to_string(index=False))
    return pii_df


def export_audit_reports(df: pd.DataFrame, audit_df: pd.DataFrame, reports_dir: Path):
    """
    Xuất 2 tệp báo cáo tổng hợp chất lượng:
    - reports/data_overview.csv
    - reports/data_quality_before.csv
    """
    print(f"\n[BƯỚC 8] Xuất các báo cáo kiểm toán vào thư mục '{reports_dir}':")
    reports_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. Báo cáo Tổng quan (reports/data_overview.csv)
    overview_records = []
    for col in df.columns:
        s = df[col].astype("string")
        # Kiểm tra nếu là PII thì không tính min/max
        if col in PII_COLUMNS:
            min_val = "[MASKED_PII]"
            max_val = "[MASKED_PII]"
        else:
            clean_s = s.dropna()
            min_val = clean_s.min() if len(clean_s) > 0 else "NA"
            max_val = clean_s.max() if len(clean_s) > 0 else "NA"
            
        overview_records.append({
            "column_name": col,
            "data_type": str(df[col].dtype),
            "total_rows": len(df),
            "null_count": int(df[col].isna().sum()),
            "null_percentage": round(df[col].isna().mean() * 100, 2),
            "unique_values": int(s.nunique(dropna=True)),
            "is_pii": col in PII_COLUMNS,
            "sample_min": str(min_val)[:50],
            "sample_max": str(max_val)[:50]
        })
    overview_df = pd.DataFrame(overview_records)
    overview_path = reports_dir / "data_overview.csv"
    overview_df.to_csv(overview_path, index=False, encoding="utf-8-sig")
    print(f"-> Đã xuất: {overview_path}")
    
    # 2. Báo cáo Chi tiết Chất lượng Dữ liệu Thô (reports/data_quality_before.csv)
    quality_records = []
    for _, row in audit_df.iterrows():
        col_name = row["Tên Cột (Column Name)"]
        null_cnt = row["Số Lượng Null"]
        null_pct = row["Tỷ Lệ Null (%)"]
        dirty_cnt = row["Tổng Lượng Bất Thường"]
        
        # Phân loại vấn đề kỹ thuật
        issues = []
        if null_cnt > 0:
            issues.append("Missing")
        if (dirty_cnt - null_cnt) > 0:
            issues.append("Invalid Format / Symbols")
        if col_name in PII_COLUMNS:
            issues.append("Privacy / PII Risk")
        if col_name == "Late_delivery_risk":
            issues.append("Label Noise / SCM Logic Required")
            
        issue_str = ", ".join(issues) if issues else "Clean Format"
        
        # Đề xuất xử lý
        if col_name in PII_COLUMNS:
            recommendation = "Loại bỏ hoàn toàn (Drop PII) theo chuẩn GDPR."
        elif col_name == "Late_delivery_risk":
            recommendation = "Khôi phục theo Quy tắc Vàng SCM: (real > scheduled) & Delivery Status."
        elif null_pct > 70:
            recommendation = "Cân nhắc loại bỏ do khuyết thiếu quá lớn (>70%)."
        elif "Invalid Format / Symbols" in issue_str:
            recommendation = "Lọc số Regex, loại bỏ đơn vị tiền tệ/khối lượng, điền median theo nhóm."
        else:
            recommendation = "Chuẩn hóa khoảng trắng, ép kiểu dữ liệu tối ưu bộ nhớ."
            
        quality_records.append({
            "Tên Cột (Column Name)": col_name,
            "Số Lượng Null": null_cnt,
            "Tỷ Lệ Null (%)": null_pct,
            "Số Ký Hiệu Dơ Phát Hiện": dirty_cnt - null_cnt,
            "Tổng Điểm Dơ": dirty_cnt,
            "Phân Loại Lỗi (Issue Type)": issue_str,
            "Đề Xuất Xử Lý Cho 02_data_cleaning.py": recommendation
        })
        
    quality_df = pd.DataFrame(quality_records)
    quality_path = reports_dir / "data_quality_before.csv"
    quality_df.to_csv(quality_path, index=False, encoding="utf-8-sig")
    print(f"-> Đã xuất: {quality_path}")


def main():
    print("=" * 80)
    print(" PROJECT 13: DATACO BIG SUPPLY CHAIN DELIVERY DELAY PREDICTION")
    print(" BÁO CÁO TOÀN DIỆN KHÁM PHÁ VÀ KIỂM TOÁN CHẤT LƯỢNG DỮ LIỆU THÔ (DATA OVERVIEW)")
    print("=" * 80)
    
    raw_path = Path("data/raw/7_PJ13_2521001054_Nguyễn Lê Nhật Hạ.csv")
    reports_dir = Path("reports")
    
    # 1. Đọc dữ liệu
    df = load_raw_data(raw_path)
    
    # 2. Kiểm tra Schema
    validate_schema(df)
    
    # 3. Kiểm tra cấu trúc & kiểu
    inspect_data_structure(df)
    
    # 4. Kiểm toán missing & ký hiệu nghi vấn
    audit_df = audit_missing_and_suspicious_symbols(df)
    
    # 5. Kiểm toán trùng lặp & khóa
    audit_duplicates_and_keys(df)
    
    # 6. Khảo sát biến mục tiêu & biến nghiệp vụ
    analyze_target_and_core_features(df)
    
    # 7. Kiểm toán PII
    audit_privacy_pii(df)
    
    # 8. Xuất báo cáo
    export_audit_reports(df, audit_df, reports_dir)
    
    print("\n" + "=" * 80)
    print(" HOÀN TẤT THỰC THI 01_DATA_OVERVIEW.PY THÀNH CÔNG!")
    print(" Các báo cáo đã được lưu vào thư mục reports/ sẵn sàng cho bước phân tích kế tiếp.")
    print("=" * 80)


if __name__ == "__main__":
    main()
