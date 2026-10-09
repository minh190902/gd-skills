---
name: gd-core
description: Game design lens, project setup and router for the gd-* skills. Use whenever a request involves game design thinking rather than pure coding — brainstorming a mechanic or system, "should we add X", "why is this not fun", choosing between design options, defining pillars or the core loop, writing a 1-pager/concept — and when a game has no docs/design/PROJECT.md yet (set it up). Routes to gd-status, gd-design-review, gd-unstuck, gd-feature-spec, gd-feature-audit, gd-narrative-design, gd-economy-balance, gd-pacing-progression, gd-ux-audit, gd-playtest, gd-game-analysis.
---

# GD Core — lăng kính thiết kế, thiết lập dự án, định tuyến

Nền tảng chung cho mọi skill `gd-*`. Dựa trên mô hình **Game Map** của gamedesign.guide (xem [SOURCES.md](SOURCES.md)).

## 1. Quy ước dự án (mọi skill gd-* đều dựa vào)

Mỗi game có một **design dir**: `<game_root>/docs/design/` (game_root = thư mục chứa `project.godot`, hoặc gốc của game với engine khác).

| File | Vai trò |
|---|---|
| `PROJECT.md` | Định danh, fantasy, pillars, core loop, ràng buộc nền tảng, vị trí dữ liệu, rủi ro đã biết. **Đọc trước khi đưa bất kỳ ý kiến thiết kế nào.** |
| `STATE.md` | Đang ở đâu, làm gì tiếp, câu hỏi mở, parking lot (`gd-status`) |
| `DECISIONS.md` | Quyết định đã chốt và lý do (`gd-design-review`, `gd-unstuck`) |
| `SYSTEMS.md` | Mục đích từng hệ thống + bản đồ ai ghi/đọc state (`gd-design-review`) |
| `gd.config.json` | Cấu hình cho các script (state owners, hàm flag…) |

Tài liệu đầu ra của các skill nằm cạnh design dir: `<game_root>/docs/{specs,audits,narrative,balance,ux,playtest,analysis}/`.

**Tìm design dir:** tìm `**/docs/design/PROJECT.md`. Có nhiều game (monorepo) thì chọn game ứng với file/thư mục đang bàn; chưa rõ thì hỏi.

**Chưa có design dir → thiết lập:**
1. Tạo `<game_root>/docs/design/`, rồi chép các file trong [templates/project/](templates/project/) vào đó (bỏ `CLAUDE.snippet.md`). Không ghi đè file đã có.
2. Điền `PROJECT.md` từ GDD/README/code. Chỗ nào chưa có thông tin thì để "TODO — hỏi người dùng", không bịa.
3. Chỉnh `gd.config.json` theo code thật: state owners (autoload giữ state), instance owners (Resource như HeroData), tên hàm set/check flag.
4. Chạy `system_map.py` (thuộc gd-design-review) để điền phần tự sinh của SYSTEMS.md. Viết phần "Mục đích" từ comment đầu mỗi file.
5. Điền STATE.md từ `git log` gần đây và các TODO hiện có.
6. Đề nghị thêm `templates/project/CLAUDE.snippet.md` vào CLAUDE.md của repo (thay `{{DESIGN_DIR}}`) để các quy tắc luôn được áp dụng.

## 2. Định tuyến

| Người dùng muốn… | Dùng |
|---|---|
| Bắt đầu/kết thúc phiên, "đang ở đâu", "làm gì tiếp" | `gd-status` |
| Đưa ý tưởng, đổi gameplay / cốt truyện / hệ thống | `gd-design-review` (**luôn chạy trước khi build**) |
| Đang rối, quá nhiều câu hỏi, không biết bắt đầu từ đâu | `gd-unstuck` |
| Thiết kế tính năng mới trước khi code | `gd-feature-spec` |
| Đánh giá tính năng đã có: giữ, gộp hay cắt | `gd-feature-audit` |
| Cốt truyện, lựa chọn & hệ quả, dialogue, quest | `gd-narrative-design` |
| Tiền tệ, giá, phần thưởng, chỉ số, độ khó theo con số | `gd-economy-balance` |
| Nhịp độ, thứ tự mở khóa, tutorial/FTUE, đường cong độ khó | `gd-pacing-progression` |
| Màn hình/flow khó hiểu, rối, thiếu feedback | `gd-ux-audit` |
| Lên kế hoạch test, xử lý feedback | `gd-playtest` |
| Phân tích game tham khảo / đối thủ | `gd-game-analysis` |
| Câu hỏi thiết kế mở, chưa rõ thuộc loại nào | Tiếp tục với skill này (mục 3–5) |

