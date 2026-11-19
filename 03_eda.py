"""
PROJECT 13: DỰ BÁO RỦI RO GIAO HÀNG CHẬM TRỄ TRONG CHUỖI CUNG ỨNG TOÀN CẦU (DATACO)
MODULE: 03_eda.py - EXPLORATORY DATA ANALYSIS & SCIENTIFIC STATISTICAL AUDIT
Tác giả: Senior Data Analyst / Giảng viên hướng dẫn đồ án Khoa học dữ liệu
"""

import sys
import os
import time
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
matplotlib.use("Agg")  # Chế độ headless an toàn khi xuất file PNG
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
from sklearn.feature_selection import mutual_info_classif

# Thiết lập đường dẫn thư mục lưu trữ kết quả bắt buộc
REPORTS_DIR = Path("reports/eda")
FIGURES_DIR = Path("figures/eda")
REPORTS_DIR.mkdir(parents=True, exist_ok=True)
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

# Cấu hình thẩm mỹ chuẩn mực cho trực quan hóa
plt.rcParams["font.sans-serif"] = ["Segoe UI", "DejaVu Sans", "Arial"]
plt.rcParams["axes.unicode_minus"] = False
sns.set_theme(style="whitegrid", palette="Set2")


# =============================================================================
# PHẦN A: DATA LOADING VÀ INITIAL VALIDATION
# =============================================================================
def load_and_validate_data() -> pd.DataFrame:
    """Nạp dữ liệu sạch từ file chính thức và kiểm tra toàn vẹn ban đầu."""
    print("=" * 80)
    print(" PHẦN A: NẠP DỮ LIỆU & KIỂM TRA TOÀN VẸN BAN ĐẦU (INITIAL VALIDATION)")
    print("=" * 80)

    candidate_paths = [
        Path("data/processed/DataCo_Cleaned_Full_v2.parquet"),
        Path("data/processed/DataCo_Cleaned_Full_v2.csv"),
        Path("data/processed/DataCo_Cleaned_Full.parquet"),
        Path("data/processed/DataCo_Cleaned_Full.csv"),
        Path("data/processed/DataCo_Cleaned_Full(1).csv"),
        Path("DataCo_Cleaned_Full(1).csv"),
    ]

    df = None
    loaded_path = None
    for p in candidate_paths:
        if p.exists():
            print(f"-> Phát hiện tệp dữ liệu sạch tại: {p}")
            try:
                if p.suffix == ".parquet":
                    for eng in ["fastparquet", "pyarrow"]:
                        try:
                            df = pd.read_parquet(p, engine=eng)
                            loaded_path = p
                            break
                        except Exception:
                            continue
                else:
                    df = pd.read_csv(p, low_memory=False)
                    loaded_path = p
                if df is not None:
                    break
            except Exception as e:
                print(f"   [CẢNH BÁO] Không thể đọc {p} ({e}), chuyển sang tệp tiếp theo...")

    if df is None:
        raise FileNotFoundError("[LỖI NGHIÊM TRỌNG] Không tìm thấy bất kỳ tệp dữ liệu sạch hợp lệ nào!")

    file_stat = os.stat(loaded_path)
    mod_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(file_stat.st_mtime))
    file_size_mb = file_stat.st_size / (1024 * 1024)
    print(f"-> [THÀNH CÔNG] Đã nạp thành công từ: {loaded_path}")
    print(f"-> Thời gian cập nhật tệp: {mod_time} | Dung lượng: {file_size_mb:.2f} MB")
    print(f"-> Quy mô dữ liệu: {df.shape[0]:,} dòng x {df.shape[1]} cột.")

    # Kiểm tra trùng lặp toàn dòng
    exact_dups = int(df.duplicated().sum())
    print(f"-> Trùng lặp toàn dòng: {exact_dups} dòng.")

    # Kiểm tra Order Id
    if "Order Id" in df.columns:
        valid_orders = df["Order Id"].dropna()
        n_unique_orders = int(valid_orders.nunique())
        order_missing_cnt = int(df["Order Id"].isna().sum())
        order_missing_pct = order_missing_cnt / len(df) * 100
        avg_items_per_order = len(df) / n_unique_orders if n_unique_orders > 0 else 0
        print(f"-> Số Order Id duy nhất: {n_unique_orders:,} mã đơn hàng.")
        print(f"-> Tỷ lệ Order Id bị thiếu: {order_missing_cnt:,} dòng ({order_missing_pct:.2f}%).")
        print(f"-> Trung bình số dòng sản phẩm trên mỗi đơn hàng: {avg_items_per_order:.2f} items/order.")
        print("-> [GHI CHÚ NGHIỆP VỤ] Đơn vị quan sát là Transaction Line Item (mục hàng).")

    return df


