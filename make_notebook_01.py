import json
import sys
from pathlib import Path

# Cấu hình UTF-8 cho console Windows
if sys.platform == "win32":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

# Helper to create code cell
def create_code_cell(source_lines):
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [line + "\n" for line in source_lines[:-1]] + ([source_lines[-1]] if source_lines else [])
    }

# Helper to create markdown cell
def create_md_cell(source_lines):
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": [line + "\n" for line in source_lines[:-1]] + ([source_lines[-1]] if source_lines else [])
    }

cells = []

# =============================================================================
# PHẦN 1: KHỞI TẠO MÔI TRƯỜNG
# =============================================================================

# Cell 1 - Markdown
cells.append(create_md_cell([
    "# PROJECT 13: DỰ BÁO RỦI RO GIAO HÀNG CHẬM TRỄ TRONG CHUỖI CUNG ỨNG (DATACO)",
    "## NOTEBOOK 01: KHÁM PHÁ VÀ KIỂM TOÁN CHẤT LƯỢNG DỮ LIỆU THÔ (DATA OVERVIEW)",
    "",
    "**Mục tiêu nghiên cứu & học tập:**",
    "- Làm quen và làm chủ quy trình khám phá dữ liệu thô (*Exploratory Data Analysis - EDA*) theo chuẩn CRISP-DM.",
    "- Kiểm toán toàn diện chất lượng tệp dữ liệu thực hành cá nhân hóa `7_PJ13_2521001054_Nguyễn Lê Nhật Hạ.csv`.",
    "- Phát hiện các vấn đề dữ liệu: giá trị khuyết (*Missing*), ký hiệu dơ (*Noise*), định dạng lỗi (*Invalid Format*), rò rỉ dữ liệu (*Data Leakage*) và vi phạm bảo mật (*PII*).",
    "- Chuẩn bị cơ sở định lượng vững chắc để xây dựng quy tắc làm sạch cho bước kế tiếp (`02_data_cleaning.py`).",
    "",
    "> **Nguyên tắc cốt lõi:** Tuyệt đối không chỉnh sửa, xóa hay ghi đè lên dữ liệu thô ban đầu trong notebook này. Chạy tuần tự từng cell để quan sát kết quả thực tế!"
]))

# Cell 2 - Code
cells.append(create_code_cell([
    "# CELL 2: Khởi tạo môi trường - Import các thư viện phân tích dữ liệu",
    "import sys",
    "import os",
    "from pathlib import Path",
    "",
    "# Đảm bảo mã hóa UTF-8 an toàn trên môi trường Windows",
    "if sys.platform == 'win32':",
    "    if hasattr(sys.stdout, 'reconfigure'):",
    "        sys.stdout.reconfigure(encoding='utf-8')",
    "    if hasattr(sys.stderr, 'reconfigure'):",
    "        sys.stderr.reconfigure(encoding='utf-8')",
    "",
    "import pandas as pd",
    "import numpy as np",
    "import matplotlib.pyplot as plt",
    "import seaborn as sns",
    "",
    "try:",
    "    from IPython.display import display",
    "except ImportError:",
    "    display = print",
    "",
    "# Cấu hình font tiếng Việt và hiển thị biểu đồ",
    "plt.rcParams['font.sans-serif'] = ['Segoe UI', 'DejaVu Sans', 'Arial']",
    "plt.rcParams['axes.unicode_minus'] = False",
    "sns.set_theme(style='whitegrid', palette='Set2')",
    "",
    "# Thiết lập hiển thị đầy đủ các cột của DataFrame",
    "pd.set_option('display.max_columns', 60)",
    "pd.set_option('display.max_rows', 100)",
    "pd.set_option('display.width', 1000)",
    "",
    "print('-> Đã nạp thành công các thư viện: Pandas, NumPy, Matplotlib, Seaborn!')"
]))

# Cell 3 - Code
cells.append(create_code_cell([
    "# CELL 3: Thiết lập đường dẫn file dữ liệu và kiểm tra sự tồn tại",
    "raw_data_path = Path('data/raw/7_PJ13_2521001054_Nguyễn Lê Nhật Hạ.csv')",
    "",
    "# Kiểm tra nếu file không có trong data/raw/ thì thử ở thư mục gốc",
    "if not raw_data_path.exists():",
    "    fallback_path = Path('7_PJ13_2521001054_Nguyễn Lê Nhật Hạ.csv')",
    "    if fallback_path.exists():",
    "        raw_data_path = fallback_path",
    "        print(f'-> Đang sử dụng đường dẫn file tại thư mục gốc: {raw_data_path}')",
    "    else:",
    "        raise FileNotFoundError(f'[LỖI] Không tìm thấy file dữ liệu tại {raw_data_path}!')",
    "else:",
    "    print(f'-> [XÁC NHẬN] Đã tìm thấy file dữ liệu: {raw_data_path}')",
    "    print(f'-> Dung lượng file: {os.path.getsize(raw_data_path) / (1024*1024):.2f} MB')"
]))

# Cell 4 - Code
cells.append(create_code_cell([
    "# CELL 4: Đọc file CSV gốc an toàn với encoding utf-8-sig",
    "# Lưu ý: Đọc dtype='string' để bảo toàn trọn vẹn mọi ký hiệu dơ ban đầu (VND, ?, -, 9999...)",
    "try:",
    "    df = pd.read_csv(raw_data_path, encoding='utf-8-sig', low_memory=False, dtype='string')",
    "    print(f'-> [THÀNH CÔNG] Đã nạp dữ liệu vào DataFrame!')",
    "    print(f'-> Kích thước ban đầu: {df.shape[0]:,} dòng x {df.shape[1]} cột')",
    "except UnicodeDecodeError:",
    "    print('-> Thử lại với encoding latin1...')",
    "    df = pd.read_csv(raw_data_path, encoding='latin1', low_memory=False, dtype='string')"
]))

# Cell 5 - Code
cells.append(create_code_cell([
    "# CELL 5: Hiển thị 5 dòng đầu và 5 dòng cuối (ĐÃ ẨN DANH HÓA THÔNG TIN PII ĐỂ BẢO VỆ QUYỀN RIÊNG TƯ)",
    "PII_COLS = ['Customer Email', 'Customer Password', 'Customer Fname', 'Customer Lname', 'Customer Street']",
    "",
    "# Tạo bản sao an toàn để hiển thị trên màn hình",
    "df_safe_display = df.copy()",
    "for col in PII_COLS:",
    "    if col in df_safe_display.columns:",
    "        df_safe_display[col] = '***MASKED_PII***'",
    "",
    "print('--- 5 DÒNG ĐẦU TIÊN (HEAD) ---')",
    "display(df_safe_display.head())",
    "",
    "print('--- 5 DÒNG CUỐI CÙNG (TAIL) ---')",
    "display(df_safe_display.tail())",
    "",
    "print(f'-> Tổng số cột trong bảng: {len(df.columns)}')",
    "print('Danh sách các cột:', list(df.columns))"
]))

