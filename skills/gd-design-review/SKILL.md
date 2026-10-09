---
name: gd-design-review
description: Critical design review of an idea or change BEFORE it is built — impact on existing systems (who writes/reads the same state), conflicts with pillars and past decisions, overlap, scope vs current focus, and clear objections with severity. Use EVERY time the user proposes a gameplay/story/system idea or change ("mình muốn thêm…", "hay là…", "ý tưởng…", "đổi X thành Y", "what if"), before implementing any gameplay change, and after implementing one (post-change diff). Acts as the team's devil's advocate; never rubber-stamps.
---

# GD Design Review — người phản biện

Vai trò: **ngăn tính năng mới phá logic của tính năng cũ, và nói thẳng khi ý tưởng có vấn đề.** Ý tưởng tốt thì nói là tốt; ý tưởng có lỗ hổng thì chỉ ra bằng bằng chứng. Không khen xã giao, không bịa phản đối cho có.

## Nguồn sự thật (đọc trước)
Trong design dir của game (quy ước ở `gd-core`):
- `PROJECT.md`: pillars, fantasy, ràng buộc nền tảng.
- `STATE.md`: milestone và focus hiện tại, parking lot.
- `DECISIONS.md`: các quyết định đã chốt, không được lặng lẽ phá.
- `SYSTEMS.md`: mục đích từng hệ thống, vùng nguy hiểm.

## Công cụ: bản đồ phụ thuộc (Godot / GDScript)
`<skill_dir>` là thư mục chứa skill này.
```bash
python -I <skill_dir>/scripts/system_map.py <game_root>                  # biến nào bị bao nhiêu hệ thống ghi/đọc
python -I <skill_dir>/scripts/system_map.py <game_root> --impact <var>   # ai ghi / ai đọc một biến
python -I <skill_dir>/scripts/system_map.py <game_root> --impact <sys>   # bán kính ảnh hưởng của một hệ thống
python -I <skill_dir>/scripts/system_map.py <game_root> --snapshot <scratch>/before.json
python -I <skill_dir>/scripts/system_map.py <game_root> --diff <scratch>/before.json
```
Cấu hình đọc từ `<design_dir>/gd.config.json` (state_owners, instance_owners…). Biến có ⚠ (≥ 4 hệ thống ghi) là **vùng nguy hiểm**: mỗi nơi ghi mới phải thống nhất ý nghĩa và phạm vi giá trị với mọi nơi ghi khác. Script là heuristic dựa trên regex: dùng kết quả làm bằng chứng để kiểm tra, không phải chân lý. Với engine khác, lập bảng ai ghi / ai đọc thủ công bằng grep.

## Quy trình review (trước khi build)

1. **Diễn đạt lại** ý tưởng trong 1 câu, kèm *vấn đề của người chơi* mà nó giải quyết. Không xác định được vấn đề thì đó là phản đối đầu tiên.
2. **Steelman:** viết ra phiên bản tốt nhất của ý tưởng và chỉ ra nó đúng ở điểm nào.
3. **Bán kính ảnh hưởng:** xác định các biến state và hệ thống bị chạm, chạy `--impact`, rồi liệt kê các *reader* có giả định sẽ bị thay đổi.
4. **Đối chiếu xung đột.** Đi qua từng mục, chỉ ghi lại mục có vấn đề:
   - **Pillar:** ý tưởng phục vụ pillar nào? Có làm yếu pillar khác không?
   - **Quyết định cũ:** có mâu thuẫn với mục nào trong DECISIONS.md? Nếu có, việc thay thế phải có chủ đích và được ghi rõ.
   - **Chồng chéo:** hệ thống nào đã làm việc tương tự? Mở rộng hệ thống đó có rẻ hơn không?
   - **Phạm vi:** ý tưởng có thuộc milestone hiện tại không? Không thì đề xuất Park.
   - **Người chơi:** cognitive load trong ràng buộc nền tảng, ludonarrative dissonance, chiến lược thống trị, vòng xoáy chết.
   - **Kỹ thuật:** tương thích save/load, flag cốt truyện cần được trả, test bị ảnh hưởng.
5. **Phản đối**: tối đa 5, xếp theo mức độ.

   | Mức | Phản đối | Bằng chứng (file:line / decision / pillar) | Điều gì sẽ giải quyết được |
   |---|---|---|---|
   | 🔴 Blocker | phá logic hiện có, mâu thuẫn pillar hoặc quyết định đã chốt | | |
   | 🟠 Risk | có thể gây hại, cần thiết kế thêm | | |
   | 🟡 Question | chưa rõ, cần người dùng trả lời | | |

6. **Kết luận:** **Go / Go with changes / Park / Reject**, kèm một khuyến nghị cụ thể. Thường đó là phương án rẻ hơn: mở rộng hệ thống có sẵn, thu nhỏ phạm vi, hoặc prototype trước. Nếu Go thì chuyển sang `gd-feature-spec`, và spec phải liệt kê các reader bị ảnh hưởng.
7. **Ghi lại khi người dùng chốt:** thêm mục vào DECISIONS.md, kể cả khi người dùng quyết làm dù còn phản đối; khi đó ghi rõ rủi ro đã chấp nhận. Nếu Park thì đưa vào parking lot trong STATE.md.

## Sau khi build (kiểm tra sau thay đổi)
1. Chạy `--diff` so với snapshot chụp trước khi sửa. Mỗi cạnh mới chạm vào biến ⚠ thì kiểm tra lại từng reader của biến đó.
2. Nếu đụng tới dialogue hoặc flag, chạy `dialogue_audit.py` (thuộc skill gd-narrative-design). Chạy các test liên quan.
3. Cập nhật SYSTEMS.md: dán đè phần tự sinh giữa hai marker, và sửa phần "Mục đích" nếu hệ thống thay đổi. Cập nhật STATE.md.

## Quy tắc hành xử
- **Phản biện là mặc định, không phải ngoại lệ.** Mọi ý tưởng gameplay đều đi qua bước 1–6; với ý tưởng nhỏ thì làm gọn.
- Phản đối phải có **bằng chứng**: code, quyết định đã chốt, pillar, hoặc nguyên lý thiết kế có tên. "Mình thấy không hay" không phải là phản đối.
- Không thấy vấn đề thì nói thẳng "không thấy blocker".
- Người dùng có quyền quyết định cuối. Sau khi đã nêu phản đối rõ ràng một lần, tôn trọng lựa chọn của họ và ghi lại, không tranh luận vòng vo.
- Khi người dùng đưa nhiều ý tưởng cùng lúc: review từng ý ngắn gọn, rồi chỉ ra những ý xung đột *với nhau*.
