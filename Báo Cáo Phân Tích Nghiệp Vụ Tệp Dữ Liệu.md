# BÁO CÁO PHÂN TÍCH NGHIỆP VỤ & KIẾN TRÚC DỮ LIỆU
**Tệp dữ liệu phân tích:** `7_PJ13_2521001054_Nguyễn Lê Nhật Hạ.csv`  
**Đề tài:** PRJ-13 - Dự báo Rủi ro Giao hàng Chậm trễ trong Chuỗi Cung ứng Toàn cầu (*DataCo Big Supply Chain Delivery Delay*)  
**Đơn vị:** Trường Đại học Tài chính - Marketing (UFM) - Khoa Khoa học Dữ liệu  
**Giảng viên hướng dẫn:** ThS. Trần Mạnh Tường  
**Sinh viên thực hiện:**
- Nguyễn Lê Nhật Hạ - MSSV: 2521001054
- Nguyễn Thanh Thiện - MSSV: 2521001102  
**Lớp học phần:** 2631101190501 | **Học kỳ:** HK3-2026

---

## 1. Bối Cảnh Kinh Doanh & Quy Trình Phát Sinh Dữ Liệu

### 1.1. Hoạt Động Kinh Doanh Cốt Lõi
Bộ dữ liệu phản ánh toàn bộ chuỗi vận hành thương mại điện tử đa kênh (*Omnichannel Retail & E-commerce*) và mạng lưới logistics quốc tế của tập đoàn bán lẻ **DataCo Global**. 

Doanh nghiệp cung cấp đa dạng các ngành hàng (Thể thao, Đồ gia dụng, Thời trang, Điện tử, Thiết bị ngoài trời) đến khách hàng thuộc 3 phân khúc chính (*Consumer, Corporate, Home Office*) trải rộng trên 5 đại thị trường toàn cầu:
- **LATAM** (Châu Mỹ Latinh): Chiếm tỷ trọng lưu lượng đơn hàng lớn nhất (~$24.2\%$).
- **Europe** (Châu Âu): Thị trường thương mại chủ chốt (~$23.4\%$).
- **Pacific Asia** (Châu Á - Thái Bình Dương): Thị trường đang phát triển nhanh (~$19.3\%$).
- **USCA** (Hoa Kỳ & Canada): Thị trường nội địa trọng tâm (~$14.3\%$).
- **Africa** (Châu Phi): Thị trường mới nổi (~$6.4\%$).

### 1.2. Các Phòng Ban Quản Lý & Cơ Chế Ghi Nhận Dữ Liệu
Dữ liệu trong tệp không phát sinh đơn lẻ mà được ghi nhận đồng bộ qua nhiều phân hệ công nghệ thông tin thuộc các phòng ban chức năng:

```
[Khách Hàng] 
     │
     ▼
[Phòng Kinh Doanh / CRM] ──(Hệ thống OMS/CRM)──> Ghi nhận thông tin Khách hàng, Sản phẩm, Đơn hàng, Giảm giá
     │
     ▼
[Phòng Tài Chính - Kế Toán] ──(Cổng Thanh Toán/ERP)──> Ghi nhận Phương thức thanh toán, Doanh thu, Lợi nhuận
     │
     ▼
[Phòng Kho Vận / Fulfillment] ──(Hệ thống WMS)──> Đóng gói, Xuất kho, Phân loại kiện hàng
     │
     ▼
[Phòng Logistics / Vận Tải] ──(Hệ thống TMS)──> Xác lập Phương thức vận chuyển, Thiết lập SLA cam kết
     │
     ▼
[Đối Tác Vận Chuyển 3PL] ──(Thiết bị Quét/EDI/API)──> Ghi nhận Ngày giao thực tế, Trạng thái đơn, Cờ trễ hạn
```

1. **Phòng Kinh doanh & Trải nghiệm Khách hàng (Sales & Customer Experience):**
   - *Hệ thống quản lý:* Hệ thống Quản trị Quan hệ Khách hàng (CRM) và Hệ thống Quản lý Đơn hàng (OMS - *Order Management System*).
   - *Phương thức ghi nhận:* Khi khách hàng đặt hàng qua website hoặc ứng dụng, hệ thống tự động ghi nhận thông tin nhân khẩu học (`Customer Segment`, `Customer City`, `Customer State`), thời điểm đặt hàng (`order date (DateOrders)`), chi tiết sản phẩm (`Product Name`, `Product Price`), số lượng đặt mua (`Order Item Quantity`) và tỷ lệ chiết khấu áp dụng (`Order Item Discount Rate`).

2. **Phòng Tài chính - Kế toán (Finance & Accounting):**
   - *Hệ thống quản lý:* Cổng thanh toán trực tuyến (*Payment Gateway*) tích hợp hệ thống Hoạch định Nguồn lực Doanh nghiệp (ERP).
   - *Phương thức ghi nhận:* Xác thực giao dịch thanh toán (`Type`: *DEBIT, CASH, PAYMENT, TRANSFER*), tính toán doanh thu thuần sau giảm giá (`Sales per customer`), tổng giá trị đơn hàng (`Sales`, `Order Item Total`) và biên lợi nhuận ròng thu về trên từng giao dịch (`Benefit per order`, `Order Profit Per Order`).