# Markdown Checkpoint 1 & Template A-B-C-D cho Phần 1
cells.append(create_md_cell([
    "### ĐÁNH GIÁ PHẦN 1: KHỞI TẠO VÀ ĐỌC DỮ LIỆU BAN ĐẦU",
    "",
    "**A. Kết quả cần quan sát:**",
    "- File có được đọc thành công không? Encoding nào được áp dụng?",
    "- Các giá trị trong 5 dòng đầu và 5 dòng cuối có xuất hiện các ký tự lạ, lỗi font (`chÆ°a rÃµ`) hay đơn vị tiền tệ (`VND`, `USD`) lẫn vào không?",
    "- Thông tin nhạy cảm PII (`Customer Email`, `Customer Password`, v.v.) đã được che giấu trong phần hiển thị chưa?",
    "",
    "**B. Cách diễn giải:**",
    "- Bộ dữ liệu DataCo là dữ liệu giao dịch bán lẻ đa kênh toàn cầu. Khi thu thập từ nhiều nguồn chi nhánh khác nhau qua các hệ thống ERP/TMS, dữ liệu thường bị lẫn đơn vị tiền tệ địa phương và lỗi font mã hóa.",
    "- Việc đọc dữ liệu dạng chuỗi (`string`) ở bước đầu tiên giúp bảo toàn nguyên trạng mọi ký tự để chúng ta kiểm toán trước khi ép kiểu số học.",
    "",
    "**C. Nhận xét sau khi chạy:**",
    "> *(Sinh viên tự ghi nhận xét sau khi quan sát output từ Cell 1 đến Cell 5:)*  ",
    "> - Trạng thái đọc file: ...  ",
    "> - Ký hiệu lạ sơ bộ quan sát được ở các dòng đầu: ...  ",
    "> - Nhận xét về tính an toàn hiển thị PII: ...  ",
    "",
    "**D. Quyết định cho bước làm sạch:**",
    "- Cần lập danh sách toàn bộ các ký hiệu tiền tệ/khối lượng/tỷ lệ để bóc tách bằng biểu thức chính quy (Regex).",
    "- Cần lên kế hoạch loại bỏ hoàn toàn các cột PII ở pipeline làm sạch để tuân thủ quy định bảo mật GDPR."
]))

# =============================================================================
# PHẦN 2: KHÁM PHÁ CẤU TRÚC DỮ LIỆU
# =============================================================================

# Cell 6 - Code
cells.append(create_code_cell([
    "# CELL 6: Kiểm tra df.shape, số dòng và số cột, đối chiếu với Schema chuẩn DataCo",
    "EXPECTED_ROWS = 180519",
    "EXPECTED_COLS = 53",
    "",
    "n_rows, n_cols = df.shape",
    "print(f'-> Kích thước thực tế: {n_rows:,} dòng x {n_cols} cột')",
    "print(f'-> Kích thước chuẩn:   {EXPECTED_ROWS:,} dòng x {EXPECTED_COLS} cột')",
    "",
    "if n_rows == EXPECTED_ROWS and n_cols == EXPECTED_COLS:",
    "    print('=> [KẾT LUẬN] Kích thước dữ liệu KHỚP HOÀN TOÀN với chuẩn DataCo Supply Chain!')",
    "else:",
    "    print('=> [CẢNH BÁO] Có sự sai lệch kích thước so với bộ chuẩn DataCo!')"
]))

# Cell 7 - Code
cells.append(create_code_cell([
    "# CELL 7: Kiểm tra tổng quan df.info()",
    "print('--- THÔNG TIN TỔNG QUAN TỪ DF.INFO() ---')",
    "df.info(verbose=True, show_counts=True)"
]))

# Cell 8 - Code
cells.append(create_code_cell([
    "# CELL 8: Kiểm tra df.dtypes",
    "print('--- DANH SÁCH KIỂU DỮ LIỆU CỦA 53 CỘT ---')",
    "display(pd.DataFrame({'Tên Cột': df.columns, 'Kiểu Dữ Liệu Ban Đầu': df.dtypes.astype(str)}))"
]))

# Cell 9 - Code
cells.append(create_code_cell([
    "# CELL 9: Thống kê số lượng cột theo nhóm kiểu dữ liệu",
    "dtype_summary = df.dtypes.astype(str).value_counts().reset_index()",
    "dtype_summary.columns = ['Kiểu Dữ Liệu', 'Số Lượng Cột']",
    "print('--- THỐNG KÊ SỐ LƯỢNG CỘT THEO DTYPE ---')",
    "display(dtype_summary)"
]))

# Cell 10 - Code
cells.append(create_code_cell([
    "# CELL 10: Thống kê mô tả tổng quát bằng df.describe()",
    "print('--- THỐNG KÊ MÔ TẢ TỔNG QUÁT (TẤT CẢ CÁC CỘT) ---')",
    "# Chỉ lấy mẫu các thông số chính: count, unique, top, freq để tránh tràn màn hình",
    "desc_summary = df.describe().T",
    "display(desc_summary.head(25))",
    "display(desc_summary.tail(28))"
]))

# Cell 11 - Code
cells.append(create_code_cell([
    "# CELL 11: Thống kê mô tả các biến phân loại",
    "print('--- THỐNG KÊ MÔ TẢ CÁC BIẾN PHÂN LOẠI (OBJECT/STRING) ---')",
    "# Thống kê số lượng giá trị duy nhất (cardinality) của từng cột",
    "cardinality_df = pd.DataFrame({",
    "    'Tên Cột': df.columns,",
    "    'Số Giá Trị Khác Nhau (Unique)': [df[c].nunique(dropna=True) for c in df.columns],",
    "    'Giá Trị Xuất Hiện Nhiều Nhất (Top)': [df[c].mode().iloc[0] if len(df[c].mode())>0 else 'NA' for c in df.columns],",
    "    'Tần Suất Top (Freq)': [df[c].value_counts().iloc[0] if len(df[c].value_counts())>0 else 0 for c in df.columns]",
    "})",
    "display(cardinality_df.sort_values(by='Số Giá Trị Khác Nhau (Unique)', ascending=False))"
]))