Chuỗi điển hình: design-review → feature-spec → economy-balance → playtest → status.

## 3. Game Map — 5 lớp để suy nghĩ về bất kỳ vấn đề nào

| Lớp | Câu hỏi | Thành phần |
|---|---|---|
| **Player** | Vì sao người chơi hành động? | Context → Need → Conflict/Gap → Motivation → Intention → Behavior; cognitive load, flow, frustration |
| **Structure** | Điều gì là có thể? | Rules, game objects, mechanics (Input→State→Action logic→Output), goals/challenges/rewards |
| **Cognition** | Người chơi có hiểu và hành động được không? | UX, UI, clarity mapping, affordance, tutorial |
| **Dynamics** | Hệ thống vận hành thế nào theo thời gian? | Core / meta / emergent loop; regulators: progression, complexity curve, pacing, balance |
| **Perception** | Hệ thống được *cảm nhận* thế nào? | Setting, theme, narrative, game feel, emotion arc, player fantasy, feedback |

Chi tiết các lớp, mô hình động lực (SDT, Quantic Foundry, Flow, B=MAP) và các loại gap: [references/game-map.md](references/game-map.md).

**Chẩn đoán:** đi từ Player tới Perception, tìm lớp *đầu tiên* bị vỡ và sửa ở lớp đó. Đừng sửa lỗi Cognition bằng cách thêm hệ thống mới (lớp Structure).

## 4. Năm câu hỏi cho mọi đề xuất

1. Need/motivation nào của người chơi được gắn vào cơ chế cụ thể nào?
2. Rules, goals và rewards có khớp vào nhau không?
3. UX/UI có giữ cognitive load thấp, trong ràng buộc nền tảng ở PROJECT.md, không?
4. Loop và các regulator có điều chỉnh được nhịp thử thách và độ sâu không?
5. Phần trình bày có khuếch đại cảm xúc và player fantasy không?

Hai luật lọc phạm vi: **tính năng không phục vụ pillar nào là scope creep**, và **hệ thống không phục vụ autonomy, competence hay relatedness thì đáng nghi ngờ**.

## 5. Thiết kế ngược từ trải nghiệm

1. Viết trải nghiệm mong muốn trong 1 câu.
2. Liệt kê các *động từ* cho người chơi cảm nhận được nó.
3. Định nghĩa rules, input, goals và rewards để các động từ đó có nghĩa.
4. Dựng loop có leo thang và giải tỏa căng thẳng.
5. Đặt output của hệ thống và các trigger hệ quả.
6. Gắn phần biểu đạt: hình, âm, chữ, biểu tượng.
7. Thiết kế feedback củng cố dòng cảm xúc.

## 6. Pillars, 1-pager, concept doc

Dùng khi tạo game mới hoặc định nghĩa lại pillars: [references/pillars-and-concept.md](references/pillars-and-concept.md).

## 7. Nguyên tắc làm việc

- **Tài liệu phải giúp ai đó implement, test hoặc phản biện.** Mỗi hệ thống viết theo 3 lớp: Intention → Functionality → Parameters.
- **Prototype phần rủi ro trước.** Spec tối thiểu khoảng 1 trang, build bản thô, quan sát, rồi mới viết spec đầy đủ.
- **Phân tích phải dẫn tới hành động:** kết thúc bằng thay đổi cụ thể, viết được thành ticket sprint.
- **Khuyến nghị một phương án**, không liệt kê lan man.
- Viết tài liệu theo ngôn ngữ của team (mặc định tiếng Việt), giữ thuật ngữ tiếng Anh chuẩn.
