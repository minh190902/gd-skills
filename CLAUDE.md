# CLAUDE.md — gd-skills (repo nguồn của bộ skill)

Đây là repo **nguồn** của bộ skill `gd-*`. Không phải game. Khi sửa:

- Skill nằm ở `skills/<name>/SKILL.md`. Frontmatter: `name` trùng tên thư mục; `description` bằng tiếng Anh, tối đa 1024 ký tự, không chứa `<` hoặc `>`, nêu rõ **khi nào dùng** (trigger). Nội dung bằng tiếng Việt, giữ thuật ngữ tiếng Anh. Mỗi SKILL.md dưới 500 dòng; chi tiết dài đưa vào `references/` hoặc `templates/`.
- **Không ghi gì đặc thù của một game cụ thể** vào skill. Thông tin riêng của game nằm trong design dir của game đó (PROJECT.md, gd.config.json). Ví dụ minh họa thì để chung chung.
- Đường dẫn script trong SKILL.md viết dạng `<skill_dir>/scripts/...`. Skill khác tham chiếu tới thì ghi tên skill (ví dụ: "system_map.py thuộc gd-design-review"). Không ghi cứng `.claude/skills/...`, vì khi cài dạng plugin đường dẫn sẽ khác.
- Script chỉ dùng thư viện chuẩn của Python, chạy với `python -I`, in UTF-8. Mỗi hành vi mới cần có fixture và test trong `tests/`.
- Mọi file dùng LF (đã có `.gitattributes`). Trên Windows, khi ghi file bằng Python phải dùng `newline="\n"`.
- Trước khi commit: `python tools/validate.py && python -m unittest discover -s tests && claude plugin validate .`
- Phát hành bản mới: tăng version trong `.claude-plugin/plugin.json` và `marketplace.json` (cả hai chỗ), rồi thêm mục vào CHANGELOG.md.