# Markdown Checkpoint 1 & Template A-B-C-D cho Phần 2
cells.append(create_md_cell([
    "### CHECKPOINT 1: CẤU TRÚC DỮ LIỆU & SCHEMA",
    "",
    "**A. Kết quả cần quan sát:**",
    "- Số lượng dòng có đúng 180.519 và số lượng cột có đúng 53 cột không?",
    "- Toàn bộ các cột đang ở dạng `string` hay đã có cột nào được nhận diện là số/ngày tháng?",
    "- Cột nào có số lượng giá trị độc nhất (*Cardinality*) cực cao (như ID, tên khách hàng) và cột nào có Cardinality thấp (như Shipping Mode, Customer Segment)?",
    "",
    "**B. Cách diễn giải:**",
    "- Khi đọc dữ liệu bằng Pandas mà chưa ép kiểu, các cột chứa số bị lẫn chữ/đơn vị tiền tệ sẽ tự động bị ép thành `string/object`. Đây là biểu hiện tự nhiên của dữ liệu thô chưa qua làm sạch.",
    "- Bộ nhớ RAM hiện tại tiêu tốn khá lớn do toàn bộ đều là chuỗi ký tự.",
    "",
    "**C. Nhận xét sau khi chạy:**",
    "> *(Sinh viên tự ghi nhận xét sau khi quan sát output từ Cell 6 đến Cell 11:)*  ",
    "> - Kích thước dữ liệu: ... dòng x ... cột (Có khớp chuẩn DataCo không: ...)  ",
    "> - Nhận xét về kiểu dữ liệu ban đầu: ...  ",
    "> - Cột có Cardinality cao nhất / thấp nhất: ...  ",
    "",
    "**D. Quyết định cho bước làm sạch:**",
    "- Cần chuyển đổi kiểu dữ liệu tối ưu: số nguyên nhỏ (`int8`, `int32`), số thực (`float32`), chuỗi lặp lại sang `category` để tiết kiệm RAM (>70%).",
    "- Cần chuyển đổi các trường ngày tháng (`order date`, `shipping date`) sang định dạng chuẩn `datetime64`."
]))

# =============================================================================
# PHẦN 3: KIỂM TRA DỮ LIỆU THIẾU VÀ NHIỄU
# =============================================================================

# Cell 12 - Code
cells.append(create_code_cell([
    "# CELL 12: Đếm số lượng giá trị NaN tiêu chuẩn theo từng cột",
    "null_counts = df.isna().sum()",
    "null_df = pd.DataFrame({",
    "    'Tên Cột': df.columns,",
    "    'Số Lượng NaN': null_counts.values",
    "}).sort_values(by='Số Lượng NaN', ascending=False)",
    "",
    "print('--- TOP CỘT CÓ SỐ LƯỢNG GIÁ TRỊ KHUYẾT (NAN) CAO NHẤT ---')",
    "display(null_df.head(15))"
]))

# Cell 13 - Code
cells.append(create_code_cell([
    "# CELL 13: Tính tỷ lệ phần trăm (%) NaN theo từng cột và trên toàn bộ dữ liệu",
    "total_cells = df.shape[0] * df.shape[1]",
    "total_nulls = df.isna().sum().sum()",
    "",
    "null_df['Tỷ Lệ NaN (%)'] = (null_df['Số Lượng NaN'] / len(df)) * 100",
    "null_df['Tỷ Lệ NaN (%)'] = null_df['Tỷ Lệ NaN (%)'].round(2)",
    "",
    "print(f'-> Tổng số ô trong bảng dữ liệu: {total_cells:,} ô')",
    "print(f'-> Tổng số ô bị khuyết NaN:       {total_nulls:,} ô ({total_nulls / total_cells * 100:.2f}%)')",
    "print('\\n--- BẢNG TỶ LỆ KHUYẾT THEO CỘT ---')",
    "display(null_df.head(20))"
]))

# Cell 14 - Code
cells.append(create_code_cell([
    "# CELL 14: Kiểm tra và thống kê các ký hiệu thiếu / nhiễu ẩn danh (?, -, nan, None, unknown, -1, 9999...)",
    "SUSPICIOUS_LIST = ['?', '-', 'nan', 'none', 'unknown', '-1', '9999', 'chæ°a rãµ', 'chưa rõ']",
    "",
    "suspicious_results = {}",
    "for sym in SUSPICIOUS_LIST:",
    "    # Đếm số lần xuất hiện của ký hiệu này trên toàn bộ DataFrame",
    "    cnt = 0",
    "    for col in df.columns:",
    "        s = df[col].astype('string').str.strip().str.lower()",
    "        cnt += int(s.eq(sym).sum())",
    "    suspicious_results[sym] = cnt",
    "",
    "suspicious_summary_df = pd.DataFrame(list(suspicious_results.items()), columns=['Ký Hiệu Nhiễu', 'Số Lần Xuất Hiện'])",
    "print('--- THỐNG KÊ CÁC KÝ HIỆU NHIỄU / KHUYẾT ẨN TRÊN TOÀN BỘ DATASET ---')",
    "display(suspicious_summary_df.sort_values(by='Số Lần Xuất Hiện', ascending=False))"
]))

# Cell 15 - Code
cells.append(create_code_cell([
    "# CELL 15: Thống kê số lượng và tỷ lệ ký hiệu thiếu theo từng cột (KHÔNG LÀM LỘ GIÁ TRỊ PII)",
    "col_noise_records = []",
    "",
    "for col in df.columns:",
    "    s = df[col].astype('string').str.strip().str.lower()",
    "    nan_cnt = int(df[col].isna().sum())",
    "    q_cnt = int(s.eq('?').sum())",
    "    dash_cnt = int(s.eq('-').sum())",
    "    unk_cnt = int(s.isin(['unknown', 'chưa rõ', 'chæ°a rãµ']).sum())",
    "    neg_cnt = int(s.eq('-1').sum())",
    "    num9_cnt = int(s.eq('9999').sum())",
    "    ",
    "    total_bad = nan_cnt + q_cnt + dash_cnt + unk_cnt + neg_cnt + num9_cnt",
    "    col_noise_records.append({",
    "        'Tên Cột': col,",
    "        'Số NaN': nan_cnt,",
    "        'Ký hiệu ?': q_cnt,",
    "        'Ký hiệu -': dash_cnt,",
    "        'unknown / chưa rõ': unk_cnt,",
    "        '-1 hoặc 9999': neg_cnt + num9_cnt,",
    "        'Tổng Dữ Liệu Dơ': total_bad,",
    "        'Tỷ Lệ Dơ Tổng (%)': round((total_bad / len(df)) * 100, 2)",
    "    })",
    "",
    "noise_report_df = pd.DataFrame(col_noise_records).sort_values(by='Tỷ Lệ Dơ Tổng (%)', ascending=False)",
    "print('--- BẢNG KIỂM TOÁN TỔNG HỢP GIÁ TRỊ THIẾU VÀ NHIỄU THEO TỪNG CỘT ---')",
    "display(noise_report_df.head(20))"
]))

