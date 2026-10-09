---
name: gd-status
description: Project compass — know where a game project stands and keep it written down. Use at the START of a work session ("tiếp tục", "hôm nay làm gì", "mình đang ở đâu", "where were we"), at the END of a session or after finishing a task, when switching tasks, when the user asks what's done/next/blocked, or when progress docs look stale compared to git history. Maintains docs/design/STATE.md as the single one-page source of truth.
---

# GD Status — la bàn dự án

Vấn đề cần tránh: sau vài tuần không biết mình đang ở đâu, tài liệu nói một đằng, code một nẻo. Giải pháp là **một trang duy nhất** luôn đúng, `<design_dir>/STATE.md`, cùng với nhật ký quyết định và bản đồ hệ thống. Design dir: xem quy ước trong `gd-core`; nếu chưa có thì thiết lập theo `gd-core` mục 1.

| File | Trả lời câu hỏi | Ai cập nhật |
|---|---|---|
| `STATE.md` | Đang ở đâu, làm gì tiếp, còn gì chưa quyết? (≤ 1 trang) | Skill này, cuối mỗi phiên |
| `DECISIONS.md` | Vì sao game như thế này? | `gd-design-review`, `gd-unstuck` khi chốt quyết định |
| `SYSTEMS.md` | Có những hệ thống nào, hệ thống nào đụng biến nào? | `gd-design-review` sau mỗi thay đổi |
| PROGRESS / CHANGELOG của dự án (nếu có) | Đã làm xong gì (lịch sử) | Lưu trữ khi đóng milestone |

## Đầu phiên — "mình đang ở đâu?"
1. Đọc STATE.md và PROJECT.md.
2. Kiểm tra **độ lệch**: chạy `git log --since=<ngày cập nhật của STATE>` và `git status`. Có commit hay thay đổi nào chưa được ghi trong STATE? Có thay đổi nào nằm ngoài focus hiện tại?
3. Trả lời trong ≤ 8 dòng:
   - **Milestone:** … · **Focus:** …
   - **Lần trước đã làm:** …
   - **Tiếp theo:** (mục đầu tiên trong "Tiếp theo")
   - **Còn chưa quyết:** …
   - **Lệch:** (nếu có)
4. Hỏi người dùng muốn làm mục tiếp theo hay đổi hướng. Nếu đổi hướng, cho ý tưởng mới qua `gd-design-review` trước.

## Cuối phiên / xong một việc
1. Bỏ việc đã xong khỏi "Đang làm". Thêm một dòng vào "Nhật ký phiên": ngày · đã làm gì · commit.
2. Cập nhật "Tiếp theo" (≤ 5, theo ưu tiên), "Câu hỏi mở" và "Parking lot".
3. Có quyết định mới thì ghi vào DECISIONS.md. Hệ thống thay đổi thì chạy `system_map.py` và cập nhật SYSTEMS.md.
4. Giữ STATE ≤ 1 trang: nhật ký phiên chỉ giữ 5 dòng gần nhất, dòng cũ hơn chuyển sang file lịch sử của dự án.
5. Sửa ngày `Cập nhật:` ở đầu file.

## Quy tắc giữ gọn
- **Một milestone tại một thời điểm**, có tiêu chí "xong" kiểm tra được.
- **Đang làm tối đa 2 việc.** Muốn bắt đầu việc thứ 3 thì hoàn thành hoặc hoãn một việc trước.
- **Ý tưởng nảy ra giữa chừng thì không làm ngay**: ghi vào parking lot, qua `gd-design-review` nếu cần đánh giá.
- Khi đóng milestone: rà lại parking lot và cùng người dùng chọn milestone kế tiếp.
- Tài liệu cũ mâu thuẫn với STATE thì STATE thắng; ghi chú lại độ lệch để dọn sau.
