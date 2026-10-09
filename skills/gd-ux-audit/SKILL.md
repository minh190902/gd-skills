---
name: gd-ux-audit
description: Audit the UX of an existing game screen or flow — clarity mapping, user-flow step count, feedback gaps, affordance, cognitive load, failure types, severity-rated findings (S1–S4) with concrete fixes. Use when the user says a screen is confusing or cluttered, "players don't notice X", "too many taps/clicks", before polishing a screen, or after a playtest reveals hesitation. This skill evaluates and fixes existing UI; for brand-new screens use the project's UI design workflow if it has one.
---

# GD UX Audit

**Lỗi UX là khoảng cách giữa điều người chơi muốn, điều giao diện gợi ý, và điều hệ thống thực sự làm.** Dấu hiệu nhận biết: người chơi phải hỏi "mình có làm X được không?".

Đọc ràng buộc nền tảng trong `PROJECT.md` trước: orientation, cách nhập liệu, kích thước vùng chạm/click tối thiểu, độ dài phiên chơi, metaphor UI và bảng màu.

## Quy trình

### 1. Xác định phạm vi và đọc màn hình
- Màn hình hoặc flow nào? Người chơi vào đây để làm gì, và vào từ đâu?
- Đọc scene/layout và script của màn, theme, sketch, cùng phần đặc tả UI liên quan. Nếu được, hãy chạy game và chụp màn hình: audit trên hình thật tốt hơn đọc code.

### 2. User flow
Liệt kê từng bước Input → Điều hướng → Feedback → Kết quả, từ lúc vào đến lúc xong. Đếm số bước/thao tác. Đánh dấu chỗ người chơi do dự, các nhánh lỗi và cách phục hồi. *Không áp dụng máy móc luật 3-click*: một flow 4 bước rõ ràng tốt hơn 1 click khó hiểu. Hãy đánh giá theo khả năng đoán trước, mức do dự và công sức bỏ ra.

### 3. Clarity mapping
1. Chọn một khoảnh khắc gameplay trên màn này.
2. Liệt kê **mọi tín hiệu**, cả UI lẫn môi trường.
3. Xếp hạng từ quan trọng nhất đến tùy chọn.
4. Tín hiệu quan trọng có nằm gần chỗ người chơi đang tập trung không?
5. Có được nhấn mạnh thêm bằng màu, âm thanh hoặc chuyển động không?
6. Các trạng thái (sẵn sàng, đang hồi chiêu, nguy hiểm, không đủ tài nguyên) có được báo hiệu không?
7. Thông tin thừa đã được bỏ chưa?

### 4. Quét 6 loại lỗi
| Loại | Ví dụ |
|---|---|
| Quá tải nhận thức | Quá nhiều chỉ số trên một thẻ cùng lúc |
| Affordance khó hiểu | Thứ bấm được trông không giống bấm được (không có trạng thái hover/pressed) |
| Lặp lại gây mệt | Phải qua 4 menu để làm một việc |
| Thiếu feedback | Hành động xong mà không có xác nhận rõ ràng |
| Khó điều hướng | Không có đường quay lại, mất ngữ cảnh |
| Chặn nhịp chơi | Popup chặn đúng lúc căng thẳng |

Cũng để ý **nợ UX vô hình**: hệ thống cũ không được cải tiến, UI rối dần khi thêm nội dung, tooltip phải gánh thay cho thiết kế kém.

### 5. Kiểm tra 5 khía cạnh
- **Clarity:** người chơi hiểu mình làm được gì và chuyện gì vừa xảy ra.
- **Control:** input phản hồi nhạy và đoán trước được.
- **Feedback:** mọi hành động đều được xác nhận, mức độ tương xứng với hệ quả.
- **Rhythm:** tôn trọng sự chú ý và độ dài phiên chơi.
- **Emotion:** gợi đúng cảm xúc và fantasy.

Kiểm tra thêm: lỗi có hoàn tác được hoặc ngăn trước được không, và màn hình có dùng được trong điều kiện khó (người chơi mệt, màn hình nhỏ, chơi một tay) không.

### 6. Chấm mức độ và đề xuất sửa
- **S1 Blocker:** người chơi không hoàn thành được mục tiêu, hoặc hiểu sai và mất tài nguyên/tiến độ.
- **S2 Major:** vẫn hoàn thành được nhưng do dự rõ rệt, thao tác sai thường xuyên, hoặc bỏ lỡ thông tin quan trọng.
- **S3 Minor:** vướng nhẹ, chậm, thiếu chăm chút.
- **S4 Polish:** cải thiện cảm giác hoặc thẩm mỹ.

Mỗi phát hiện gồm: vị trí (đường dẫn node/element), mô tả, loại lỗi, mức độ, bằng chứng, **đề xuất sửa cụ thể**, và công sức ước tính. Việc sửa tuân theo chuẩn code/UI của dự án (ghi trong PROJECT.md).

### 7. Đầu ra
Lưu vào `<game_root>/docs/ux/<YYYY-MM-DD>-<screen>.md` theo [templates/ux-report.md](templates/ux-report.md). Khi trình bày: đưa bảng phát hiện xếp theo mức độ trước, rồi top 3 việc nên sửa ngay.

## Checklist nhanh
- [ ] Dùng được mà không cần hướng dẫn?
- [ ] Không có chỗ người chơi do dự hoặc bấm thử lung tung?
- [ ] Feedback tức thì và rõ ràng?
- [ ] UI vẫn ổn khi nội dung tăng gấp 3?
- [ ] Không có popup thừa làm mất sự chú ý?
- [ ] UX củng cố tone, nhịp và fantasy?
- [ ] Icon, màu và bố cục vẫn truyền đạt được mục đích khi bỏ hết chữ?