3. **Phòng Quản lý Kho bãi & Hoàn tất Đơn hàng (Warehouse Operations & Fulfillment):**
   - *Hệ thống quản lý:* Hệ thống Quản lý Kho bãi (WMS - *Warehouse Management System*).
   - *Phương thức ghi nhận:* Quản lý vị trí lưu kho, phân loại danh mục hàng hóa (`Category Name`, `Department Name`), kiểm soát tồn kho (`Product Status`) và đóng gói kiện hàng sẵn sàng xuất kho.

4. **Phòng Điều phối Vận tải & Logistics (Logistics & Transportation):**
   - *Hệ thống quản lý:* Hệ thống Quản lý Vận tải (TMS - *Transportation Management System*).
   - *Phương thức ghi nhận:* Tiếp nhận yêu cầu vận chuyển, gắn phương thức vận chuyển mà khách lựa chọn (`Shipping Mode`: *Standard Class, Second Class, First Class, Same Day*), đồng thời dựa trên bảng thỏa thuận mức dịch vụ (SLA) để ấn định số ngày cam kết hoàn thành tối đa (`Days for shipment (scheduled)`).

5. **Đối tác Vận tải Chặng cuối (Third-Party Logistics - 3PL Carriers):**
   - *Hệ thống quản lý:* Thiết bị quét mã vạch cầm tay (*Handheld Scanner*), ứng dụng tài xế giao hàng và cổng giao tiếp điện tử EDI / API.
   - *Phương thức ghi nhận:* Khi kiện hàng được phát thành công hoặc gặp sự cố chặng cuối, đối tác 3PL quét mã vận đơn, ghi nhận tức thời mốc thời gian giao hàng thực tế (`shipping date (DateOrders)`), tổng số ngày vận chuyển thực tế (`Days for shipping (real)`) và trạng thái giao hàng (`Delivery Status`). Hệ thống tự động so khớp để dán nhãn rủi ro trễ hạn (`Late_delivery_risk`).

---

## 2. Đơn Vị Quan Sát & Cỡ Mẫu (Granularity & Sample Size)

### 2.1. Đơn Vị Quan Sát Cốt Lõi (Unit of Observation)
- Đơn vị quan sát của bộ dữ liệu là **Một mục hàng trong đơn hàng (Line Item / Order Item Transaction)**, không phải là một đơn hàng tổng thể.
- **Ý nghĩa thực tế:** Một khách hàng khi tiến hành mua sắm có thể đặt một đơn hàng duy nhất (`Order Id`), nhưng đơn hàng đó có thể bao gồm nhiều sản phẩm khác nhau. Mỗi sản phẩm được gắn một mã định danh mục hàng riêng biệt (`Order Item Id`).
  - *Ví dụ thực tế:* Đơn hàng mã `Order Id = 12345` gồm 1 đôi giày chạy bộ và 2 chiếc áo thun thể thao sẽ được lưu trữ thành **2 dòng giao dịch riêng biệt** trong tệp dữ liệu. Hai dòng này dùng chung thông tin khách hàng, ngày đặt, thị trường và địa chỉ nhận, nhưng khác nhau về mã sản phẩm (`Product Card Id`), số lượng (`Order Item Quantity`), giá thành và lợi nhuận từng mục hàng.

### 2.2. Quy Mô Dữ Liệu & Cỡ Mẫu Ban Đầu
- **Tổng số dòng dữ liệu (Rows):** $180,519$ bản ghi giao dịch.
- **Tổng số cột thuộc tính (Columns):** $53$ trường thông tin phản ánh toàn diện chuỗi giá trị.
- **Dung lượng tệp dữ liệu thô trên đĩa:** $\approx 87.24\text{ MB}$.
- **Quy mô sau khi tiền xử lý và loại bỏ PII:** $180,519$ dòng $\times$ $51$ cột (bảo toàn nguyên vẹn 100% cỡ mẫu, không xóa dòng gây thất thoát thông tin nghiệp vụ; loại bỏ 2 cột định danh nhạy cảm `Customer Email` và `Customer Password` theo chuẩn Data Governance).

---

## 3. Kiến Trúc & Từ Điển Dữ Liệu (Data Architecture & Data Dictionary)

### 3.1. Kiến Trúc Quan Hệ Logic Giữa Các Thực Thể (Logical Data Architecture)
Dữ liệu thực chất được giải chuẩn hóa (*denormalized*) từ mô hình cơ sở dữ liệu quan hệ dạng hình sao (*Star / Snowflake Schema*), trong đó bảng trung tâm là **Order Items Fact Table** liên kết với các bảng chiều (*Dimension Tables*):

