---
name: gd-feature-audit
description: Audit existing game features/systems for purpose, core-loop fit, overlap, scalability and whether they should be kept, deepened, merged, reworked or cut. Use when the user asks "is feature X worth it", "why does nobody use X", "too many systems", "simplify the game", "review our systems", before a refactor/sprint planning, or after several systems were added in a row. Includes an overlap matrix for systems that affect the same variables.
---

# GD Feature Audit

*"Nếu bỏ nó đi mà không có gì thay đổi, nó là nhiễu."* Mục tiêu: quyết định **Keep / Deepen / Merge / Rework / Cut** cho từng tính năng, dựa trên bằng chứng trong code và tài liệu thiết kế, không dựa vào cảm tính.

## Quy trình

### 1. Xác định phạm vi và thu thập bằng chứng
- Audit một tính năng, hay một cụm (ví dụ: mọi hệ thống chạm vào "tâm trạng" nhân vật)?
- Đọc `PROJECT.md` và `SYSTEMS.md`. Chạy `system_map.py` (thuộc gd-design-review) để biết mỗi hệ thống ghi/đọc biến nào.
- Với mỗi tính năng, tìm: file logic, data/Resource, signal, nơi hiển thị trên UI, hook trong dialogue, có được lưu vào save không, có test không. Ghi đường dẫn đầy đủ.
- Đọc mô tả trong GDD/PRD để biết *ý định*, rồi so với *thực tế* trong code.

### 2. Phân tích 7 bước cho từng tính năng

| Bước | Câu hỏi |
|---|---|
| **Purpose** | Giải quyết vấn đề gì của người chơi? Phục vụ pillar nào? |
| **Core fit** | Gắn vào phase nào của core loop? Có làm thay đổi quyết định của người chơi không? |
| **Mental model** | Người chơi *nghĩ* nó làm gì? Có khớp với thực tế không? Họ có nhìn thấy nó không? |
| **Feedback** | Dùng nó có cảm giác thế nào? Feedback hiện ở đâu? Có chỗ vướng víu không? |
| **Failure modes** | Chuyện gì xảy ra khi nó hỏng, bị lạm dụng, bị bỏ qua, hoặc bị hiểu sai? |
| **Scalability** | Ở cuối game nó còn hữu ích, hay chỉ có ý nghĩa ở đầu game? |
| **System hooks** | Hệ thống nào phụ thuộc vào nó? Bỏ đi thì cái gì hỏng? |

### 3. Dấu hiệu cảnh báo
- Hệ thống cô lập, không nối với hệ thống nào.
- **Chức năng chồng chéo**: nhiều cơ chế cùng giới hạn một thứ.
- **Động cơ mâu thuẫn**: câu chuyện khuyến khích một kiểu hành xử, cơ chế lại thưởng cho kiểu ngược lại (ludonarrative dissonance).
- Người chơi dùng nhiều lúc đầu rồi bỏ.
- Ảnh hưởng lớn nhưng người chơi không nhận ra.
- Tooltip đang phải gánh thay cho thiết kế kém.

### 4. Vòng đời
Giới thiệu (có được dạy một cách có ý nghĩa?) → Phát triển (có sâu thêm, có biến thể?) → Tích hợp (có nối với hệ thống khác?) → Hết vai trò (có vô dụng ở cuối game?). *Tính năng tốt thì scale được, biến đổi được, hoặc rút lui gọn gàng.*

### 5. Ma trận chồng chéo (khi audit từ 2 hệ thống trở lên)
Hàng là hệ thống, cột là **biến hoặc hành vi bị ảnh hưởng** (lấy từ `system_map.py`). Đánh dấu những ô có từ 2 hệ thống trở lên cùng tác động. Với mỗi cột bị trùng:
- Người chơi có phân biệt được nguyên nhân không? Không phân biệt được thì cân nhắc **Merge** (gộp thành một hệ thống nhận nhiều nguồn đầu vào) hoặc **Rework** (tách vai trò rõ ràng).
- Đếm số chỉ số trạng thái mà một màn hình phải hiển thị, rồi đánh giá cognitive load trong ràng buộc nền tảng.

### 6. Kết luận và hành động
Mỗi tính năng nhận một kết luận **Keep / Deepen / Merge / Rework / Cut**, kèm lý do 1–2 câu và bằng chứng (file:line). Mọi kết luận khác Keep phải đi kèm **một hành động viết được thành ticket**: làm gì, ở file nào, đo thành công bằng gì, rủi ro tương thích save. Xếp ưu tiên theo ma trận tác động × công sức.

## Đầu ra
Lưu vào `<game_root>/docs/audits/<YYYY-MM-DD>-<scope>.md` theo [templates/feature-audit.md](templates/feature-audit.md). Khi trình bày, đưa bảng kết luận lên trước, chi tiết sau. **Không tự ý xóa code**: audit chỉ đề xuất. Khi người dùng duyệt thì ghi vào DECISIONS.md, rồi dùng `gd-feature-spec` cho phần rework.

## Checklist cho mỗi tính năng
- [ ] Phục vụ một mục tiêu rõ ràng của người chơi
- [ ] Tích hợp với core loop
- [ ] Scale được, phát triển được, thưởng cho sự thành thạo
- [ ] Người chơi *cảm nhận* được, không chỉ *nhìn thấy*
- [ ] Bỏ đi thì có thứ hỏng (nếu không, nó là nhiễu)
