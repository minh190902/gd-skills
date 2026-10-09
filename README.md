# Game Design Skills for Claude Code

Bộ 12 skill giúp Claude Code làm việc như một **game designer có quy trình**:
- **phản biện ý tưởng** bằng bằng chứng, không gật đầu mặc định;
- **chặn chuyện thêm tính năng này làm vỡ logic tính năng khác**, nhờ bản đồ ai ghi/đọc state;
- **gỡ rối** khi bạn bị ngợp;
- **luôn biết dự án đang ở đâu.**

Ngoài ra còn có các quy trình viết spec, audit hệ thống, thiết kế narrative, cân bằng kinh tế, nhịp độ, UX, playtest và phân tích game tham khảo.

Phương pháp dựa trên [Game Design Guide](https://gamedesign.guide) (CC BY 4.0, xem [NOTICE.md](NOTICE.md)). Các công cụ đi kèm hỗ trợ **Godot 4 / GDScript** và **Nathan Hoad Dialogue Manager**; phần quy trình dùng được cho mọi engine.

> *English summary:* 12 Claude Code skills for game design. They challenge ideas with evidence, map which systems write and read shared state (so new features don't silently break old ones), help untangle confusion, and keep a one-page project STATE. They also cover feature specs and audits, narrative consequence audits, Monte Carlo economy simulation, pacing, UX audits, playtests and game analysis. The skill text is in Vietnamese; descriptions are in English.

## Skills

| Skill | Dùng khi |
|---|---|
| `gd-core` | Câu hỏi thiết kế chung; thiết lập design dir cho game mới; định tuyến sang skill khác |
| `gd-status` | Đầu/cuối phiên: "đang ở đâu, làm gì tiếp" (STATE.md) |
| `gd-design-review` | **Mỗi khi đưa ra ý tưởng**: kiểm tra ảnh hưởng, xung đột, phản đối kèm mức độ |
| `gd-unstuck` | Khi rối: tách vấn đề, tìm quyết định đang chặn, chọn bước tiếp theo |
| `gd-feature-spec` | Viết spec trước khi code |
| `gd-feature-audit` | Giữ, gộp hay cắt tính năng; ma trận chồng chéo |
| `gd-narrative-design` | Lựa chọn và hệ quả, trả flag, arc nhân vật |
| `gd-economy-balance` | Nguồn thu/khoản chi, đường cong giá trị, mô phỏng kinh tế |
| `gd-pacing-progression` | Nhịp độ, lịch mở khóa, FTUE |
| `gd-ux-audit` | Audit màn hình, mức độ S1–S4 |
| `gd-playtest` | Kế hoạch test, phân loại kết quả, nhật ký quyết định |
| `gd-game-analysis` | Mổ xẻ game tham khảo và rút ra việc cần làm |

## Cài đặt

Yêu cầu: Claude Code, Python 3.8+ (chỉ dùng thư viện chuẩn).

### Cách 1: Plugin marketplace (Claude Code)
```
/plugin marketplace add minh190902/game-design-skills
/plugin install game-design-skills@game-design-skills
```
Skill sẽ có tên dạng `game-design-skills:gd-core`. Sau đó mở game và yêu cầu Claude "thiết lập design dir cho game này" (theo mục 1 của `gd-core`).

### Cách 2: Chép vào repo game (khuyên dùng cho team)
Cách này giữ skill trong git của repo game, nên cả team dùng cùng một phiên bản.
```bash
git clone https://github.com/minh190902/game-design-skills
python game-design-skills/tools/install.py --target <repo_game> --init <thư_mục_game>
```
- `--target`: repo nhận skill, chép vào `<repo>/.claude/skills/gd-*`.
- `--init`: tạo `<thư_mục_game>/docs/design/` từ template (không ghi đè file đã có) và chèn khối quy tắc vào `CLAUDE.md` của repo.
- `--global`: cài vào `~/.claude/skills/` để dùng cho mọi dự án.
- `--dry-run`: chỉ in ra những gì sẽ làm.

**Cập nhật:** `git pull` rồi chạy lại đúng lệnh cũ. Thư mục `gd-*` được thay mới hoàn toàn; tài liệu thiết kế của bạn được giữ nguyên.

## Mỗi game có một design dir

```
<game_root>/docs/design/
├── PROJECT.md      # định danh, fantasy, pillars, core loop, ràng buộc nền tảng, rủi ro
├── STATE.md        # đang ở đâu, tiếp theo, câu hỏi mở, parking lot (≤ 1 trang)
├── DECISIONS.md    # quyết định đã chốt và lý do
├── SYSTEMS.md      # mục đích từng hệ thống + bản đồ phụ thuộc tự sinh
└── gd.config.json  # cấu hình cho công cụ
```
Skill dùng chung, còn dữ liệu nằm trong từng game. Monorepo nhiều game thì mỗi game có design dir riêng.

`gd.config.json` (mọi khóa đều tùy chọn):
```json
{
  "state_owners":    {"GameState": "scripts/game_state.gd"},
  "instance_owners": {"HeroData": "scripts/data/hero_data.gd"},
  "save_systems":    ["SaveLoadManager"],
  "flag_set_fns":    ["set_flag"],
  "flag_read_fns":   ["check_flag", "get_flag"]
}
```

## Công cụ (Godot)

```bash
# Ai ghi/đọc biến state nào; bán kính ảnh hưởng; so sánh trước và sau khi sửa
python -I skills/gd-design-review/scripts/system_map.py <game_root> [--impact gold] [--snapshot f | --diff f]
# Flag set mà không đọc, flag đọc mà không set, jump hỏng, title mồ côi, bảng lựa chọn và hệ quả
python -I skills/gd-narrative-design/scripts/dialogue_audit.py <game_root> [--stage ch1] [--json]
# Mô phỏng kinh tế theo màn; kiểm tra đường cong ×1.2
python -I skills/gd-economy-balance/scripts/economy_sim.py sim model.json | curve 100 120 150
```
Các script dựa trên regex, không phải parser đầy đủ: hãy dùng kết quả làm bằng chứng để kiểm tra, không phải chân lý. Giới hạn được ghi trong docstring của từng script.

## Ví dụ cách dùng

- *"Mình muốn thêm hệ thống tinh thần quân làm giảm loyalty khi thua."* → `gd-design-review` liệt kê mọi hệ thống đang ghi/đọc `loyalty`, nêu xung đột với các hệ thống khác cũng chạm vào loyalty, đưa phản đối 🔴/🟠/🟡 và kết luận Go / Park / Reject.
- *"Rối quá, không biết nên làm combat hay story trước."* → `gd-unstuck`.
- *"Tiếp tục thôi."* → `gd-status` đọc STATE.md, so với git, và đề xuất việc tiếp theo.
- *"Lựa chọn của người chơi có thực sự quan trọng không?"* → `gd-narrative-design`, quy trình B.

## Phát triển

```bash
python tools/validate.py                  # frontmatter, link, LF, JSON, version
python -m unittest discover -s tests -v   # test hồi quy với fixture Godot nhỏ
claude plugin validate .                  # kiểm tra manifest của Claude Code
```
Quy ước cho người đóng góp: xem [CLAUDE.md](CLAUDE.md). Lịch sử thay đổi: [CHANGELOG.md](CHANGELOG.md).

## License

Code và nội dung skill: [MIT](LICENSE). Phần phương pháp được diễn giải từ gamedesign.guide theo CC BY 4.0, ghi công trong [NOTICE.md](NOTICE.md).