```
┌─────────────────────────┐           ┌─────────────────────────┐
│   CUSTOMERS DIMENSION   │           │    PRODUCTS DIMENSION   │
├─────────────────────────┤           ├─────────────────────────┤
│ PK: Customer Id         │           │ PK: Product Card Id     │
│ - Customer Fname, Lname │           │ - Product Name          │
│ - Customer Segment      │           │ - Product Price         │
│ - Customer City, State  │           │ FK: Category Id         │
└────────────┬────────────┘           └────────────┬────────────┘
             │                                     │
             │ (1 - n)                             │ (1 - n)
             ▼                                     ▼
┌─────────────────────────┐           ┌─────────────────────────┐
│     ORDERS DIMENSION    │           │   CATEGORIES DIMENSION  │
├─────────────────────────┤           ├─────────────────────────┤
│ PK: Order Id            │           │ PK: Category Id         │
│ - order date (DateOrders│           │ - Category Name         │
│ - Order Status, Type    │           │ FK: Department Id       │
│ - Market, Order Region  │           └────────────┬────────────┘
│ FK: Order Customer Id   │                        │
└────────────┬────────────┘                        │ (1 - n)
             │                                     ▼
             │ (1 - n)                ┌─────────────────────────┐
             ▼                        │  DEPARTMENTS DIMENSION  │
┌─────────────────────────────────────┴┐       ├─────────────────────────┤
│         ORDER ITEMS FACT TABLE       │       │ PK: Department Id       │
├──────────────────────────────────────┤       │ - Department Name       │
│ PK: Order Item Id                    │       └─────────────────────────┘
│ FK: Order Id                         │
│ FK: Order Item Cardprod Id           │
│ - Order Item Quantity, Product Price │
│ - Order Item Discount, Total, Profit │
│ - Days for shipment (scheduled)      │
│ - Days for shipping (real)           │
│ - Shipping Mode, Delivery Status     │
│ - TARGET: Late_delivery_risk (0 / 1) │
└──────────────────────────────────────┘
```

### 3.2. Cột Khóa Liên Kết Chính (Primary & Foreign Keys)
1. `Order Item Id`: **Khóa chính duy nhất (Primary Key)** của từng dòng bản ghi giao dịch.
2. `Order Id`: **Khóa ngoại (Foreign Key)** gom cụm các sản phẩm thuộc về cùng một đơn hàng.
3. `Customer Id` / `Order Customer Id`: **Khóa ngoại** định danh khách hàng thực hiện giao dịch.
4. `Product Card Id` / `Order Item Cardprod Id`: **Khóa ngoại** liên kết mục hàng với thông tin sản phẩm trong kho.
5. `Category Id` / `Product Category Id`: **Khóa ngoại** phân loại sản phẩm vào từng ngành hàng.
6. `Department Id`: **Khóa ngoại** xác định phòng ban phụ trách chuỗi cung ứng của sản phẩm.

---

### 3.3. Từ Điển Dữ Liệu Chi Tiết 53 Thuộc Tính (Data Dictionary)

Bảng từ điển dữ liệu được phân chia khoa học thành 6 nhóm nghiệp vụ chính:

#### Nhóm 1: Vận Chuyển, Giao Nhận & Cam Kết Dịch Vụ SLA (Core Logistics)
| STT | Tên Biến | Ý Nghĩa Thực Tế | Đơn Vị Tính | Kiểu Gốc | Kiểu Chuẩn Hóa | Vai Trò / Ý Nghĩa Nghiệp Vụ |
| :---: | :--- | :--- | :---: | :---: | :---: | :--- |
| 1 | `Shipping Mode` | Phương thức vận chuyển được chọn (*Standard, Second, First, Same Day*) | Danh mục | object | category | Đặc trưng đầu vào quyết định SLA cam kết |
| 2 | `Days for shipment (scheduled)` | Số ngày vận chuyển tối đa cam kết với khách hàng theo SLA | Ngày | object (nhiễu) | int8 | **Đặc trưng then chốt** cam kết ngày giao |
| 3 | `Days for shipping (real)` | Số ngày vận chuyển thực tế từ lúc xuất kho đến tay người nhận | Ngày | object (nhiễu) | int8 | **Hậu vận chuyển** (Biến rò rỉ - Chỉ dùng tính cờ) |
| 4 | `Delivery Status` | Trạng thái giao hàng thực tế (*Late delivery, Advance, Shipping on time...*) | Danh mục | object | category | **Hậu vận chuyển** (Biến rò rỉ - Tương quan 100% với rủi ro) |
| 5 | `Late_delivery_risk` | Cờ chỉ báo rủi ro giao hàng trễ (1: Trễ hạn, 0: Đúng hạn/Sớm) | Nhị phân | object (nhiễu) | int8 | **BIẾN MỤC TIÊU (TARGET LABEL)** |
| 6 | `shipping date (DateOrders)` | Mốc thời gian hoàn tất giao kiện hàng đến người nhận | Ngày - Giờ | object (nhiễu) | datetime64 | **Hậu vận chuyển** (Biến rò rỉ) |