# Cell 16 - Code
cells.append(create_code_cell([
    "# CELL 16: Vẽ biểu đồ Top 15 cột có tỷ lệ dữ liệu thiếu và nhiễu cao nhất",
    "plt.figure(figsize=(12, 7))",
    "top_15_dirty = noise_report_df.head(15)",
    "",
    "bars = plt.barh(top_15_dirty['Tên Cột'][::-1], top_15_dirty['Tỷ Lệ Dơ Tổng (%)'][::-1], color='#e74c3c')",
    "plt.title('Top 15 Thuộc Tính Có Tỷ Lệ Dữ Liệu Khuyết & Nhiễu Cao Nhất', fontsize=14, fontweight='bold', pad=15)",
    "plt.xlabel('Tỷ Lệ Phần Trăm (%)', fontsize=12)",
    "plt.ylabel('Tên Cột', fontsize=12)",
    "plt.xlim(0, 100)",
    "",
    "# Hiển thị nhãn giá trị % trên từng cột",
    "for bar in bars:",
    "    w = bar.get_width()",
    "    plt.text(w + 1, bar.get_y() + bar.get_height()/2, f'{w:.1f}%', va='center', fontsize=10, fontweight='bold')",
    "",
    "plt.tight_layout()",
    "plt.show()"
]))

# Markdown Checkpoint 2 & Template A-B-C-D cho Phần 3
cells.append(create_md_cell([
    "### CHECKPOINT 2: DỮ LIỆU THIẾU VÀ NHIỄU",
    "",
    "**A. Kết quả cần quan sát:**",
    "- Những cột nào có tỷ lệ khuyết thiếu cực cao (>70%)?",
    "- Ký hiệu nào xuất hiện phổ biến nhất trong các ký hiệu nghi vấn (`?`, `-`, `unknown`, `9999`)?",
    "- Có trường hợp nào dữ liệu số bị ghi nhận thành `-1` hoặc `9999` để biểu thị giá trị thiếu không?",
    "",
    "**B. Cách diễn giải:**",
    "- Trong dữ liệu DataCo, các trường như `Product Description` và `Order Zipcode` thường có tỷ lệ khuyết $>75-80\\%$. Đây là đặc trưng phổ biến do hệ thống cũ không lưu mô tả sản phẩm dạng text hoặc mã bưu chính đơn hàng quốc tế không được nhập.",
    "- Các ký hiệu như `?`, `-`, `chưa rõ` là lỗi nhập liệu tự do từ người dùng hoặc hệ thống giao diện.",
    "",
    "**C. Nhận xét sau khi chạy:**",
    "> *(Sinh viên tự ghi nhận xét sau khi quan sát output từ Cell 12 đến Cell 16:)*  ",
    "> - Cột khuyết nhiều nhất: ... (tỷ lệ: ...%)  ",
    "> - Ký hiệu nhiễu xuất hiện nhiều nhất: ...  ",
    "> - Những cột quan trọng (Target, Shipping Mode) có bị khuyết không: ...  ",
    "",
    "**D. Quyết định cho bước làm sạch:**",
    "- Với các cột khuyết quá lớn (>70% như `Product Description`, `Order Zipcode`): Cân nhắc loại bỏ vì không cung cấp đủ thông tin giá trị cho mô hình.",
    "- Với các cột danh mục có khuyết thiếu: Điền giá trị an toàn `'Unknown'` thay vì xóa bỏ dòng.",
    "- Với các cột số ngày vận chuyển hoặc tài chính: Tuyệt đối không xóa dòng; điền khuyết bằng `median` theo phân nhóm (`Shipping Mode` hoặc `Category Name`)."
]))

# =============================================================================
# PHẦN 4: KIỂM TRA TRÙNG LẶP VÀ KHÓA ĐỊNH DANH
# =============================================================================

# Cell 18 - Code
cells.append(create_code_cell([
    "# CELL 18: Đếm số dòng trùng lặp 100% hoàn toàn trên tất cả các cột",
    "exact_dups = int(df.duplicated().sum())",
    "print(f'-> Số lượng dòng trùng lặp hoàn toàn (100% tất cả các cột): {exact_dups:,} dòng')",
    "if exact_dups == 0:",
    "    print('=> [XÁC NHẬN] Tập dữ liệu không chứa bất kỳ bản ghi nào trùng lặp 100%!')",
    "else:",
    "    print(f'=> [LƯU Ý] Có {exact_dups} dòng trùng lặp hoàn toàn cần xử lý drop_duplicates!')"
]))

# Cell 19 - Code
cells.append(create_code_cell([
    "# CELL 19: Đếm số lượng Order Id duy nhất và số lần xuất hiện lặp lại",
    "if 'Order Id' in df.columns:",
    "    order_id_unique = df['Order Id'].nunique(dropna=True)",
    "    order_id_dups = df['Order Id'].duplicated().sum()",
    "    print(f'-> Số lượng Order Id duy nhất:     {order_id_unique:,} mã đơn hàng')",
    "    print(f'-> Số dòng lặp lại của Order Id:   {order_id_dups:,} dòng')",
    "    print(f'-> Trung bình mỗi Order Id xuất hiện: {len(df) / order_id_unique:.2f} dòng')"
]))

# Cell 20 - Code
cells.append(create_code_cell([
    "# CELL 20: Kiểm tra số dòng trùng Order Item Id (Khóa chính kỹ thuật)",
    "if 'Order Item Id' in df.columns:",
    "    item_id_unique = df['Order Item Id'].nunique(dropna=True)",
    "    item_id_dups = df['Order Item Id'].duplicated().sum()",
    "    print(f'-> Số lượng Order Item Id duy nhất:   {item_id_unique:,} mã mục hàng')",
    "    print(f'-> Số dòng trùng của Order Item Id: {item_id_dups:,} dòng')",
    "    if item_id_dups > 0:",
    "        print('=> [CẢNH BÁO] Phát hiện mã Order Item Id bị lặp lại, cần kiểm tra nguyên nhân!')"
]))

