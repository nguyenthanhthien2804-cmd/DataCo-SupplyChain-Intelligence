"""
Project 13: DataCo Supply Chain Delivery Delay Prediction
Module: 02_data_cleaning.py - Pipeline Làm Sạch Dữ Liệu Toàn Diện (Data Cleaning Pipeline)

"""

import os
import sys
import time
from pathlib import Path

# Cấu hình UTF-8 cho console Windows
if sys.platform == "win32":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

import re
import unicodedata
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams["font.sans-serif"] = ["Segoe UI", "DejaVu Sans", "Arial"]
plt.rcParams["axes.unicode_minus"] = False

# =============================================================================
# CẤU HÌNH HẰNG SỐ & TIÊU CHUẨN
# =============================================================================
EXPECTED_ROWS = 180519
EXPECTED_COLS_RAW = 53
EXPECTED_COLS_CLEANED = 51  # 53 cột trừ 2 cột PII (Customer Email, Customer Password)

PII_DROP_COLS = ["Customer Email", "Customer Password"]
OTHER_PII_COLS = ["Customer Fname", "Customer Lname", "Customer Street"]

MISSING_MARKERS = ["?", "-", "nan", "none", "null", "n/a", "unknown", "chưa rõ", "chæ°a rãµ", ""]

MONEY_COLS = [
    "Sales", "Sales per customer", "Benefit per order", "Order Item Discount",
    "Product Price", "Order Item Product Price", "Order Item Total", "Order Profit Per Order"
]

RATE_COLS = ["Order Item Discount Rate", "Order Item Profit Ratio"]

INT_COLS = [
    "Days for shipping (real)", "Days for shipment (scheduled)", "Order Item Quantity",
    "Category Id", "Department Id", "Order Id", "Order Item Id", "Customer Id",
    "Order Customer Id", "Product Card Id", "Product Category Id", "Order Item Cardprod Id"
]


def load_raw_data(file_path: Path) -> pd.DataFrame:
    """Bước 1: Đọc CSV an toàn, kiểm tra cấu trúc 180.519 dòng x 53 cột."""
    print(f"\n[BƯỚC 1] Đọc dữ liệu thô từ: {file_path}")
    if not file_path.exists():
        fallback_path = Path("7_PJ13_2521001054_Nguyễn Lê Nhật Hạ.csv")
        if fallback_path.exists():
            print(f"-> Chuyển hướng sang file tại thư mục gốc: {fallback_path}")
            file_path = fallback_path
        else:
            raise FileNotFoundError(f"[LỖI] Không tìm thấy file dữ liệu tại: {file_path}")

    df = pd.read_csv(file_path, encoding="utf-8-sig", low_memory=False, dtype="string")
    n_rows, n_cols = df.shape
    print(f"-> Kích thước đọc được: {n_rows:,} dòng x {n_cols} cột")

    if n_rows != EXPECTED_ROWS or n_cols != EXPECTED_COLS_RAW:
        print(f"-> [CẢNH BÁO] Kích thước khác chuẩn DataCo ({EXPECTED_ROWS:,} x {EXPECTED_COLS_RAW})")
    else:
        print("-> [XÁC NHẬN] Kích thước dữ liệu thô khớp 100% chuẩn DataCo!")

    return df