#### Nhóm 2: Quản Lý Đơn Hàng & Phân Bổ Địa Lý (Orders & Geography)
| STT | Tên Biến | Ý Nghĩa Thực Tế | Đơn Vị Tính | Kiểu Gốc | Kiểu Chuẩn Hóa | Vai Trò / Ý Nghĩa Nghiệp Vụ |
| :---: | :--- | :--- | :---: | :---: | :---: | :--- |
| 7 | `Order Id` | Mã định danh đơn hàng tổng thể | Khóa | object (nhiễu) | int32 | Gom cụm mục hàng theo đơn |
| 8 | `order date (DateOrders)` | Mốc thời gian khách hàng chốt tạo đơn thành công | Ngày - Giờ | object (nhiễu) | datetime64 | Đặc trưng thời gian, mùa vụ (Tháng, Giờ, Ngày trong tuần) |
| 9 | `Type` | Phương thức thanh toán (*DEBIT, CASH, TRANSFER, PAYMENT*) | Danh mục | object | category | Đánh giá mức độ ưu tiên xử lý đơn |
| 10 | `Order Status` | Trạng thái xử lý của đơn hàng (*COMPLETE, PENDING, PROCESSING...*) | Danh mục | object | category | Trạng thái tiến trình đơn hàng |
| 11 | `Market` | Đại thị trường khu vực nhận hàng (*LATAM, Europe, Pacific Asia...*) | Danh mục | object | category | Đặc trưng địa lý vĩ mô |
| 12 | `Order Region` | Phân vùng hành chính nhận hàng (*Western Europe, Central America...*) | Danh mục | object | category | Phản ánh tuyến đường vận chuyển |
| 13 | `Order Country` | Quốc gia đích đến nhận hàng | Danh mục | object | category | Đánh giá rào cản hải quan, biên giới |
| 14 | `Order City` | Thành phố nhận hàng | Danh mục | object | category | Đánh giá năng lực giao vận chặng cuối nội đô |
| 15 | `Order State` | Bang/Tỉnh nơi nhận hàng | Danh mục | object | category | Thông tin địa lý chi tiết |
| 16 | `Order Zipcode` | Mã bưu chính của khu vực giao hàng | Mã số | object (nhiễu) | category / float32 | Khuyết >79%, mã bưu cục nhận |

#### Nhóm 3: Kinh Tế Đơn Vị & Tài Chính (Unit Economics & Finance)
| STT | Tên Biến | Ý Nghĩa Thực Tế | Đơn Vị Tính | Kiểu Gốc | Kiểu Chuẩn Hóa | Vai Trò / Ý Nghĩa Nghiệp Vụ |
| :---: | :--- | :--- | :---: | :---: | :---: | :--- |
| 17 | `Sales per customer` | Doanh thu thực nhận sau khi trừ chiết khấu cho khách hàng | USD | object (nhiễu) | float32 | Giá trị dòng tiền thực thu trên đơn hàng |
| 18 | `Benefit per order` | Lợi nhuận ròng thu về trên mỗi đơn hàng | USD | object (nhiễu) | float32 | Đánh giá mức độ sinh lời của đơn hàng |
| 19 | `Sales` | Doanh số gộp ước tính trước chiết khấu | USD | object (nhiễu) | float32 | Tổng giá trị danh nghĩa |
| 20 | `Order Item Quantity` | Số lượng sản phẩm của mục hàng trong đơn | Đơn vị cái | object (nhiễu) | int32 | Quy mô đơn (ảnh hưởng bốc xếp, đóng gói) |
| 21 | `Order Item Discount` | Giá trị chiết khấu bằng tiền cho mục hàng | USD | object (nhiễu) | float32 | Mức độ khuyến mại |
| 22 | `Order Item Discount Rate`| Tỷ lệ chiết khấu áp dụng trên giá niêm yết | Tỷ lệ (0-1) | object (nhiễu) | float32 | Chính sách giá khuyến mại |
| 23 | `Order Item Product Price`| Đơn giá niêm yết tại thời điểm tạo đơn | USD | object (nhiễu) | float32 | Mức giá gốc của sản phẩm |
| 24 | `Order Item Profit Ratio` | Tỷ suất lợi nhuận của mục hàng | Tỷ lệ | object (nhiễu) | float32 | Hiệu quả tài chính đơn vị |
| 25 | `Order Item Total` | Tổng số tiền thanh toán thực tế của mục hàng | USD | object (nhiễu) | float32 | Quy mô thanh toán của mục hàng |
| 26 | `Order Profit Per Order` | Lợi nhuận ghi nhận trên mỗi đơn hàng | USD | object (nhiễu) | float32 | Trùng lặp với `Benefit per order` |