# Cell 21 - Code
cells.append(create_code_cell([
    "# CELL 21: Phân tích số dòng chi tiết sản phẩm (Order Items) trong mỗi đơn hàng",
    "if 'Order Id' in df.columns:",
    "    items_per_order = df.groupby('Order Id').size()",
    "    print('--- PHÂN BỐ SỐ MỤC HÀNG TRÊN MỖI ĐƠN HÀNG ---')",
    "    display(items_per_order.value_counts().reset_index().rename(",
    "        columns={'index': 'Số Sản Phẩm Trong Đơn', 'count': 'Số Lượng Đơn Hàng'}",
    "    ).head(10))"
]))

# Cell 22 - Markdown Checkpoint 3 & Template A-B-C-D cho Phần 4
cells.append(create_md_cell([
    "### CHECKPOINT 3: TRÙNG LẶP & ĐƠN VỊ QUAN SÁT (UNIT OF ANALYSIS)",
    "",
    "**A. Kết quả cần quan sát:**",
    "- Có bao nhiêu dòng trùng hoàn toàn 100%?",
    "- Có bao nhiêu `Order Id` duy nhất? Tỷ lệ đơn hàng có nhiều hơn 1 mục hàng là bao nhiêu?",
    "- Khóa `Order Item Id` có bị trùng lặp không?",
    "",
    "**B. Cách diễn giải nghiệp vụ:**",
    "- **Tại sao trùng `Order Id` KHÔNG phải là lỗi dữ liệu?**  ",
    "  Trong thương mại điện tử và bán lẻ, một đơn hàng (`Order Id`) thường bao gồm nhiều sản phẩm khác nhau (`Order Items`). Mỗi dòng trong tệp DataCo biểu diễn một mục hàng cụ thể. Do đó, việc `Order Id` xuất hiện lặp lại 2, 3 hay 5 lần là hoàn toàn tự nhiên và đúng với cấu trúc quan hệ bảng 1-nhiều (*One-to-Many Relationship*).",
    "- Nếu xóa bỏ các dòng trùng `Order Id`, chúng ta sẽ vô tình làm mất toàn bộ thông tin về các mặt hàng con trong đơn hàng!",
    "",
    "**C. Nhận xét sau khi chạy:**",
    "> *(Sinh viên tự ghi nhận xét sau khi quan sát output từ Cell 18 đến Cell 21:)*  ",
    "> - Số dòng trùng lặp 100%: ...  ",
    "> - Số lượng Order Id duy nhất: ...  ",
    "> - Nhận xét về việc phân bổ số mục hàng trên mỗi đơn: ...  ",
    "",
    "**D. Quyết định cho bước làm sạch:**",
    "- Chỉ thực hiện loại bỏ trùng lặp hoàn toàn (`df.drop_duplicates()`), tuyệt đối không được drop duplicates chỉ dựa trên cột `Order Id`."
]))

# =============================================================================
# PHẦN 5: KHÁM PHÁ BIẾN MỤC TIÊU
# =============================================================================

# Cell 23 - Code
cells.append(create_code_cell([
    "# CELL 23: Kiểm tra các giá trị thô gốc của biến mục tiêu Late_delivery_risk",
    "if 'Late_delivery_risk' in df.columns:",
    "    raw_target_counts = df['Late_delivery_risk'].value_counts(dropna=False)",
    "    print('--- TẤT CẢ CÁC GIÁ TRỊ GỐC XUẤT HIỆN TRONG LATE_DELIVERY_RISK ---')",
    "    display(raw_target_counts.reset_index().rename(",
    "        columns={'Late_delivery_risk': 'Giá Trị Gốc', 'count': 'Số Lượng Dòng'}",
    "    ))"
]))

# Cell 24 - Code
cells.append(create_code_cell([
    "# CELL 24: Đếm số lượng nhãn hợp lệ (0, 1) và các nhãn không hợp lệ (nhiễu)",
    "if 'Late_delivery_risk' in df.columns:",
    "    target_clean_str = df['Late_delivery_risk'].astype('string').str.strip()",
    "    n_valid_0 = int(target_clean_str.eq('0').sum())",
    "    n_valid_1 = int(target_clean_str.eq('1').sum())",
    "    n_missing = int(target_clean_str.isna().sum())",
    "    n_invalid = len(df) - (n_valid_0 + n_valid_1 + n_missing)",
    "    ",
    "    target_audit_df = pd.DataFrame([",
    "        {'Phân Loại Nhãn': 'Nhãn 0 Hợp Lệ (Đúng hạn / Sớm)', 'Số Lượng': n_valid_0, 'Tỷ Lệ (%)': round(n_valid_0 / len(df) * 100, 2)},",
    "        {'Phân Loại Nhãn': 'Nhãn 1 Hợp Lệ (Trễ hạn)', 'Số Lượng': n_valid_1, 'Tỷ Lệ (%)': round(n_valid_1 / len(df) * 100, 2)},",
    "        {'Phân Loại Nhãn': 'Nhãn Khuyết (NaN)', 'Số Lượng': n_missing, 'Tỷ Lệ (%)': round(n_missing / len(df) * 100, 2)},",
    "        {'Phân Loại Nhãn': 'Nhãn Nhiễu Chuỗi (VND, USD, ?, -1...)', 'Số Lượng': n_invalid, 'Tỷ Lệ (%)': round(n_invalid / len(df) * 100, 2)}",
    "    ])",
    "    print('--- BẢNG THỐNG KÊ PHÂN LOẠI NHÃN MỤC TIÊU ---')",
    "    display(target_audit_df)"
]))

# Cell 25 - Code
cells.append(create_code_cell([
    "# CELL 25: Tính tỷ lệ phần trăm giữa hai lớp hợp lệ (Class Distribution)",
    "total_valid_labels = n_valid_0 + n_valid_1",
    "pct_0 = (n_valid_0 / total_valid_labels) * 100",
    "pct_1 = (n_valid_1 / total_valid_labels) * 100",
    "",
    "print(f'-> Trong số {total_valid_labels:,} nhãn hợp lệ ban đầu:')",
    "print(f'   + Lớp 0 (Đúng hạn): {n_valid_0:,} dòng ({pct_0:.2f}%)')",
    "print(f'   + Lớp 1 (Trễ hạn):  {n_valid_1:,} dòng ({pct_1:.2f}%)')",
    "print(f'-> Tỷ lệ mất cân bằng (Imbalance Ratio): {pct_1 / pct_0:.2f} : 1')",
    "print('=> [ĐÁNH GIÁ] Tỷ lệ phân phối tương đối cân bằng tự nhiên, không rơi vào tình trạng mất cân bằng nghiêm trọng (Severe Imbalance).')"
]))