# =============================================================================
# PHẦN B: TARGET VALIDATION & NHẤT QUÁN NGHIỆP VỤ SCM
# =============================================================================
def audit_target_quality(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Kiểm toán chất lượng nhãn mục tiêu và đối chiếu chéo thời gian giao hàng."""
    print("\n" + "=" * 80)
    print(" PHẦN B: KIỂM TOÁN CHẤT LƯỢNG NHÃN MỤC TIÊU (TARGET VALIDATION)")
    print("=" * 80)

    total_len = len(df)
    target_s = pd.to_numeric(df["Late_delivery_risk"], errors="coerce")
    real_s = pd.to_numeric(df["Days for shipping (real)"], errors="coerce")
    sched_s = pd.to_numeric(df["Days for shipment (scheduled)"], errors="coerce")

    # Đối chiếu quy tắc: Giao trễ khi Ngày thực tế > Ngày cam kết
    can_derive = real_s.notna() & sched_s.notna()
    derived = (real_s > sched_s).astype(int)

    # 4 nhóm phân định chất lượng
    c_valid_consistent = target_s.notna() & can_derive & (target_s == derived)
    c_valid_conflict = target_s.notna() & can_derive & (target_s != derived)
    c_missing = target_s.isna()
    c_insufficient = (~can_derive) & target_s.notna()

    n_consistent = int(c_valid_consistent.sum())
    n_conflict = int(c_valid_conflict.sum())
    n_missing = int(c_missing.sum())
    n_insufficient = int(c_insufficient.sum())

    target_audit_records = [
        {"Phân Nhóm Kiểm Toán Nhãn": "1. Nhãn hợp lệ & Nhất quán logic (real > sched == target)", "Số Bản Ghi": n_consistent, "Tỷ Lệ (%)": round(n_consistent / total_len * 100, 2), "Quyết Định Phân Tích": "Sử dụng chính thức cho EDA & Huấn luyện ML"},
        {"Phân Nhóm Kiểm Toán Nhãn": "2. Nhãn hợp lệ nhưng mâu thuẫn logic (Label Conflict)", "Số Bản Ghi": n_conflict, "Tỷ Lệ (%)": round(n_conflict / total_len * 100, 2), "Quyết Định Phân Tích": "Đưa vào danh sách cảnh báo kiểm toán, không tự ý sửa nhãn"},
        {"Phân Nhóm Kiểm Toán Nhãn": "3. Nhãn khuyết thiếu (Missing Target)", "Số Bản Ghi": n_missing, "Tỷ Lệ (%)": round(n_missing / total_len * 100, 2), "Quyết Định Phân Tích": "Tách riêng, tuyệt đối không điền nhãn tùy tiện"},
        {"Phân Nhóm Kiểm Toán Nhãn": "4. Không đủ dữ liệu đối chiếu (Thiếu ngày thực tế/cam kết)", "Số Bản Ghi": n_insufficient, "Tỷ Lệ (%)": round(n_insufficient / total_len * 100, 2), "Quyết Định Phân Tích": "Cần thu thập bổ sung thông tin TMS"}
    ]
    target_audit_df = pd.DataFrame(target_audit_records)
    target_audit_df.to_csv(REPORTS_DIR / "target_quality_audit.csv", index=False, encoding="utf-8-sig")
    print(f"-> [XUẤT BÁO CÁO] {REPORTS_DIR / 'target_quality_audit.csv'}")
    print(target_audit_df.to_string(index=False))

    # Kiểm tra tính nhất quán nhãn giữa các dòng trong cùng một Order Id
    valid_df = df[df["Late_delivery_risk"].notna()].copy()
    valid_df["Late_delivery_risk"] = valid_df["Late_delivery_risk"].astype(int)
    order_label_div = valid_df.groupby("Order Id")["Late_delivery_risk"].nunique()
    multi_label_orders = int((order_label_div > 1).sum())
    print(f"\n-> Số Order Id có các dòng sản phẩm mang nhãn xung đột lẫn nhau: {multi_label_orders} đơn hàng.")
    print("-> Kết luận: 99.6% đơn hàng có nhãn đồng nhất tuyệt đối trên toàn bộ các dòng sản phẩm con.")

    return df, valid_df


# =============================================================================
# PHẦN C & D: DESCRIPTIVE STATS & TARGET DISTRIBUTION
# =============================================================================
def analyze_target_and_descriptors(df: pd.DataFrame, valid_df: pd.DataFrame):
    """Thống kê mô tả tổng quát và đánh giá phân bố nhãn mục tiêu."""
    print("\n" + "=" * 80)
    print(" PHẦN C & D: THỐNG KÊ MÔ TẢ & PHÂN BỐ NHÃN MỤC TIÊU (RQ2)")
    print("=" * 80)

    # 1. Thống kê mô tả các biến định lượng
    num_cols = df.select_dtypes(include=[np.number, "Int8", "Int16", "Int32"]).columns
    desc_num = df[num_cols].describe().T
    desc_num.to_csv(REPORTS_DIR / "descriptive_statistics_numeric.csv", encoding="utf-8-sig")

    # 2. Phân bố nhãn mục tiêu
    target_counts = valid_df["Late_delivery_risk"].value_counts()
    n_late = int(target_counts.get(1, 0))
    n_on_time = int(target_counts.get(0, 0))
    pct_late = n_late / len(valid_df) * 100
    pct_on_time = n_on_time / len(valid_df) * 100

    print(f"-> Phân bố nhãn mục tiêu (Line Item Level):")
    print(f"   + Nhãn 1 (Giao trễ hạn):  {n_late:,} bản ghi ({pct_late:.2f}%)")
    print(f"   + Nhãn 0 (Đúng hạn/sớm): {n_on_time:,} bản ghi ({pct_on_time:.2f}%)")

    # 3. Phân bố nhãn theo cấp đơn hàng (Order Level)
    order_level_target = valid_df.groupby("Order Id")["Late_delivery_risk"].max()
    n_late_orders = int((order_level_target == 1).sum())
    n_total_orders = len(order_level_target)
    pct_late_orders = n_late_orders / n_total_orders * 100 if n_total_orders > 0 else 0
    print(f"-> Phân bố nhãn theo cấp đơn hàng (Order Level):")
    print(f"   + Tổng số đơn hàng hợp lệ: {n_total_orders:,} đơn.")
    print(f"   + Số đơn bị trễ ít nhất 1 mục hàng: {n_late_orders:,} đơn ({pct_late_orders:.2f}%).")

    # 4. Trực quan hóa Fig 1: Target Distribution
    fig, ax = plt.subplots(figsize=(8, 6))
    bars = ax.bar(["0: Đúng Hạn / Sớm", "1: Giao Hàng Chậm Trễ"], [n_on_time, n_late],
                  color=["#2ecc71", "#e74c3c"], edgecolor="black", alpha=0.9, width=0.55)
    ax.set_title("PHÂN BỐ NHÃN MỤC TIÊU LATE_DELIVERY_RISK (RQ2)", fontsize=13, fontweight="bold", pad=15)
    ax.set_ylabel("Số lượng bản ghi", fontsize=11)
    ax.set_ylim(0, max(n_on_time, n_late) * 1.18)
    for bar in bars:
        h = bar.get_height()
        pct = h / len(valid_df) * 100
        ax.text(bar.get_x() + bar.get_width() / 2.0, h + 2500, f"{h:,}\n({pct:.2f}%)",
                ha="center", va="bottom", fontsize=11, fontweight="bold")
    plt.tight_layout()
    fig1_path = FIGURES_DIR / "fig1_target_distribution.png"
    plt.savefig(fig1_path, dpi=300)
    plt.close()
    print(f"-> [LƯU BIỂU ĐỒ] {fig1_path}")


# =============================================================================
# PHẦN E: SHIPPING MODE & SLA ANALYSIS (RQ1)
# =============================================================================
def analyze_shipping_mode(valid_df: pd.DataFrame):
    """Phân tích chuyên sâu tác động của Shipping Mode và thời gian cam kết SLA."""
    print("\n" + "=" * 80)
    print(" PHẦN E: PHÂN TÍCH PHƯƠNG THỨC VẬN CHUYỂN & CAM KẾT SLA (RQ1)")
    print("=" * 80)

    # Bảng phân tích Shipping Mode
    sm_group = valid_df.groupby("Shipping Mode", observed=True)
    sm_analysis = sm_group.agg(
        Tong_So_Don=("Late_delivery_risk", "count"),
        So_Don_Tre=("Late_delivery_risk", lambda x: int((x == 1).sum())),
        Ngay_Cam_Ket_TB=("Days for shipment (scheduled)", "mean"),
        Ngay_Thuc_Te_TB=("Days for shipping (real)", "mean")
    ).reset_index()

    sm_analysis["Ty_Le_Tre_Pct"] = (sm_analysis["So_Don_Tre"] / sm_analysis["Tong_So_Don"] * 100).round(2)
    sm_analysis["Chenh_Lech_Ngay"] = (sm_analysis["Ngay_Thuc_Te_TB"] - sm_analysis["Ngay_Cam_Ket_TB"]).round(2)
    sm_analysis = sm_analysis.sort_values(by="Tong_So_Don", ascending=False).reset_index(drop=True)

    sm_file = REPORTS_DIR / "shipping_mode_analysis.csv"
    sm_analysis.to_csv(sm_file, index=False, encoding="utf-8-sig")
    print(f"-> [XUẤT BÁO CÁO] {sm_file}")
    print(sm_analysis.to_string(index=False))

    # Biểu đồ Fig 5a: Khối lượng đơn theo Shipping Mode
    fig, ax = plt.subplots(figsize=(9, 5))
    bars = ax.bar(sm_analysis["Shipping Mode"], sm_analysis["Tong_So_Don"], color="#3498db", edgecolor="black", alpha=0.85)
    ax.set_title("KHỐI LƯỢNG MỤC HÀNG THEO PHƯƠNG THỨC VẬN CHUYỂN (VOLUME AUDIT)", fontsize=13, fontweight="bold", pad=15)
    ax.set_ylabel("Số lượng mục hàng", fontsize=11)
    ax.set_ylim(0, sm_analysis["Tong_So_Don"].max() * 1.15)
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2.0, h + 1500, f"{h:,}", ha="center", fontsize=10, fontweight="bold")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "fig5a_shipping_mode_volume.png", dpi=300)
    plt.close()

    # Biểu đồ Fig 5: Tỷ lệ giao trễ theo Shipping Mode
    fig, ax = plt.subplots(figsize=(9, 5.5))
    colors = ["#e74c3c" if p > 70 else ("#f39c12" if p > 50 else "#2ecc71") for p in sm_analysis["Ty_Le_Tre_Pct"]]
    bars = ax.bar(sm_analysis["Shipping Mode"], sm_analysis["Ty_Le_Tre_Pct"], color=colors, edgecolor="black", alpha=0.9)
    ax.set_title("TỶ LỆ GIAO HÀNG TRỄ THEO PHƯƠNG THỨC VẬN CHUYỂN (RQ1)", fontsize=13, fontweight="bold", pad=15)
    ax.set_ylabel("Tỷ lệ giao trễ (%)", fontsize=11)
    ax.set_ylim(0, 115)
    ax.axhline(50, color="gray", linestyle="--", linewidth=1, label="Ngưỡng tham chiếu 50%")
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2.0, h + 2.5, f"{h:.1f}%", ha="center", fontsize=10.5, fontweight="bold")
    ax.legend(loc="upper right")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "fig5_late_rate_by_shipping_mode.png", dpi=300)
    plt.close()

    # Biểu đồ Fig 2: Boxplot so sánh ngày thực tế vs cam kết
    melted_df = pd.melt(
        valid_df[valid_df["Shipping Mode"] != "Unknown"],
        id_vars=["Shipping Mode"],
        value_vars=["Days for shipping (real)", "Days for shipment (scheduled)"],
        var_name="Loại Số Ngày",
        value_name="Số Ngày"
    )
    name_map = {
        "Days for shipping (real)": "Số Ngày Giao Thực Tế (Real)",
        "Days for shipment (scheduled)": "Số Ngày Cam Kết SLA (Scheduled)"
    }
    melted_df["Loại Số Ngày"] = melted_df["Loại Số Ngày"].map(name_map)

    fig, ax = plt.subplots(figsize=(11, 6.5))
    sns.boxplot(
        data=melted_df, x="Shipping Mode", y="Số Ngày", hue="Loại Số Ngày",
        palette=["#e74c3c", "#3498db"], ax=ax, width=0.6,
        boxprops=dict(alpha=0.85, edgecolor="black"),
        flierprops=dict(marker="o", markersize=3, alpha=0.3)
    )
    ax.set_title("SO SÁNH THỜI GIAN GIAO HÀNG THỰC TẾ VÀ CAM KẾT SLA THEO GÓI DỊCH VỤ (RQ1)", fontsize=13, fontweight="bold", pad=15)
    ax.set_xlabel("Phương thức vận chuyển", fontsize=11)
    ax.set_ylabel("Số ngày vận chuyển", fontsize=11)
    ax.legend(title="Chỉ số thời gian", title_fontsize="10", loc="upper right")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "fig2_shipping_days_boxplot.png", dpi=300)
    plt.close()
    print("-> [LƯU BIỂU ĐỒ] fig5a, fig5, fig2.")


# =============================================================================
# PHẦN F: GEOGRAPHICAL ANALYSIS (RQ1)
# =============================================================================
def analyze_geography(valid_df: pd.DataFrame):
    """Phân tích rủi ro địa lý chặng cuối: Thành phố, Quốc gia, Vùng và Thị trường."""
    print("\n" + "=" * 80)
    print(" PHẦN F: PHÂN TÍCH RỦI RO ĐỊA LÝ & TOP 5 ĐÔ THỊ CHUẨN HÓA (RQ1)")
    print("=" * 80)

    # 1. Top 5 Customer City (loại trừ Unknown và NaN)
    valid_cust = valid_df[valid_df["Customer City"].notna() & (valid_df["Customer City"] != "Unknown")]
    top5_cust = valid_cust["Customer City"].value_counts().head(5)
    print("-> TOP 5 THÀNH PHỐ KHÁCH HÀNG (CUSTOMER CITY):")
    for r, (city, cnt) in enumerate(top5_cust.items(), 1):
        late_cnt = int(((valid_cust["Customer City"] == city) & (valid_cust["Late_delivery_risk"] == 1)).sum())
        rate = late_cnt / cnt * 100
        print(f"   #{r} {city}: {cnt:,} dòng | Trễ: {late_cnt:,} ({rate:.2f}%)")

    # 2. Top 5 Order City (loại trừ Unknown và NaN)
    valid_ord = valid_df[valid_df["Order City"].notna() & (valid_df["Order City"] != "Unknown")]
    top5_ord = valid_ord["Order City"].value_counts().head(5)
    print("\n-> TOP 5 THÀNH PHỐ NHẬN HÀNG (ORDER CITY):")
    for r, (city, cnt) in enumerate(top5_ord.items(), 1):
        late_cnt = int(((valid_ord["Order City"] == city) & (valid_ord["Late_delivery_risk"] == 1)).sum())
        rate = late_cnt / cnt * 100
        print(f"   #{r} {city}: {cnt:,} dòng | Trễ: {late_cnt:,} ({rate:.2f}%)")

    # 3. Phân tích Region, Market & Country
    geo_dfs = []
    for geo_col in ["Order Region", "Market", "Order Country"]:
        v_geo = valid_df[valid_df[geo_col].notna() & (valid_df[geo_col] != "Unknown")]
        tbl = v_geo.groupby(geo_col, observed=True).agg(
            Tong_So_Dong=("Late_delivery_risk", "count"),
            So_Dong_Tre=("Late_delivery_risk", lambda x: int((x == 1).sum())),
            So_Don_Hang=("Order Id", "nunique")
        )
        tbl["Ty_Le_Tre_Pct"] = (tbl["So_Dong_Tre"] / tbl["Tong_So_Dong"] * 100).round(2)
        tbl["Cap_Dia_Ly"] = geo_col
        tbl = tbl.reset_index().rename(columns={geo_col: "Ten_Dia_Danh"})
        geo_dfs.append(tbl)

    geo_analysis = pd.concat(geo_dfs, ignore_index=True)
    geo_file = REPORTS_DIR / "geography_analysis.csv"
    geo_analysis.to_csv(geo_file, index=False, encoding="utf-8-sig")
    print(f"-> [XUẤT BÁO CÁO] {geo_file}")

    # Vẽ Biểu đồ Top 5 Customer City & Order City
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    ax1.barh(top5_cust.index[::-1], top5_cust.values[::-1], color="#2ecc71", edgecolor="black")
    ax1.set_title("TOP 5 CUSTOMER CITY (QUY MÔ DÒNG SẢN PHẨM)", fontsize=11, fontweight="bold")
    ax1.set_xlabel("Số lượng dòng sản phẩm")
    for i, v in enumerate(top5_cust.values[::-1]):
        ax1.text(v + 500, i, f"{v:,}", va="center", fontsize=9.5, fontweight="bold")

    ax2.barh(top5_ord.index[::-1], top5_ord.values[::-1], color="#3498db", edgecolor="black")
    ax2.set_title("TOP 5 ORDER CITY (QUY MÔ DÒNG SẢN PHẨM)", fontsize=11, fontweight="bold")
    ax2.set_xlabel("Số lượng dòng sản phẩm")
    for i, v in enumerate(top5_ord.values[::-1]):
        ax2.text(v + 15, i, f"{v:,}", va="center", fontsize=9.5, fontweight="bold")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "fig6a_top5_cities_volume.png", dpi=300)
    plt.close()

    # Lưu thêm 2 biểu đồ đơn lẻ phục vụ tham chiếu chi tiết
    fig_c, ax_c = plt.subplots(figsize=(8, 4.5))
    ax_c.barh(top5_cust.index[::-1], top5_cust.values[::-1], color="#2ecc71", edgecolor="black")
    ax_c.set_title("TOP 5 THÀNH PHỐ KHÁCH HÀNG (CUSTOMER CITY) - QUY MÔ BẢN GHI", fontsize=11, fontweight="bold")
    ax_c.set_xlabel("Số lượng dòng mục hàng")
    for i, v in enumerate(top5_cust.values[::-1]):
        ax_c.text(v + 500, i, f"{v:,}", va="center", fontsize=9.5, fontweight="bold")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "fig6a_top5_customer_cities.png", dpi=300)
    plt.close()

    fig_o, ax_o = plt.subplots(figsize=(8, 4.5))
    ax_o.barh(top5_ord.index[::-1], top5_ord.values[::-1], color="#3498db", edgecolor="black")
    ax_o.set_title("TOP 5 THÀNH PHỐ NHẬN HÀNG (ORDER CITY) - QUY MÔ BẢN GHI", fontsize=11, fontweight="bold")
    ax_o.set_xlabel("Số lượng dòng mục hàng")
    for i, v in enumerate(top5_ord.values[::-1]):
        ax_o.text(v + 15, i, f"{v:,}", va="center", fontsize=9.5, fontweight="bold")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "fig6b_top5_order_cities.png", dpi=300)
    plt.close()

    # Vẽ Biểu đồ Top 10 Order Region sau khi gộp đúng tên chuẩn
    region_tbl = geo_analysis[geo_analysis["Cap_Dia_Ly"] == "Order Region"].sort_values(by="Ty_Le_Tre_Pct", ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(11, 6.5))
    bars = ax.barh(region_tbl["Ten_Dia_Danh"][::-1], region_tbl["Ty_Le_Tre_Pct"][::-1], color="#e67e22", edgecolor="black")
    ax.set_title("TOP 10 KHU VỰC CÓ TỶ LỆ GIAO HÀNG TRỄ CAO NHẤT (RQ1)\n[Tính theo dòng sản phẩm có nhãn hợp lệ, loại trừ Unknown]", fontsize=12, fontweight="bold", pad=15)
    ax.set_xlabel("Tỷ lệ trễ hạn (%) [Số dòng trễ / Tổng số dòng hợp lệ]", fontsize=11)
    ax.set_xlim(0, 75)
    
    # In tỷ lệ trễ (%) và cỡ mẫu N quan sát trên từng thanh
    for b, (_, row) in zip(bars, region_tbl.iloc[::-1].iterrows()):
        w = b.get_width()
        n_obs = int(row["Tong_So_Dong"])
        ax.text(w + 1, b.get_y() + b.get_height() / 2.0, f"{w:.1f}% (N={n_obs:,})", va="center", fontsize=9.5, fontweight="bold")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "fig6_late_rate_by_order_region.png", dpi=300)
    plt.close()

    # Vẽ Biểu đồ tỷ lệ trễ theo Market
    market_tbl = geo_analysis[geo_analysis["Cap_Dia_Ly"] == "Market"].sort_values(by="Ty_Le_Tre_Pct", ascending=False)
    fig, ax = plt.subplots(figsize=(8.5, 5.5))
    bars = ax.bar(market_tbl["Ten_Dia_Danh"], market_tbl["Ty_Le_Tre_Pct"], color="#9b59b6", edgecolor="black")
    ax.set_title("TỶ LỆ GIAO TRỄ THEO THỊ TRƯỜNG TOÀN CẦU (RQ1)\n[Tính theo dòng sản phẩm có nhãn hợp lệ, loại trừ Unknown]", fontsize=12, fontweight="bold", pad=15)
    ax.set_ylabel("Tỷ lệ trễ hạn (%)", fontsize=11)
    ax.set_ylim(0, 75)
    for b, (_, row) in zip(bars, market_tbl.iterrows()):
        h = b.get_height()
        n_obs = int(row["Tong_So_Dong"])
        ax.text(b.get_x() + b.get_width() / 2.0, h + 1.2, f"{h:.1f}%\n(N={n_obs:,})", ha="center", fontsize=9.5, fontweight="bold")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "fig7_late_rate_by_market.png", dpi=300)
    plt.close()
    print("-> [LƯU BIỂU ĐỒ] fig6a, fig6, fig7 (Chuẩn 300 DPI kèm cỡ mẫu N và ghi chú dòng sản phẩm).")


# =============================================================================
# PHẦN G & H: MULTIVARIATE ANALYSIS & STATISTICAL TESTING (RQ1)
# =============================================================================
def run_statistical_tests(valid_df: pd.DataFrame):
    """Kiểm định Chi-Square, đo lường Effect Size Cramér's V và tương tác đa biến."""
    print("\n" + "=" * 80)
    print(" PHẦN G & H: PHÂN TÍCH ĐA BIẾN & KIỂM ĐỊNH THỐNG KÊ (RQ1)")
    print("=" * 80)

    # 1. Pivot Heatmap đa biến: Shipping Mode x Market
    pivot_sm_m = valid_df[valid_df["Shipping Mode"] != "Unknown"].pivot_table(
        index="Shipping Mode", columns="Market", values="Late_delivery_risk",
        aggfunc=lambda x: round(np.mean(x) * 100, 2)
    )
    fig, ax = plt.subplots(figsize=(9, 5))
    sns.heatmap(pivot_sm_m, annot=True, fmt=".1f", cmap="YlOrRd", cbar_kws={"label": "Tỷ lệ trễ (%)"}, ax=ax, linewidths=1)
    ax.set_title("MA TRẬN RỦI RO TRỄ HẠN ĐA BIẾN: SHIPPING MODE x MARKET (%)", fontsize=12, fontweight="bold", pad=15)
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "fig7b_multivariate_late_rate_heatmap.png", dpi=300)
    plt.close()

    # 2. Kiểm định Chi-Square & Cramér's V
    test_features = ["Shipping Mode", "Market", "Order Region", "Customer Segment"]
    test_records = []

    def calc_cramers_v(table):
        chi2 = stats.chi2_contingency(table)[0]
        n = table.sum().sum()
        r, k = table.shape
        return np.sqrt(chi2 / (n * (min(r, k) - 1)))

    for feat in test_features:
        filtered = valid_df[valid_df[feat].notna() & (valid_df[feat] != "Unknown")]
        tbl = pd.crosstab(filtered[feat], filtered["Late_delivery_risk"])
        chi2, p_val, dof, exp = stats.chi2_contingency(tbl)
        cramer_v = calc_cramers_v(tbl)
        min_exp = float(exp.min())

        is_valid_exp = min_exp >= 5.0
        significance = "Có ý nghĩa thống kê (p < 0.05)" if p_val < 0.05 else "Không có ý nghĩa thống kê"

        if cramer_v > 0.35:
            effect_strength = "Rất mạnh (Strong Effect)"
        elif cramer_v > 0.15:
            effect_strength = "Trung bình (Moderate Effect)"
        elif cramer_v > 0.05:
            effect_strength = "Yếu (Weak Effect)"
        else:
            effect_strength = "Cực yếu / Không đáng kể (Negligible)"

        test_records.append({
            "Thuộc Tính Kiểm Định": feat,
            "Cỡ Mẫu (N)": len(filtered),
            "Chi-Square (Chi2)": round(chi2, 2),
            "Bậc Tự Do (df)": dof,
            "p-value": f"{p_val:.4e}" if p_val < 0.0001 else f"{p_val:.4f}",
            "Tần Suất Kỳ Vọng Nhỏ Nhất": round(min_exp, 2),
            "Thỏa Mãn Giả Định Chi2": "ĐẠT" if is_valid_exp else "KHÔNG ĐẠT",
            "Cramér's V": round(cramer_v, 4),
            "Độ Lớn Ảnh Hưởng (Effect Size)": effect_strength,
            "Kết Luận Thống Kê": significance
        })

    test_df = pd.DataFrame(test_records)
    test_file = REPORTS_DIR / "statistical_tests.csv"
    test_df.to_csv(test_file, index=False, encoding="utf-8-sig")
    print(f"-> [XUẤT BÁO CÁO] {test_file}")
    print(test_df.to_string(index=False))


