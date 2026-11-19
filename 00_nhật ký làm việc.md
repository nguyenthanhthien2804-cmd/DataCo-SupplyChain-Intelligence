# Nhật ký Làm việc Dự án

Tệp này tự động lưu vết các phiên làm việc giữa Người dùng và Antigravity IDE.  
*Tác giả cấu hình:* N.Lê.Nhật.Hạ  


## [2026-10-28 13:16] - Khôi Phục Lại Bản Gốc Chương 3 Theo Yêu Cầu Của Người Dùng
- **Mục tiêu phiên:** Hoàn trả (revert) nguyên trạng bản thảo gốc của Chương 3 trong [PRJ13_Bao_Cao_Tieu_Luan.qmd](file:///c:/Users/nhath/Downloads/.agents/PRJ13_Bao_Cao_Tieu_Luan.qmd) (từ dòng 405 đến dòng 527) theo yêu cầu người dùng, đảm bảo giữ nguyên bản thảo trước khi viết mở rộng.
- **Tình trạng tệp:** Tệp `PRJ13_Bao_Cao_Tieu_Luan.qmd` đã được đưa về đúng cấu trúc ban đầu gồm 796 dòng, Chương 4 bắt đầu từ dòng 529.

---

## [2026-10-28 10:42] - Soạn Thảo Hoàn Chỉnh Toàn Diện Chương 3 Trong Báo Cáo Tiểu Luận Quarto
- **Mục tiêu phiên:** Viết lại hoàn chỉnh Chương 3 trong [PRJ13_Bao_Cao_Tieu_Luan.qmd](file:///c:/Users/nhath/Downloads/.agents/PRJ13_Bao_Cao_Tieu_Luan.qmd) theo khung xương học thuật chuẩn đại học, tích hợp toàn bộ kết quả kiểm toán từ `02_data_cleaning` và phân tích khám phá từ `03_eda`.
- **Cấu trúc 9 phần đã hoàn thiện:**
  1. **3.1. Mô tả nguồn gốc và Cấu trúc tập dữ liệu đa chiều:** Bối cảnh DataCo, phân định hạt nhân cấp độ mục hàng ($180,519$ bản ghi) và đơn hàng ($65,752$ đơn), từ điển 6 nhóm biến số.
  2. **3.2. Quy trình làm sạch dữ liệu kiểm toán:** Nguyên tắc Zero Data Loss (bảo toàn 100% bản ghi), loại bỏ PII, khử nhiễu Regex, pipeline chuẩn hóa địa lý 8 cột chuyên sâu (`Order Region` giảm 80% từ 115 về 23 vùng chuẩn, `Market` từ 26 về 5 thị trường), kiểm toán nhãn mục tiêu ($91.43\%$ khớp tuyệt đối, $5.08\%$ mâu thuẫn do hủy đơn, độ nhất quán đơn hàng $99.6\%$), tối ưu hóa RAM giảm $36.42\%$ (từ $104.54\text{ MB}$ xuống $66.47\text{ MB}$).
  3. **3.3. Khảo sát Phân bố Biến Mục tiêu & Tính Cân bằng Thống kê (RQ2):** Thống kê mô tả nhãn mục tiêu ở cấp mục hàng ($54.84\%$ trễ vs $45.16\%$ đúng hạn) và đơn hàng ($55.15\%$ trễ vs $44.85\%$ đúng hạn); đánh giá tính cân bằng tự nhiên ($1.21 : 1$), hoàn toàn không bàn luận về thuật toán ML/SMOTE nhằm giữ đúng phạm vi EDA.
  4. **3.4. Phân tích yếu tố vận tải và Khám phá Nghịch lý SLA First Class (RQ1):** Thống kê chi tiết 4 gói vận chuyển; chứng minh toán học nghịch lý First Class có tỷ lệ trễ $95.76\%$ (SLA cam kết 1 ngày vs thực tế 2 ngày), Standard Class trễ $38.01\%$; kiểm định $\chi^2 = 34,863.00, p < 10^{-16}$, Cramér's V = $0.4473$ (ảnh hưởng rất mạnh).
  5. **3.5. Phân tích không gian địa lý sau chuẩn hóa (RQ1):** Khảo sát 23 vùng (`Order Region`: Central Africa $57.30\%$, Western Europe $55.93\%$), 5 đại thị trường (`Market`: $\chi^2 = 5.81, p = 0.325 > 0.05$ không có ý nghĩa thống kê ở cấp đại lục), hiện tượng siêu tập trung tại Caguas ($52,382$ bản ghi, $29.02\%$ toàn hệ thống).
  6. **3.6. Tương tác đa biến & Kiểm định giả thuyết thống kê (RQ1):** Ma trận nhiệt đa biến khẳng định nghịch lý First Class diễn ra đồng nhất $>95\%$ trên toàn cầu; chứng minh tính độc lập giữa giá trị đơn hàng và tốc độ giao hàng (Pearson $r \approx -0.0037$, ANOVA $F = 1.09, p = 0.36$); bảng tổng hợp các phép kiểm định thống kê.
  7. **3.7. Khảo sát ngoại lệ (IQR) và Rào chắn chống rò rỉ dữ liệu:** Hàng rào IQR Tukey cho biến tài chính; phân loại và cô lập 100% các biến hậu giao hàng (`Days for shipping (real)`, `Delivery Status`, `shipping date`) khỏi không gian đặc trưng đầu vào $X$.
  8. **3.8. Tổng hợp Bộ 6 Insights kinh doanh định lượng:** Trình bày chi tiết 6 insight nghiệp vụ từ `reports/eda/eda_insights.csv` kèm bằng chứng thống kê, ý nghĩa nghiệp vụ và khuyến nghị logistics cụ thể.
  9. **3.9. Tóm tắt Chương 3 & Các căn cứ thực nghiệm chuyển giao sang Chương 4:** Tóm tắt kết quả cốt lõi, xác lập không gian biến đầu vào sạch và phương pháp kiểm định chéo phân tầng (Stratified K-Fold) sẵn sàng cho Chương 4.
- **Tích hợp hình ảnh:** Nhúng toàn bộ 9 biểu đồ chất lượng cao $300\text{ DPI}$ từ thư mục [figures/eda/](file:///c:/Users/nhath/Downloads/.agents/figures/eda/) kèm caption và đánh số Quarto.

---

## [2026-10-28 10:05] - Cập Nhật Trực Tiếp File Jupyter Notebook (02_data_cleaning.ipynb & 03_eda.ipynb)
- **Mục tiêu thực hiện:** Thực hiện cập nhật trực tiếp cấu trúc hai tệp Jupyter Notebook trên ổ đĩa bằng thư viện `nbformat` theo yêu cầu kiểm toán học thuật nghiêm ngặt, đảm bảo logic mã nguồn, bảng số liệu và biểu đồ hình ảnh khớp 100% với các file Python script (`02_data_cleaning.py` và `03_eda.py`).
- **Quy trình thực hiện:**
  1. **Sao lưu an toàn:** Tạo 2 bản sao lưu dự phòng [02_data_cleaning.ipynb.bak](file:///c:/Users/nhath/Downloads/.agents/02_data_cleaning.ipynb.bak) và [03_eda.ipynb.bak](file:///c:/Users/nhath/Downloads/.agents/03_eda.ipynb.bak).
  2. **Cập nhật trực tiếp [02_data_cleaning.ipynb](file:///c:/Users/nhath/Downloads/.agents/02_data_cleaning.ipynb):**
     - Nâng cấp toàn diện Phần 6B (Cells 46 - 61) từ chỉ chuẩn hóa thành phố lên **chuẩn hóa toàn diện 8 cột địa danh SCM** (`Customer City`, `Order City`, `Order Region`, `Market`, `Customer Country`, `Customer State`, `Order Country`, `Order State`).
     - Triệt tiêu lỗi phân mảnh danh mục `Order Region` (từ $115$ nhóm về đúng $23$ nhóm chuẩn; sửa triệt để `CENTRAL ASIA`, `central africa`, `EAST AFRICA`, `southern africa`, `western europe`, `Southeast Asi`).
     - Gom $26$ nhóm `Market` về đúng $5$ thị trường chuẩn (khắc phục lỗi cắt cụt `Pacific As` $\rightarrow$ `Pacific Asia`).
     - Bổ sung cell đo lường Before vs After cho toàn bộ 8 cột địa lý và xuất `reports/geo_before_after.csv` và `reports/geo_mapping_audit.csv`.
     - Cập nhật Cell 95 và 96 xuất đồng bộ cả 4 tệp dữ liệu sạch: `DataCo_Cleaned_Full_v2.csv`, `DataCo_Cleaned_Full_v2.parquet`, `DataCo_Cleaned_Full.csv`, `DataCo_Cleaned_Full.parquet`.
     - Xóa toàn bộ output cũ của các cell đã sửa.
  3. **Cập nhật trực tiếp [03_eda.ipynb](file:///c:/Users/nhath/Downloads/.agents/03_eda.ipynb):**
     - Kiểm tra và xác nhận Cell 4 nạp chính xác tệp dữ liệu sạch mới nhất (`DataCo_Cleaned_Full_v2.parquet` / `.csv`).
     - Tách biệt rõ ràng Figure 7 (`fig7_late_rate_by_market.png`) về đúng **Cell 48** (ngay sau bảng phân tích Thị trường toàn cầu) kèm cỡ mẫu $N$ và nhãn tỷ lệ %.
     - Giữ **Cell 51** thuần túy chỉ trực quan hóa biểu đồ thanh ngang Figure 6 (`fig6_late_rate_by_order_region.png`) cho Top 10 khu vực trễ hạn cao nhất, hiển thị trực quan tỷ lệ % và cỡ mẫu $N$.
     - Bảo toàn đầy đủ 109 cells với cấu trúc chuẩn học thuật (Markdown mục tiêu $\rightarrow$ Code thực thi $\rightarrow$ Display bảng $\rightarrow$ Plot biểu đồ $\rightarrow$ Markdown nhận xét).
  4. **Kiểm thử thực thi thành công:**
     - Kiểm tra cú pháp: $100\%$ code cells trong cả 2 notebook biên dịch hợp lệ không lỗi.
     - Chạy kiểm thử [02_data_cleaning.py](file:///c:/Users/nhath/Downloads/.agents/02_data_cleaning.py): Hoàn tất trong $41.37$ giây ($180,519$ dòng $\times$ $53$ cột).
     - Chạy kiểm thử [03_eda.py](file:///c:/Users/nhath/Downloads/.agents/03_eda.py): Hoàn tất trong $48.10$ giây, xuất đầy đủ toàn bộ 14 biểu đồ $300\text{ DPI}$ tại [figures/eda/](file:///c:/Users/nhath/Downloads/.agents/figures/eda/) và 7 bảng báo cáo tại [reports/eda/](file:///c:/Users/nhath/Downloads/.agents/reports/eda/).

---

## [2026-10-26 15:55] - Chuẩn Hóa Địa Lý Toàn Diện 8 Cột & Sửa Triệt Để Lỗi Trùng Lặp Vùng Trong EDA
- **Hiện tượng phát hiện:** Biểu đồ EDA *"Top 10 khu vực có tỷ lệ giao hàng trễ cao nhất (RQ1)"* xuất hiện các vùng bị trùng lặp do chưa chuẩn hóa danh mục (`CENTRAL ASIA`, `central asia`, `Central Asia`; `Central Africa`, `central africa`; `east africa`, `EAST AFRICA`; `southern africa`, `SOUTHERN AFRICA`; `western europe`, `WESTERN EUROPE`; `SOUTH ASIA`, `Southeast Asi`).
- **Nguyên nhân:** Dữ liệu gốc DataCo tồn tại chuỗi bị cắt cụt độ dài (ví dụ: `Southeast Asi` bị cắt từ `Southeast Asia`, `Central Ameri`, `Western Europ`), viết hoa/thường bất nhất và khoảng trắng thừa.
- **Quy trình giải quyết 6 bước thực chứng:**
  1. **Khảo sát toàn bộ 8 cột địa lý:** `Customer City`, `Order City`, `Customer State`, `Order State`, `Customer Country`, `Order Country`, `Order Region`, `Market`.
  2. **Chuẩn hóa toàn diện:**
     - `Order Region`: Từ **$115$ nhóm thô phân mảnh** về đúng **$23$ vùng địa lý chuẩn** (độ giảm $80.00\%$), loại bỏ hoàn toàn trùng lặp.
     - `Market`: Gom từ **$26$ nhóm thô** về **$5$ thị trường chuẩn** (xử lý lỗi cắt cụt `Pacific As` $\rightarrow$ `Pacific Asia`).
     - `Customer Country`: Gom về **$2$ quốc gia** (`EE. UU.` và `Puerto Rico`).
     - `Customer State`: Gom về **$44$ mã bang chuẩn** (viết hoa 2 ký tự).
     - `Order Country`: Gom từ $746$ nhóm về **$164$ quốc gia đích**.
     - `Order State`: Gom từ $4,729$ nhóm về **$1,079$ bang/tỉnh đích**.
  3. **Xuất báo cáo kiểm toán trước/sau:**
     - [reports/geo_mapping_audit.csv](file:///c:/Users/nhath/Downloads/.agents/reports/geo_mapping_audit.csv): $23,180$ dòng ánh xạ chi tiết tên gốc $\rightarrow$ tên chuẩn và trạng thái xác minh.
     - [reports/geo_before_after.csv](file:///c:/Users/nhath/Downloads/.agents/reports/geo_before_after.csv): Thống kê độ giảm nhóm của toàn bộ 8 cột địa lý.
  4. **Cập nhật dữ liệu sạch có phiên bản:**
     - [data/processed/DataCo_Cleaned_Full_v2.csv](file:///c:/Users/nhath/Downloads/.agents/data/processed/DataCo_Cleaned_Full_v2.csv) ($83.16\text{ MB}$)
     - [data/processed/DataCo_Cleaned_Full_v2.parquet](file:///c:/Users/nhath/Downloads/.agents/data/processed/DataCo_Cleaned_Full_v2.parquet) ($11.41\text{ MB}$)
     - Đồng bộ cập nhật vào `DataCo_Cleaned_Full.csv` và `.parquet`.
  5. **Cập nhật mã nguồn & Notebook:**
     - Sửa [02_data_cleaning.py](file:///c:/Users/nhath/Downloads/.agents/02_data_cleaning.py).
     - Sửa [03_eda.py](file:///c:/Users/nhath/Downloads/.agents/03_eda.py) và tái tạo [03_eda.ipynb](file:///c:/Users/nhath/Downloads/.agents/03_eda.ipynb) ($109$ cells tuần tự).
     - Vẽ lại biểu đồ Top 10 khu vực trễ hạn: `fig6_late_rate_by_order_region.png` hiển thị cả tỷ lệ trễ (%) và cỡ mẫu $N$, ghi rõ tính theo dòng sản phẩm có nhãn hợp lệ.
  6. **Kết quả xác minh:**
     - `Central Africa`: duy nhất 1 nhóm ($57.30\%$, $N=1,124$).
     - `South Asia`: duy nhất 1 nhóm ($56.10\%$, $N=5,048$).
     - `East Africa`: duy nhất 1 nhóm ($55.99\%$, $N=1,218$).
     - Không còn bất kỳ biến thể viết hoa/thường hay cắt cụt nào bị tính thành nhóm riêng.

---

## [2026-10-23 16:40] - Tái Cấu Trúc Toàn Diện Bước 03 - Exploratory Data Analysis (EDA) Theo Tiêu Chuẩn Học Thuật
- **Mục tiêu:** Xây dựng mới hoàn toàn `03_eda.py` và `03_eda.ipynb` (chuẩn 109 cells độc lập từ Part A đến Part M) trả lời 2 câu hỏi nghiên cứu cốt lõi RQ1 và RQ2, tuân thủ 14 nguyên tắc khoa học khắt khe: Không dùng data giả, không phụ thuộc file cũ `visualize_eda.py`, không tự động ghi đè nhãn/xóa outlier, loại bỏ hoàn toàn rủi ro Data Leakage, phân tích chuẩn hóa địa danh thực tế (loại `Unknown` khỏi Top 5).
- **Cấu trúc 13 Phần (Part A - Part M, 109 Cells):**
  - **Phần A (Cells 1-10):** Data Loading & Initial Validation ($180,519$ dòng $\times$ $53$ cột, $65,752$ đơn hàng duy nhất).
  - **Phần B (Cells 11-18):** Target Validation ($91.43\%$ hợp lệ nhất quán, $5.08\%$ mâu thuẫn do hủy đơn, $3.49\%$ thiếu nhãn).
  - **Phần C (Cells 19-23):** Descriptive Statistics phân biệt $180,519$ dòng sản phẩm và $65,752$ đơn hàng độc lập.
  - **Phần D (Cells 24-29):** Target Distribution ($54.84\%$ giao trễ vs $45.16\%$ đúng hạn, mất cân bằng nhẹ, khuyến nghị class weights).
  - **Phần E (Cells 30-38):** Shipping Mode & SLA Analysis (First Class trễ $95.76\%$ do cam kết 1 ngày; Standard Class $38.01\%$).
  - **Phần F (Cells 39-52):** Geographical Analysis (Top 5 Customer Cities: Caguas $54.79\%$, Chicago, Brooklyn, Los Angeles, New York; loại sạch Unknown khỏi Top 5).
  - **Phần G (Cells 53-59):** Multivariate Interaction Analysis (Shipping Mode $\times$ Market $\times$ Region $\times$ Segment).
  - **Phần H (Cells 60-69):** Statistical Hypothesis Testing ($\chi^2 = 34,852.65, p < 10^{-16}$, Cramér's V = $0.4613$ cho Shipping Mode; Region Cramér's V = $0.0301$; Market và Segment không có ý nghĩa thống kê $p > 0.05$).
  - **Phần I (Cells 70-78):** Data Quality Analysis & Verification Before/After.
  - **Phần J (Cells 79-87):** Outlier Analysis qua IQR & Skewness trên bản sao dữ liệu (bảo toàn 100% dữ liệu gốc trong EDA).
  - **Phần K (Cells 88-95):** Correlation & Feature Leakage Audit (cô lập triệt để `Days for shipping (real)`, `Delivery Status`, `shipping date`).
  - **Phần L (Cells 96-100):** Tổng hợp 5 Insights thực chứng kèm bằng chứng số liệu và giải pháp chuỗi cung ứng.
  - **Phần M (Cells 101-109):** Xuất toàn bộ 7 báo cáo CSV và 14 hình ảnh biểu đồ $300\text{ DPI}$.
- **Tập tin đã tạo & kiểm thử:**
  - [03_eda.py](file:///c:/Users/nhath/Downloads/.agents/03_eda.py): Thực thi hoàn tất không lỗi, thời gian $14.66$s.
  - [03_eda.ipynb](file:///c:/Users/nhath/Downloads/.agents/03_eda.ipynb): 109 cells tuần tự kèm cấu trúc Markdown học thuật chuẩn hóa.
  - 7 báo cáo CSV trong [reports/eda/](file:///c:/Users/nhath/Downloads/.agents/reports/eda/): `target_quality_audit.csv`, `shipping_mode_analysis.csv`, `geography_analysis.csv`, `statistical_tests.csv`, `data_quality_analysis.csv`, `feature_leakage_audit.csv`, `eda_insights.csv`.
  - 14 biểu đồ chất lượng cao $300\text{ DPI}$ trong [figures/eda/](file:///c:/Users/nhath/Downloads/.agents/figures/eda/).

---

## [2026-10-23 16:20] - Chuẩn Hóa Địa Danh Chuyên Sâu (City Normalization Pipeline) & Tích Hợp Vào EDA
- **Mục tiêu:** Khắc phục tình trạng phân mảnh danh mục địa danh trong dữ liệu gốc DataCo (`Customer City` và `Order City`) do sai lệch chữ hoa/thường, khoảng trắng thừa và ký hiệu khuyết/nhiễu (`?`, `unknown`, `chưa rõ`), ngăn chặn sai số khi tính toán tỷ lệ giao hàng trễ theo đô thị.
- **Quy trình chuẩn hóa 7 bước thực hiện:**
  1. Chuẩn hóa Unicode `NFKC`.
  2. Cắt bỏ khoảng trắng thừa đầu/cuối (`.str.strip()`).
  3. Gộp nhiều khoảng trắng liên tiếp thành một khoảng trắng đơn (`re.sub(r'\s+', ' ', s)`).
  4. Quy đổi ký hiệu thiếu ẩn (`?`, `unknown`, `chưa rõ`, `none`, `-1`, `9999`) về `pd.NA`.
  5. Title Case thông minh xử lý từ ghép gạch ngang (ví dụ: `Port-au-Prince`, `Winston-Salem`).
  6. Bảo toàn các hư từ tiếng Tây Ban Nha / Anh (`de`, `del`, `la`, `las`, `los`, `el`, `sur`, `of`).
  7. Chuẩn hóa viết hoa cho từ viết tắt đô thị (`DC`, `St.`, `Ft.`).
- **Kết quả kiểm toán định lượng Before vs After:**
  - **Customer City:** Gom từ **$2,811$ nhóm thô** về **$566$ thành phố chuẩn** (độ giảm $79.86\%$). Đô thị khách hàng lớn nhất **Caguas** được quy tụ trọn vẹn từ $24,822$ bản ghi phân mảnh thành **$52,382$ bản ghi** ($29.02\%$ toàn bộ tập dữ liệu hoặc $36.98\%$ trên tập có địa danh hợp lệ). Top 5 đô thị khách hàng: Caguas ($52,382$), Chicago ($3,043$), Brooklyn ($2,688$), Los Angeles ($2,674$), New York ($1,409$).
  - **Order City:** Gom từ **$14,560$ nhóm thô** về **$3,556$ đô thị đích chuẩn** (độ giảm $75.58\%$). Top 5 đô thị nhận hàng lớn nhất: Santo Domingo ($1,424$), New York City ($1,370$), Los Angeles ($1,147$), Tegucigalpa ($1,118$), Managua ($1,050$).
  - Toàn bộ $180,519$ dòng dữ liệu được bảo toàn nguyên vẹn 100%, không bị dropna tùy tiện.
- **Tạo các tệp báo cáo & trực quan hóa xuất xưởng:**
  - [reports/city_mapping_audit.csv](file:///c:/Users/nhath/Downloads/.agents/reports/city_mapping_audit.csv): $17,371$ dòng ánh xạ chi tiết tên gốc $\rightarrow$ tên chuẩn, số bản ghi và phương pháp.
  - [reports/city_before_after.csv](file:///c:/Users/nhath/Downloads/.agents/reports/city_before_after.csv): Thống kê tổng hợp so sánh các chỉ số Before vs After.
  - [reports/city_unresolved.csv](file:///c:/Users/nhath/Downloads/.agents/reports/city_unresolved.csv): $8$ dòng ghi nhận các ký hiệu khuyết/nhiễu đã quy đổi về `pd.NA`.
  - [figures/city_top5_comparison.png](file:///c:/Users/nhath/Downloads/.agents/figures/city_top5_comparison.png): Biểu đồ 4 góc so sánh Top 5 Before vs After $300\text{ DPI}$.
  - [figures/eda/fig11_city_delay_rates.png](file:///c:/Users/nhath/Downloads/.agents/figures/eda/fig11_city_delay_rates.png): Phân tích tỷ lệ trễ hạn theo Top 10 đô thị đến và đô thị đi.
- **Cập nhật code & Notebook:**
  - Bổ sung trọn vẹn quy trình vào [02_data_cleaning.py](file:///c:/Users/nhath/Downloads/.agents/02_data_cleaning.py), thêm cột phân nhóm phụ trợ `Customer_City_Top5_Group` và `Order_City_Top5_Group`.
  - Bổ sung đầy đủ **15 cell** vào [02_data_cleaning.ipynb](file:///c:/Users/nhath/Downloads/.agents/02_data_cleaning.ipynb).
  - Cập nhật [03_eda.py](file:///c:/Users/nhath/Downloads/.agents/03_eda.py) và chạy lại toàn bộ thống kê rủi ro giao hàng trễ theo đô thị đã chuẩn hóa.

---

## [2026-10-23 16:00] - Kiểm Thử Toàn Diện & Khắc Phục Lỗi Chạy File Python: 01, 02, 03
- **Hiện tượng lỗi:** Khi người dùng chạy lệnh trong Terminal:
  `& C:/Users/nhath/AppData/Local/Programs/Python/Python314/python3.14t.exe ...`
  bị lỗi: `ImportError: No module named 'numpy._core._multiarray_umath'`.
- **Nguyên nhân cốt lõi:**
  - File thực thi `python3.14t.exe` (có chữ `t`) là bản dựng **Free-threaded (no-GIL)** thử nghiệm của Python 3.14. Các thư viện C-extensions như NumPy, SciPy được biên dịch cho bản CPython tiêu chuẩn (`python.exe`), không tương thích với `python3.14t.exe`.
- **Giải pháp & Kiểm thử thành công:**
  - Thực thi với trình thông dịch tiêu chuẩn `python.exe` (`C:\Users\nhath\AppData\Local\Programs\Python\Python314\python.exe`):
    1. [01_data_overview.py](file:///c:/Users/nhath/Downloads/.agents/01_data_overview.py): Chạy thành công 100%, xuất đầy đủ báo cáo.
    2. [02_data_cleaning.py](file:///c:/Users/nhath/Downloads/.agents/02_data_cleaning.py): Hoàn tất pipeline làm sạch trong $19.09$ giây, xuất tệp CSV ($72.74\text{ MB}$) và Parquet ($11.19\text{ MB}$).
    3. [03_eda.py](file:///c:/Users/nhath/Downloads/.agents/03_eda.py): Hoàn tất EDA trong $15.12$ giây, xuất toàn bộ $10$ biểu đồ $300\text{ DPI}$, $11$ bảng CSV và báo cáo `reports/EDA_Insights.md`.
  - Đã loại bỏ hoàn toàn cảnh báo `SyntaxWarning` trong [03_eda.py](file:///c:/Users/nhath/Downloads/.agents/03_eda.py).

---

## [2026-10-23 15:43] - Khắc Phục Lỗi ArrowKeyError Khi Đọc Parquet Trên Jupyter Notebook
- **Hiện tượng:** Khi chạy Cell nạp dữ liệu trên `03_eda.ipynb`, phát sinh lỗi `ArrowKeyError: No type extension with name arrow.py_extension_type found` do xung đột nội bộ giữa phiên bản `pandas 3.0.6` và hàm đăng ký extension type của `pyarrow`.
- **Giải pháp triệt để:**
  1. Cài đặt thêm engine `fastparquet 2026.9.0` (cùng `cramjam`, `fsspec`) vào môi trường `notebook-env`. Engine này đọc file `.parquet` hoàn toàn độc lập, tốc độ cực nhanh và không phụ thuộc vào extension types của PyArrow.
  2. Nâng cấp hàm đọc dữ liệu tại cả hai file [03_eda.py](file:///c:/Users/nhath/Downloads/.agents/03_eda.py) và [03_eda.ipynb](file:///c:/Users/nhath/Downloads/.agents/03_eda.ipynb) với cơ chế phòng vệ 3 lớp:
     - Thử đọc Parquet bằng `fastparquet`
     - Thử đọc Parquet bằng `pyarrow`
     - Tự động fallback sang đọc `DataCo_Cleaned_Full.csv`
  3. Kiểm tra kiểm thử: Nạp thành công toàn bộ **$180,519$ dòng $\times$ $51$ cột**.

---

## [2026-10-23 15:37] - Khắc Phục Lỗi Kernel Jupyter Notebook: ModuleNotFoundError: No module named 'scipy'
- **Hiện tượng:** Khi chạy `03_eda.ipynb`, cell đầu tiên báo lỗi `ModuleNotFoundError: No module named 'scipy'` tại dòng `import scipy.stats as stats`.
- **Nguyên nhân chính xác:** VS Code đang thực thi Jupyter Notebook bằng môi trường Conda tại `c:\Users\nhath\miniconda3\envs\notebook-env\python.exe`. Môi trường này chỉ có sẵn `pandas`, `numpy`, `matplotlib` nhưng chưa có `scipy`, `scikit-learn` và `pyarrow`.
- **Giải pháp triệt để:** 
  1. Đã cài đặt thành công `scipy 1.18.1`, `scikit-learn 1.9.1`, `pyarrow 26.0.0` trực tiếp vào đúng môi trường Conda `notebook-env`.
  2. Đã đồng bộ cài đặt vào cả `Python 3.13` và `Python 3.14`.
  3. Kiểm tra import thực tế: `NOTEBOOK-ENV TEST PASSED 100%`.
  4. Hướng dẫn người dùng bấm nút **Restart Kernel** trên thanh công cụ Notebook để nạp lại thư viện vừa cài.

---

## [2026-10-23 15:25] - Triển Khai Module Khám Phá Dữ Liệu 03_eda.py & Notebook 03_eda.ipynb
- **Môi trường:** Windows | Python 3.14 | Pandas | NumPy | SciPy | Seaborn | Matplotlib | Scikit-learn
- **Mục tiêu phiên:** 
  1. Kế thừa và chuẩn hóa 3 biểu đồ từ [visualize_eda.py](file:///c:/Users/nhath/Downloads/.agents/visualize_eda.py) (Countplot nhãn mục tiêu, Boxplot số ngày thực tế vs cam kết, Heatmap tương quan).
  2. Mở rộng toàn diện theo 4 câu hỏi nghiên cứu (RQ1 - RQ4): kiểm định thống kê $\chi^2$, Cramér's V, Welch $t$-test, Mann-Whitney U, One-Way ANOVA, Kruskal-Wallis, tính toán Skewness và Mutual Information.
  3. Xây dựng script tự động hóa [03_eda.py](file:///c:/Users/nhath/Downloads/.agents/03_eda.py) và Jupyter Notebook tương tác [03_eda.ipynb](file:///c:/Users/nhath/Downloads/.agents/03_eda.ipynb) (62 cell qua 10 phần).
  4. Chạy thực nghiệm end-to-end trên [data/processed/DataCo_Cleaned_Full.parquet](file:///c:/Users/nhath/Downloads/.agents/data/processed/DataCo_Cleaned_Full.parquet) ($180,519$ dòng $\times$ $51$ cột), xuất 10 hình ảnh 300 DPI, 11 bảng thống kê CSV và báo cáo chuyên sâu `reports/EDA_Insights.md`.
- **Kết quả đạt được:**
  - **RQ1 & RQ4:** Khẳng định nghịch lý First Class ($\chi^2 = 34,863.00$, Cramér's V = $0.4473$): tỷ lệ trễ hạn First Class lên tới **$95.28\%$** do thời gian cam kết cố định 1 ngày quá gấp rút; trong khi Standard Class trễ thấp nhất (**$38.11\%$**). Kiểm định ANOVA cho thấy giá trị đơn hàng `Sales` không có sự khác biệt giữa các gói vận chuyển ($F = 1.09, p = 0.36$), chứng tỏ đơn hàng VIP chưa có phân luồng ưu tiên.
  - **RQ2:** Đánh giá phân phối nhãn mục tiêu cân bằng tự nhiên ($54.84\%$ trễ vs $45.16\%$ đúng hạn). Ngoại lệ `Sales` ($5.02\%$) đại diện cho đơn hàng bán sỉ hợp lệ và được giữ nguyên.
  - **RQ3:** Xếp hạng Mutual Information cho thấy hai biến chi phối mạnh nhất là `Days for shipment (scheduled)` ($\text{MI} = 0.1262$) và `Shipping Mode` ($\text{MI} = 0.1155$). Thiết lập rào chắn loại bỏ hoàn toàn các biến hậu giao hàng (`Days for shipping (real)`, `Delivery Status`, `shipping date`) để ngăn chặn rò rỉ dữ liệu (*Data Leakage*).
  - Xuất thành công:
    - 10 hình ảnh chất lượng cao 300 DPI tại [figures/eda/](file:///c:/Users/nhath/Downloads/.agents/figures/eda/)
    - 11 bảng số liệu chi tiết tại [reports/eda/](file:///c:/Users/nhath/Downloads/.agents/reports/eda/)
    - Báo cáo phân tích chuyên sâu tại [reports/EDA_Insights.md](file:///c:/Users/nhath/Downloads/.agents/reports/EDA_Insights.md)

---

## [2026-10-22 10:15] - Triển Khai Pipeline Kiểm Toán Dữ Liệu & Huấn Luyện Baseline Machine Learning
- **Môi trường:** Windows | Python 3.14 | Scikit-learn 1.9.1 | Pandas | SciPy
- **Mục tiêu phiên:** 
  1. Cài đặt hoàn chỉnh bộ thư viện học máy `scikit-learn`, `scipy`, `threadpoolctl` trên Python 3.14.
  2. Nâng cấp và cấu hình script pipeline [Untitled-1.py](file:///c:/Users/nhath/Downloads/.agents/Untitled-1.py) (chuẩn hóa encoding UTF-8, đồng nhất kiểu dữ liệu chuỗi/số chống lỗi mã hóa OneHotEncoder, loại bỏ triệt để rò rỉ dữ liệu *Data Leakage* bằng cách loại trừ `Days for shipping (real)`, `Delivery Status`, `shipping date (DateOrders)`).
  3. Chạy thực nghiệm end-to-end trên tập dữ liệu thô [7_PJ13_2521001054_Nguyễn Lê Nhật Hạ.csv](file:///c:/Users/nhath/Downloads/.agents/7_PJ13_2521001054_Nguy%E1%BB%85n%20L%C3%AA%20Nh%E1%BA%ADt%20H%E1%BA%A1.csv) ($180,519$ dòng $\times$ $53$ cột).
- **Kết quả đạt được:**
  - Xuất thành công bộ 4 tệp báo cáo chất lượng và dữ liệu sạch tại thư mục [output/](file:///c:/Users/nhath/Downloads/.agents/output/):
    - `DataCo_Cleaned_Full.csv`: $180,519$ dòng $\times$ $51$ cột sạch, không còn PII.
    - `DataCo_Data_Quality_Report.csv` & `DataCo_Audit_Summary.csv`: Thống kê tỷ lệ khuyết và ký hiệu dơ.
    - `DataCo_Baseline_ML_Evaluation.csv`: Kết quả đánh giá hiệu năng 2 mô hình cơ sở.
  - Phân chia tập dữ liệu: Tập huấn luyện (Train) **$126,161$ dòng** (80%), Tập kiểm tra (Test) **$31,541$ dòng** (20%), phân tầng `stratify=y` theo nhãn `Late_delivery_risk`.
  - Hiệu năng phân loại Baseline Model:
    - **Logistic Regression:** ROC-AUC: **$0.7285$** | PR-AUC: **$0.7932$** | Accuracy: **$0.6872$** | Precision: **$0.8048$** | Recall: **$0.5578$** | F1-Score: **$0.6589$**.
    - **Random Forest:** ROC-AUC: **$0.7310$** | PR-AUC: **$0.7952$** | Accuracy: **$0.6814$** | Precision: **$0.7482$** | Recall: **$0.6205$** | F1-Score: **$0.6784$**.

---

## [2026-10-20 11:18] - Đồng Bộ Bảng Từ Điển Dữ Liệu 53 Thuộc Tính Vào Tệp 07_Nguyễn Lê Nhật Hạ...qmd
- **Môi trường:** Windows | Quarto (.qmd)
- **Mục tiêu phiên:** Thay thế toàn bộ 6 bảng từ điển dữ liệu cũ tại Mục 3.3 trong tệp [[07_Nguyễn Lê Nhật Hạ_2521001054_Nguyễn Thanh Thiện_2521001102.qmd](file:///c:/Users/nhath/Downloads/.agents/07_Nguy%E1%BB%85n%20L%C3%AA%20Nh%E1%BA%ADt%20H%E1%BA%A1_2521001054_Nguy%E1%BB%85n%20Thanh%20Thi%E1%BB%87n_2521001102.qmd)] bằng hệ thống bảng 7 cột mới:
  - Bổ sung cột *Ký hiệu dơ / Nhiễu phát hiện* (`?`, `-`, `-1`, `9999`, `chÆ°a rÃµ`, đơn vị tiền tệ/khối lượng `VND`, `USD`, `kg`, `%`, `đ`, dấu phẩy thập phân `,`, tỷ lệ khuyết $>79\%$).
  - Bổ sung cột *Phương pháp xử lý pipeline áp dụng* (Vectorized Regex, điền median theo nhóm `Shipping Mode` / `Category Name`, điền nhãn an toàn `'Unknown'`, đối chiếu chéo thời gian, loại bỏ các biến rò rỉ dữ liệu `Days for shipping (real)`, `Delivery Status`, `shipping date` và loại bỏ hoàn toàn 2 trường PII nhạy cảm `Customer Email`, `Customer Password`).

---

## [2026-10-20 11:05] - Cập Nhật Từ Điển Dữ Liệu 53 Thuộc Tính Kèm Ký Hiệu Dơ & Pipeline Vào Báo cáo.qmd
- **Môi trường:** Windows | Quarto (.qmd)
- **Mục tiêu phiên:** Bổ sung toàn diện cột *Ký hiệu dơ / Nhiễu phát hiện* và *Phương pháp xử lý pipeline áp dụng* vào Bảng từ điển dữ liệu Mục 3.3 trong tệp [Báo cáo.qmd](file:///c:/Users/nhath/Downloads/.agents/B%C3%A1o%20c%C3%A1o.qmd):
  - Phân chia chi tiết thành 6 nhóm nghiệp vụ với 7 cột chuẩn: `STT`, `Tên Cột (Column Name)`, `Ý Nghĩa Thực Tế / Nghiệp Vụ`, `Kiểu Gốc`, `Kiểu Sạch`, `Ký Hiệu Dơ / Nhiễu Phát Hiện`, và `Phương Pháp Xử Lý Pipeline Áp Dụng`.
  - Liệt kê chi tiết toàn bộ các ký hiệu lỗi thực tế: `?`, `-`, `-1`, `9999`, lỗi font UTF-8 (`chÆ°a rÃµ`), các đơn vị tiền tệ/khối lượng/tỷ lệ trôi nổi (`VND`, `USD`, `kg`, `%`, `đ`), dấu phẩy thập phân `,` $\rightarrow$ `.`, và tỷ lệ khuyết lớn.
  - Đồng bộ phương pháp xử lý pipeline tương ứng: Vectorized Regex, điền khuyết median theo nhóm `Shipping Mode` / `Category Name`, điền nhãn an toàn `'Unknown'`, đối chiếu chéo thời gian đơn hàng và loại bỏ các biến rò rỉ dữ liệu (*Data Leakage*) cùng 2 trường PII nhạy cảm (`Customer Email`, `Customer Password`).

---

## [2026-10-20 09:05] - Cập Nhật Toàn Diện Mục 3.2, 3.3 và 3.4 Trong Báo Cáo Tiểu Luận
- **Môi trường:** Windows | Quarto (.qmd) | Python 3.14
- **Mục tiêu phiên:** Đồng bộ hóa toàn diện các mục 3.2, 3.3, 3.4 trong [PRJ13_Bao_Cao_Tieu_Luan.qmd](file:///c:/Users/nhath/Downloads/.agents/PRJ13_Bao_Cao_Tieu_Luan.qmd) dựa trên các yêu cầu phân tích nghiệp vụ, pipeline làm sạch [clean_data.py](file:///c:/Users/nhath/Downloads/.agents/clean_data.py) và module trực quan hóa [visualize_eda.py](file:///c:/Users/nhath/Downloads/.agents/visualize_eda.py):
  1. **Mục 3.2 (Ghép nối dữ liệu & Tối ưu RAM):** Mô tả kiến trúc liên kết Star/Snowflake Schema giữa Bảng Fact mục hàng và các Bảng Chiều; trình bày kỹ thuật Downcasting số thực (`float32`), số nguyên (`int32`, `int8`), chuyển chuỗi sang `category`, giúp giảm RAM từ **$144.67\text{ MB}$ xuống $26.00\text{ MB}$ (tiết kiệm $82.0\%$ RAM)**; lưu trữ kép định dạng Parquet ($11.06\text{ MB}$) và CSV ($78.82\text{ MB}$).
  2. **Mục 3.3 (Làm sạch & Điền khuyết theo Quy tắc SCM):** Loại bỏ 2 trường PII (`Customer Email`, `Customer Password`) theo chuẩn GDPR (còn 51 cột); kiểm định `.drop_duplicates()` bảo toàn trọn vẹn **$180,519$ dòng**; khử nhiễu chuỗi Vectorized Regex loại bỏ đơn vị tiền tệ/khối lượng; áp dụng **Quy tắc Nghiệp vụ Vàng SCM** khôi phục nhãn mục tiêu `Late_delivery_risk` ($100\%$ ăn khớp với `Delivery Status`); điền khuyết toàn diện theo median nhóm `Shipping Mode` và `Category Name`, đạt **0 NaN** trên toàn bộ 51 cột.
  3. **Mục 3.4 (Thống kê mô tả & Trực quan hóa EDA):** Lập bảng tóm tắt 5 con số cho các biến định lượng cốt lõi; phân tích tỷ lệ nhãn mục tiêu chuẩn xác: **$54.62\%$** ($98,597$ đơn trễ) vs **$45.38\%$** ($81,922$ đơn đúng hạn/sớm) - tỷ lệ tự nhiên cân bằng; nhúng 3 hình ảnh trực quan hóa chất lượng cao 300 DPI (biểu đồ cột tỷ lệ mục tiêu, biểu đồ hộp số ngày theo phương thức vận chuyển bóc tách nghịch lý First Class, và ma trận tương quan heatmap kèm cảnh báo chống rò rỉ dữ liệu).

---

## [2026-10-19 16:50] - Chuẩn Hóa Phân Loại 53 Thuộc Tính Dữ Liệu Theo 6 Trụ Cột Nghiệp Vụ SCM
- **Môi trường:** Windows | Quarto (.qmd)
- **Mục tiêu phiên:** Đồng bộ nội dung phân loại biến số từ [Ngiệp vụ.qmd](file:///c:/Users/nhath/Downloads/.agents/Ngi%E1%BB%87p%20v%E1%BB%A5.qmd) vào Mục 3.1 của tệp báo cáo chính [PRJ13_Bao_Cao_Tieu_Luan.qmd](file:///c:/Users/nhath/Downloads/.agents/PRJ13_Bao_Cao_Tieu_Luan.qmd):
  - Thay thế danh sách tóm tắt sơ sài bằng cấu trúc phân loại toàn diện 53 thuộc tính quanh 6 trụ cột nghiệp vụ chuỗi cung ứng:
    1. Nhóm Vận chuyển & Cam kết Dịch vụ SLA (Trọng tâm đề tài).
    2. Nhóm Quản lý Đơn hàng & Phân bổ Địa lý.
    3. Nhóm Kinh tế Đơn vị & Tài chính (Unit Economics).
    4. Nhóm Phân khúc & Hồ sơ Khách hàng.
    5. Nhóm Danh mục Sản phẩm & Kho bãi.
    6. Nhóm Quản trị Dữ liệu & Thông tin Định danh (Data Governance & PII).
  - Bổ sung diễn giải nghiệp vụ chi tiết cho từng trường dữ liệu, vai trò của từng biến đối với bài toán rủi ro trễ hạn và lý do loại bỏ các thuộc tính PII nhạy cảm theo chuẩn GDPR.

---

## [2026-10-19 14:38] - Xây Dựng Module Trực Quan Hóa Kiểm Soát Dữ Liệu Sạch (EDA Visualization)
- **Môi trường:** Windows | Python 3.14 | Matplotlib | Seaborn
- **Mục tiêu phiên:** Viết script [visualize_eda.py](file:///c:/Users/nhath/Downloads/.agents/visualize_eda.py) sử dụng `matplotlib` và `seaborn` kiểm tra trực quan dữ liệu từ [DataCo_Cleaned_Full.csv](file:///c:/Users/nhath/Downloads/.agents/DataCo_Cleaned_Full.csv):
  1. Biểu đồ cột (`countplot`) thể hiện phân phối và tỷ lệ % biến mục tiêu `Late_delivery_risk` (0: $45.38\%$ vs 1: $54.62\%$).
  2. Biểu đồ hộp (`boxplot`) so sánh ngày thực tế (`Days for shipping (real)`) và ngày cam kết SLA (`Days for shipment (scheduled)`) theo từng `Shipping Mode`, làm nổi bật nghịch lý First Class.
  3. Ma trận tương quan (`heatmap`) thể hiện mối liên hệ giữa các biến định lượng với biến mục tiêu.
- **Nội dung đã hoàn thành:**
  - Thiết lập font tiếng Việt `Segoe UI` chuẩn Unicode, cấu hình `plt.tight_layout()`, palette màu `Set2`.
  - Xuất thành công 3 tệp hình ảnh độ phân giải cao 300 DPI phục vụ chèn vào Chương 3 của báo cáo Quarto:
    - [chart1_late_delivery_risk_countplot.png](file:///c:/Users/nhath/Downloads/.agents/chart1_late_delivery_risk_countplot.png) ($150.0\text{ KB}$).
    - [chart2_shipping_days_boxplot.png](file:///c:/Users/nhath/Downloads/.agents/chart2_shipping_days_boxplot.png) ($183.9\text{ KB}$).
    - [chart3_correlation_heatmap.png](file:///c:/Users/nhath/Downloads/.agents/chart3_correlation_heatmap.png) ($384.6\text{ KB}$).

---

## [2026-10-19 10:02] - Hoàn Thiện Cơ Sở Lý Thuyết Chương 2 (KPIs, OTIF & Giao Vận 3PL Chặng Cuối)
- **Môi trường:** Windows | Quarto (.qmd)
- **Mục tiêu phiên:** Cập nhật đồng bộ Mục 2.1 trong tệp [PRJ13_Bao_Cao_Tieu_Luan.qmd](file:///c:/Users/nhath/Downloads/.agents/PRJ13_Bao_Cao_Tieu_Luan.qmd):
  1. **Mục 2.1.2 (Logistics KPIs):** Chuẩn hóa định nghĩa Lead Time, Scheduled Shipping Days, Real Shipping Days; bổ sung công thức và phân định hai thành tố của chỉ số **OTIF (On-Time In-Full)**: Thành tố Đúng hạn (*On-Time* qua tương quan ngày giao thực tế vs cam kết) và Thành tố Đủ số lượng (*In-Full* qua `Order Item Quantity` và `Order Status`); liên kết trực tiếp với biến mục tiêu `Late_delivery_risk`.
  2. **Mục 2.1.3 (3PL Last-mile Delivery & Hậu kiểm):** Trình bày chi tiết vai trò của khâu giao vận chặng cuối của đối tác 3PL (quét mã, ghi nhận mốc thời gian, trạng thái `Delivery Status`), cơ chế hậu kiểm đối soát SLA tự động và cảnh báo học thuật về rò rỉ dữ liệu (*Data Leakage*).

---

## [2026-10-18 20:20] - Hoàn Thiện Toàn Diện Báo Cáo Phân Tích Nghiệp Vụ & Kiến Trúc Dữ Liệu
- **Môi trường:** Windows | Markdown
- **Mục tiêu phiên:** Nâng cấp toàn diện tệp [Báo Cáo Phân Tích Nghiệp Vụ Tệp Dữ Liệu.md](file:///c:/Users/nhath/Downloads/.agents/B%C3%A1o%20C%C3%A1o%20Ph%C3%A2n%20T%C3%ADch%20Nghi%E1%BB%87p%20V%E1%BB%A5%20T%E1%BB%87p%20D%E1%BB%AF%20Li%E1%BB%87u.md) theo yêu cầu học thuật và thực tiễn SCM:
  1. **Bối cảnh kinh doanh & Quy trình phát sinh dữ liệu:** Hoạt động bán lẻ đa kênh toàn cầu của DataCo; quy trình phối hợp giữa 5 phòng ban (Kinh doanh/CRM, Tài chính/ERP, Kho vận/WMS, Logistics/TMS và Đối tác vận chuyển 3PL).
  2. **Đơn vị quan sát & Cỡ mẫu:** Khẳng định đơn vị quan sát là một mục hàng giao dịch (*Line Item / Order Item Transaction*) với $180,519$ dòng $\times$ $53$ cột thô (sau xử lý PII là $51$ cột).
  3. **Kiến trúc & Từ điển dữ liệu (Data Dictionary):** Mô hình hóa kiến trúc ER logic (Star/Snowflake Schema) và lập bảng từ điển dữ liệu chi tiết cho đủ 53 trường thuộc tính qua 6 nhóm nghiệp vụ với tên biến, ý nghĩa, đơn vị tính, kiểu dữ liệu và vai trò liên kết.
  4. **Kiểm toán độ sạch ban đầu:** Phân loại tỷ lệ khuyết thiếu (nhóm cực cao $>70\%$, trung bình $15-25\%$, then chốt $4-15\%$), rà soát nhiễu chuỗi tiền tệ/khối lượng, dấu phẩy thập phân, ngoại lai biên lợi nhuận/thời gian và cảnh báo rò rỉ dữ liệu (*Data Leakage*).
  5. **Mục tiêu phân tích & Bộ 4 câu hỏi kinh doanh cam kết:** Đánh giá, phê chuẩn và phát triển chi tiết phương pháp luận giải quyết 4 câu hỏi nghiên cứu bằng Python (Descriptive/Diagnostic, Data Preprocessing/EDA, Predictive Machine Learning, và Prescriptive Analytics).

---

## [2026-10-18 20:07] - Cập Nhật Loại Bỏ PII (Customer Email, Password) & Triệt Tiêu Trùng Lặp (.drop_duplicates())
- **Môi trường:** Windows | Python 3.14 | Pandas
- **Mục tiêu phiên:** Bổ sung yêu cầu loại bỏ 2 cột định danh cá nhân nhạy cảm (`Customer Email`, `Customer Password`) trước khi đưa dữ liệu vào xử lý sâu (Data Lake Pipeline) và bổ sung bước `.drop_duplicates()` loại bỏ trùng lặp hoàn toàn trong [clean_data.py](file:///c:/Users/nhath/Downloads/.agents/clean_data.py).
- **Nội dung đã hoàn thành:**
  - Cập nhật hàm [apply_data_governance_and_privacy](file:///c:/Users/nhath/Downloads/.agents/clean_data.py#L91) và pipeline với `drop_pii_cols = True` mặc định: Loại bỏ hoàn toàn 2 cột PII `Customer Email` và `Customer Password`, dữ liệu còn **51 cột chuẩn**.
  - Bổ sung bước thực thi `df = df.drop_duplicates()` nhằm đảm bảo không còn bản ghi dư thừa/trùng lặp hoàn toàn trong Data Lake.
  - Chạy kiểm thử thành công pipeline với kết quả:
    - Quy mô dữ liệu: **$180,519$ dòng $\times$ $51$ cột**.
    - Dung lượng RAM: $144.67\text{ MB} \rightarrow 26.00\text{ MB}$ (Tiết kiệm $82.0\%$).
    - Kiểm tra giá trị khuyết (NaN): **0 giá trị NaN** trên toàn bộ 51 cột.
    - Xuất tệp cập nhật: [DataCo_Cleaned_Full.csv](file:///c:/Users/nhath/Downloads/.agents/DataCo_Cleaned_Full.csv) ($78.82\text{ MB}$) và [DataCo_Cleaned_Full.parquet](file:///c:/Users/nhath/Downloads/.agents/DataCo_Cleaned_Full.parquet) ($11.06\text{ MB}$).

---

## [2026-10-18 16:54] - Hoàn Thiện Script Làm Sạch DataCo_Cleaned_Full (180,519 dòng x 53 cột)
- **Môi trường:** Windows | Python 3.14 | Pandas
- **Mục tiêu phiên:** Xây dựng script Python bằng Pandas làm sạch toàn diện dữ liệu thô [7_PJ13_2521001054_Nguyễn Lê Nhật Hạ.csv](file:///c:/Users/nhath/Downloads/.agents/7_PJ13_2521001054_Nguy%E1%BB%85n%20L%C3%AA%20Nh%E1%BA%ADt%20H%E1%BA%A1.csv), bảo toàn trọn vẹn $180,519$ dòng và cấu trúc chuẩn $53$ cột của DataCo, tuân thủ nguyên tắc Quản trị dữ liệu & Bảo vệ quyền riêng tư, tái tính toán biến mục tiêu `Late_delivery_risk` và xuất file đầu ra [DataCo_Cleaned_Full.csv](file:///c:/Users/nhath/Downloads/.agents/DataCo_Cleaned_Full.csv) cùng [DataCo_Cleaned_Full.parquet](file:///c:/Users/nhath/Downloads/.agents/DataCo_Cleaned_Full.parquet).
- **Nội dung đã hoàn thành:**
  - **Quản trị dữ liệu & Bảo mật PII:** Ẩn danh hóa thông tin định danh nhạy cảm (`Customer Email`, `Customer Password`) về chuẩn an toàn `'XXXXXXXXX'`, đồng thời hỗ trợ tham số `drop_pii_cols` linh hoạt; chuẩn hóa lỗi nhập liệu tự do ở trường `Late_delivery_risk`.
  - **Bảo toàn quy mô & cấu trúc:** Giữ nguyên 100% quy mô **$180,519$ dòng $\times$ $53$ cột** (không dropna/không drop_duplicates làm thất thoát dòng dữ liệu).
  - **Khử nhiễu Regex & Ép kiểu định lượng:** Loại bỏ triệt để đơn vị tiền tệ/khối lượng/tỷ lệ (`VND`, `USD`, `kg`, `%`, `đ`), chuyển đổi dấu phẩy thập phân `,` thành `.`, đưa các mã lỗi (`?`, `-`, `-1`, `9999`) về `np.nan`; ép kiểu tối ưu `float32`, `int32`, `int8`.
  - **Tái tính toán Logic SCM Biến Mục Tiêu:** Thiết lập `Late_delivery_risk = 1` nếu `Days for shipping (real) > Days for shipment (scheduled)`, ngược lại `0` (Tỷ lệ trễ hạn: $54.62\%$ vs đúng hạn/sớm: $45.38\%$).
  - **Điền khuyết hoàn chỉnh (Complete Imputation):** Điền median theo `Shipping Mode` cho số ngày vận chuyển, theo `Category Name` cho các biến tài chính/sản phẩm; điền `'Unknown'` cho biến phân loại; chuyển đổi `pd.to_datetime` và đối chiếu chéo tự động khôi phục ngày đặt / ngày giao hàng. Đạt **0 giá trị NaN** trên toàn bộ 53 cột.
  - **Tối ưu RAM & Xuất kết quả:** Giảm RAM từ 144.67 MB xuống còn **26.34 MB** (tiết kiệm **81.8%**). Xuất thành công tệp [DataCo_Cleaned_Full.csv](file:///c:/Users/nhath/Downloads/.agents/DataCo_Cleaned_Full.csv) (82.27 MB) và [DataCo_Cleaned_Full.parquet](file:///c:/Users/nhath/Downloads/.agents/DataCo_Cleaned_Full.parquet) (11.06 MB) chỉ trong $19.10$ giây.
- **Tồn đọng & Bước tiếp theo:**
  - Sử dụng trực tiếp `DataCo_Cleaned_Full.parquet` cho các bước EDA, trực quan hóa và huấn luyện mô hình dự báo rủi ro trễ hạn.

---

## [2026-10-18 16:17] - Nâng Cấp Toàn Diện Pipeline clean_data.py & Đồng Bộ File Quarto
- **Môi trường:** Windows
- **Mục tiêu phiên:** Nâng cấp trực tiếp script [clean_data.py](file:///c:/Users/nhath/Downloads/.agents/clean_data.py) để chuẩn hóa chuỗi phân loại, tái tính toán logic `Late_delivery_risk = (real > scheduled)`, điền khuyết median theo `Shipping Mode`, loại bỏ PII/định danh, tối ưu RAM và xuất tệp sạch cuối cùng [DataCo_Cleaned_Final.parquet](file:///c:/Users/nhath/Downloads/.agents/DataCo_Cleaned_Final.parquet) & [DataCo_Cleaned_Final.csv](file:///c:/Users/nhath/Downloads/.agents/DataCo_Cleaned_Final.csv); đồng bộ toàn bộ nội dung vào tệp Quarto [PRJ13_Bao_Cao_Tieu_Luan.qmd](file:///c:/Users/nhath/Downloads/.agents/PRJ13_Bao_Cao_Tieu_Luan.qmd).
- **Nội dung đã hoàn thành:**
  - Chuẩn hóa văn bản: lowercase (`str.lower()`), cắt tỉa khoảng trắng (`str.strip()`), hợp nhất các nhãn nhiễu/lỗi font (`unknown`, `?`, `chưa rõ`, `chæ°a rã`, `none`) về `np.nan`.
  - Tái tính toán biến mục tiêu: `Late_delivery_risk = 1` nếu `Days for shipping (real) > Days for shipment (scheduled)`, ngược lại `0` (phân phối cân bằng tự nhiên: 51.90% trễ hạn vs 48.10% đúng hạn).
  - Điền giá trị khuyết: `median` theo nhóm `Shipping Mode` cho biến số tài chính (`Sales per customer`, `Benefit per order`), điền `'unknown'` cho các biến định tính (`Order Region`, `Category Name`, `Customer City`).
  - Bảo vệ PII & loại bỏ cột thừa: Đã loại bỏ 9 cột (`Customer Email, Password, Fname, Lname, Street, Customer Id, Order Customer Id, Product Image, Customer Zipcode`).
  - Tối ưu hóa bộ nhớ RAM: Chuyển đổi toàn bộ cột chuỗi sang `category`, hạ kiểu số (`float32`, `int8`), giảm dung lượng RAM từ 101.12 MB xuống còn **21.80 MB** (tiết kiệm **78.4%**).
  - Xuất thành công 2 file sạch:
    - [DataCo_Cleaned_Final.parquet](file:///c:/Users/nhath/Downloads/.agents/DataCo_Cleaned_Final.parquet) (8.24 MB).
    - [DataCo_Cleaned_Final.csv](file:///c:/Users/nhath/Downloads/.agents/DataCo_Cleaned_Final.csv) (47.19 MB, $161,356$ dòng $\times$ $42$ cột).
  - Đồng bộ cập nhật file Quarto [PRJ13_Bao_Cao_Tieu_Luan.qmd](file:///c:/Users/nhath/Downloads/.agents/PRJ13_Bao_Cao_Tieu_Luan.qmd): Thông tin tác giả nhóm sinh viên (Nguyễn Lê Nhật Hạ & Nguyễn Thanh Thiện), Trường ĐH Tài chính - Marketing (UFM), GVHD ThS. Trần Mạnh Tường, cùng số liệu Chương 3 và Phụ lục A.
- **Quyết định kỹ thuật:**
  - Áp dụng kỹ thuật kiểm tra và ép kiểu an toàn tránh lỗi `IntCastingNaNError` trên Pandas.
- **Tồn đọng & Bước tiếp theo:**
  - Sử dụng file `DataCo_Cleaned_Final.parquet` hoặc `DataCo_Cleaned_Final.csv` để hoàn thiện EDA và mô hình hóa trong notebook.


## [2026-10-18 15:16] - Xây Dựng Script Tiền Xử Lý Dữ Liệu clean_data.py
- **Môi trường:** Windows
- **Mục tiêu phiên:** Viết script Python chuẩn PEP 8 bằng Pandas làm sạch dữ liệu thô [7_PJ13_2521001054_Nguyễn Lê Nhật Hạ.csv](file:///c:/Users/nhath/Downloads/.agents/7_PJ13_2521001054_Nguy%E1%BB%85n%20L%C3%AA%20Nh%E1%BA%ADt%20H%E1%BA%A1.csv) và xuất ra file [DataCo_Cleaned.csv](file:///c:/Users/nhath/Downloads/.agents/DataCo_Cleaned.csv) cùng [DataCo_Cleaned.parquet](file:///c:/Users/nhath/Downloads/.agents/DataCo_Cleaned.parquet).
- **Nội dung đã hoàn thành:**
  - Viết và kiểm thử thành công script [clean_data.py](file:///c:/Users/nhath/Downloads/.agents/clean_data.py).
  - Loại bỏ các cột PII bảo mật (`Customer Email`, `Customer Password`, `Customer Fname`, `Customer Lname`, `Customer Street`).
  - Loại bỏ các cột khuyết > 70% (`Order Zipcode`, `Product Description`).
  - Xây dựng hàm Regex Vectorized loại bỏ đơn vị (`VND`, `USD`, `kg`, `đ`, `%`) và thay thế các mã khuyết (`?`, `-`, `-1`, `9999`) thành `np.nan`.
  - Ép kiểu dữ liệu: các cột số đưa về `float32` và `int32`, chuẩn hóa cột mục tiêu `Late_delivery_risk` về nhị phân `int8` (0/1).
  - Điền giá trị khuyết (Imputation) bằng median theo nhóm `Shipping Mode` cho các cột ngày vận chuyển.
  - Tối ưu hóa bộ nhớ: chuyển đổi các cột phân loại sang `category`, giảm RAM từ 145.30 MB xuống 79.33 MB (tiết kiệm 45.4%).
  - Xuất thành công tệp sạch [DataCo_Cleaned.csv](file:///c:/Users/nhath/Downloads/.agents/DataCo_Cleaned.csv) (62.56 MB) định dạng UTF-8-SIG (tương thích hoàn hảo với Excel/Notebook) và tệp nén [DataCo_Cleaned.parquet](file:///c:/Users/nhath/Downloads/.agents/DataCo_Cleaned.parquet) (10.36 MB) với 161,356 dòng và 46 cột.
- **Quyết định kỹ thuật:**
  - Áp dụng kỹ thuật Vectorized Regex trên Pandas thay vì lặp từng phần tử để giảm thời gian xử lý từ 40 giây xuống dưới 2 giây.
  - Tích hợp cấu hình `sys.stdout.reconfigure(encoding="utf-8")` đảm bảo script chạy an toàn không lỗi encoding trên môi trường Windows.
- **Tồn đọng & Bước tiếp theo:**
  - Đưa tệp `DataCo_Cleaned.csv` / `DataCo_Cleaned.parquet` vào notebook [Phân tích data.ipynb](file:///c:/Users/nhath/Downloads/.agents/Ph%C3%A2n%20t%C3%ADch%20data.ipynb) để tiến hành EDA và huấn luyện mô hình.


## [2026-10-18 15:10] - Xây Dựng Module Khám Phá Dữ Liệu 01_data_overview.py & Notebook 01_data_overview.ipynb
- **Môi trường:** Windows | Python 3.14 | Pandas | NumPy | Matplotlib | Seaborn | Jupyter Notebook
- **Mục tiêu phiên:** 
  1. Xây dựng script Python [01_data_overview.py](file:///c:/Users/nhath/Downloads/.agents/01_data_overview.py) chuẩn Senior Data Analyst: đọc dữ liệu thô an toàn từ `data/raw/7_PJ13_2521001054_Nguyễn Lê Nhật Hạ.csv`, kiểm toán đối chiếu schema 180,519 dòng x 53 cột, thống kê missing/noise (`?`, `-`, `unknown`, `-1`, `9999`), kiểm toán PII bảo mật GDPR, phân tích nhãn mục tiêu và xuất 2 báo cáo `reports/data_overview.csv` và `reports/data_quality_before.csv`.
  2. Xây dựng Jupyter Notebook tương tác [01_data_overview.ipynb](file:///c:/Users/nhath/Downloads/.agents/01_data_overview.ipynb) chia rõ 7 phần gồm 38 cell và 5 checkpoint theo chuẩn học tập nghiên cứu, có cấu trúc A-B-C-D sau mỗi nhóm cell để sinh viên tự ghi nhận xét.
  3. Chạy thử nghiệm thực tế toàn bộ script và tất cả các cell trong notebook, đảm bảo 100% không phát sinh lỗi và không làm lộ lọt thông tin cá nhân PII.
- **Kết quả đạt được:**
  - Xác nhận kích thước dữ liệu chuẩn: **180,519 dòng x 53 cột**.
  - Kiểm toán 5 trường PII (`Customer Email`, `Customer Password`, `Customer Fname`, `Customer Lname`, `Customer Street`) được ẩn danh hóa và đề xuất loại bỏ.
  - Nhận diện các thuộc tính khuyết trầm trọng: `Product Description` (khuyết $83.46\%$) và `Order Zipcode` (khuyết $79.30\%$).
  - Phân tích biến mục tiêu `Late_delivery_risk`: phát hiện $16.73\%$ nhãn bị dơ do dính đơn vị tiền tệ (`1 VND`, `1 USD`, `1 kg`, `1 %`), đối chiếu khớp $100\%$ logic Quy tắc Vàng SCM (`Days for shipping (real) > Days for shipment (scheduled)`).
  - Xuất thành công hai tệp báo cáo: [reports/data_overview.csv](file:///c:/Users/nhath/Downloads/.agents/reports/data_overview.csv) và [reports/data_quality_before.csv](file:///c:/Users/nhath/Downloads/.agents/reports/data_quality_before.csv).


## [2026-10-18 14:58] - Phân Tích Nghiệp Vụ Tệp Dữ Liệu 7_PJ13_2521001054_Nguyễn Lê Nhật Hạ.csv
- **Môi trường:** Windows
- **Mục tiêu phiên:** Phân tích toàn diện góc nhìn nghiệp vụ chuỗi cung ứng, cấu trúc 53 cột, dị thường dữ liệu (noisy/dirty data) và các quy tắc nghiệp vụ vàng (Ground Truth) trong tệp [7_PJ13_2521001054_Nguyễn Lê Nhật Hạ.csv](file:///c:/Users/nhath/Downloads/.agents/7_PJ13_2521001054_Nguy%E1%BB%85n%20L%C3%AA%20Nh%E1%BA%ADt%20H%E1%BA%A1.csv).
- **Nội dung đã hoàn thành:**
  - Khám phá hồ sơ dữ liệu: $180,519$ dòng $\times$ $53$ cột, nhận diện tập dữ liệu thực hành cá nhân hóa cho sinh viên Nguyễn Lê Nhật Hạ (MSSV: 2521001054).
  - Phân loại 53 trường thành 6 nhóm nghiệp vụ: Vận chuyển & Giao nhận, Đơn hàng & Thanh toán, Kinh tế đơn vị & Tài chính, Hồ sơ khách hàng, Danh mục sản phẩm, Bảo mật thông tin (PII).
  - Phát hiện dị thường dữ liệu: Biến mục tiêu `Late_delivery_risk` bị nhiễu chuỗi đơn vị (`1 VND`, `1 USD`, `1 kg`, `1 %`), giá trị mã hóa lỗi (`?`, `-`, `9999`, `-1`), và thiếu $8,378$ giá trị.
  - Khám phá Quy tắc Nghiệp vụ Vàng: Tương quan 100% giữa `Delivery Status` (`Late delivery` $\rightarrow 1$, các trạng thái khác $\rightarrow 0$) và logic `Days for shipping (real) > Days for shipment (scheduled)` giúp khôi phục dữ liệu mục tiêu.
  - Cảnh báo rủi ro rò rỉ dữ liệu (*Data Leakage*): Các cột hậu giao hàng (`Days for shipping (real)`, `Delivery Status`, `shipping date`) tuyệt đối không dùng làm đặc trưng đầu vào cho mô hình dự báo thời điểm tạo đơn.
- **Quyết định kỹ thuật:**
  - Áp dụng các quy tắc suy luận nghiệp vụ (Business Rules Imputation) để làm sạch nhãn mục tiêu và chuẩn hóa các cột phân loại trước khi đưa vào pipeline.
- **Tồn đọng & Bước tiếp theo:**
  - Xây dựng module làm sạch dữ liệu tự động cho tệp này và cập nhật số liệu thực tế vào báo cáo [PRJ13_Bao_Cao_Tieu_Luan.qmd](file:///c:/Users/nhath/Downloads/.agents/PRJ13_Bao_Cao_Tieu_Luan.qmd).


## [2026-10-08 11:40] - Khởi tạo Tệp Quarto Báo Cáo Tiểu Luận PRJ-13
- **Môi trường:** Windows
- **Mục tiêu phiên:** Tạo tệp Quarto (`.qmd`) chuẩn hóa toàn diện theo dàn ý chi tiết tiểu luận báo cáo đề tài PRJ-13: "Dự báo Rủi ro Giao hàng Chậm trễ trong Chuỗi Cung ứng Toàn cầu (DataCo Big Supply Chain Delivery Delay)".
- **Nội dung đã hoàn thành:**
  - Khởi tạo tệp Quarto [PRJ13_Bao_Cao_Tieu_Luan.qmd](file:///c:/Users/nhath/Downloads/.agents/PRJ13_Bao_Cao_Tieu_Luan.qmd) với đầy đủ bố cục học thuật:
    - Trang bìa chuẩn, Lời cam đoan, Lời cảm ơn.
    - Danh mục viết tắt, Danh mục bảng biểu, Danh mục hình vẽ.
    - Executive Summary (Tóm tắt đồ án 250 - 350 từ).
    - Chương 1: Tổng quan đề tài, bài toán cốt lõi và mục tiêu SMART.
    - Chương 2: Cơ sở lý thuyết SCM, quy trình CRISP-DM 7 giai đoạn, kiểm định $\chi^2$, $t$-test, các mô hình phân loại và thước đo ưu tiên (Recall, ROC-AUC).
    - Chương 3: EDA, kỹ thuật ghép nối bảng và tối ưu bộ nhớ (>70% RAM), xử lý IQR/Missing values, trực quan hóa và 4 insight định lượng.
    - Chương 4: Kỹ thuật đặc trưng, chống Data Leakage bằng Scikit-learn Pipeline, huấn luyện Logistic Regression, Random Forest, XGBoost, trích xuất Feature Importance và thảo luận thực nghiệm.
    - Chương 5: Khuyến nghị cảnh báo sớm ERP/OMS, SLA vận tải, lộ trình 3 giai đoạn, đạo đức AI & Human-in-the-loop.
    - Danh mục tài liệu tham khảo chuẩn APA 7th.
    - Phụ lục A (Mã nguồn Python sạch PEP 8) và Phụ lục B (Trích xuất nhật ký P-D-M-V).
- **Quyết định kỹ thuật:**
  - Định dạng YAML linh hoạt hỗ trợ xuất đa nền tảng cả HTML (với code tools, folding, theme) và PDF (LaTeX booktabs, caption, A4 geometry).
  - Triệt tiêu hoàn toàn rò rỉ dữ liệu bằng cách loại bỏ các biến hậu vận chuyển (`Days for shipping (real)`, `Delivery Status`) khỏi đặc trưng đầu vào mô hình.
- **Tồn đọng & Bước tiếp theo:**
  - Thực thi chạy thử mã nguồn thực nghiệm với tệp dữ liệu `DataCoSupplyChainDataset.csv` trong workspace.
  - Kết xuất biểu đồ trực quan hóa và cập nhật bảng số liệu thực tế vào báo cáo.

---
