# BÁO CÁO PHÂN TÍCH KHÁM PHÁ DỮ LIỆU & INSIGHTS NGHIỆP VỤ (EDA INSIGHTS)
**Đề tài PRJ-13:** Dự Báo Rủi Ro Giao Hàng Chậm Trễ Trong Chuỗi Cung Ứng Toàn Cầu (DataCo Smart Supply Chain)  
**Tác giả:** Senior Data Analyst | Nhóm sinh viên thực hiện: Nguyễn Lê Nhật Hạ & Nguyễn Thanh Thiện  
**Nguồn dữ liệu:** `data/processed/DataCo_Cleaned_Full.parquet` ($180,519$ dòng $	imes$ $51$ cột sạch)

---

## 1. MỤC TIÊU & CƠ SỞ ĐÁNH GIÁ (RQ1 - RQ4)
Báo cáo này giải quyết trọn vẹn 4 câu hỏi nghiên cứu cốt lõi của đề tài:
- **RQ1 (Phân tích mối liên hệ):** Xác định các nhân tố vận tải và địa lý chi phối mạnh mẽ nhất đến rủi ro trễ hạn `Late_delivery_risk`.
- **RQ2 (Đánh giá chất lượng dữ liệu):** Đo lường tính cân bằng của nhãn mục tiêu, độ lệch Skewness, ngoại lệ IQR và phân định rõ ràng giữa đơn vị quan sát cấp đơn hàng (*Order*) và cấp mục hàng (*Line Item*).
- **RQ3 (Chuẩn bị bằng chứng dự báo):** Xếp hạng Mutual Information cho các đặc trưng đầu vào tiềm năng và thiết lập rào chắn chống rò rỉ dữ liệu (*Data Leakage Prevention*).
- **RQ4 (Khuyến nghị quản trị):** Chỉ ra các điểm nghẽn SLA chặng cuối để đề xuất tái cấu trúc hợp đồng vận chuyển.

---

## 2. BỘ 5 INSIGHTS NGHIỆP VỤ ĐỊNH LƯỢNG CỐT LÕI

### INSIGHT 1: Nghịch Lý Cam Kết SLA Gói First Class (The First Class SLA Paradox)
- **Bằng chứng số liệu:**
  - Gói vận chuyển **First Class** có tỷ lệ trễ hạn lên tới **$95.28\%$** ($26,894 / 28,225$ đơn trễ).
  - Ngược lại, gói **Standard Class** có tỷ lệ trễ hạn thấp nhất toàn hệ thống, chỉ **$38.11\%$** ($38,720 / 101,607$ đơn trễ).
  - Kiểm định Chi-Square khẳng định mối quan hệ cực kỳ chặt chẽ: $\chi^2 = 34,863.00$, $p\text{-value} < 10^{-16}$, hệ số tương quan định danh Cramér's V đạt **$0.4473$** (mức độ ảnh hưởng mạnh).
- **Nhận xét thống kê:** Sự khác biệt về tỷ lệ trễ giữa các gói giao hàng không xuất phát từ năng lực của tài xế, mà do sự chênh lệch trong thiết lập kỳ vọng SLA của hệ thống TMS: First Class bị ép cam kết cố định 1 ngày bất kể khoảng cách địa lý, trong khi Standard Class có biên độ đệm an toàn tới 4 ngày.
- **Ý nghĩa nghiệp vụ:** Doanh nghiệp đang thu phí dịch vụ cao cấp First Class nhưng lại giao trễ tới 95% đơn hàng, dẫn đến nguy cơ mất khách hàng trung thành và chịu chi phí bồi thường SLA khổng lồ.
- **Hạn chế phương pháp luận:** Chưa thu thập được biến số khoảng cách địa lý (Km) giữa kho gửi và địa chỉ người nhận để đo lường vận tốc thực tế.
- **Đề xuất hành động tiếp theo:** Chuyển đổi từ mô hình cam kết SLA cố định (Fixed SLA) sang cam kết động (Dynamic SLA) dựa trên bán kính vận chuyển.

---

### INSIGHT 2: Sự Độc Lập Giữa Giá Trị Đơn Hàng Và Tốc Độ Giao Vận (Order Value vs Priority)
- **Bằng chứng số liệu:**
  - Kiểm định One-Way ANOVA cho giá trị đơn hàng `Sales` giữa 4 phương thức vận chuyển cho thấy $F = 0.82$, $p	ext{-value} = 0.48 > 0.05$ (không có sự khác biệt mang ý nghĩa thống kê).
  - Tương quan Pearson giữa `Sales per customer` và biến mục tiêu `Late_delivery_risk` gần như bằng 0 ($r = -0.0037$), Mutual Information đạt xấp xỉ $0.0000$.
- **Nhận xét thống kê:** Giá trị tiền tệ của đơn hàng (dù là $20$ USD hay $1,500$ USD) hoàn toàn không ảnh hưởng đến việc đơn hàng đó được giao nhanh hay chậm.
- **Ý nghĩa nghiệp vụ:** DataCo chưa hề thiết lập cơ chế **Luồng ưu tiên (Priority Dispatch Routing)** cho các đơn hàng giá trị cao hoặc khách hàng VIP. Đơn hàng tiền triệu và đơn hàng vài chục nghìn đều xếp chung một hàng đợi bốc xếp tại kho 3PL.
- **Hạn chế:** Dữ liệu chưa ghi nhận chỉ số độ thỏa mãn của khách hàng (CSAT/NPS) để đo lường mức độ phẫn nộ của nhóm khách hàng mua sỉ khi bị trễ hạn.
- **Đề xuất hành động tiếp theo:** Đưa thuộc tính `Sales` và phân khúc `Customer Segment` vào thuật toán OMS để kích hoạt cờ ưu tiên xuất kho (*Priority Warehouse Picking*).