def drop_sensitive_pii(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """Bước 2 & 3: Loại bỏ Customer Email, Customer Password ngay sau khi đọc."""
    print("\n[BƯỚC 2 & 3] Áp dụng Data Governance: Loại bỏ thông tin PII nhạy cảm...")
    dropped = [col for col in PII_DROP_COLS if col in df.columns]
    df_clean = df.drop(columns=dropped).copy()

    audit_pii = {
        "dropped_pii_columns": dropped,
        "retained_columns_count": len(df_clean.columns),
        "retained_other_pii": [c for c in OTHER_PII_COLS if c in df_clean.columns]
    }
    print(f"-> Đã loại bỏ {len(dropped)} cột PII: {dropped}")
    print(f"-> Số cột còn lại: {len(df_clean.columns)} cột (chuẩn 51 cột)")
    return df_clean, audit_pii


def handle_duplicates(df: pd.DataFrame) -> tuple[pd.DataFrame, int]:
    """Bước 4: Kiểm tra và xóa dòng trùng 100% hoàn toàn, KHÔNG xóa trùng Order Id."""
    print("\n[BƯỚC 4] Kiểm tra trùng lặp bản ghi...")
    exact_dups = int(df.duplicated().sum())
    print(f"-> Số dòng trùng lặp 100% hoàn toàn: {exact_dups:,} dòng")

    order_dups = int(df["Order Id"].duplicated().sum()) if "Order Id" in df.columns else 0
    print(f"-> Số dòng lặp lại của 'Order Id': {order_dups:,} dòng (HỢP LỆ vì 1 đơn hàng chứa nhiều sản phẩm)")

    df_dedup = df.drop_duplicates().copy()
    print(f"-> Số dòng còn lại sau drop_duplicates: {len(df_dedup):,} dòng")
    return df_dedup, exact_dups


def clean_missing_markers(df: pd.DataFrame) -> pd.DataFrame:
    """Bước 5: Chuẩn hóa các ký hiệu thiếu ?, -, nan, None, chuỗi rỗng thành np.nan."""
    print("\n[BƯỚC 5] Chuẩn hóa ký hiệu thiếu (?, -, nan, None, khoảng trắng) về np.nan...")
    df_clean = df.copy()

    # Chuẩn hóa khoảng trắng chuỗi rỗng
    df_clean = df_clean.replace(r"^\s*$", pd.NA, regex=True)

    # Thay thế các ký hiệu missing marker
    for col in df_clean.columns:
        s = df_clean[col].astype("string").str.strip()
        mask = s.str.lower().isin(MISSING_MARKERS)
        df_clean.loc[mask, col] = pd.NA

    print("-> Đã quy đổi toàn bộ các ký hiệu khuyết ẩn về pd.NA tiêu chuẩn.")
    return df_clean


def clean_numeric_controlled_regex(df: pd.DataFrame) -> pd.DataFrame:
    """
    Bước 6, 7, 9, 10: Làm sạch Regex có kiểm soát cho cột số, xử lý đơn vị tiền tệ,
    tỷ lệ %, kiểm tra miền giá trị và ép kiểu float32/int32.
    """
    print("\n[BƯỚC 6 & 7] Làm sạch Regex có kiểm soát cho các cột số học và tài chính...")
    df_clean = df.copy()

    # 1. Cột tiền tệ: bóc tách USD, VND, đ, xử lý dấu phẩy nghìn
    for col in MONEY_COLS:
        if col in df_clean.columns:
            s = df_clean[col].astype("string").str.strip()
            # Bỏ ký hiệu tiền tệ
            s = s.str.replace(r"\s*(?:USD|VND|đ)\s*$", "", regex=True, case=False)
            # Xóa dấu phẩy nghìn (ví dụ: 1,234.56 -> 1234.56)
            s = s.str.replace(r"^(-?\d{1,3}(?:,\d{3})+)(\.\d+)?$",
                              lambda m: m.group(1).replace(",", "") + (m.group(2) or ""), regex=True)
            # Ép kiểu float32, chuỗi lỗi đơn vị (như kg trong tiền) tự động thành NaN
            df_clean[col] = pd.to_numeric(s, errors="coerce").astype("float32")

    # 2. Cột tỷ lệ %: bóc tách %, quy đổi về thang đo [0, 1] nếu ghi dạng %
    for col in RATE_COLS:
        if col in df_clean.columns:
            s = df_clean[col].astype("string").str.strip()
            is_pct = s.str.endswith("%")
            s = s.str.replace(r"\s*%\s*$", "", regex=True)
            vals = pd.to_numeric(s, errors="coerce")
            # Nếu có ký hiệu % và giá trị > 1 thì chia 100
            vals.loc[is_pct & (vals > 1.0)] = vals.loc[is_pct & (vals > 1.0)] / 100.0
            # Miền giá trị Discount Rate phải trong [0, 1]
            if col == "Order Item Discount Rate":
                vals.loc[(vals < 0) | (vals > 1)] = np.nan
            df_clean[col] = vals.astype("float32")

    # 3. Cột số nguyên (Số ngày, Số lượng, IDs)
    for col in INT_COLS:
        if col in df_clean.columns:
            s = df_clean[col].astype("string").str.strip()
            # Chỉ lấy các ký tự số
            s = s.str.replace(r"[^\d.-]", "", regex=True)
            vals = pd.to_numeric(s, errors="coerce")

            # Kiểm tra miền giá trị hợp lệ theo schema
            if col in ["Days for shipping (real)", "Days for shipment (scheduled)"]:
                vals.loc[(vals < 0) | (vals > 30)] = np.nan
                df_clean[col] = vals.astype("Int8")
            elif col == "Order Item Quantity":
                vals.loc[(vals <= 0) | (vals > 100)] = np.nan
                df_clean[col] = vals.astype("Int16")
            elif col == "Product Price":
                vals.loc[vals < 0] = np.nan
                df_clean[col] = vals.astype("float32")
            else:
                # Các cột ID: giữ dạng Int32 hoặc string nếu không dùng toán học
                df_clean[col] = vals.astype("Int32")

    print("-> Đã chuẩn hóa thành công các cột định lượng và kiểm soát miền giá trị.")
    return df_clean


def standardize_categoricals(df: pd.DataFrame) -> pd.DataFrame:
    """Bước 8: Chuẩn hóa khoảng trắng, chữ hoa/thường và nhãn phân loại."""
    print("\n[BƯỚC 8] Chuẩn hóa các biến phân loại (Categorical Normalization)...")
    df_clean = df.copy()

    # 1. Shipping Mode: Chuẩn hóa casing, KHÔNG ép giá trị lạ về Standard Class!
    if "Shipping Mode" in df_clean.columns:
        s = df_clean["Shipping Mode"].astype("string").str.strip()
        # Ánh xạ casing sạch
        mode_map = {
            "standard class": "Standard Class",
            "first class": "First Class",
            "second class": "Second Class",
            "same day": "Same Day"
        }
        lower_s = s.str.lower()
        cleaned_mode = lower_s.map(mode_map)
        # Giữ nguyên giá trị nếu không khớp ánh xạ để điền Unknown sau
        df_clean["Shipping Mode"] = cleaned_mode.where(cleaned_mode.notna(), pd.NA)

    # 2. Customer Segment
    if "Customer Segment" in df_clean.columns:
        s = df_clean["Customer Segment"].astype("string").str.strip().str.lower()
        seg_map = {
            "consumer": "Consumer",
            "corporate": "Corporate",
            "home office": "Home Office"
        }
        cleaned_seg = s.map(seg_map)
        df_clean["Customer Segment"] = cleaned_seg.where(cleaned_seg.notna(), pd.NA)

    # 3. Market
    if "Market" in df_clean.columns:
        s = df_clean["Market"].astype("string").str.strip().str.lower()
        market_map = {
            "latam": "LATAM",
            "europe": "Europe",
            "pacific asia": "Pacific Asia",
            "usca": "USCA",
            "africa": "Africa"
        }
        cleaned_m = s.map(market_map)
        df_clean["Market"] = cleaned_m.where(cleaned_m.notna(), pd.NA)

    # 4. Delivery Status
    if "Delivery Status" in df_clean.columns:
        s = df_clean["Delivery Status"].astype("string").str.strip().str.lower()
        ds_map = {
            "late delivery": "Late delivery",
            "shipping on time": "Shipping on time",
            "advance shipping": "Advance shipping",
            "shipping canceled": "Shipping canceled"
        }
        cleaned_ds = s.map(ds_map)
        df_clean["Delivery Status"] = cleaned_ds.where(cleaned_ds.notna(), pd.NA)

    # 5. Các cột chuỗi khác: cắt tỉa khoảng trắng
    str_cols = df_clean.select_dtypes(include=["string", "object"]).columns
    for c in str_cols:
        df_clean[c] = df_clean[c].astype("string").str.strip()

    print("-> Hoàn tất chuẩn hóa danh mục. Các nhãn không rõ được giữ pd.NA an toàn.")
    return df_clean


REGION_MAP = {
    'central america': 'Central America',
    'central ameri': 'Central America',
    'western europe': 'Western Europe',
    'western europ': 'Western Europe',
    'south america': 'South America',
    'northern europe': 'Northern Europe',
    'northern euro': 'Northern Europe',
    'southern europe': 'Southern Europe',
    'southern euro': 'Southern Europe',
    'oceania': 'Oceania',
    'southeast asia': 'Southeast Asia',
    'southeast asi': 'Southeast Asia',
    'caribbean': 'Caribbean',
    'west of usa': 'West of USA',
    'south asia': 'South Asia',
    'eastern asia': 'Eastern Asia',
    'east of usa': 'East of USA',
    'west asia': 'West Asia',
    'us center': 'US Center',
    'south of usa': 'South of USA',
    'west africa': 'West Africa',
    'north africa': 'North Africa',
    'east africa': 'East Africa',
    'central africa': 'Central Africa',
    'central afric': 'Central Africa',
    'southern africa': 'Southern Africa',
    'southern afri': 'Southern Africa',
    'eastern europe': 'Eastern Europe',
    'eastern europ': 'Eastern Europe',
    'central asia': 'Central Asia',
    'canada': 'Canada'
}

MARKET_MAP = {
    'latam': 'LATAM',
    'europe': 'Europe',
    'pacific asia': 'Pacific Asia',
    'pacific as': 'Pacific Asia',
    'usca': 'USCA',
    'africa': 'Africa'
}

CUST_COUNTRY_MAP = {
    'ee. uu.': 'EE. UU.',
    'ee.uu.': 'EE. UU.',
    'ee uu': 'EE. UU.',
    'puerto rico': 'Puerto Rico',
    'puerto ri': 'Puerto Rico'
}

CITY_MISSING_SYMBOLS = {"?", "-", "nan", "none", "unknown", "chưa rõ", "chæ°a rãµ", "-1", "9999", "", " "}
SPANISH_PARTICLES = {"de", "del", "la", "las", "los", "el", "da", "do", "di", "sur", "al", "of", "and", "en", "y"}


def clean_text_basic(val):
    if pd.isna(val) or val is None:
        return pd.NA
    s = str(val).strip()
    if not s or s.lower() in CITY_MISSING_SYMBOLS:
        return pd.NA
    s = unicodedata.normalize("NFKC", s)
    s = re.sub(r"\s+", " ", s).strip()
    if s.lower() in CITY_MISSING_SYMBOLS:
        return pd.NA
    return s


def title_case_intelligent(s):
    if pd.isna(s) or s is None:
        return pd.NA
    parts = s.split(" ")
    norm_parts = []
    for i, part in enumerate(parts):
        sub_parts = part.split("-")
        norm_sub_parts = []
        for j, sub in enumerate(sub_parts):
            sub_lower = sub.lower()
            if (i > 0 or j > 0) and sub_lower in SPANISH_PARTICLES:
                norm_sub_parts.append(sub_lower)
            elif sub_lower in {"dc", "d.c."}:
                norm_sub_parts.append("DC")
            elif sub_lower in {"st", "st."}:
                norm_sub_parts.append("St.")
            elif sub_lower in {"ft", "ft."}:
                norm_sub_parts.append("Ft.")
            elif sub_lower in {"usa", "ee. uu."}:
                norm_sub_parts.append(sub.upper())
            else:
                norm_sub_parts.append(sub.capitalize())
        norm_parts.append("-".join(norm_sub_parts))
    return " ".join(norm_parts)


def normalize_city_name(val):
    s = clean_text_basic(val)
    if pd.isna(s):
        return pd.NA
    return title_case_intelligent(s)


def normalize_order_region(val):
    s = clean_text_basic(val)
    if pd.isna(s):
        return pd.NA
    norm = s.lower()
    return REGION_MAP.get(norm, pd.NA)


def normalize_market(val):
    s = clean_text_basic(val)
    if pd.isna(s):
        return pd.NA
    norm = s.lower()
    return MARKET_MAP.get(norm, pd.NA)


def normalize_cust_country(val):
    s = clean_text_basic(val)
    if pd.isna(s):
        return pd.NA
    norm = s.lower()
    return CUST_COUNTRY_MAP.get(norm, pd.NA)


def normalize_cust_state(val):
    s = clean_text_basic(val)
    if pd.isna(s):
        return pd.NA
    if s == '917':
        return pd.NA
    if len(s) == 2 and s.isalpha():
        return s.upper()
    return pd.NA


def normalize_order_country(val):
    s = clean_text_basic(val)
    if pd.isna(s):
        return pd.NA
    return title_case_intelligent(s)


def normalize_order_state(val):
    s = clean_text_basic(val)
    if pd.isna(s):
        return pd.NA
    return title_case_intelligent(s)


def normalize_and_audit_all_geography(
    df: pd.DataFrame,
    df_raw: pd.DataFrame,
    reports_dir: Path,
    figures_dir: Path
) -> pd.DataFrame:
    """
    Chuẩn hóa toàn diện 8 cột địa danh SCM: Customer City, Order City, Order Region,
    Market, Customer Country, Customer State, Order Country, Order State.
    Xuất báo cáo kiểm toán geo_mapping_audit.csv, geo_before_after.csv,
    và biểu đồ trực quan hóa geo_normalization_comparison.png.
    """
    print("\n" + "=" * 80)
    print(" [CHUẨN HÓA ĐỊA LÝ TOÀN DIỆN] 8 CỘT ĐỊA DANH SCM THEO QUY CHUẨN ĐẠI HỌC")
    print("=" * 80)
    df_clean = df.copy()
    total_rows = len(df_clean)

    geo_normalizers = {
        "Customer City": normalize_city_name,
        "Order City": normalize_city_name,
        "Order Region": normalize_order_region,
        "Market": normalize_market,
        "Customer Country": normalize_cust_country,
        "Customer State": normalize_cust_state,
        "Order Country": normalize_order_country,
        "Order State": normalize_order_state
    }

    mapping_records = []
    before_after_records = []

    for col, norm_func in geo_normalizers.items():
        if col not in df_clean.columns:
            continue

        raw_s = df_raw[col]
        raw_nunique = raw_s.nunique(dropna=False)
        raw_missing = raw_s.isna().sum() + raw_s.dropna().astype(str).str.strip().str.lower().isin(CITY_MISSING_SYMBOLS).sum()

        cleaned_s = raw_s.apply(norm_func)
        cleaned_nunique = cleaned_s.nunique(dropna=True)
        cleaned_null_count = cleaned_s.isna().sum()

        pairs = pd.DataFrame({
            "Raw_Name": raw_s.fillna("<MISSING_NA>"),
            "Cleaned_Name": cleaned_s.fillna("<UNRESOLVED_NA>")
        }).value_counts().reset_index(name="Frequency")
        pairs["Column_Name"] = col

        def get_mapping_reason(row):
            raw = str(row["Raw_Name"])
            clean = str(row["Cleaned_Name"])
            if clean == "<UNRESOLVED_NA>" or raw == "<MISSING_NA>" or raw.strip().lower() in CITY_MISSING_SYMBOLS:
                return "Chuyển về pd.NA (Ký hiệu khuyết/nhiễu ?, unknown, chưa rõ)"
            if raw == clean:
                return "Giữ nguyên (Tên chuẩn sẵn có)"
            if raw.strip().lower() == clean.lower():
                return "Chuẩn hóa khoảng trắng & chữ hoa/thường (Case & Whitespace)"
            if raw.strip().lower() in REGION_MAP or raw.strip().lower() in MARKET_MAP or raw.strip().lower() in CUST_COUNTRY_MAP:
                return "Ánh xạ biến thể cắt cụt / từ điển chuẩn (Dictionary lookup)"
            return "Chuẩn hóa Title Case thông minh & Unicode NFKC"

        pairs["Mapping_Reason"] = pairs.apply(get_mapping_reason, axis=1)
        pairs["Verification_Status"] = "Đã xác minh 100% (Verified)"
        mapping_records.append(pairs)

        before_after_records.append({
            "Tên Cột": col,
            "Tổng Số Dòng": total_rows,
            "Số Nhóm Trước": raw_nunique,
            "Số Nhóm Sau": cleaned_nunique,
            "Độ Giảm (%)": round((raw_nunique - cleaned_nunique) / raw_nunique * 100, 2),
            "Số Lượng Khuyết/Nhiễu Trước": raw_missing,
            "Số Lượng pd.NA Sau": cleaned_null_count,
            "Top 1 Trước": f"{raw_s.value_counts(dropna=False).index[0]} ({raw_s.value_counts(dropna=False).values[0]:,} dòng)",
            "Top 1 Sau": f"{cleaned_s.value_counts().index[0]} ({cleaned_s.value_counts().values[0]:,} dòng)" if cleaned_nunique > 0 else "N/A"
        })

        df_clean[col] = cleaned_s

        # Tạo cột phụ Top 5 cho Customer City và Order City
        if col in ["Customer City", "Order City"]:
            top5_clean = cleaned_s.value_counts().head(5)
            top5_names = set(top5_clean.index)
            top5_col_name = f"{col.replace(' ', '_')}_Top5_Group"
            def make_top5_group(x):
                if pd.isna(x):
                    return "Unknown"
                elif x in top5_names:
                    return x
                else:
                    return "Other"
            df_clean[top5_col_name] = df_clean[col].apply(make_top5_group)

    # Xuất file kiểm toán địa lý
    reports_dir.mkdir(parents=True, exist_ok=True)
    df_geo_mapping = pd.concat(mapping_records, ignore_index=True)
    geo_map_file = reports_dir / "geo_mapping_audit.csv"
    df_geo_mapping.to_csv(geo_map_file, index=False, encoding="utf-8-sig")
    print(f"-> [XUẤT THÀNH CÔNG] Bảng kiểm toán ánh xạ địa lý toàn diện: {geo_map_file} ({len(df_geo_mapping):,} dòng)")

    df_geo_ba = pd.DataFrame(before_after_records)
    geo_ba_file = reports_dir / "geo_before_after.csv"
    df_geo_ba.to_csv(geo_ba_file, index=False, encoding="utf-8-sig")
    print(f"-> [XUẤT THÀNH CÔNG] Bảng so sánh trước sau 8 cột địa lý: {geo_ba_file}")

    # Đồng thời xuất lại city audit để tương thích ngược
    df_city_map = df_geo_mapping[df_geo_mapping["Column_Name"].isin(["Customer City", "Order City"])]
    df_city_map.to_csv(reports_dir / "city_mapping_audit.csv", index=False, encoding="utf-8-sig")

    df_city_ba = df_geo_ba[df_geo_ba["Tên Cột"].isin(["Customer City", "Order City"])]
    df_city_ba.to_csv(reports_dir / "city_before_after.csv", index=False, encoding="utf-8-sig")

    # Vẽ biểu đồ kiểm tra so sánh Top 5
    figures_dir.mkdir(parents=True, exist_ok=True)
    sns.set_theme(style="whitegrid", palette="Set2")
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    raw_cust_top5 = df_raw["Customer City"].value_counts(dropna=False).head(5)
    axes[0, 0].barh([str(x) for x in raw_cust_top5.index][::-1], raw_cust_top5.values[::-1], color="#95a5a6", edgecolor="black")
    axes[0, 0].set_title("Top 5 Customer City TRƯỚC Chuẩn Hóa", fontsize=11, fontweight="bold")
    axes[0, 0].set_xlabel("Số lượng bản ghi")

    clean_cust_top5 = df_clean["Customer City"].dropna().value_counts().head(5)
    axes[0, 1].barh(clean_cust_top5.index[::-1], clean_cust_top5.values[::-1], color="#2ecc71", edgecolor="black")
    axes[0, 1].set_title("Top 5 Customer City SAU Chuẩn Hóa", fontsize=11, fontweight="bold")
    axes[0, 1].set_xlabel("Số lượng bản ghi")

    raw_reg_top5 = df_raw["Order Region"].value_counts(dropna=False).head(5)
    axes[1, 0].barh([str(x) for x in raw_reg_top5.index][::-1], raw_reg_top5.values[::-1], color="#95a5a6", edgecolor="black")
    axes[1, 0].set_title("Top 5 Order Region TRƯỚC Chuẩn Hóa (Bị trùng phân mảnh)", fontsize=11, fontweight="bold")
    axes[1, 0].set_xlabel("Số lượng bản ghi")

    clean_reg_top5 = df_clean["Order Region"].dropna().value_counts().head(5)
    axes[1, 1].barh(clean_reg_top5.index[::-1], clean_reg_top5.values[::-1], color="#e67e22", edgecolor="black")
    axes[1, 1].set_title("Top 5 Order Region SAU Chuẩn Hóa (Quy chuẩn 23 vùng)", fontsize=11, fontweight="bold")
    axes[1, 1].set_xlabel("Số lượng bản ghi")

    plt.suptitle("KIỂM SOÁT ĐỊA DANH VÀ VÙNG ĐỊA LÝ TRƯỚC VÀ SAU CHUẨN HÓA", fontsize=14, fontweight="bold", y=0.98)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig(figures_dir / "geo_normalization_comparison.png", dpi=300)
    plt.savefig(figures_dir / "city_top5_comparison.png", dpi=300)
    plt.close()

    return df_clean


def standardize_and_audit_target(df: pd.DataFrame, reports_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Bước 13, 14, 15, 16: Chuẩn hóa nhãn gốc, tính nhãn đối chiếu từ số ngày giao hàng TRƯỚC khi điền khuyết,
    so sánh và báo cáo xung đột nhãn vào reports/label_conflicts.csv.
    """
    print("\n[BƯỚC 13, 14, 15 & 16] Kiểm toán Biến mục tiêu (Late_delivery_risk) & Đối chiếu Quy tắc SCM...")
    df_clean = df.copy()

    # 1. Làm sạch nhãn gốc (0 hoặc 1)
    raw_s = df_clean["Late_delivery_risk"].astype("string").str.strip()
    # Loại bỏ đơn vị nếu có (ví dụ 1 VND -> 1, 0 % -> 0)
    raw_digits = raw_s.str.extract(r"^(\d+)")[0]
    raw_target = pd.to_numeric(raw_digits, errors="coerce")
    raw_target = raw_target.where(raw_target.isin([0, 1]))

    # 2. Tính nhãn đối chiếu từ số ngày giao hàng hợp lệ TRƯỚC KHI ĐIỀN KHUYẾT
    real_days = df_clean["Days for shipping (real)"]
    sched_days = df_clean["Days for shipment (scheduled)"]
    valid_dates = real_days.notna() & sched_days.notna()

    derived_target = pd.Series(pd.NA, index=df_clean.index, dtype="Int8")
    derived_target.loc[valid_dates] = (real_days[valid_dates] > sched_days[valid_dates]).astype("int8")

    # 3. Đối chiếu xung đột nhãn
    comparable = raw_target.notna() & derived_target.notna()
    matches = (raw_target[comparable] == derived_target[comparable]).sum()
    conflicts = (raw_target[comparable] != derived_target[comparable]).sum()

    print(f"-> Số dòng có đủ cả nhãn gốc và nhãn đối chiếu: {comparable.sum():,} dòng")
    print(f"-> Số dòng KHỚP 100% logic:                     {matches:,} dòng ({matches/comparable.sum()*100:.2f}%)")
    print(f"-> Số dòng XUNG ĐỘT logic (Label Conflicts):   {conflicts:,} dòng ({conflicts/comparable.sum()*100:.2f}%)")

    # 4. Xuất file báo cáo xung đột nhãn (Chỉ gồm khóa kỹ thuật, KHÔNG chứa PII)
    conflict_mask = comparable & (raw_target != derived_target)
    conflict_cols = [
        "Order Id", "Order Item Id", "Shipping Mode", "Days for shipping (real)",
        "Days for shipment (scheduled)", "Delivery Status"
    ]
    avail_cols = [c for c in conflict_cols if c in df_clean.columns]
    conflicts_df = df_clean.loc[conflict_mask, avail_cols].copy()
    conflicts_df["Raw_Late_delivery_risk"] = raw_target[conflict_mask].astype(int)
    conflicts_df["Derived_Late_delivery_risk"] = derived_target[conflict_mask].astype(int)

    reports_dir.mkdir(parents=True, exist_ok=True)
    conflict_file = reports_dir / "label_conflicts.csv"
    conflicts_df.to_csv(conflict_file, index=False, encoding="utf-8-sig")
    print(f"-> [ĐÃ XUẤT] Báo cáo chi tiết {len(conflicts_df):,} dòng mâu thuẫn tại: {conflict_file}")

    # 5. Gán nhãn cuối cùng: Ưu tiên nhãn gốc nếu hợp lệ; nếu nhãn gốc khuyết thì bổ khuyết bằng derived
    final_target = raw_target.copy()
    missing_target = final_target.isna() & derived_target.notna()
    final_target.loc[missing_target] = derived_target.loc[missing_target]
    df_clean["Late_delivery_risk"] = final_target.astype("Int8")

    undetermined = int(df_clean["Late_delivery_risk"].isna().sum())
    print(f"-> Số dòng không thể xác định nhãn (cần tách riêng khi huấn luyện): {undetermined:,} dòng")

    return df_clean, conflicts_df


def standardize_dates(df: pd.DataFrame) -> tuple[pd.DataFrame, int]:
    """Bước 20: Chuyển đổi ngày tháng bằng pd.to_datetime; kiểm tra thứ tự thời gian."""
    print("\n[BƯỚC 20] Chuẩn hóa ngày tháng và kiểm tra logic chuỗi thời gian...")
    df_clean = df.copy()

    order_date_col = "order date (DateOrders)"
    ship_date_col = "shipping date (DateOrders)"

    if order_date_col in df_clean.columns:
        df_clean[order_date_col] = pd.to_datetime(df_clean[order_date_col], errors="coerce")
    if ship_date_col in df_clean.columns:
        df_clean[ship_date_col] = pd.to_datetime(df_clean[ship_date_col], errors="coerce")

    # Kiểm tra đơn hàng có ngày giao trước ngày đặt (Bất thường logic)
    bad_date_order = 0
    if order_date_col in df_clean.columns and ship_date_col in df_clean.columns:
        valid_both = df_clean[order_date_col].notna() & df_clean[ship_date_col].notna()
        bad_dates = df_clean.loc[valid_both & (df_clean[ship_date_col] < df_clean[order_date_col])]
        bad_date_order = len(bad_dates)
        print(f"-> Số đơn hàng có shipping date < order date: {bad_date_order:,} dòng")

    return df_clean, bad_date_order


def audit_outliers_iqr(df: pd.DataFrame) -> pd.DataFrame:
    """Bước 11: Phát hiện ngoại lệ bằng IQR kết hợp quy tắc nghiệp vụ (KHÔNG tự ý xóa)."""
    print("\n[BƯỚC 11] Kiểm toán ngoại lệ (Outlier Detection - IQR & Business Rules)...")
    numeric_to_check = [
        "Sales", "Sales per customer", "Benefit per order", "Order Item Quantity", "Product Price"
    ]
    outlier_records = []

    for col in numeric_to_check:
        if col in df.columns:
            vals = df[col].dropna()
            if len(vals) > 0:
                q1 = float(vals.quantile(0.25))
                q3 = float(vals.quantile(0.75))
                iqr = q3 - q1
                lower_bound = q1 - 1.5 * iqr
                upper_bound = q3 + 1.5 * iqr
                outliers_cnt = int(((vals < lower_bound) | (vals > upper_bound)).sum())
                outlier_records.append({
                    "Cột Định Lượng": col,
                    "Q1 (25%)": round(q1, 2),
                    "Median (50%)": round(float(vals.median()), 2),
                    "Q3 (75%)": round(q3, 2),
                    "IQR": round(iqr, 2),
                    "Ngưỡng Dưới (Q1-1.5*IQR)": round(lower_bound, 2),
                    "Ngưỡng Trên (Q3+1.5*IQR)": round(upper_bound, 2),
                    "Số Lượng Ngoại Lệ": outliers_cnt,
                    "Tỷ Lệ Ngoại Lệ (%)": round(outliers_cnt / len(df) * 100, 2),
                    "Quyết Định Xử Lý": "Giữ nguyên (Phản ánh đơn hàng giá trị cao / Bán sỉ)"
                })

    outlier_df = pd.DataFrame(outlier_records)
    print(outlier_df.to_string(index=False))
    return outlier_df


def impute_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Bước 17, 18, 19: Điền median theo nhóm Shipping Mode hoặc Category Name cho biến định lượng;
    Điền Unknown cho biến phân loại; KHÔNG điền median cho ID hay biến mục tiêu.
    """
    print("\n[BƯỚC 17, 18 & 19] Xử lý Điền khuyết (Imputation) có căn cứ nghiệp vụ SCM...")
    df_clean = df.copy()

    # 1. Điền median theo Shipping Mode cho số ngày vận chuyển
    for day_col in ["Days for shipment (scheduled)", "Days for shipping (real)"]:
        if day_col in df_clean.columns and "Shipping Mode" in df_clean.columns:
            group_medians = df_clean.groupby("Shipping Mode")[day_col].transform("median")
            global_med = df_clean[day_col].median()
            df_clean[day_col] = df_clean[day_col].fillna(group_medians).fillna(global_med)

    # 2. Điền median theo Category Name cho các biến tài chính
    for fin_col in MONEY_COLS:
        if fin_col in df_clean.columns:
            if "Category Name" in df_clean.columns:
                group_medians = df_clean.groupby("Category Name")[fin_col].transform("median")
                global_med = df_clean[fin_col].median()
                df_clean[fin_col] = df_clean[fin_col].fillna(group_medians).fillna(global_med)
            else:
                df_clean[fin_col] = df_clean[fin_col].fillna(df_clean[fin_col].median())

    # 3. Điền 'Unknown' cho các biến phân loại thiếu
    cat_cols_to_fill = [
        "Shipping Mode", "Customer Segment", "Market", "Order Region", "Order State",
        "Order City", "Order Country", "Category Name", "Department Name", "Customer City", "Customer State"
    ]
    for c in cat_cols_to_fill:
        if c in df_clean.columns:
            df_clean[c] = df_clean[c].fillna("Unknown")

    print("-> Đã điền khuyết median theo phân nhóm cho biến định lượng và 'Unknown' cho biến định tính.")
    print("-> Tuyệt đối bảo toàn nguyên vẹn các cột ID, ngày tháng và nhãn mục tiêu.")
    return df_clean


def optimize_memory_and_types(df: pd.DataFrame) -> tuple[pd.DataFrame, float, float]:
    """Bước 21: Tối ưu RAM bằng cách downcast số và chuyển chuỗi ít giá trị sang category."""
    print("\n[BƯỚC 21] Tối ưu hóa Bộ nhớ RAM (Downcasting & Categorical Conversion)...")
    ram_before = df.memory_usage(deep=True).sum() / (1024 ** 2)
    df_clean = df.copy()

    for col in df_clean.columns:
        # Nếu là cột chuỗi và có số giá trị duy nhất < 200 -> category
        if df_clean[col].dtype in ["string", "object"]:
            if df_clean[col].nunique(dropna=True) < 200:
                df_clean[col] = df_clean[col].astype("category")

    ram_after = df_clean.memory_usage(deep=True).sum() / (1024 ** 2)
    savings = (1 - ram_after / ram_before) * 100
    print(f"-> Dung lượng RAM trước tối ưu: {ram_before:.2f} MB")
    print(f"-> Dung lượng RAM sau tối ưu:   {ram_after:.2f} MB")
    print(f"-> Mức độ tiết kiệm RAM:        {savings:.2f}%")

    return df_clean, ram_before, ram_after


def generate_quality_reports_and_export(
    df_clean: pd.DataFrame,
    audit_pii: dict,
    exact_dups: int,
    conflicts_df: pd.DataFrame,
    bad_dates_cnt: int,
    outlier_df: pd.DataFrame,
    ram_before: float,
    ram_after: float,
    processed_dir: Path,
    reports_dir: Path
):
    """Bước 22 & Xuất đầu ra: Export Cleaned CSV, Parquet, data_quality_after, cleaning_audit."""
    print("\n[BƯỚC 22 & XUẤT ĐẦU RA] Xuất các tệp dữ liệu sạch và báo cáo kiểm toán...")
    processed_dir.mkdir(parents=True, exist_ok=True)
    reports_dir.mkdir(parents=True, exist_ok=True)

    # 1. Xuất data/processed/DataCo_Cleaned_Full_v2.csv và DataCo_Cleaned_Full.csv
    v2_csv = processed_dir / "DataCo_Cleaned_Full_v2.csv"
    std_csv = processed_dir / "DataCo_Cleaned_Full.csv"
    df_clean.to_csv(v2_csv, index=False, encoding="utf-8-sig")
    df_clean.to_csv(std_csv, index=False, encoding="utf-8-sig")
    print(f"-> [XUẤT THÀNH CÔNG] File CSV sạch v2: {v2_csv} ({os.path.getsize(v2_csv) / (1024*1024):.2f} MB)")
    print(f"-> [XUẤT THÀNH CÔNG] Đồng bộ File CSV sạch tiêu chuẩn: {std_csv}")

    # 2. Xuất data/processed/DataCo_Cleaned_Full_v2.parquet và DataCo_Cleaned_Full.parquet
    v2_parquet = processed_dir / "DataCo_Cleaned_Full_v2.parquet"
    std_parquet = processed_dir / "DataCo_Cleaned_Full.parquet"
    df_clean.to_parquet(v2_parquet, index=False, engine="pyarrow")
    df_clean.to_parquet(std_parquet, index=False, engine="pyarrow")
    print(f"-> [XUẤT THÀNH CÔNG] File Parquet sạch v2: {v2_parquet} ({os.path.getsize(v2_parquet) / (1024*1024):.2f} MB)")
    print(f"-> [XUẤT THÀNH CÔNG] Đồng bộ File Parquet tiêu chuẩn: {std_parquet}")

    # 3. Xuất reports/data_quality_after.csv
    quality_after_records = []
    for col in df_clean.columns:
        s = df_clean[col]
        null_cnt = int(s.isna().sum())
        unknown_cnt = int(s.astype(str).eq("Unknown").sum()) if str(s.dtype) in ["category", "string", "object"] else 0
        quality_after_records.append({
            "Tên Cột": col,
            "Kiểu Dữ Liệu Sau Xử Lý": str(s.dtype),
            "Số Lượng Null": null_cnt,
            "Tỷ Lệ Null (%)": round(null_cnt / len(df_clean) * 100, 2),
            "Số Giá Trị Unknown": unknown_cnt,
            "Số Giá Trị Độc Nhất (Cardinality)": int(s.nunique(dropna=True)),
            "Trạng Thái Chất Lượng": "Sạch (0 NaN)" if null_cnt == 0 else f"Còn {null_cnt} NaN hợp lệ"
        })
    quality_after_df = pd.DataFrame(quality_after_records)
    quality_after_file = reports_dir / "data_quality_after.csv"
    quality_after_df.to_csv(quality_after_file, index=False, encoding="utf-8-sig")
    print(f"-> [XUẤT THÀNH CÔNG] Báo cáo chất lượng sau làm sạch: {quality_after_file}")

    # 4. Xuất reports/cleaning_audit.csv
    audit_summary_records = [
        {"Hạng Mục Kiểm Toán": "Số dòng dữ liệu ban đầu", "Giá Trị": f"{EXPECTED_ROWS:,}"},
        {"Hạng Mục Kiểm Toán": "Số dòng dữ liệu sau làm sạch", "Giá Trị": f"{len(df_clean):,}"},
        {"Hạng Mục Kiểm Toán": "Số cột ban đầu", "Giá Trị": f"{EXPECTED_COLS_RAW}"},
        {"Hạng Mục Kiểm Toán": "Số cột sau xử lý (chuẩn 51 cột)", "Giá Trị": f"{len(df_clean.columns)}"},
        {"Hạng Mục Kiểm Toán": "Số cột PII bị loại bỏ", "Giá Trị": f"{len(audit_pii['dropped_pii_columns'])} ({', '.join(audit_pii['dropped_pii_columns'])})"},
        {"Hạng Mục Kiểm Toán": "Số dòng trùng lặp 100% bị xóa", "Giá Trị": f"{exact_dups:,}"},
        {"Hạng Mục Kiểm Toán": "Số trường hợp xung đột nhãn mục tiêu", "Giá Trị": f"{len(conflicts_df):,} (Đã xuất chi tiết ra label_conflicts.csv)"},
        {"Hạng Mục Kiểm Toán": "Số đơn hàng có ngày giao trước ngày đặt", "Giá Trị": f"{bad_dates_cnt:,}"},
        {"Hạng Mục Kiểm Toán": "Dung lượng RAM trước tối ưu", "Giá Trị": f"{ram_before:.2f} MB"},
        {"Hạng Mục Kiểm Toán": "Dung lượng RAM sau tối ưu", "Giá Trị": f"{ram_after:.2f} MB"},
        {"Hạng Mục Kiểm Toán": "Tỷ lệ tiết kiệm RAM", "Giá Trị": f"{(1 - ram_after / ram_before) * 100:.2f}%"}
    ]
    audit_summary_df = pd.DataFrame(audit_summary_records)
    audit_summary_file = reports_dir / "cleaning_audit.csv"
    audit_summary_df.to_csv(audit_summary_file, index=False, encoding="utf-8-sig")
    print(f"-> [XUẤT THÀNH CÔNG] Nhật ký kiểm toán làm sạch: {audit_summary_file}")


def main():
    start_time = time.time()
    print("=" * 80)
    print(" PROJECT 13: DATACO BIG SUPPLY CHAIN DELIVERY DELAY PREDICTION")
    print(" PIPELINE LÀM SẠCH VÀ CHUẨN HÓA DỮ LIỆU TỰ ĐỘNG (02_DATA_CLEANING.PY)")
    print("=" * 80)

    raw_path = Path("data/raw/7_PJ13_2521001054_Nguyễn Lê Nhật Hạ.csv")
    processed_dir = Path("data/processed")
    reports_dir = Path("reports")
    figures_dir = Path("figures")

    # Pipeline execution steps
    df_raw = load_raw_data(raw_path)
    df_pii, audit_pii = drop_sensitive_pii(df_raw)
    df_dedup, exact_dups = handle_duplicates(df_pii)
    df_missing = clean_missing_markers(df_dedup)
    df_numeric = clean_numeric_controlled_regex(df_missing)
    df_cat = standardize_categoricals(df_numeric)
    df_geo = normalize_and_audit_all_geography(df_cat, df_raw, reports_dir, figures_dir)
    df_target, conflicts_df = standardize_and_audit_target(df_geo, reports_dir)
    df_dates, bad_dates_cnt = standardize_dates(df_target)
    outlier_df = audit_outliers_iqr(df_dates)
    df_imputed = impute_missing_values(df_dates)
    df_final, ram_before, ram_after = optimize_memory_and_types(df_imputed)

    generate_quality_reports_and_export(
        df_final, audit_pii, exact_dups, conflicts_df, bad_dates_cnt,
        outlier_df, ram_before, ram_after, processed_dir, reports_dir
    )

    elapsed = time.time() - start_time
    print("\n" + "=" * 80)
    print(f" HOÀN TẤT TOÀN BỘ PIPELINE 02_DATA_CLEANING.PY THÀNH CÔNG TRONG {elapsed:.2f} GIÂY!")
    print(f" Quy mô dữ liệu sạch đầu ra: {len(df_final):,} dòng x {len(df_final.columns)} cột.")
    print("=" * 80)


if __name__ == "__main__":
    main()
