---
name: gd-feature-spec
description: Write a buildable design spec for a new game feature, mechanic or system BEFORE implementing it (Intention → Functionality → Parameters, state table, edge cases, dependencies, KPIs, validation plan). Use when the user asks to add/design/plan a feature, start a new sprint item, "làm tính năng X", "thêm hệ thống Y", or when a request to code a gameplay feature has no spec yet. Produces a spec file under docs/specs that maps to data resources and code.
---

# GD Feature Spec

Mục tiêu: một spec mà **dev implement không phải hỏi lại, designer phản biện được, QA test được các edge case**. Đừng viết thành tiểu thuyết: khoảng 1 trang là đủ cho prototype, viết đầy đủ khi hệ thống đã ổn định.

## Quy trình

### 0. Thu thập bối cảnh (bắt buộc)
- Đọc `PROJECT.md` và `SYSTEMS.md` trong design dir (quy ước ở `gd-core`).
- Ý tưởng đã qua `gd-design-review` chưa? Chưa thì chạy review trước.
- Grep code và data liên quan: đã có hệ thống nào làm việc tương tự chưa? **Nếu một hệ thống hiện có đã đáp ứng khoảng 70% nhu cầu, đề xuất mở rộng nó thay vì thêm mới.**
- Đọc GDD/PRD liên quan (vị trí ghi trong PROJECT.md).

### 1. Intention (vì sao tồn tại)
- **Vấn đề của người chơi** mà tính năng giải quyết (need/gap nào trong Game Map)? Vì sao làm *bây giờ*?
- **Pillar** mà nó phục vụ (ít nhất 1; không có thì dừng lại và báo là scope creep).
- **Trải nghiệm mong muốn** trong 1 câu, và **hành vi** muốn khơi gợi.
- **Kiểm tra fantasy:** tính năng làm player fantasy trong PROJECT.md mạnh hơn hay yếu đi?

### 2. Functionality (hoạt động thế nào)
- **Interaction loop** dạng `Action → Feedback → Gain/Spend/Unlock`, nối ra meta loop.
- **Feature block** cho mỗi hành động: *Goal · Conditions · Player input · System response · Edge cases*.
- **Bảng state:** `Input → Required state → Result`. Từ 3 trạng thái trở lên thì dùng FSM, ghi entry/exit và cue cho mỗi lần chuyển. Tránh nhiều boolean chồng nhau.
- **Action logic** theo thứ tự: kiểm tra điều kiện → áp kết quả → cập nhật state → phát event/signal → nối sang bước tiếp hoặc cooldown.
- **Feedback** ở 3 mức (nhỏ / chuẩn / lớn), mạnh yếu tương xứng với hệ quả, và hiển thị ở đâu trên màn hình.
- **Điều kiện thất bại**, và cách thất bại dạy người chơi điều gì thay vì phạt vô cớ.
- **Độ minh bạch của luật:** người chơi thấy được gì, cái gì được giấu có chủ đích.

### 3. Parameters (con số)
Bảng tham số gồm: giá trị khởi đầu, đơn vị, phạm vi hợp lệ, và **chỗ đặt trong code/data** (Resource, config). Không hard-code số trong logic. Với tham số tăng theo tier, lấy quy tắc ×1.2/tier làm điểm xuất phát (xem `gd-economy-balance`).

### 4. Dependencies & rủi ro
- Bảng **Hệ thống · Kiểu thay đổi · Mức rủi ro**: signal/event mới, save/load, dialogue, UI.
- Chạy `system_map.py --impact` (thuộc gd-design-review) cho từng biến state bị chạm, và **ghi danh sách reader bị ảnh hưởng vào spec**.
- **Save/Load:** state nào cần lưu lâu dài phải được serialize, kèm migration cho save cũ.
- **Hook cho narrative:** flag hoặc hàm cầu nối để dialogue phản ứng với tính năng.
- **Ý định và tác động thực tế:** người chơi có thể tối ưu hóa làm mất ý đồ thiết kế bằng cách nào?

### 5. Validation
- **KPI / tín hiệu:** đo được, liên quan, có thời hạn. Nếu chưa có telemetry thì dùng quan sát playtest và unit test cho logic.
- **Giả thuyết · Cách kiểm tra · Ngưỡng · Phương án dự phòng.**
- **Kế hoạch iteration:** v0.1 (prototype thô, chứng minh cảm giác) → v0.3 → v0.6 → v1.0.
- **Test case cần viết**, ít nhất một test cho mỗi edge case.

### 6. Ghi file và bàn giao
- Lưu vào `<game_root>/docs/specs/<feature-kebab>.md` theo [templates/feature-spec.md](templates/feature-spec.md). Changelog đặt ở đầu file, gắn tag `WIP`/`Final`, có mục "Open questions".
- Kết thúc bằng **danh sách task implement** theo chuẩn code của dự án (ghi trong PROJECT.md), rồi hỏi người dùng có muốn bắt đầu không.

## Checklist chất lượng
- [ ] Giải quyết một vấn đề đã được định nghĩa, gắn với pillar
- [ ] Intention, Functionality và Parameters tách riêng
- [ ] Mọi input đều có output và feedback; edge case đã được xử lý (spam, thiếu tài nguyên, đối tượng bị xóa giữa chừng, save/load giữa chừng)
- [ ] Không trùng chức năng với hệ thống hiện có, hoặc có giải thích vì sao
- [ ] Các reader của state dùng chung đã được liệt kê và kiểm tra
- [ ] Tham số nằm trong data/config và có phạm vi hợp lệ
- [ ] Đã đánh giá ảnh hưởng tới UX (cognitive load trên nền tảng), economy và balance
- [ ] Có kế hoạch validation và kế hoạch iteration
- [ ] Dev implement được mà không phải hỏi; QA viết được test

**Mẹo:** dùng chính spec làm prompt để sinh code. Nếu code sinh ra phải sửa nhiều, spec còn thiếu.