#### Nhóm 4: Phân Khúc & Hồ Sơ Khách Hàng (Customer Demographics)
| STT | Tên Biến | Ý Nghĩa Thực Tế | Đơn Vị Tính | Kiểu Gốc | Kiểu Chuẩn Hóa | Vai Trò / Ý Nghĩa Nghiệp Vụ |
| :---: | :--- | :--- | :---: | :---: | :---: | :--- |
| 27 | `Customer Id` | Mã định danh khách hàng trên hệ thống CRM | Khóa | object (nhiễu) | int32 | Xác định hành vi mua sắm lặp lại |
| 28 | `Customer Segment` | Phân khúc khách hàng (*Consumer, Corporate, Home Office*) | Danh mục | object | category | Phân cấp mức độ ưu tiên khách hàng |
| 29 | `Customer City` | Thành phố cư trú của khách hàng đặt mua | Danh mục | object | category | Nơi khách hàng đăng ký tài khoản |
| 30 | `Customer State` | Bang/Tỉnh cư trú của khách hàng | Danh mục | object | category | Khu vực địa lý người gửi |
| 31 | `Customer Country` | Quốc gia cư trú của khách hàng (*EE. UU., Puerto Rico*) | Danh mục | object | category | Thị trường khởi tạo đơn hàng |
| 32 | `Customer Zipcode` | Mã bưu chính của khách hàng | Mã số | int64 | category / int32 | Vùng địa chỉ gửi hàng |
| 33 | `Latitude` | Tọa độ Vĩ độ của địa chỉ kho/khách hàng gửi | Độ thập phân | object (nhiễu) | float32 | Tính toán khoảng cách không gian (Haversine) |
| 34 | `Longitude` | Tọa độ Kinh độ của địa chỉ kho/khách hàng gửi | Độ thập phân | object (nhiễu) | float32 | Tính toán khoảng cách không gian (Haversine) |

#### Nhóm 5: Danh Mục Sản Phẩm & Kho Bãi (Product Catalog & Warehouse)
| STT | Tên Biến | Ý Nghĩa Thực Tế | Đơn Vị Tính | Kiểu Gốc | Kiểu Chuẩn Hóa | Vai Trò / Ý Nghĩa Nghiệp Vụ |
| :---: | :--- | :--- | :---: | :---: | :---: | :--- |
| 35 | `Order Item Id` | Mã định danh duy nhất của mục hàng giao dịch | Khóa | object (nhiễu) | int32 | **Primary Key** của bảng dữ liệu |
| 36 | `Order Item Cardprod Id` | Mã sản phẩm gắn với mục hàng | Khóa | object (nhiễu) | int32 | Liên kết sang bảng sản phẩm |
| 37 | `Product Card Id` | Mã nhận diện sản phẩm trong danh mục kho | Khóa | object (nhiễu) | int32 | Khóa ngoại xác định sản phẩm |
| 38 | `Product Name` | Tên thương mại của sản phẩm | Chuỗi văn bản | object | category | Phân tích rủi ro theo loại sản phẩm |
| 39 | `Product Price` | Giá bán lẻ niêm yết của sản phẩm | USD | object (nhiễu) | float32 | Phân loại phân khúc giá trị sản phẩm |
| 40 | `Product Status` | Tình trạng sản phẩm trong kho (0: Bình thường) | Nhị phân | object (nhiễu) | int8 | Tình trạng sẵn sàng xuất kho |
| 41 | `Category Id` | Mã danh mục sản phẩm | Khóa | object (nhiễu) | int32 | Nhóm sản phẩm |
| 42 | `Category Name` | Tên nhóm danh mục sản phẩm (*Sporting Goods, Cleats...*) | Danh mục | object | category | Phản ánh đặc tính hàng hóa (kích thước, tính chất) |
| 43 | `Department Id` | Mã phòng ban quản lý ngành hàng | Khóa | object (nhiễu) | int32 | Phòng ban nghiệp vụ |
| 44 | `Department Name` | Tên phòng ban quản lý (*Fitness, Apparel, Fan Shop...*) | Danh mục | object | category | Phân bổ chuỗi cung ứng theo phòng ban |
| 45 | `Product Description` | Mô tả chi tiết kỹ thuật của sản phẩm | Văn bản | object (nhiễu) | category | Khuyết >83%, trường mô tả phụ |
| 46 | `Product Image` | Đường dẫn URL hình ảnh sản phẩm phục vụ hiển thị web | URL | object | category | Không có giá trị phân tích định lượng |