---

### INSIGHT 3: Phân Hóa Rủi Ro Theo Khu Vực Địa Lý Và Rào Cản Thông Quan (Regional Disparities)
- **Bằng chứng số liệu:**
  - Khu vực **Western Europe** (Tây Âu) và **Central America** có tỷ lệ trễ hạn vượt ngưỡng **$58\%$** ($61.2\%$ tại một số tiểu vùng quốc tế).
  - Ngược lại, khu vực **USCA** (Mỹ và Canada) duy trì tỷ lệ trễ hạn thấp hơn đáng kể (~$46\%$).
  - Kiểm định Chi-Square theo khu vực đạt $\chi^2 = 2,418.52$, $p	ext{-value} < 10^{-16}$.
- **Nhận xét thống kê:** Yếu tố địa lý và mạng lưới đối tác giao vận địa phương có sự phân hóa rõ nét về năng lực hoàn tất đơn hàng.
- **Ý nghĩa nghiệp vụ:** Các đơn hàng xuất khẩu liên lục địa sang châu Âu thường gặp điểm nghẽn tại khâu thủ tục hải quan và chuyển tải chặng giữa (*Cross-docking*).
- **Hạn chế:** Thiếu dữ liệu thời gian thông quan chi tiết của từng cửa khẩu cảng biển/sân bay.
- **Đề xuất hành động tiếp theo:** Bổ sung thêm nhà thầu vận tải địa phương dự phòng (*Secondary 3PL Carriers*) tại Tây Âu để san sẻ tải trọng vào mùa cao điểm.

---

### INSIGHT 4: Tính Ổn Định Và Hợp Lệ Của Các Điểm Ngoại Lệ Tài Chính (Legitimate Outliers)
- **Bằng chứng số liệu:**
  - Phương pháp IQR phát hiện $9,064$ điểm ngoại lệ trong `Sales` ($5.02\%$) và $18,185$ ngoại lệ trong `Benefit per order` ($10.07\%$).
  - Ngưỡng trên của Sales theo $Q_3 + 1.5 	imes 	ext{IQR}$ là $585.03$ USD, trong khi giá trị cao nhất đạt $1,999.99$ USD.
  - Phân tích sâu cho thấy toàn bộ các đơn hàng ngoại lệ này đều có `Order Item Quantity` từ 3 đến 5 sản phẩm thuộc danh mục máy tính hoặc thiết bị dã ngoại cao cấp.
- **Nhận xét thống kê:** Các điểm ngoại lệ tài chính không phải là lỗi nhập liệu (Data Entry Error), mà là các giao dịch mua sỉ hoặc bán sản phẩm giá trị cao hoàn toàn có thật.
- **Ý nghĩa nghiệp vụ:** Quyết định **giữ nguyên không xóa/clip ngoại lệ** là hoàn toàn đúng đắn. Việc cắt xén ngoại lệ sẽ làm mô hình học sai phân phối doanh thu của doanh nghiệp.
- **Hạn chế:** Các mô hình tuyến tính (Logistic Regression) nhạy cảm với độ lệch Skewness của các biến này ($Skewness_{Sales} = 1.98$).
- **Đề xuất kỹ thuật:** Áp dụng biến đổi phi tuyến `np.log1p()` khi đưa vào mô hình hóa ở Chương 4.

---

### INSIGHT 5: Bằng Chứng Lựa Chọn Đặc Trưng & Cảnh Báo Chống Rò Rỉ Dữ Liệu (RQ3 Evidence)
- **Bằng chứng số liệu:**
  - Đo lường Mutual Information (MI) với nhãn mục tiêu cho thấy hai biến chi phối mạnh nhất là:
    1. `Days for shipment (scheduled)`: $	ext{MI} = 0.1239$.
    2. `Shipping Mode`: $	ext{MI} = 0.1151$.
  - Toàn bộ các biến nhân khẩu học và tài chính đều có $	ext{MI} < 0.005$.
  - Biến `Days for shipping (real)` có tương quan Pearson dương cao nhất ($r = +0.40$), trong khi `Days for shipment (scheduled)` có tương quan âm mạnh nhất ($r = -0.37$).
- **Cảnh báo học thuật nghiêm ngặt về Data Leakage:**
  - Biến `Days for shipping (real)`, `Delivery Status`, và `shipping date (DateOrders)` là các **thông tin hậu giao hàng (Post-fulfillment metrics)**, chỉ phát sinh sau khi đơn hàng đã rời kho hoặc được đối tác 3PL quét mã xác nhận.
  - Nếu đưa các thuộc tính này vào huấn luyện mô hình dự báo tại thời điểm khách đặt hàng (Checkout), mô hình sẽ đạt độ chính xác ảo nhưng hoàn toàn vô dụng trong triển khai thực tế.
- **Quyết định cho Chương 4 (Modeling):**
  - Không gian đặc trưng đầu vào ($X$) sẽ tập trung vào nhóm biến thời điểm khởi tạo: `Days for shipment (scheduled)`, `Shipping Mode`, `Market`, `Order Region`, `Customer Segment`, kết hợp các biến thời gian trích xuất từ `order date` (Thứ trong tuần, Tháng, Cuối tuần).

---
*Báo cáo được khởi tạo tự động từ Module 03_eda.py phục vụ hoàn thiện Chương 3 và Chương 4 của đề tài PRJ-13.*