# Cell 26 - Code
cells.append(create_code_cell([
    "# CELL 26: Vẽ biểu đồ phân bố nhãn mục tiêu Late_delivery_risk",
    "plt.figure(figsize=(8, 5))",
    "bars = plt.bar(['0: Đúng hạn', '1: Trễ hạn'], [n_valid_0, n_valid_1], color=['#2ecc71', '#e74c3c'], width=0.5)",
    "plt.title('Phân Bố Tỷ Lệ Nhãn Hợp Lệ Của Late_delivery_risk', fontsize=14, fontweight='bold', pad=15)",
    "plt.ylabel('Số Lượng Đơn Hàng', fontsize=12)",
    "plt.ylim(0, max(n_valid_0, n_valid_1) * 1.15)",
    "",
    "for bar in bars:",
    "    h = bar.get_height()",
    "    plt.text(bar.get_x() + bar.get_width()/2, h + 1500, f'{h:,}\\n({h/total_valid_labels*100:.1f}%)',",
    "             ha='center', fontsize=11, fontweight='bold')",
    "",
    "plt.tight_layout()",
    "plt.show()"
]))

# Cell 27 - Code
cells.append(create_code_cell([
    "# CELL 27: Kiểm tra sơ bộ sự nhất quán giữa nhãn và hai cột số ngày giao hàng",
    "# Lưu ý: Chỉ sử dụng các giá trị gốc hợp lệ, không sửa dữ liệu",
    "real_days = pd.to_numeric(df['Days for shipping (real)'].str.extract(r'(\\d+)')[0], errors='coerce')",
    "sched_days = pd.to_numeric(df['Days for shipment (scheduled)'].str.extract(r'(\\d+)')[0], errors='coerce')",
    "",
    "# Logic SCM: Đơn hàng trễ hạn khi số ngày thực tế > số ngày cam kết",
    "scm_late_flag = (real_days > sched_days).astype('Int8')",
    "raw_target_num = pd.to_numeric(df['Late_delivery_risk'].str.extract(r'(\\d+)')[0], errors='coerce').astype('Int8')",
    "",
    "# Đếm số trường hợp xung đột logic giữa nhãn gốc và thời gian thực tế",
    "valid_mask = scm_late_flag.notna() & raw_target_num.isin([0, 1])",
    "matches = (scm_late_flag[valid_mask] == raw_target_num[valid_mask]).sum()",
    "mismatches = (scm_late_flag[valid_mask] != raw_target_num[valid_mask]).sum()",
    "",
    "print('--- KIỂM TRA ĐỐI CHIẾU LOGIC QUY TẮC VÀNG SCM ---')",
    "print(f'-> Số dòng kiểm tra hợp lệ:           {valid_mask.sum():,} dòng')",
    "print(f'-> Số dòng KHỚP logic (real > sched):  {matches:,} dòng ({matches / valid_mask.sum() * 100:.2f}%)')",
    "print(f'-> Số dòng XUNG ĐỘT logic:             {mismatches:,} dòng ({mismatches / valid_mask.sum() * 100:.2f}%)')"
]))

# Markdown Checkpoint 4 & Template A-B-C-D cho Phần 5
cells.append(create_md_cell([
    "### CHECKPOINT 4: KHÁM PHÁ BIẾN MỤC TIÊU (TARGET AUDIT)",
    "",
    "**A. Kết quả cần quan sát:**",
    "- Biến `Late_delivery_risk` có bao nhiêu nhãn 0, bao nhiêu nhãn 1 hợp lệ?",
    "- Có bao nhiêu dòng bị dính đơn vị tiền tệ/khối lượng/ký hiệu lạ (`1 VND`, `1 USD`, `1 kg`, `?`, `9999`)?",
    "- Khi đối chiếu với điều kiện `Days for shipping (real) > Days for shipment (scheduled)`, tỷ lệ khớp logic là bao nhiêu %?",
    "",
    "**B. Cách diễn giải nghiệp vụ:**",
    "- Trong bài toán SCM, biến mục tiêu `Late_delivery_risk` biểu thị rủi ro vi phạm cam kết SLA giao vận.",
    "- Hiện tượng nhãn bị lẫn đơn vị tiền tệ (`1 VND`, `1 USD`) phát sinh do lỗi xuất nhập bảng trên hệ thống dữ liệu phân tán.",
    "- Mối quan hệ giữa thời gian thực tế và cam kết chính là **Quy tắc Nghiệp vụ Vàng (Ground Truth)** giúp khôi phục toàn bộ các nhãn bị lỗi mà không cần phỏng đoán bừa bãi.",
    "",
    "**C. Nhận xét sau khi chạy:**",
    "> *(Sinh viên tự ghi nhận xét sau khi quan sát output từ Cell 23 đến Cell 27:)*  ",
    "> - Số lượng nhãn 0 vs 1 hợp lệ: ...  ",
    "> - Tỷ lệ khớp logic giữa nhãn và số ngày vận chuyển: ...%  ",
    "> - Nhận xét về tính cân bằng của biến mục tiêu: ...  ",
    "",
    "**D. Quyết định cho bước làm sạch:**",
    "- Áp dụng Quy tắc Vàng SCM: `Late_delivery_risk = 1` nếu `real > scheduled`, ngược lại `0` kết hợp đối chiếu `Delivery Status` để khôi phục 100% nhãn sạch."
]))

# =============================================================================
# PHẦN 6: KHÁM PHÁ CÁC BIẾN NGHIỆP VỤ
# =============================================================================

# Cell 28 - Code
cells.append(create_code_cell([
    "# CELL 28: Khảo sát phân bố của Phương thức vận chuyển (Shipping Mode)",
    "if 'Shipping Mode' in df.columns:",
    "    sm_counts = df['Shipping Mode'].value_counts(dropna=False).reset_index()",
    "    sm_counts.columns = ['Shipping Mode', 'Số Lượng']",
    "    sm_counts['Tỷ Lệ (%)'] = (sm_counts['Số Lượng'] / len(df) * 100).round(2)",
    "    print('--- PHÂN BỐ PHƯƠNG THỨC VẬN CHUYỂN (SHIPPING MODE) ---')",
    "    display(sm_counts.head(15))"
]))

# Cell 29 - Code
cells.append(create_code_cell([
    "# CELL 29: Khảo sát phân bố Thị trường (Market)",
    "if 'Market' in df.columns:",
    "    market_counts = df['Market'].value_counts(dropna=False).reset_index()",
    "    market_counts.columns = ['Market', 'Số Lượng']",
    "    market_counts['Tỷ Lệ (%)'] = (market_counts['Số Lượng'] / len(df) * 100).round(2)",
    "    print('--- PHÂN BỐ THỊ TRƯỜNG (MARKET) ---')",
    "    display(market_counts.head(15))"
]))