#### Nhóm 6: Quản Trị Dữ Liệu & Thông Tin Định Danh Nhạy Cảm (PII & Data Governance)
| STT | Tên Biến | Ý Nghĩa Thực Tế | Đơn Vị Tính | Kiểu Gốc | Xử Lý Pipeline | Lý Do Quản Trị Dữ Liệu & GDPR |
| :---: | :--- | :--- | :---: | :---: | :---: | :--- |
| 47 | `Customer Email` | Địa chỉ thư điện tử của khách hàng | Chuỗi | object (nhiễu) | **LOẠI BỎ (DROP)** | Thông tin định danh cá nhân (PII) nhạy cảm |
| 48 | `Customer Password` | Mật khẩu truy cập tài khoản của khách hàng | Chuỗi | object (nhiễu) | **LOẠI BỎ (DROP)** | Mật khẩu bảo mật, bắt buộc loại trừ |
| 49 | `Customer Fname` | Tên của khách hàng | Tên riêng | object | Chuẩn hóa / Ẩn danh | PII định danh, không dùng dự báo |
| 50 | `Customer Lname` | Họ và tên đệm của khách hàng | Tên riêng | object | Chuẩn hóa / Ẩn danh | PII định danh, không dùng dự báo |
| 51 | `Customer Street` | Số nhà và tên đường cư trú của khách hàng | Địa chỉ | object | Chuẩn hóa / Ẩn danh | Địa chỉ cư trú cụ thể |
| 52 | `Order Customer Id` | Khóa liên kết khách hàng trong đơn | Khóa | object (nhiễu) | int32 | Trùng lặp hoàn toàn với `Customer Id` |
| 53 | `Product Category Id` | Khóa liên kết danh mục | Khóa | object (nhiễu) | int32 | Trùng lặp hoàn toàn với `Category Id` |

---

## 4. Kiểm Toán Độ Sạch Ban Đầu Của Dữ Liệu (Initial Data Quality Audit)

Qua rà soát chuyên sâu $180,519$ dòng dữ liệu thô của sinh viên Nguyễn Lê Nhật Hạ, nhóm ghi nhận các vấn đề chất lượng dữ liệu nghiêm trọng cần giải quyết:

### 4.1. Kiểm Toán Mức Độ Khuyết Thiếu (Missing Value Audit)
Dữ liệu thô bị khuyết thiếu ở toàn bộ $53$ cột với nhiều mức độ khác nhau:
1. **Nhóm khuyết thiếu cực cao (>70%):**
   - `Product Description`: Thiếu $150,661$ dòng ($83.46\%$).
   - `Order Zipcode`: Thiếu $143,152$ dòng ($79.30\%$).
   - *Giải pháp:* Không dùng làm biến đặc trưng số học; điền nhãn `'Unknown'` / $0$ khi bảo toàn cấu trúc bảng.
2. **Nhóm khuyết thiếu trung bình (15% - 25%):**
   - `Order State` ($24.90\%$), `Category Name` ($24.56\%$), `Order City` ($23.21\%$), `Delivery Status` ($22.41\%$), `Order Country` ($22.39\%$), `Customer Street` ($21.13\%$), `Type` ($20.67\%$), `Days for shipment (scheduled)` ($17.26\%$).
3. **Nhóm khuyết thiếu then chốt đối với bài toán (4% - 15%):**
   - `Days for shipping (real)`: Thiếu $13,544$ dòng ($7.50\%$).
   - `Late_delivery_risk`: Thiếu $8,378$ dòng ($4.64\%$).
   - `Shipping Mode`: Thiếu $5,859$ dòng ($3.25\%$).

### 4.2. Lỗi Dị Thường Nhập Liệu & Nhiễu Chuỗi (String & Ingestion Noise)
1. **Nhiễu đơn vị tiền tệ/khối lượng trong cột số:**
   - Trong biến mục tiêu `Late_delivery_risk` và các cột số tài chính xuất hiện các chuỗi chứa đơn vị: `'1 VND'`, `'1 USD'`, `'1 kg'`, `'1 %'`, `'1 đ'`, `'0 VND'`, `'0 kg'`, `'0 USD'`, `'0 đ'`, `'0 %'`.
2. **Ký hiệu khuyết không chuẩn:**
   - Nhiều trường thay vì để trống hoặc `NaN` lại chứa các ký tự mã hóa lỗi: `'?'`, `'-'`, `'-1'`, `'-1.0'`, `'9999'`, `'chưa rõ'`, `'unknown'`, `'null'`.
3. **Dấu phẩy thập phân kiểu châu Âu:**
   - Hàng loạt cột số thực (`Sales per customer`, `Benefit per order`, `Latitude`, `Longitude`, `Product Price`...) sử dụng dấu phẩy `,` ngăn cách phần thập phân (ví dụ: `12,34` thay vì `12.34`), nếu ép kiểu trực tiếp bằng `pd.to_numeric` sẽ bị biến thành `NaN`.
4. **Lỗi font chữ tiếng Việt và khoảng trắng bất thường:**
   - Xuất hiện chuỗi lỗi bảng mã UTF-8: `'chÆ°a rÃµ'`, `'chæ°a rãµ'`, và lỗi thừa khoảng trắng: `'  Standard Cla'`, `'  Second Class'`.

