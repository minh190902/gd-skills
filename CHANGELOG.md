# Changelog

Định dạng theo [Keep a Changelog](https://keepachangelog.com/), phiên bản theo [SemVer](https://semver.org/).

## [0.1.0] - 2026-10-09
### Added
- 12 skill `gd-*`: core (router + thiết lập dự án), status, design-review, unstuck, feature-spec, feature-audit, narrative-design, economy-balance, pacing-progression, ux-audit, playtest, game-analysis.
- Quy ước design dir cho mỗi game: `docs/design/{PROJECT,STATE,DECISIONS,SYSTEMS}.md` và `gd.config.json`.
- Công cụ: `system_map.py` (ai ghi/đọc state, impact, diff), `dialogue_audit.py` (Dialogue Manager), `economy_sim.py` (Monte Carlo + ×1.2 curve).
- `tools/install.py` (cài vào repo hoặc global, khởi tạo design dir, chèn khối rules vào CLAUDE.md), `tools/validate.py`, test hồi quy với fixture Godot nhỏ.
- CI GitHub Actions (Ubuntu + Windows, Python 3.9 / 3.13), `.editorconfig`, `.gitignore`, `.gitattributes` (LF).