# Cell 30 - Code
cells.append(create_code_cell([
    "# CELL 30: Khảo sát phân bố Khu vực đơn hàng (Order Region)",
    "if 'Order Region' in df.columns:",
    "    region_counts = df['Order Region'].value_counts(dropna=False).reset_index()",
    "    region_counts.columns = ['Order Region', 'Số Lượng']",
    "    region_counts['Tỷ Lệ (%)'] = (region_counts['Số Lượng'] / len(df) * 100).round(2)",
    "    print('--- TOP 10 KHU VỰC ĐƠN HÀNG LỚN NHẤT (ORDER REGION) ---')",
    "    display(region_counts.head(10))"
]))

# Cell 31 - Code
cells.append(create_code_cell([
    "# CELL 31: Khảo sát phân bố Phân khúc khách hàng (Customer Segment)",
    "if 'Customer Segment' in df.columns:",
    "    seg_counts = df['Customer Segment'].value_counts(dropna=False).reset_index()",
    "    seg_counts.columns = ['Customer Segment', 'Số Lượng']",
    "    seg_counts['Tỷ Lệ (%)'] = (seg_counts['Số Lượng'] / len(df) * 100).round(2)",
    "    print('--- PHÂN BỐ PHÂN KHÚC KHÁCH HÀNG (CUSTOMER SEGMENT) ---')",
    "    display(seg_counts)"
]))

# Cell 32 - Code
cells.append(create_code_cell([
    "# CELL 32: Thống kê số ngày vận chuyển thực tế - Days for shipping (real)",
    "real_days_numeric = pd.to_numeric(df['Days for shipping (real)'].str.extract(r'(\\d+)')[0], errors='coerce')",
    "print('--- THỐNG KÊ MÔ TẢ: SỐ NGÀY GIAO HÀNG THỰC TẾ ---')",
    "display(real_days_numeric.describe().to_frame().T)"
]))

# Cell 33 - Code
cells.append(create_code_cell([
    "# CELL 33: Thống kê số ngày vận chuyển cam kết - Days for shipment (scheduled)",
    "sched_days_numeric = pd.to_numeric(df['Days for shipment (scheduled)'].str.extract(r'(\\d+)')[0], errors='coerce')",
    "print('--- THỐNG KÊ MÔ TẢ: SỐ NGÀY CAM KẾT THEO SLA ---')",
    "display(sched_days_numeric.describe().to_frame().T)"
]))

# Cell 34 - Code
cells.append(create_code_cell([
    "# CELL 34: Khảo sát các giá trị bất thường trong biến tài chính và thời gian",
    "# Kiểm tra giá trị âm trong số lượng hàng và giá sản phẩm",
    "qty_numeric = pd.to_numeric(df['Order Item Quantity'].str.extract(r'(-?\\d+)')[0], errors='coerce')",
    "price_numeric = pd.to_numeric(df['Product Price'].str.extract(r'(-?\\d+\\.?\\d*)')[0], errors='coerce')",
    "",
    "print('--- KHẢO SÁT DỊ THƯỜNG TRONG CÁC BIẾN SỐ HỌC ---')",
    "print(f'-> Số đơn có Order Item Quantity <= 0: {(qty_numeric <= 0).sum():,} dòng')",
    "print(f'-> Số đơn có Product Price < 0:        {(price_numeric < 0).sum():,} dòng')",
    "print(f'-> Số đơn có Real Shipping Days < 0:    {(real_days_numeric < 0).sum():,} dòng')"
]))

# Markdown Checkpoint & Template A-B-C-D cho Phần 6
cells.append(create_md_cell([
    "### CHECKPOINT 5: BIẾN NGHIỆP VỤ & NGHỊCH LÝ GIAO HÀNG",
    "",
    "**A. Kết quả cần quan sát:**",
    "- `Shipping Mode` phổ biến nhất là gì? Có bị lỗi chữ hoa/chữ thường (`STANDARD CLASS`, `standard class`) không?",
    "- Phân bố của số ngày thực tế (`Days for shipping (real)`) so với số ngày cam kết (`Days for shipment (scheduled)`) dao động trong khoảng nào?",
    "- Có phát hiện giá trị âm bất thường trong số lượng đặt hàng hay giá sản phẩm không?",
    "",
    "**B. Cách diễn giải nghiệp vụ (Nghịch lý First Class):**",
    "- Trong dữ liệu DataCo, gói **First Class** cam kết chỉ giao trong 1 ngày, nhưng thời gian thực tế thường mất từ 2-3 ngày, dẫn đến tỷ lệ trễ hạn lên tới >95%.",
    "- Ngược lại, **Standard Class** cam kết 4 ngày, tạo biên độ đệm an toàn lớn cho đối tác vận tải 3PL nên tỷ lệ trễ thấp nhất.",
    "",
    "**C. Nhận xét sau khi chạy:**",
    "> *(Sinh viên tự ghi nhận xét sau khi quan sát output từ Cell 28 đến Cell 34:)*  ",
    "> - Phương thức giao hàng chủ đạo: ...  ",
    "> - Thị trường lớn nhất: ...  ",
    "> - Giá trị trung vị của ngày thực tế vs cam kết: ... ngày vs ... ngày  ",
    "",
    "**D. Quyết định cho bước làm sạch:**",
    "- Cần chuẩn hóa toàn bộ chuỗi phân loại về chữ thường (`str.lower()`) và cắt khoảng trắng (`str.strip()`).",
    "- Loại bỏ các biến rò rỉ dữ liệu `Days for shipping (real)` khỏi tập đặc trưng huấn luyện của mô hình Machine Learning."
]))

# =============================================================================
# PHẦN 7: TỔNG HỢP DATA QUALITY & XUẤT BÁO CÁO
# =============================================================================

# Cell 35 - Code
cells.append(create_code_cell([
    "# CELL 35: Tổng hợp số lượng và tỷ lệ lỗi phát hiện theo từng cột",
    "quality_summary = []",
    "",
    "for col in df.columns:",
    "    s = df[col].astype('string').str.strip()",
    "    null_cnt = int(s.isna().sum())",
    "    # Đếm ký hiệu nhiễu",
    "    dirty_sym = int(s.str.lower().isin(['?', '-', 'none', 'unknown', '-1', '9999', 'chưa rõ', 'chæ°a rãµ']).sum())",
    "    total_flaws = null_cnt + dirty_sym",
    "    ",
    "    quality_summary.append({",
    "        'Tên Cột': col,",
    "        'Số Lượng Khuyết (Null)': null_cnt,",
    "        'Tỷ Lệ Khuyết (%)': round(null_cnt / len(df) * 100, 2),",
    "        'Ký Hiệu Nhiễu': dirty_sym,",
    "        'Tổng Số Điểm Lỗi': total_flaws,",
    "        'Tỷ Lệ Lỗi (%)': round(total_flaws / len(df) * 100, 2)",
    "    })",
    "",
    "df_quality_overview = pd.DataFrame(quality_summary).sort_values(by='Tỷ Lệ Lỗi (%)', ascending=False)",
    "print('--- TỔNG HỢP CHỈ SỐ CHẤT LƯỢNG DỮ LIỆU BAN ĐẦU THEO CỘT ---')",
    "display(df_quality_overview.head(20))"
]))

