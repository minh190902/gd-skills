---
name: gd-pacing-progression
description: Pacing, progression and onboarding design — level/stage tension maps, complexity curve (when each mechanic or system is introduced), difficulty curve, emotion arc across a chapter, FTUE/tutorial flow, unlock schedules, session length. Use when planning a new chapter or batch of levels, deciding when to unlock a system, designing or reviewing the tutorial or first 15 minutes, "the mid-game is boring", "too much at once", "players quit early", or reordering content.
---

# GD Pacing & Progression

Bốn bộ điều tiết của lớp Dynamics: **Progression** (thay đổi có chủ đích theo thời gian), **Complexity curve** (độ khó học cộng độ khó chơi), **Pacing** (nhịp căng và chùng), và **Balance** (xem `gd-economy-balance`). Complexity khác difficulty. Đọc `PROJECT.md` để biết độ dài phiên chơi và ràng buộc nền tảng.

## Quy trình A — Bản đồ nhịp của một chương / chuỗi màn

1. **Kiểm kê từng màn** (từ config/data của level và nội dung narrative): số wave hoặc thử thách, kẻ địch mới, nhân vật mới, cơ chế hoặc hệ thống *xuất hiện lần đầu*, các lựa chọn lớn, thời lượng ước tính.
2. **Lập bảng nhịp** theo [templates/pacing-map.md](templates/pacing-map.md): mỗi hàng là một màn hoặc một lát 10–15 phút. Các cột: cơ chế mới · độ căng (L/M/H) · độ phức tạp (L/M/H) · cảm xúc mục tiêu · khoảng thở/phần thưởng · bất ngờ. Mã màu năng lượng: 🔴 cao · 🔵 bình tĩnh · 🟡 phần thưởng.
3. **Kiểm tra các mẫu nhịp:**
   - Có tương phản: không bao giờ căng tối đa liên tục.
   - Mỗi cơ chế mới đi theo Học → Thử → Nghỉ.
   - Có gài trước rồi mới trả: mối nguy hoặc bí ẩn được đặt trước khi giải quyết.
   - Có khoảng lặng trước va chạm lớn.
   - Phần thưởng xen giữa các đoạn áp lực.
   - Mỗi màn có ít nhất một khoảnh khắc lặng.
4. **Chẩn đoán lỗi:** nhịp phẳng → chán; căng liên tục → kiệt sức; quá dày → tê liệt; giữa game yếu → người chơi bỏ.
5. **Đề xuất** sắp xếp lại, dời thời điểm mở khóa, hoặc thêm khoảng thở, kèm thay đổi cụ thể trong data/nội dung.

## Quy trình B — Complexity curve (lịch mở khóa hệ thống)

1. Chia game thành **3 hồi**. Với mỗi hồi, ghi cơ chế hoặc hệ thống mới nào xuất hiện và nó tương tác với cái cũ ra sao.
2. 7 luật giới thiệu cơ chế:
   - Mỗi lần chỉ một cơ chế.
   - Xây trên thứ người chơi đã thành thạo.
   - Đưa ra lúc người chơi còn dư sức.
   - Rải đều qua các hồi.
   - Dạy trong ngữ cảnh.
   - Lên lịch khoảng thở.
   - Cắt bớt chồng chéo ở cuối game.
3. Đánh dấu các điểm nghỉ và điểm đỉnh (nơi nhiều hệ thống chồng lên nhau, boss).
4. Tùy chọn: **đỉnh giả**, tức là thêm một lớp mới đúng lúc người chơi tưởng mình đã thấy hết.
5. Đầu ra là bảng `Hệ thống · Mở khóa hiện tại · Mở khóa đề xuất · Cách dạy · Lý do`, rồi kiểm tra tutorial hiện có có khớp với lịch này không. Danh sách hệ thống lấy từ SYSTEMS.md.

## Quy trình C — FTUE / 15 phút đầu

Nhịp chuẩn: **Hook** (hình ảnh, chủ đề hoặc câu chuyện) → **dạy một hành động cốt lõi** → thử thách đơn giản dùng hành động đó → **thưởng ngay** → hé lộ core loop → gợi ý người chơi có thể trở thành gì.

Checklist:
- [ ] Người chơi biết phải làm gì trong 10 giây đầu?
- [ ] Hành động chính xuất hiện ngay?
- [ ] Thấy được toàn bộ core loop trong 5–10 phút đầu?
- [ ] Có phần thưởng trước khi đòi người chơi cam kết?
- [ ] Cảm được tone và fantasy ghi trong PROJECT.md?
- [ ] Tutorial dạy qua hành động, tách từng khái niệm trước khi trộn, bỏ qua được, hợp tone?
- [ ] *"Nếu người chơi quên rằng mình đang ở tutorial, bạn đã làm đúng."*

Cách kiểm tra: mô tả 15 phút đầu theo từng lát 3 phút, chấm thấp/vừa/cao, đánh dấu khoảng thở, bất ngờ, chỗ chuyển cơ chế, và ít nhất một khoảnh khắc lặng.

## Progression
- Các loại: chỉ số, không gian, câu chuyện, cơ chế, ngoại hình, hệ thống. Các cấu trúc: tuyến tính, phân nhánh, module, lặp lại, động.
- **Progression tốt cho người chơi thêm lựa chọn.** Progression tệ là cùng một lối chơi, chỉ có số to hơn. Mỗi lần lên cấp nên mở ra một *lựa chọn* mới, không chỉ cộng chỉ số.
- Checklist: sự tăng trưởng có rõ? có mốc để mong chờ? có thay đổi lối chơi cốt lõi? nhịp có cân đối? có nhiều lớp? có hỗ trợ theme?
- Bản đồ mốc: vẽ các mốc theo từng màn, rồi tìm những đoạn dài quá 2 màn mà không có mốc nào.

## Phiên chơi
Mỗi màn nên vừa với một phiên chơi điển hình (ghi trong PROJECT.md) và có điểm dừng tự nhiên, kèm save ở điểm dừng. Màn nào vượt quá khoảng 1,5 lần độ dài phiên thì cân nhắc chia nhỏ.