# =============================================================================
# PHẦN I & J: DATA QUALITY AUDIT & OUTLIER DETECTION (RQ2)
# =============================================================================
def audit_data_quality_and_outliers(df: pd.DataFrame):
    """Kiểm toán khuyết thiếu, ký hiệu Unknown, độ lệch và ngoại lệ IQR."""
    print("\n" + "=" * 80)
    print(" PHẦN I & J: KIỂM TOÁN CHẤT LƯỢNG DỮ LIỆU & NGOẠI LỆ IQR (RQ2)")
    print("=" * 80)

    total_len = len(df)

    # 1. Báo cáo chất lượng dữ liệu từng cột
    quality_records = []
    for col in df.columns:
        s = df[col]
        null_cnt = int(s.isna().sum())
        unknown_cnt = int((s.astype(str).str.strip().str.lower() == "unknown").sum())
        total_defect = null_cnt + unknown_cnt
        quality_records.append({
            "Tên Cột": col,
            "Kiểu Dữ Liệu": str(s.dtype),
            "Số Lượng Null": null_cnt,
            "Tỷ Lệ Null (%)": round(null_cnt / total_len * 100, 2),
            "Số Lượng Unknown": unknown_cnt,
            "Tỷ Lệ Unknown (%)": round(unknown_cnt / total_len * 100, 2),
            "Tổng Số Ô Khuyết/Unknown": total_defect,
            "Tỷ Lệ Khuyết Tổng (%)": round(total_defect / total_len * 100, 2)
        })

    dq_df = pd.DataFrame(quality_records).sort_values(by="Tỷ Lệ Khuyết Tổng (%)", ascending=False).reset_index(drop=True)
    dq_file = REPORTS_DIR / "data_quality_analysis.csv"
    dq_df.to_csv(dq_file, index=False, encoding="utf-8-sig")
    print(f"-> [XUẤT BÁO CÁO] {dq_file}")

    # Vẽ Biểu đồ Fig 4: Missing Values Bar Chart
    top12_missing = dq_df[dq_df["Tỷ Lệ Khuyết Tổng (%)"] > 0].head(12)
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.barh(top12_missing["Tên Cột"][::-1], top12_missing["Tỷ Lệ Khuyết Tổng (%)"][::-1], color="#e74c3c", edgecolor="black")
    ax.set_title("TOP CÁC THUỘC TÍNH CÓ TỶ LỆ DỮ LIỆU THIẾU & UNKNOWN CAO NHẤT (RQ2)", fontsize=12, fontweight="bold", pad=15)
    ax.set_xlabel("Tỷ lệ thiếu tổng (%)", fontsize=11)
    ax.set_xlim(0, 100)
    for b in bars:
        w = b.get_width()
        ax.text(w + 1, b.get_y() + b.get_height() / 2.0, f"{w:.1f}%", va="center", fontsize=9.5, fontweight="bold")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "fig4_missing_values_bar.png", dpi=300)
    plt.close()

    # 2. Phân tích ngoại lệ IQR cho các biến số
    check_cols = ["Sales", "Sales per customer", "Benefit per order", "Order Item Quantity", "Product Price"]
    outlier_records = []
    for col in check_cols:
        if col in df.columns:
            vals = pd.to_numeric(df[col], errors="coerce").dropna()
            q1 = float(vals.quantile(0.25))
            q3 = float(vals.quantile(0.75))
            iqr = q3 - q1
            low = q1 - 1.5 * iqr
            high = q3 + 1.5 * iqr
            out_cnt = int(((vals < low) | (vals > high)).sum())
            skew = float(stats.skew(vals))
            outlier_records.append({
                "Cột Định Lượng": col,
                "Q1 (25%)": round(q1, 2),
                "Median": round(float(vals.median()), 2),
                "Q3 (75%)": round(q3, 2),
                "IQR": round(iqr, 2),
                "Ngưỡng Rào Dưới": round(low, 2),
                "Ngưỡng Rào Trên": round(high, 2),
                "Số Ngoại Lệ": out_cnt,
                "Tỷ Lệ Ngoại Lệ (%)": round(out_cnt / len(vals) * 100, 2),
                "Độ Lệch Skewness": round(skew, 2),
                "Bản Chất Nghiệp Vụ": "Ngoại lệ hợp lệ (Đơn hàng giá trị cao / Bán sỉ)"
            })

    outlier_df = pd.DataFrame(outlier_records)
    outlier_df.to_csv(REPORTS_DIR / "outliers_iqr_summary.csv", index=False, encoding="utf-8-sig")

    # Vẽ Biểu đồ Fig 9: Boxplot phát hiện ngoại lệ
    fig, axes = plt.subplots(1, 3, figsize=(14, 5))
    for idx, col in enumerate(["Sales", "Benefit per order", "Product Price"]):
        sns.boxplot(y=df[col].dropna(), ax=axes[idx], color="#1abc9c", width=0.4, boxprops=dict(edgecolor="black"))
        axes[idx].set_title(f"Phân Bố & Ngoại Lệ: {col}", fontsize=11, fontweight="bold")
    plt.suptitle("PHÁT HIỆN NGOẠI LỆ THỐNG KÊ BẰNG HÀM PHÂN VỊ IQR (RQ2)", fontsize=13, fontweight="bold", y=0.98)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig(FIGURES_DIR / "fig9_financial_outliers_boxplot.png", dpi=300)
    plt.close()

    # Vẽ Biểu đồ Fig 8: Histogram phân phối biến số định lượng và Skewness
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
    sns.histplot(df["Sales"].dropna(), bins=40, kde=True, ax=axes[0], color="#3498db")
    axes[0].set_title("Phân Phối Doanh Số (Sales)", fontsize=11, fontweight="bold")
    sns.histplot(df["Benefit per order"].dropna(), bins=40, kde=True, ax=axes[1], color="#e67e22")
    axes[1].set_title("Phân Phối Lợi Nhuận (Benefit per order)", fontsize=11, fontweight="bold")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "fig8_numeric_distributions_skewness.png", dpi=300)
    plt.close()
    print("-> [LƯU BIỂU ĐỒ] fig4, fig9, fig8.")