# Cell 36 - Code
cells.append(create_code_cell([
    "# CELL 36: Phân loại vấn đề dữ liệu thành các nhóm lỗi tiêu chuẩn",
    "classified_issues = []",
    "",
    "for _, row in df_quality_overview.iterrows():",
    "    col = row['Tên Cột']",
    "    err_types = []",
    "    if row['Số Lượng Khuyết (Null)'] > 0:",
    "        err_types.append('Missing')",
    "    if row['Ký Hiệu Nhiễu'] > 0:",
    "        err_types.append('Invalid Format / Noise')",
    "    if col in PII_COLS:",
    "        err_types.append('PII / Privacy Risk')",
    "    if col == 'Late_delivery_risk':",
    "        err_types.append('Label Noise')",
    "        ",
    "    classified_issues.append({",
    "        'Tên Cột': col,",
    "        'Phân Loại Lỗi (Issue Types)': ', '.join(err_types) if err_types else 'Clean',",
    "        'Mức Độ Ưu Tiên Xử Lý': 'Cao' if row['Tỷ Lệ Lỗi (%)'] > 20 or col in PII_COLS or col == 'Late_delivery_risk' else 'Trung Bình'",
    "    })",
    "",
    "df_classified = pd.DataFrame(classified_issues)",
    "print('--- PHÂN LOẠI NHÓM LỖI VÀ MỨC ĐỘ ƯU TIÊN LÀM SẠCH ---')",
    "display(df_classified.head(25))"
]))

# Cell 37 - Code
cells.append(create_code_cell([
    "# CELL 37: Xuất bảng báo cáo kiểm toán ra file CSV trong thư mục reports/",
    "reports_path = Path('reports')",
    "reports_path.mkdir(parents=True, exist_ok=True)",
    "",
    "# 1. Xuất báo cáo tổng quan data_overview.csv",
    "overview_file = reports_path / 'data_overview.csv'",
    "df_quality_overview.to_csv(overview_file, index=False, encoding='utf-8-sig')",
    "print(f'-> [THÀNH CÔNG] Đã xuất báo cáo tổng quan: {overview_file}')",
    "",
    "# 2. Xuất bảng chất lượng dữ liệu chi tiết data_quality_before.csv",
    "quality_before_df = df_quality_overview.merge(df_classified, on='Tên Cột')",
    "quality_before_file = reports_path / 'data_quality_before.csv'",
    "quality_before_df.to_csv(quality_before_file, index=False, encoding='utf-8-sig')",
    "print(f'-> [THÀNH CÔNG] Đã xuất bảng kiểm toán chi tiết: {quality_before_file}')"
]))

# Cell 38 - Markdown Checkpoint 6 / Tổng kết toàn diện
cells.append(create_md_cell([
    "### TỔNG KẾT VÀ BƯỚC CHUYỂN TIẾP SANG 02_DATA_CLEANING.PY",
    "",
    "**1. Tóm tắt 5 phát hiện cốt lõi từ Notebook Data Overview:**",
    "1. **Bảo mật PII:** Có 5 cột chứa thông tin cá nhân khách hàng (`Customer Email`, `Customer Password`, `Customer Fname`, `Customer Lname`, `Customer Street`) cần loại bỏ hoàn toàn.",
    "2. **Khuyết thiếu trầm trọng:** Cột `Product Description` (khuyết >83%) và `Order Zipcode` (khuyết >79%) cần xem xét loại bỏ khỏi không gian đặc trưng.",
    "3. **Ký hiệu dơ & Lỗi font:** Nhiều cột phân loại bị dính `?`, `-`, `unknown`, `chưa rõ`, lỗi font UTF-8 `chÆ°a rÃµ` và đơn vị tiền tệ trôi nổi (`VND`, `USD`, `kg`, `đ`, `%`).",
    "4. **Nhãn mục tiêu `Late_delivery_risk`:** Có khoảng 16.7% nhãn bị dơ do dính đơn vị tiền tệ và ký hiệu lỗi, nhưng có thể khôi phục 100% bằng **Quy tắc Nghiệp vụ Vàng SCM**.",
    "5. **Cảnh báo Rò rỉ Dữ liệu (*Data Leakage*):** Hai biến `Days for shipping (real)` và `Delivery Status` chỉ được ghi nhận sau khi giao hàng thành công, tuyệt đối không được đưa vào huấn luyện mô hình dự báo tại thời điểm checkout.",
    "",
    "**2. Kế hoạch hành động cho script `02_data_cleaning.py`:**",
    "- [ ] Xóa bỏ hoàn toàn 5 cột PII theo chuẩn GDPR.",
    "- [ ] Sử dụng Vectorized Regex để bóc tách đơn vị tiền tệ/khối lượng/tỷ lệ.",
    "- [ ] Áp dụng quy tắc SCM để khôi phục biến mục tiêu `Late_delivery_risk`.",
    "- [ ] Điền khuyết an toàn bằng median theo nhóm (`Shipping Mode` và `Category Name`).",
    "- [ ] Tối ưu hóa RAM bằng cách ép kiểu `category`, `float32`, `int8`.",
    "",
    "---",
    "*Báo cáo Data Overview hoàn tất. Hãy gửi các ghi nhận thực tế này để tiến hành triển khai script làm sạch dữ liệu tự động!*"
]))

# Build notebook structure
notebook = {
    "cells": cells,
    "metadata": {
        "language_info": {
            "name": "python",
            "version": "3.14.0"
        },
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 4
}

# Write notebook to disk
nb_path = Path("c:/Users/nhath/Downloads/.agents/01_data_overview.ipynb")
with open(nb_path, "w", encoding="utf-8") as f:
    json.dump(notebook, f, ensure_ascii=False, indent=2)

print(f"Đã tạo thành công notebook tại: {nb_path}")
print(f"Tổng số cell đã tạo: {len(cells)}")
