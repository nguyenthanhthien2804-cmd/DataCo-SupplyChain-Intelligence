---
name: nhat-ky-lam-viec
description: Tự động ghi chép, cập nhật và khôi phục ngữ cảnh làm việc qua các phiên trong tệp '00_nhật ký làm việc.md' tại thư mục gốc của dự án. Kích hoạt khi bắt đầu phiên mới, khi hoàn thành tác vụ/tạo file quan trọng, hoặc khi người dùng yêu cầu tổng kết/lưu nhật ký.
---
 
<!--
Author: N.Lê.Nhật.Hạ
Description: Antigravity Skill for Cross-Session Project Worklog Management (Windows & Linux compatible)
-->
 
# Session Worklog Manager (Nhật Ký Làm Việc Dự Án)
 
Kỹ năng này giúp duy trì bộ nhớ dài hạn, tính liên tục và lưu vết toàn bộ tiến trình công việc giữa các phiên làm việc độc lập. Tệp nhật ký mặc định duy nhất là `00_nhật ký làm việc.md` đặt tại thư mục gốc của workspace.
 
---
 
## 1. Nguyên Tắc Cốt Lõi (Core Principles)
 
1. **Phạm vi tệp mục tiêu:** Chỉ ghi vào `./00_nhật ký làm việc.md` tại thư mục gốc của dự án (tuyệt đối không nhầm lẫn với cac file khac).
2. **Thứ tự thời gian đảo ngược:** Mục mới nhất **luôn được chèn lên trên cùng** (ngay bên dưới tiêu đề chính và dòng phân cách ngang `---` đầu tiên).
3. **Tiết kiệm Token & Ngữ cảnh (Context Efficiency):** Khi khôi phục ngữ cảnh đầu phiên, chỉ đọc tiêu đề và **3–5 phiên gần nhất** (3–5 khối `## [YYYY-MM-DD ...]`) để tránh làm tràn bộ nhớ ngữ cảnh.
4. **Tiêu chí ghi log:** Cập nhật nhật ký khi:
   - Hoàn thành một tính năng, giải quyết xong một milestone/task cụ thể.
   - Tạo mới hoặc sửa đổi các tệp mã nguồn, tài liệu, bài tập, slide quan trọng.
   - Người dùng yêu cầu rõ ràng (*"lưu nhật ký"*, *"tổng kết phiên"*, *"cập nhật worklog"*, *"kết thúc phiên"*).
   - *Không ghi log cho các câu hỏi tra cứu, giải thích ngắn hoặc thao tác đọc thử một file.*
5. **Tương thích Đa nền tảng (Cross-Platform):** Nhận diện rõ thiết bị đang thực thi (`Windows` hoặc `Linux`), sử dụng đường dẫn markdown link đúng theo hệ điều hành hiện tại `[tên_file](file:///đường_dẫn)`.
6. **Chuẩn Typography Tiếng Việt & Markdown:**
   - Dấu câu dính liền ký tự trước nó, có đúng 1 khoảng trắng sau nó.
   - Bắt buộc có dòng trắng rỗng (blank line) trước và sau mọi danh sách gạch đầu dòng (`-`) hoặc đánh số (`1.`).
   - Viết hoa chuẩn tên công nghệ (*Python, NumPy, Pandas, Matplotlib, Quarto, Antigravity IDE...*).
 
---
 
## 2. Quy Trình Thực Thi (Execution Workflow)
 
### A. Khôi Phục Ngữ Cảnh Đầu Phiên (Session Startup / Context Recovery)
 
1. Kiểm tra sự tồn tại của tệp `00_nhật ký làm việc.md` tại thư mục gốc của workspace.
2. Nếu tệp tồn tại:
   - Đọc phần Header và **3–5 phiên gần nhất**.
   - Chạy lệnh đồng bộ Google Drive (nếu được cấu hình).
   - Tóm tắt ngắn gọn và chủ động cho người dùng:
     > *"✅ Đã khôi phục ngữ cảnh làm việc. Phiên trước ([YYYY-MM-DD]) chúng ta đã hoàn thành [Tóm tắt việc đã làm]. Bước tiếp theo dự kiến là [Bước tiếp theo]. Sẵn sàng bắt đầu!"*
3. Nếu tệp chưa tồn tại: Khởi tạo tệp theo Mẫu Cấu trúc Chuẩn (Template) bên dưới khi kết thúc tác vụ lớn đầu tiên.
 
---
 
### B. Ghi Nhận Cuối Phiên / Hoàn Tất Tác Vụ (Session Wrap-up)
 
1. Lấy thời gian hiện tại (`YYYY-MM-DD HH:MM`) và nhận diện hệ điều hành (`Windows` hoặc `Linux`).
2. Tổng hợp ngắn gọn, súc tích nội dung phiên làm việc:
   - **Môi trường:** `Windows` (hoặc `Linux`).
   - **Mục tiêu phiên:** Yêu cầu hoặc bài toán cần giải quyết.
   - **Nội dung đã hoàn thành:** Các chức năng đã code, các file đã tạo mới/thay đổi (kèm link Markdown `[tên_file](file:///đường_dẫn)`).
   - **Quyết định kỹ thuật:** Kiến trúc, thư viện, lưu ý sư phạm hoặc quy ước cần nhớ.
   - **Tồn đọng & Bước tiếp theo:** 2–3 đầu việc ưu tiên cho phiên kế tiếp.
3. Chèn khối nhật ký mới vào ngay bên dưới đường phân cách `---` đầu tiên của `00_nhật ký làm việc.md`.
 
---
 
## 3. Mẫu Cấu Trúc Chuẩn (Template)
 
```markdown
# Nhật ký Làm việc Dự án
 
Tệp này tự động lưu vết các phiên làm việc giữa Người dùng và Antigravity IDE.  
*Tác giả cấu hình:* N.Lê.Nhật.Hạ
  
---
 
## [YYYY-MM-DD HH:MM] - [Tiêu đề Tóm tắt Công việc]
- **Môi trường:** Windows (hoặc Linux)
- **Mục tiêu phiên:** Mô tả ngắn gọn mục tiêu chính của phiên làm việc.
- **Nội dung đã hoàn thành:**
  - Mô tả chi tiết việc đã làm, tệp đã sửa đổi kèm link Markdown `[file_name](file:///path)`.
- **Quyết định kỹ thuật:** Các lưu ý hoặc quyết định quan trọng cần nhớ.
- **Tồn đọng & Bước tiếp theo:** 2–3 việc ưu tiên cho phiên kế tiếp.
 
---
```
 
---
 
## 4. Quản Lý Lưu Trữ (Archive Management)
 
- Khi tệp `00_nhật ký làm việc.md` vượt quá **30–50 phiên**, chủ động đề xuất chuyển các phiên cũ vào `docs/history_worklog.md` và chỉ giữ lại 10 phiên gần nhất trong tệp chính để tối ưu hóa hiệu năng và dung lượng.