### 4.3. Kiểm Toán Giá Trị Ngoại Lai (Outlier Audit)
- Biến tài chính (`Benefit per order`, `Order Profit Per Order`): Xuất hiện các giá trị âm sâu (tối đa âm $-425.58\text{ USD}$), phản ánh các đơn hàng doanh nghiệp chịu lỗ nặng do chính sách chiết khấu quá mức hoặc đổi trả hàng. Ngược lại, có những đơn bán sỉ đạt lợi nhuận cực lớn ($>900\text{ USD}$).
- Biến thời gian (`Days for shipping (real)`): Có những trường hợp thời gian giao thực tế kéo dài $6$ ngày (trong khi cam kết tối đa của Standard Class chỉ là $4$ ngày), là nguyên nhân trực tiếp dẫn tới vi phạm SLA.

### 4.4. Cảnh Báo Rò Rỉ Dữ Liệu Nghiêm Trọng (Critical Data Leakage Warning)
- Ba biến số: `Days for shipping (real)`, `Delivery Status`, và `shipping date (DateOrders)` là **những thông tin chỉ được ghi nhận sau khi đơn hàng đã xuất kho và vận chuyển thành công**.
- **Cảnh báo học thuật:** Nếu người xây dựng mô hình đưa 3 biến này vào tập đặc trưng đầu vào ($X$) để dự báo rủi ro trễ hạn tại thời điểm đặt hàng, mô hình sẽ bị rò rỉ dữ liệu 100%, đạt độ chính xác ảo tuyệt đối ($100\%$) nhưng hoàn toàn vô dụng trên thực tế vận hành. Do đó, 3 biến này **bắt buộc phải bị loại khỏi tập biến đầu vào của mô hình Machine Learning**.

---

## 5. Mục Tiêu Phân Tích: Bộ 4 Câu Hỏi Kinh Doanh Cam Kết Trả Lời Bằng Python

Bộ 4 câu hỏi dưới đây được nhóm nghiên cứu thiết kế chuẩn mực theo tư duy Khoa học Dữ liệu ứng dụng trong Chuỗi cung ứng, bao quát từ tầng Khám phá Dữ liệu (Descriptive/Diagnostic), tầng Mô hình hóa Học máy (Predictive) cho đến tầng Ra quyết định Quản trị (Prescriptive):

---

### Câu Hỏi 1 (Về Thuộc Tính & Tương Quan Nghiệp Vụ - Descriptive & Diagnostic Analytics)
> **"Những yếu tố nào (như phương thức vận chuyển Shipping Mode, khu vực giao hàng Order Region, hay số ngày cam kết Days for shipment (scheduled)) có tác động chi phối mạnh nhất đến rủi ro giao hàng chậm trễ?"**

- **Mục tiêu phân tích:**
  - Xác định các "điểm nghẽn" (*bottlenecks*) lớn nhất trong mạng lưới logistics hiện tại của DataCo.
  - Kiểm tra xem rủi ro trễ hạn bắt nguồn từ chính sách cam kết SLA thiếu thực tế (ví dụ: cam kết First Class giao trong 1 ngày trên toàn cầu) hay do rào cản địa lý và thủ tục thông quan tại các thị trường đích.
- **Công cụ & Phương pháp Python cam kết:**
  - Sử dụng `pandas` và `scipy.stats` thực hiện **Kiểm định Chi bình phương ($\chi^2$ test of independence)** đối với các biến phân loại (`Shipping Mode`, `Order Region`, `Market`, `Customer Segment`).
  - Thực hiện **Kiểm định $t$-test / ANOVA** đối với các biến định lượng giữa hai nhóm giao trễ ($1$) và đúng hạn ($0$).
  - Trích xuất hệ số tương quan và chỉ số **Mutual Information / Feature Importance** từ mô hình cây quyết định để xếp hạng mức độ ảnh hưởng của từng thuộc tính.

---

### Câu Hỏi 2 (Về Xử Lý & Khám Phá Dữ Liệu - Data Preprocessing & Exploratory Analysis)
> **"Mức độ mất cân bằng lớp của biến mục tiêu và hiện tượng nhiễu/ngoại lai trong thời gian thực tế ảnh hưởng như thế nào đến chất lượng phân tích?"**

- **Mục tiêu phân tích:**
  - Đánh giá phân phối tự nhiên của biến mục tiêu `Late_delivery_risk` sau khi tái tính toán logic chuẩn SCM: Tỷ lệ trễ hạn đạt **$54.62\%$ (nhãn 1)** so với đúng hạn **$45.38\%$ (nhãn 0)**.
  - Khẳng định bộ dữ liệu có sự cân bằng lớp tự nhiên rất lý tưởng (~$55:45$), không gặp phải tình trạng mất cân bằng cực đoan (*severe class imbalance*), do đó **không cần thiết phải lạm dụng các kỹ thuật sinh mẫu nhân tạo như SMOTE/ADASYN** (vốn có thể tạo ra mẫu ngoại lai phi logic trong dữ liệu dạng bảng).
  - Khảo sát tác động của các giá trị ngoại lai trong thời gian giao hàng thực tế và doanh số tài chính đến độ lệch phân phối (*skewness*).