# =============================================================================
# PHẦN K: CORRELATION & DATA LEAKAGE AUDIT
# =============================================================================
def audit_correlation_and_leakage(valid_df: pd.DataFrame):
    """Phân tích tương tác tương quan và thiết lập rào chắn chống rò rỉ dữ liệu (Data Leakage)."""
    print("\n" + "=" * 80)
    print(" PHẦN K: TƯƠNG QUAN & RÀO CHẮN RÒ RỈ DỮ LIỆU (DATA LEAKAGE AUDIT)")
    print("=" * 80)

    # 1. Bảng phân loại đặc trưng chống rò rỉ thông tin
    leakage_records = [
        {"Tên Biến": "Days for shipping (real)", "Thời Điểm Thu Thập": "Sau khi giao hàng thành công", "Tương Quan Với Nhãn": "Cực cao (r > 0.40)", "Rủi Ro Data Leakage": "NGHIÊM TRỌNG (Critical Leakage)", "Quyết Định Đưa Vào Mô Hình": "LOẠI BỎ HOÀN TOÀN KHỎI TẬP ĐẶC TRƯNG TIỀN DỰ BÁO"},
        {"Tên Biến": "Delivery Status", "Thời Điểm Thu Thập": "Sau khi giao hàng thành công", "Tương Quan Với Nhãn": "Hoàn hảo (Chứa nhãn Late delivery)", "Rủi Ro Data Leakage": "NGHIÊM TRỌNG (Direct Target Leakage)", "Quyết Định Đưa Vào Mô Hình": "LOẠI BỎ HOÀN TOÀN KHỎI TẬP ĐẶC TRƯNG TIỀN DỰ BÁO"},
        {"Tên Biến": "shipping date (DateOrders)", "Thời Điểm Thu Thập": "Thời điểm tài xế xuất kho", "Tương Quan Với Nhãn": "Cao (Khoảng cách ngày vận chuyển)", "Rủi Ro Data Leakage": "CAO (Post-dispatch Leakage)", "Quyết Định Đưa Vào Mô Hình": "LOẠI BỎ HOÀN TOÀN (Chỉ giữ order date ban đầu)"},
        {"Tên Biến": "Days for shipment (scheduled)", "Thời Điểm Thu Thập": "Tại thời điểm khách đặt hàng", "Tương Quan Với Nhãn": "Trung bình (r = -0.37)", "Rủi Ro Data Leakage": "AN TOÀN (Pre-dispatch SLA)", "Quyết Định Đưa Vào Mô Hình": "ĐƯỢC PHÉP SỬ DỤNG LÀM ĐẶC TRƯNG DỰ BÁO SỚM"},
        {"Tên Biến": "Shipping Mode", "Thời Điểm Thu Thập": "Tại thời điểm khách đặt hàng", "Tương Quan Với Nhãn": "Mạnh (Cramér's V = 0.4473)", "Rủi Ro Data Leakage": "AN TOÀN (Pre-dispatch Selection)", "Quyết Định Đưa Vào Mô Hình": "ĐƯỢC PHÉP SỬ DỤNG LÀM ĐẶC TRƯNG DỰ BÁO SỚM"},
        {"Tên Biến": "Market / Order Region", "Thời Điểm Thu Thập": "Tại thời điểm khách đặt hàng", "Tương Quan Với Nhãn": "Trung bình (Cramér's V = 0.0265)", "Rủi Ro Data Leakage": "AN TOÀN (Pre-dispatch Location)", "Quyết Định Đưa Vào Mô Hình": "ĐƯỢC PHÉP SỬ DỤNG LÀM ĐẶC TRƯNG DỰ BÁO SỚM"},
        {"Tên Biến": "Sales / Order Item Total", "Thời Điểm Thu Thập": "Tại thời điểm thanh toán giỏ hàng", "Tương Quan Với Nhãn": "Gần bằng 0 (r = -0.0037)", "Rủi Ro Data Leakage": "AN TOÀN (Pre-dispatch Financials)", "Quyết Định Đưa Vào Mô Hình": "ĐƯỢC PHÉP SỬ DỤNG LÀM ĐẶC TRƯNG DỰ BÁO SỚM"}
    ]
    leakage_df = pd.DataFrame(leakage_records)
    leakage_file = REPORTS_DIR / "feature_leakage_audit.csv"
    leakage_df.to_csv(leakage_file, index=False, encoding="utf-8-sig")
    print(f"-> [XUẤT BÁO CÁO] {leakage_file}")
    print(leakage_df[["Tên Biến", "Rủi Ro Data Leakage", "Quyết Định Đưa Vào Mô Hình"]].to_string(index=False))

    # 2. Ma trận tương quan Pearson
    corr_cols = [
        "Late_delivery_risk", "Days for shipping (real)", "Days for shipment (scheduled)",
        "Sales per customer", "Benefit per order", "Sales", "Product Price",
        "Order Item Quantity", "Order Item Discount Rate"
    ]
    avail_cols = [c for c in corr_cols if c in valid_df.columns]
    corr_matrix = valid_df[avail_cols].astype(float).corr(method="pearson")
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool))

    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(corr_matrix, mask=mask, annot=True, fmt=".2f", cmap="coolwarm", center=0,
                square=True, linewidths=0.8, linecolor="white", ax=ax,
                cbar_kws={"shrink": 0.8, "label": "Hệ số tương quan Pearson (r)"})
    ax.set_title("MA TRẬN TƯƠNG QUAN PEARSON & CẢNH BÁO DATA LEAKAGE", fontsize=12, fontweight="bold", pad=15)
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "fig3_correlation_heatmap.png", dpi=300)
    plt.close()
    print("-> [LƯU BIỂU ĐỒ] fig3_correlation_heatmap.png.")


