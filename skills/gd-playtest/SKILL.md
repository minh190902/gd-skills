---
name: gd-playtest
description: Plan playtests and turn playtest feedback into decisions — test goals, metrics, tester types, observation script, capture setup, triage, decision log, and insight-to-action tickets. Use when the user wants to test a build, prepare questions for testers, has playtest notes/recordings/feedback to process, "people said X", wants to decide what to fix next from feedback, or asks whether an analysis is actionable.
---

# GD Playtest & Iteration

*Bẫy lớn nhất: thu thập feedback mà không hành động được.* Mục tiêu: từ build hoàn chỉnh → quyết định được ghi lại trong 72 giờ.

## Quy trình A — Lập kế hoạch playtest

1. **Mục tiêu ≤ 2 câu**, chọn 1–2 hạng mục:

   | Hạng mục | Câu hỏi | Tín hiệu đo |
   |---|---|---|
   | Feel & Flow | Hành động cốt lõi có sướng? Loop dễ đọc? | Thời gian tới khi thành thạo, tỉ lệ input sai |
   | Balance | Thử thách công bằng? Tài nguyên tạo căng thẳng? | Màn/wave thua, tài nguyên cuối màn, nhân vật chết |
   | Clarity | Hiểu chuyện gì xảy ra và vì sao? | Tỉ lệ skip tutorial, số lần hỏi/do dự |
   | Emotion | Cảm được đỉnh và đáy? | Tự báo cáo theo beat |
   | Retention hook | Có muốn chơi phiên nữa? | Điểm ý định quay lại 1–5 |

2. **Loại test** (nhỏ & thường xuyên trước): nội bộ team → nội bộ mù (chưa biết game) → bạn bè/gia đình → nhóm tập trung → closed alpha → demo công khai.
3. **Chọn tester** (3–5 người, trộn các kiểu): *blind* (onboarding) · *careful explorer* (giải thích thừa) · *optimizer* (khai thác) · *chaos agent* (giới hạn hệ thống).
4. **Chuẩn bị capture** — kiểm tra trước khi test: quay màn hình điện thoại, think-aloud, log sự kiện (nếu có: thêm log tạm cho các sự kiện chính: bắt đầu/kết thúc màn, tài nguyên, nhân vật chết, lựa chọn dialogue), khảo sát 5 câu gắn với mục tiêu.
5. **Kịch bản quan sát** cho người điều phối: *không bao giờ giải thích trong lúc test*; không sửa giữa chừng; ghi lại im lặng, thở dài, chỗ dừng lâu.
6. Output: `<game_root>/docs/playtest/<YYYY-MM-DD>-plan.md` theo [templates/playtest.md](templates/playtest.md) (phần Plan). Ghi build/commit hash và changelog.

## Quy trình B — Xử lý kết quả

1. **Ghi lại bất ngờ** trước, rồi tách **triệu chứng** (lạc đường) khỏi **nguyên nhân** (thiếu chỉ dẫn).
2. **Đọc tín hiệu hành vi:**

   | Hành vi | Thường nghĩa là |
   |---|---|
   | Dừng lâu | Ma sát hoặc quá tải |
   | Lặp lại một hành động | Feedback không rõ / affordance hỏng |
   | Bỏ qua thứ hiển nhiên | Phân cấp thị giác kém |
   | Không phản ứng | Nhịp phẳng |
   | Cười sai chỗ | Mâu thuẫn hoặc emergent play |
   | Quay lui | Mục tiêu không rõ |
   | Skip | Chán hoặc không tin tưởng |
   | Im lặng đột ngột | Đỉnh căng thẳng (tốt) hoặc mất hứng |

   *"Người chơi không bao giờ sai. Nếu họ hiểu sai hệ thống, hệ thống đã thể hiện sai."* Nhưng đừng phản ứng thái quá với một người — tìm pattern qua các phiên.
3. **Nghĩ theo hệ thống:** hành động nào kích hoạt nó, hệ thống phản hồi thế nào, lớp nào của Game Map bị vỡ.
4. **Gom & phân loại:** theo pillar và mức độ → **Critical / Important / Nice-to-have** (parking lot). Fix ước tính >1 ngày → spike prototype trước.
5. **Decision log:** Vấn đề · Thay đổi đề xuất · Owner · Hạn · Pillar phục vụ · Cách xác nhận ở lần test sau.
6. Chuyển mỗi quyết định thành ticket (ghi vào backlog của dự án nếu người dùng đồng ý; quyết định quan trọng → DECISIONS.md) và gọi skill phù hợp: UX → `gd-ux-audit`, số → `gd-economy-balance`, truyện → `gd-narrative-design`, tính năng → `gd-feature-spec`/`gd-feature-audit`.

## Insight → Action (áp dụng cho MỌI phân tích)
Pattern ("skip dialogue sau 10s") → hỏi vì sao → kiểm ngữ cảnh (onboarding hay endgame) → giả thuyết → bước tiếp theo (thử bản cắt ngắn) → theo dõi tác động.

Phân tích chỉ actionable nếu trả lời ít nhất một: *thay đổi gì, giữ gì, test gì, bỏ/hoãn gì, cái gì có khả năng hỏng/gây thích thú*. Test cuối: **có viết được thành một ticket sprint không?** Nếu không → còn là bình luận.

Cảnh báo dữ liệu: vài người trên Discord, cảm giác, ý kiến streamer, test 8 người = *tín hiệu*, không phải *dữ liệu*. Tương quan ≠ nhân quả.

## Nhịp gợi ý
Thứ Hai build + test · Thứ Tư quyết định · Thứ Sáu implement.

## Checklist
- [ ] Mục tiêu ≤ 2 câu
- [ ] Build number + changelog đã chia sẻ
- [ ] Capture đã kiểm tra trước
- [ ] Phân loại trong 48 giờ
- [ ] Mỗi hành động gắn với một pillar
- [ ] Lần test tiếp theo đã lên lịch