- **Công cụ & Phương pháp Python cam kết:**
  - Sử dụng `seaborn` và `matplotlib` trực quan hóa biểu đồ phân phối đếm (`countplot`), biểu đồ hộp (`boxplot`) và ma trận tương quan (`heatmap`).
  - Áp dụng phương pháp khoảng tứ phân vị (IQR) và `numpy.clip` / Robust Scaler để kiểm soát ngoại lai mà không làm méo mó bản chất vận hành chuỗi cung ứng.

---

### Câu Hỏi 3 (Về Mô Hình Hóa Học Máy Dự Báo Sớm - Predictive Analytics)
> **"Thuật toán Học máy nào (Logistic Regression, Random Forest Classifier hay XGBoost) mang lại hiệu năng dự báo cao nhất, đặc biệt đối với chỉ số Recall và ROC-AUC nhằm hạn chế tối đa việc bỏ sót đơn trễ?"**

- **Mục tiêu phân tích:**
  - Xây dựng mô hình phân loại dự báo rủi ro giao hàng trễ **ngay tại thời điểm khách hàng vừa chốt tạo đơn hàng** (chỉ sử dụng thông tin khách hàng, sản phẩm, thanh toán và phương thức vận chuyển cam kết).
  - So sánh đối đầu giữa 3 trường phái thuật toán đại diện:
    1. *Mô hình Tuyến tính có điều chuẩn:* Logistic Regression (Baseline, dễ giải thích).
    2. *Mô hình Rừng cây ngẫu nhiên (Bagging):* Random Forest Classifier (ổn định, kháng nhiễu tốt).
    3. *Mô hình Tăng cường độ dốc (Boosting):* XGBoost Classifier (hiệu năng tối ưu trên dữ liệu dạng bảng).
  - **Tiêu chuẩn đánh giá ưu tiên:** Đặt chỉ số **Recall (Độ nhạy trên lớp 1)** và **ROC-AUC** lên hàng đầu. Trong kinh doanh logistics, chi phí của việc bỏ sót một đơn hàng bị trễ (*False Negative* - khách hàng thất vọng, khiếu nại, phạt hợp đồng SLA) tốn kém hơn nhiều so với việc cảnh báo nhầm một đơn hàng đúng hạn (*False Positive* - chỉ tốn thêm một bước kiểm tra điều phối).
- **Công cụ & Phương pháp Python cam kết:**
  - Xây dựng quy trình xử lý khép kín bằng `sklearn.pipeline.Pipeline` và `ColumnTransformer` để triệt tiêu hoàn toàn Data Leakage.
  - Đánh giá chéo phân tầng K-lần (`StratifiedKFold(n_splits=5)`).
  - Tối ưu hóa siêu tham số bằng `GridSearchCV` hoặc `Optuna`.
  - Vẽ đường cong ROC-PR và trích xuất độ quan trọng đặc trưng bằng **SHAP (SHapley Additive exPlanations)** để giải thích cơ chế ra quyết định của mô hình (Explainable AI - XAI).

---

### Câu Hỏi 4 (Về Đề Xuất Quản Trị & Tối Ưu Vận Hành SCM - Prescriptive Analytics)
> **"Doanh nghiệp có thể ứng dụng kết quả dự báo từ mô hình như thế nào để tối ưu hóa quy trình vận chuyển và cải thiện tỷ lệ OTIF?"**

- **Mục tiêu phân tích:**
  - Chuyển hóa xác suất rủi ro dự báo từ mô hình AI thành các hành động điều hành cụ thể tại các phòng ban vận hành:
    1. *Cảnh báo sớm tại tầng OMS/WMS:* Nếu đơn hàng có điểm số rủi ro trễ $>0.7$, hệ thống tự động gắn nhãn "Đơn hàng rủi ro cao", ưu tiên bốc xếp và xuất kho trước trong vòng 2 giờ.
    2. *Tái cấu trúc chính sách SLA (Dynamic SLA):* Chấm dứt chính sách cam kết cứng $1$ ngày của gói First Class đối với các tuyến giao quốc tế vượt đại dương (chuyển sang $2 - 3$ ngày tùy theo khoảng cách địa lý).
    3. *Tối ưu hóa điều phối đối tác vận chuyển 3PL:* Đánh giá lại năng lực của các đơn vị 3PL tại hai thị trường điểm nóng LATAM và Europe, đưa chỉ số OTIF thành điều khoản thưởng/phạt trực tiếp trong hợp đồng dịch vụ logistics.
- **Công cụ & Phương pháp Python cam kết:**
  - Lập bảng ma trận quyết định (*Decision Matrix*) và ngưỡng phân loại tối ưu (*Cost-Benefit Threshold Tuning*) dựa trên hàm chi phí phạt SLA.
  - Phân tích kịch bản mô phỏng (*What-If Simulation*) trên Python để định lượng tỷ lệ đơn hàng cứu vãn thành công và mức chi phí vận tải tiết kiệm được sau khi triển khai hệ thống cảnh báo sớm.
