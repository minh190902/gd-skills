---
name: gd-economy-balance
description: Economy and balance design — resource sources/sinks, currency flow, upkeep and cost tuning, tier/cost curves, unit/enemy stat scaling, "is this too easy/hard/strong", dominant strategies. Use when changing gameplay numbers in data/resources, designing a new currency/cost/reward, reviewing difficulty or power curves, or checking whether the economy matches the design intent in PROJECT.md. Includes economy_sim.py (Monte Carlo economy per stage + ×1.2 curve check).
---

# GD Economy & Balance

Balance là *"làm cho mọi lựa chọn đều đáng được cân nhắc"*: một trạng thái cân bằng động, phụ thuộc vào cảm nhận và thay đổi theo thời gian. Mục tiêu không phải là làm mọi thứ bằng nhau. Đọc `PROJECT.md` để biết ý định thiết kế, ví dụ kinh tế "khắc nghiệt" hay "rộng rãi", vì đó là chuẩn để đánh giá các con số.

## Công cụ
`<skill_dir>` là thư mục chứa skill này.
```bash
python -I <skill_dir>/scripts/economy_sim.py sim <model.json> --runs 2000   # Monte Carlo: nguồn thu → quỹ → khoản chi, theo từng stage
python -I <skill_dir>/scripts/economy_sim.py curve 150 200 250 300 350       # so độ tăng giữa các tier với quy tắc ×1.2
```
Định dạng model: xem docstring của script và [examples/sample_model.json](examples/sample_model.json). Ví dụ đó chỉ để minh họa; **luôn dùng số lấy từ code thật**. Lưu model của dự án vào `<game_root>/docs/balance/` để chạy lại về sau.

## Quy trình

### 1. Xác định câu hỏi balance
Viết thành một câu, ví dụ: "Ở giữa game, người chơi có phải bỏ một khoản chi mỗi màn không?" hoặc "Unit hiếm có luôn tốt hơn 2 unit thường không?". Chọn **loại balance**: toán học, cảm nhận, chiến lược, hay trải nghiệm.

### 2. Lấy số thật từ code, không đoán
Tìm mọi nguồn thu, khoản chi và công thức trong data/Resource và code. Ghi thành bảng **Nguồn thu · Quỹ · Khoản chi · Loại khan hiếm**, mỗi con số kèm file:line. `system_map.py --impact <currency>` (thuộc gd-design-review) liệt kê mọi hệ thống đang thay đổi một loại tiền tệ.

### 3. Mô hình hóa
- **Kinh tế:** viết model JSON rồi chạy `sim`. Đọc 3 chỉ số:
  - `deficit%`: tỉ lệ không trả nổi các khoản bắt buộc.
  - `optional%`: tỉ lệ mua được các khoản chi tùy chọn.
  - Lượng tiền mang sang màn sau (p50).

  Điểm xuất phát cho kiểu kinh tế "khắc nghiệt nhưng công bằng": deficit 5–20% ở màn khó, optional 30–70%, và lượng tiền mang sang không tăng đều qua mọi màn. Đây là chỗ bắt đầu để playtest, không phải chân lý.
- **Đường cong:** chạy `curve` cho mỗi chuỗi tier (phần thưởng, giá, HP, sức mạnh). Quy tắc kinh nghiệm là tăng khoảng ×1.2 mỗi tier. Bước nhảy lớn hơn ×1.3 chỉ nên có khi cố ý (sang chương mới, gặp boss).
- **Sức mạnh và lựa chọn:** viết công thức và bảng tier với các cột giá · sức mạnh · hiệu suất (sức mạnh/giá). Xem [references/balance-math.md](references/balance-math.md) cho diminishing returns, soft cap, nguồn thu/khoản chi, feedback loop.

### 4. Kiểm tra chiến lược thống trị
- **So hai lựa chọn cạnh tranh:** với mỗi lựa chọn, ghi sức mạnh, giới hạn và lối chơi. Có lựa chọn nào gần như bắt buộc phải chọn? Có lựa chọn nào vô dụng?
- Liệt kê các vòng **feedback dương** (giàu càng giàu) và **feedback âm** (cơ chế giúp người chơi bắt kịp). Đánh dấu vòng nào có thể vượt tầm kiểm soát hoặc bị khai thác.
- Ưu tiên cách khắc chế mềm hơn là chặn cứng.

### 5. Đề xuất thay đổi
Lập bảng: Tham số · Giá trị cũ · Giá trị mới · File · Lý do · Kết quả sim trước/sau. Mỗi lần **chỉ đổi một nhóm tham số** để đo được tác động. Chạy lại sim để chứng minh thay đổi đạt mục tiêu. Ghi vào `<game_root>/docs/balance/<YYYY-MM-DD>-<topic>.md`. Thay đổi lớn thì qua `gd-design-review` và ghi vào DECISIONS.md.

### 6. Xác nhận
Số trên bảng tính chỉ là giả thuyết. Cần playtest để xác nhận (`gd-playtest`, nhóm mục tiêu Balance). Nếu công thức thay đổi thì thêm hoặc sửa test.

## Checklist
- [ ] Mọi lựa chọn cốt lõi đều đáng chọn trong *một bối cảnh nào đó*
- [ ] Không có lựa chọn bắt buộc phải chọn
- [ ] Có thể khắc chế bằng kỹ năng hoặc kế hoạch
- [ ] Phần thưởng tương xứng với công sức
- [ ] Vẫn công bằng khi người chơi thất bại (có lối thoát khỏi vòng xoáy thua liên tục)
- [ ] Mỗi nguồn thu có khoản chi tương ứng, tiền mang sang không lạm phát
- [ ] Số liệu lấy từ code, có file:line, và đã chạy lại sim sau khi đổi
- [ ] Monetization không phá pillar: không pay-to-win, tỉ lệ được công khai