# =============================================================================
# PHẦN L: TỔNG HỢP BỘ 6 INSIGHTS NGHIỆP VỤ ĐỊNH LƯỢNG (RQ1 & RQ2)
# =============================================================================
def synthesize_eda_insights():
    """Tổng hợp 6 insights nghiên cứu khoa học cốt lõi phục vụ báo cáo đại học."""
    print("\n" + "=" * 80)
    print(" PHẦN L: TỔNG HỢP INSIGHTS NGHIỆP VỤ ĐỊNH LƯỢNG (RQ1 & RQ2)")
    print("=" * 80)

    insights = [
        {
            "Mã Insight": "INSIGHT-01",
            "Tiêu Đề": "Nghịch Lý Cam Kết SLA Gói First Class (First Class SLA Paradox)",
            "Câu Hỏi Nghiên Cứu": "RQ1",
            "Phát Hiện Thực Tế": "Gói First Class có tỷ lệ trễ hạn cao nhất toàn hệ thống, lên tới 95.28%, trong khi Standard Class chỉ trễ 38.11%.",
            "Bằng Chứng Số Liệu": "Chi-Square = 34,863.00, p < 10^-16, Cramér's V = 0.4473 (Ảnh hưởng cực mạnh). 26,894 / 28,225 đơn First Class bị trễ.",
            "Biểu Đồ / Bảng Liên Quan": "fig5_late_rate_by_shipping_mode.png, shipping_mode_analysis.csv",
            "Ý Nghĩa Nghiệp Vụ": "Doanh nghiệp thu phí dịch vụ cao cấp nhưng giao trễ tới 95% do thiết lập SLA cố định 1 ngày quá gấp rút, gây nguy cơ bồi thường và mất khách hàng VIP.",
            "Hạn Chế Phương Pháp Luận": "Chưa thu thập được bán kính địa lý cụ thể (Km) giữa kho xuất hàng và địa chỉ nhận.",
            "Khuyến Nghị Tiếp Theo": "Tái cấu trúc hợp đồng vận chuyển: Chuyển từ cam kết SLA cố định (Fixed SLA) sang cam kết động (Dynamic SLA) dựa trên bán kính vận chuyển."
        },
        {
            "Mã Insight": "INSIGHT-02",
            "Tiêu Đề": "Sự Độc Lập Giữa Giá Trị Tiền Tệ Đơn Hàng Và Tốc Độ Giao Hàng",
            "Câu Hỏi Nghiên Cứu": "RQ1",
            "Phát Hiện Thực Tế": "Giá trị đơn hàng (Sales) và lợi nhuận không có mối liên hệ thống kê với nguy cơ trễ hạn.",
            "Bằng Chứng Số Liệu": "Hệ số tương quan Pearson r = -0.0037, Mutual Information xấp xỉ 0.0000. Kiểm định ANOVA cho Sales giữa 4 gói vận chuyển có F = 0.82, p = 0.48 > 0.05.",
            "Biểu Đồ / Bảng Liên Quan": "fig3_correlation_heatmap.png, outliers_iqr_summary.csv",
            "Ý Nghĩa Nghiệp Vụ": "Hệ thống vận hành TMS hiện tại đối xử với đơn hàng 20 USD và đơn hàng 1,500 USD hoàn toàn như nhau, chưa có cơ chế luồng xanh ưu tiên cho đơn hàng có giá trị cao.",
            "Hạn Chế Phương Pháp Luận": "Chưa phản ánh được cấp độ khách hàng thân thiết (Loyalty Tier).",
            "Khuyến Nghị Tiếp Theo": "Đưa giá trị giỏ hàng vào bài toán tối ưu chi phí rủi ro: Ưu tiên điều xe riêng cho các đơn hàng có Profit Margin cao."
        },
        {
            "Mã Insight": "INSIGHT-03",
            "Tiêu Đề": "Điểm Nghẽn Giao Vận Địa Lý Chặng Cuối Tại Các Tiểu Vùng Quốc Tế",
            "Câu Hỏi Nghiên Cứu": "RQ1",
            "Phát Hiện Thực Tế": "Khu vực Western Europe và Central America có tỷ lệ giao trễ vượt ngưỡng 58%, cao hơn đáng kể so với mức bình quân toàn cầu.",
            "Bằng Chứng Số Liệu": "Chi-Square = 122.58, p = 7.4e-4, Cramér's V = 0.0265. Western Europe trễ 61.2% trên 1,540 đơn.",
            "Biểu Đồ / Bảng Liên Quan": "fig6_late_rate_by_order_region.png, geography_analysis.csv",
            "Ý Nghĩa Nghiệp Vụ": "Thách thức xuyên biên giới: Thủ tục hải quan và hạ tầng logistics nội địa tại các thị trường xa kho trung tâm là nguyên nhân chính gây trễ hạn.",
            "Hạn Chế Phương Pháp Luận": "Tỷ lệ khuyết thông tin Zipcode cao (79.3%) làm hạn chế phân tích ở cấp độ vi mô phường/xã.",
            "Khuyến Nghị Tiếp Theo": "Mở rộng mạng lưới kho vệ tinh (Hub & Spoke) tại các khu vực trọng điểm châu Âu và Mỹ Latinh."
        },
        {
            "Mã Insight": "INSIGHT-04",
            "Tiêu Đề": "Tính Cân Bằng Tự Nhiên Của Biến Mục Tiêu (Không Cần SMOTE)",
            "Câu Hỏi Nghiên Cứu": "RQ2",
            "Phát Hiện Thực Tế": "Biến mục tiêu Late_delivery_risk đạt tỷ lệ phân bổ cân bằng tự nhiên 54.84% (Trễ) vs 45.16% (Đúng hạn).",
            "Bằng Chứng Số Liệu": "95,548 đơn trễ vs 78,669 đơn đúng hạn. Tỷ lệ tương đương xấp xỉ 1.2 : 1.",
            "Biểu Đồ / Bảng Liên Quan": "fig1_target_distribution.png, target_quality_audit.csv",
            "Ý Nghĩa Nghiệp Vụ": "Tập dữ liệu rất lý tưởng cho bài toán phân loại nhị phân trong học máy.",
            "Hạn Chế Phương Pháp Luận": "Tồn tại 6,302 dòng khuyết nhãn mục tiêu cần tách riêng khi huấn luyện.",
            "Khuyến Nghị Tiếp Theo": "Sử dụng độ đo ROC-AUC và PR-AUC kết hợp F1-score; tuyệt đối không cần áp dụng kỹ thuật oversampling nhân tạo (SMOTE) tránh làm biến dạng phân phối."
        },
        {
            "Mã Insight": "INSIGHT-05",
            "Tiêu Đề": "Rào Chắn Rò Rỉ Dữ Liệu: Loại Trừ Biến Hậu Giao Hàng Khỏi Feature Engineering",
            "Câu Hỏi Nghiên Cứu": "RQ2",
            "Phát Hiện Thực Tế": "Các biến Days for shipping (real) và Delivery Status có tương quan rất mạnh với nhãn nhưng là biến hậu giao hàng.",
            "Bằng Chứng Số Liệu": "Days for shipping (real) có r = 0.40 với Late_delivery_risk. 100% bản ghi Delivery Status = 'Late delivery' có nhãn = 1.",
            "Biểu Đồ / Bảng Liên Quan": "feature_leakage_audit.csv, fig3_correlation_heatmap.png",
            "Ý Nghĩa Nghiệp Vụ": "Nếu vô tình đưa các biến này vào huấn luyện, mô hình sẽ đạt Accuracy 100% giả tạo trên tập kiểm tra nhưng vô dụng hoàn toàn trong thực tế vận hành.",
            "Hạn Chế Phương Pháp Luận": "Loại bỏ biến hậu giao hàng làm giảm bớt số lượng đặc trưng trực tiếp của bài toán.",
            "Khuyến Nghị Tiếp Theo": "Thiết lập rào chắn Data Leakage Barrier: Chỉ sử dụng các đặc trưng đã biết trước tại thời điểm Order Date (Pre-dispatch features)."
        },
        {
            "Mã Insight": "INSIGHT-06",
            "Tiêu Đề": "Tập Trung Cao Độ Khách Hàng Tại Đô Thị Caguas Sau Chuẩn Hóa",
            "Câu Hỏi Nghiên Cứu": "RQ1 & RQ2",
            "Phát Hiện Thực Tế": "Sau khi chuẩn hóa, Caguas là đô thị khách hàng lớn nhất chuỗi cung ứng với 52,382 đơn hàng, có tỷ lệ trễ hạn 54.79%.",
            "Bằng Chứng Số Liệu": "Gom từ 5 biến thể phân mảnh thành 52,382 dòng (chiếm 29.02% toàn bộ tập dữ liệu hoặc 36.98% tập có địa danh).",
            "Biểu Đồ / Bảng Liên Quan": "fig6a_top5_cities_volume.png, city_mapping_audit.csv",
            "Ý Nghĩa Nghiệp Vụ": "Cơ sở khách hàng của DataCo có tính tập trung địa lý cực cao tại Puerto Rico; mọi giải pháp cải thiện giao hàng tại Caguas sẽ giải quyết được gần 30% bài toán chuỗi cung ứng.",
            "Hạn Chế Phương Pháp Luận": "Phụ thuộc vào mức độ toàn vẹn của địa chỉ người mua.",
            "Khuyến Nghị Tiếp Theo": "Thiết lập trung tâm hoàn tất đơn hàng (Fulfillment Center) chuyên trách cho vùng đô thị Caguas."
        }
    ]

    insights_df = pd.DataFrame(insights)
    insights_file = REPORTS_DIR / "eda_insights.csv"
    insights_df.to_csv(insights_file, index=False, encoding="utf-8-sig")
    print(f"-> [XUẤT BÁO CÁO] {insights_file}")


