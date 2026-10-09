---
name: gd-narrative-design
description: Narrative design for branching, consequence-driven games — choice & consequence tables, flag payoff audits, character arcs, chapter/quest structure, ludonarrative and agency checks. Use when writing or reviewing dialogue, adding choices, planning story or character arcs, checking "do our choices matter", designing quests/events, or before/after editing .dialogue files. Includes dialogue_audit.py for Godot Nathan Hoad Dialogue Manager (unused flags, unreachable branches, broken jumps, orphan titles).
---

# GD Narrative Design

Narrative design là *cách* câu chuyện được truyền tải qua hệ thống: flag, hệ quả, gameplay, UI. Scriptwriting là *nội dung* được kể. Skill này phụ trách phần đầu và kiểm soát chất lượng phần sau. Đọc `PROJECT.md` để biết các pillar liên quan tới câu chuyện và fantasy của người chơi.

## Công cụ: audit tĩnh (Godot + Dialogue Manager)
`<skill_dir>` là thư mục chứa skill này.
```bash
python -I <skill_dir>/scripts/dialogue_audit.py <game_root>                 # toàn bộ
python -I <skill_dir>/scripts/dialogue_audit.py <game_root> --stage stage_3 # bảng choice của các file có tên chứa "stage_3"
python -I <skill_dir>/scripts/dialogue_audit.py <game_root> --json          # để xử lý tiếp
```
Báo cáo gồm:
- Flag được set nhưng không chỗ nào đọc: hệ quả chưa bao giờ được trả, có thể là *choice illusion*.
- Flag được đọc nhưng không chỗ nào set: nhánh không tới được, hoặc gõ sai tên.
- Jump tới title không tồn tại.
- Title không có đường nào dẫn tới.
- Lựa chọn không có hệ quả gì.
- Bảng lựa chọn và hệ quả.

Tên hàm set/check flag lấy từ `gd.config.json` (`flag_set_fns`, `flag_read_fns`). Flag dựng bằng format string thì phải kiểm tra bằng tay. Với công cụ narrative khác (ink, Yarn…), lập bảng tương tự bằng grep.

**Chạy audit trước và sau mỗi lần sửa dialogue.** Không báo "xong" khi còn jump hỏng hoặc phát sinh flag được đọc mà không được set.

## Quy trình A — Viết hoặc mở rộng một chương / màn

1. **Bối cảnh:** đọc nội dung chương trước, các entry point mà code gọi tới, và kết quả audit để biết flag nào từ trước *đang chờ được trả*.
2. **Beat sheet:** Setup → Tension → Twist → Resolution, gắn với các phase của core loop. Ghi cảm xúc mục tiêu ở đầu, giữa và cuối, kèm **một beat cảm xúc thấp** làm khoảng thở.
3. **Lựa chọn chính.** Thiết kế bằng bảng *trước khi viết lời thoại*:

   | Moment | Option | Kết quả cơ học (ngay) | Kết quả truyện (ngay) | Payoff về sau (chương, title) |
   |---|---|---|---|---|

   - Mỗi option phải khác nhau về *hành trình*, không chỉ khác câu chữ. Mỗi option cần ít nhất một hệ quả cơ học, hoặc một payoff về sau đã lên lịch.
   - **Mỗi flag mới phải có ít nhất một chỗ đọc đã lên kế hoạch** (ghi ở cột Payoff). Không có thì bỏ flag, hoặc chuyển nó thành hệ quả tức thời.
   - Option có điều kiện (dựa trên lịch sử của người chơi) là phần thưởng cho những gì họ đã làm. Hãy dùng nhiều, vì nó làm các quyết định cũ có trọng lượng.
   - Ghi trước con số thay đổi trên nhãn option chỉ khi muốn người chơi chọn theo số. Với lựa chọn đạo đức thuần túy, cân nhắc ẩn số đi.
   - Tránh option "đúng hiển nhiên". Một dilemma tốt là khi lựa chọn nào cũng mất một thứ người chơi quý.
4. **Trả nợ payoff:** với mỗi flag cũ có liên quan, viết ít nhất một phản ứng: một dòng thoại có điều kiện, một option có điều kiện, một thay đổi trong gameplay, hoặc một biến thể epilogue.
5. **Viết dialogue** theo quy ước có sẵn của dự án, giữ giọng nhân vật nhất quán với arc của họ.
6. **Audit và sửa:** chạy script, sửa jump hỏng và flag mồ côi, dán bảng lựa chọn và hệ quả vào tài liệu thiết kế của chương.
7. **Tích hợp hệ thống:** hệ quả có cần hook ngoài dialogue không? Nếu cần thêm hệ thống mới thì dùng `gd-design-review` rồi `gd-feature-spec`.

## Quy trình B — Audit "lựa chọn của người chơi có quan trọng không?"

1. Chạy audit toàn bộ. Nhóm các flag set mà không đọc theo chương và theo nhân vật/arc.
2. Phân loại từng flag:
   - **(a) cần payoff:** lựa chọn lớn mà người chơi sẽ nhớ.
   - **(b) chỉ để log/thống kê:** ghi chú rõ, có thể dùng cho epilogue.
   - **(c) rác:** xóa.
3. Với nhóm (a), đề xuất payoff cụ thể: chương nào, title nào, dạng gì. Ưu tiên payoff rẻ như một dòng thoại có điều kiện, một option có điều kiện, hoặc một biến thể epilogue.
4. Kiểm tra 4 lớp của Thomas Grip cho từng chương (bảng ở [references/narrative-checklists.md](references/narrative-checklists.md)).
5. Đầu ra: `<game_root>/docs/narrative/<YYYY-MM-DD>-consequence-audit.md`, với bảng flag → loại → payoff đề xuất → ticket.

## Quy trình C — Arc nhân vật / quest

Dùng bảng Character Arc và checklist quest trong [references/narrative-checklists.md](references/narrative-checklists.md). Nếu nhân vật có thể chết hoặc vắng mặt, luôn viết **nhánh thay thế** cho mọi beat quan trọng của nhân vật đó.

## Kiểm tra bắt buộc trước khi giao
- [ ] Audit sạch: không có jump hỏng, không có flag mới bị đọc mà không được set
- [ ] Mỗi flag mới có payoff được ghi lại
- [ ] Không có ludonarrative dissonance: cơ chế thưởng đúng điều câu chuyện đề cao, hoặc sự lệch là có chủ đích
- [ ] Mục tiêu của người chơi khớp với mục tiêu của nhân vật; nếu người chơi biết khác nhân vật thì sự chênh lệch đó là có chủ đích
- [ ] Có beat cảm xúc thấp, không phải khoảnh khắc nào cũng cao trào
- [ ] Mỗi mảnh lore có ngữ cảnh trong thế giới game và có thể bỏ qua
- [ ] Đã xử lý trường hợp nhân vật vắng mặt hoặc đã chết
- [ ] Text sẵn sàng cho localization (không ghép chuỗi trong code)
