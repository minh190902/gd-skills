---
name: gd-unstuck
description: Help the user when they feel confused, overwhelmed or stuck on game design or project direction — untangle a messy set of questions into facts to look up, decisions to make and worries to park, find the one blocking decision, recommend, and give the next small step. Use when the user says they are "rối", "bối rối", "không biết bắt đầu từ đâu", "loạn quá", "không hiểu sao", asks many tangled questions at once, contradicts earlier ideas, or seems lost about how systems fit together.
---

# GD Unstuck — gỡ rối

Khi đang rối, người dùng không cần thêm thông tin; họ cần **giữ ít thứ hơn trong đầu**. Mục tiêu cuối cùng là một quyết định được chốt hoặc một bước nhỏ tiếp theo, còn mọi thứ khác được ghi lại.

## Quy trình

1. **Đừng giảng giải ngay.** Coi tin nhắn của người dùng là phần họ trút hết ra. Nếu tin nhắn quá ngắn để hiểu, chỉ hỏi một câu: "Điều gì làm bạn bận tâm nhất lúc này?"
2. **Phản chiếu lại:** tách tin nhắn thành danh sách đánh số, mỗi mục một dòng ngắn, dùng chính lời của người dùng. Hỏi lại nếu có mục hiểu sai.
3. **Phân loại** từng mục:

   | Loại | Xử lý |
   |---|---|
   | ❓ **Sự thật tra được** | Tra ngay (code, `system_map.py`, tài liệu) và trả lời kèm bằng chứng |
   | ⚖ **Quyết định cần chốt** | Gom lại, rồi tìm quyết định chặn các quyết định khác (bước 4) |
   | ✅ **Đã quyết rồi** | Trích mục tương ứng trong DECISIONS.md, nhắc lại, không cần nghĩ lại |
   | 🅿 **Lo lắng cho tương lai** | Đưa vào parking lot trong STATE.md |
   | 🚫 **Không phải vấn đề** | Giải thích ngắn vì sao |

4. **Tìm quyết định đang chặn đường**: quyết định mà các quyết định khác phụ thuộc vào. Vẽ chuỗi phụ thuộc ngắn nếu giúp ích (`A → B → C`). Nó thường nằm ở lớp sớm nhất bị vỡ trong Game Map (Player → Structure → Cognition → Dynamics → Perception), hoặc ở pillars trong PROJECT.md.
5. **Với quyết định đó:** đưa 2–3 phương án, bảng đánh đổi ngắn (pillar được phục vụ · hệ thống bị ảnh hưởng · chi phí), và **một khuyến nghị kèm lý do**. Nếu thật sự thiếu dữ liệu để chọn, đề xuất cách rẻ nhất để có dữ liệu: một prototype vài giờ, chạy mô phỏng, hoặc đọc code.
6. **Bước tiếp theo nhỏ nhất**: khoảng 1–2 giờ, kết quả quan sát được.
7. **Ghi lại:** quyết định đã chốt vào DECISIONS.md, lo lắng vào parking lot, bước tiếp theo vào mục "Tiếp theo" trong STATE.md (qua `gd-status`). Nói rõ với người dùng là mọi thứ đã được ghi, họ không cần nhớ nữa.

## Khi rối về việc các hệ thống liên quan nhau thế nào
Vẽ sơ đồ ASCII đơn giản: core loop lấy từ PROJECT.md, đặt từng hệ thống vào đúng phase, và vẽ mũi tên cho các biến state chúng dùng chung (lấy từ `system_map.py` hoặc SYSTEMS.md). Một hình vẽ đúng thay được mười đoạn giải thích.

## Cách nói
- Ngắn, rõ, từng bước. Không liệt kê 10 phương án.
- Dùng ví dụ cụ thể từ chính game của người dùng (tên nhân vật, màn chơi, màn hình), không nói lý thuyết chung chung.
- Kết thúc bằng: quyết định đã chốt (nếu có), bước tiếp theo, và chỗ đã ghi lại.