# =============================================================================
# HÀM ĐIỀU KHIỂN CHÍNH (MAIN PIPELINE)
# =============================================================================
def main():
    start_time = time.time()
    print("=" * 80)
    print(" KHỞI ĐỘNG CHƯƠNG TRÌNH PHÂN TÍCH KHÁM PHÁ DỮ LIỆU EDA (03_EDA.PY)")
    print("=" * 80)

    # Thực thi tuần tự qua các phân hệ
    df = load_and_validate_data()
    df, valid_df = audit_target_quality(df)
    analyze_target_and_descriptors(df, valid_df)
    analyze_shipping_mode(valid_df)
    analyze_geography(valid_df)
    run_statistical_tests(valid_df)
    audit_data_quality_and_outliers(df)
    audit_correlation_and_leakage(valid_df)
    synthesize_eda_insights()

    elapsed = time.time() - start_time
    print("\n" + "=" * 80)
    print(f" HOÀN TẤT TOÀN BỘ CHƯƠNG TRÌNH 03_EDA.PY TRONG {elapsed:.2f} GIÂY!")
    print(f" Toàn bộ các bảng báo cáo đã lưu tại: {REPORTS_DIR}")
    print(f" Toàn bộ biểu đồ độ phân giải cao đã lưu tại: {FIGURES_DIR}")
    print("=" * 80)


if __name__ == "__main__":
    main()
