---
name: gd-game-analysis
description: Analyze or deconstruct a reference game (or an open-source game repo) and extract actionable lessons for our projects — core loop, systems, progression/economy, UX/FTUE, narrative, monetization, market fit, and system-level comparison/benchmark between games. Use when the user shares a game, store page, video, review set or repo to study ("phân tích game X", "học gì từ Y", "so sánh với Z"), when researching competitors, or when writing documents like "Cultivation Simulator Analysis.md".
---

# GD Game Analysis

Mục đích không phải tóm tắt game người khác, mà là **rút ra quyết định cho game của chúng ta**. Mọi phân tích kết thúc bằng các khuyến nghị có thể thành ticket, gắn với pillar của dự án đích.

## Quy trình

### 1. Xác định câu hỏi & dự án đích
Phân tích cho game nào của chúng ta? Câu hỏi cụ thể là gì ("họ làm hệ quả dài hạn thế nào?", "họ giữ kinh tế căng ra sao?")? Đọc `PROJECT.md` trong design dir của game đích (quy ước ở `gd-core`).

### 2. Thu thập nguồn — chọn lăng kính phù hợp
| Lăng kính | Cho insight về | Cách |
|---|---|---|
| Chơi / xem gameplay | Hành vi | Ghi hành động lặp lại, chỗ dừng, do dự, cảm xúc, chỗ vỡ nhập tâm |
| Reviews (Steam, store, Reddit) | Cảm xúc | Gắn tag: pacing, feedback, economy, tone, kỳ vọng. Review tiêu cực thường giá trị nhất |
| MDA | Nhân quả | Mechanics → Dynamics → Aesthetics (8 loại fun: Challenge, Fantasy, Narrative, Discovery, Expression, Fellowship, Submission, Sensation) |
| AERM | Bền vững kinh doanh | Acquisition, Engagement, Retention, Monetization |
| Sơ đồ | Hệ thống | Mind map, flowchart quyết định/state, sơ đồ dòng tài nguyên |
| Source code (repo mã nguồn mở) | Cách implement | Đọc vòng lặp chính, data model, cách hệ quả được lưu & đọc |

Dùng WebSearch/WebFetch cho store page, wiki, review; dùng Explore agent cho repo lớn.

### 3. 7 câu hỏi phân tích bất kỳ game nào
1. Người chơi làm gì phần lớn thời gian? (core loop — vẽ dạng Action → Feedback → Progress)
2. Hệ thống nào củng cố hoặc ngắt loop?
3. Game dạy ở đâu và thế nào?
4. Căng thẳng tăng/giảm khi nào, vì sao?
5. Feedback nào đáng nhớ, thỏa mãn, hoặc gây bối rối?
6. Theme, cơ chế và nhịp nối với nhau ra sao?
7. Bạn có chơi tiếp không, điều gì kéo bạn quay lại?

### 4. Feature breakdown (cho tính năng muốn học)
Purpose · Core fit · Mental model · Feedback · Failure modes · Scalability · System hooks. *Hiểu vì sao nó hoạt động, trong bối cảnh nào, cho ai* — đừng copy tính năng thiếu bối cảnh.

### 5. So sánh (khi có ≥2 game)
So sánh **hệ thống và kết quả, không phải danh sách tính năng**, trên 7 chiều: Core loop · Cognitive load · Progression · Onboarding · Emotional hook · Monetization · Presentation. Hỏi: cùng ràng buộc gì? cùng vấn đề giải khác nhau thế nào? cái gì vắng mặt và vì sao? ý định vs tác động?

Red flags so sánh lười: copy vì đối thủ có; "polished" không định nghĩa; copy hit mà bỏ bối cảnh; so khác thể loại/khác ngân sách không sắc thái; chỉ so hình ảnh.

### 6. Chuyển thành hành động cho dự án đích
Với mỗi bài học:
| Bài học | Bằng chứng (nguồn) | Áp dụng cho (hệ thống/file của ta) | Thay đổi đề xuất | Pillar | Effort | Rủi ro |
Phân loại: **Áp dụng ngay / Thử nghiệm (prototype) / Ghi nhận (không phù hợp lúc này, vì sao)**. Tối đa ~5–7 khuyến nghị ưu tiên — ít mà chắc.

### 7. Output
Lưu `<game_root>/docs/analysis/<game-kebab>.md` (hoặc `docs/analysis/` cấp repo nếu phân tích dùng chung cho nhiều game) theo [templates/deconstruction.md](templates/deconstruction.md). Phần "Key takeaways" và bảng hành động đặt **lên đầu** file.

## Checklist
- [ ] Có câu hỏi phân tích & dự án đích rõ ràng
- [ ] Phân tích hệ thống, không liệt kê tính năng
- [ ] Biết *vì sao* nó hoạt động, cho ai
- [ ] Gồm cả cảm xúc và UX, không chỉ cơ chế
- [ ] Mọi khuyến nghị có bằng chứng, gắn file/hệ thống của ta, thành ticket được
- [ ] Ghi rõ những gì cố ý *không* áp dụng
