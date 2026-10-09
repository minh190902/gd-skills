# Game Map — tham chiếu chi tiết

Nguồn: gamedesign.guide/theory (CC BY 4.0), diễn giải.

## Lớp Player

**Chuỗi:** Context → Need → Conflict/Gap → Motivation → Intention → Behavior.

| Yếu tố | Câu hỏi |
|---|---|
| Context | Ai chơi, tâm trạng gì, ở đâu, bao nhiêu thời gian, thiết bị gì? |
| Need | Họ muốn lấp khoảng trống nào? |
| Conflict | Điều gì tạo căng thẳng? |
| Motivation | Điều gì định hướng năng lượng? |
| Intention | Họ đang *cố* làm gì? |
| Behavior | Họ *thực sự* làm gì? |

**Loại gap** (không có gap = không có lý do chơi; chỉnh kích thước gap để lái động lực): thiếu công nhận → bảng xếp hạng; xả stress → combat; chán vặt → level ngắn; tò mò/thành thạo → pattern sâu hơn; giữ tâm trạng → loop thư giãn; thuộc về → chơi nhóm; **kiểm soát → sandbox/quản lý**; mới lạ giác quan → procedural.

**Context profile:** Geography, Demographics, Emotional goal, Gaming history, Session pattern, Device setup, Preferred features, **Implication** (ưu tiên gì). Ví dụ người chơi mobile phiên 10–15 phút → ưu tiên rõ ràng, giảm thời gian chết, chia nội dung thành module.

**Need → chiến lược:** Progression ↔ Competence (feedback thấy được, thất bại công bằng); Economy ↔ Control/Stability (thưởng dự đoán được, vai trò tài nguyên rõ); Narrative ↔ Purpose/Belonging (hệ quả, biểu tượng); UX ↔ Safety/Clarity; Social ↔ Relatedness.

**Conflict types:** Personal, Systemic (khan hiếm, timer, fog), Social, Moral (dilemma), Cognitive. Mạnh nhất khi nhiều lớp: hệ thống + cảm xúc + danh tính. *Nếu người chơi không nhận ra hoặc không tác động được vào conflict, nó thành grind.*

Mechanic → conflict ẩn: countdown → khẩn cấp; dialogue choice → căng thẳng đạo đức; trade tài nguyên → hy sinh; vai trò ẩn → tin/ngờ; bản đồ procedural → thiếu thông tin.

### Mô hình động lực

| Mô hình | Thành phần | Dùng khi |
|---|---|---|
| SDT | Competence, Autonomy, Relatedness | Core loop, onboarding |
| Quantic Foundry | Action, Social, Mastery, Achievement, Immersion, Creativity | Phân khúc tính năng/nội dung |
| Bartle | Achiever, Explorer, Socializer, Killer | Online/social (thô cho single-player) |
| Big Five | Openness→sandbox, Conscientiousness→strategy/sim… | Persona, độ khó, tone |
| Flow | Challenge≈skill, mục tiêu rõ, feedback tức thì | Đường cong thử thách, boss |

**Công thức framework → loop (7 bước):** chọn MỘT framework → viết 1 dòng tension ("Người chơi thiếu…") → map mỗi motive vào 1 design lever → prototype micro-loop làm motive xuất hiện ~mỗi 30s → đo KPI (time-to-first-action, retry rate, session length) → chỉnh 1 núm mỗi sprint → dừng khi cải thiện chững lại.

Extrinsic (XP, loot) là mồi lửa; intrinsic (tò mò, thành thạo, ý nghĩa) là nhiên liệu. **Overjustification:** cơ chế có còn vui nếu bỏ phần thưởng? Nếu retention dựa vào frustration → thiết kế đang phục vụ compulsion.

**Fogg B=MAP:** hành vi xảy ra khi Motivation, Ability, Prompt cùng có mặt. Chẩn đoán hành vi xấu: *"Hệ thống nào đã làm hành vi này có lợi hoặc khó bị phản chế?"*

**Cognitive load:** intrinsic (độ phức tạp nhiệm vụ — quản lý), extraneous (UI tệ — loại bỏ), germane (công sức học — nuôi dưỡng). Kỹ thuật: progressive disclosure, phân cấp UI, chunking, tutorial theo ngữ cảnh. *Cấu trúc thắng tối giản.*

**Frustration:** productive = constructive ("suýt được") / exploratory (có mẹo ẩn); destructive = punitive (thua không biết vì sao) / accidental (hành động ≠ ý định). Điểm gãy: Intention→Behavior ("không biết làm gì"), Behavior→Action ("bấm không ăn"), Action→Feedback ("không công bằng"), Feedback→Learning ("thôi kệ"). *Hệ thống tốt làm thất bại có thông tin; hệ thống tệ làm thất bại mang tính cá nhân.*

## Lớp Structure

- **Rule** = điều kiện cho phép/cấm/kích hoạt; **Mechanic** = động từ người chơi dùng, xây từ rules + objects. Rules (nguyên tử) → mechanics (phân tử) → systems (hệ sinh thái).
- **Mechanic spec:** Name (động từ), Rules, Objects, Input, State checks, Action logic, Output/Feedback, Edge cases.
- **Input / Output / Feedback:** Output = thay đổi state (hệ thống); Feedback = trình bày cảm giác (người chơi). Fairness cảm nhận phụ thuộc chất lượng I/O nhiều hơn balance.
- **Game state:** Data (HP=42) ≠ State ("wounded") ≠ Feedback (nháy đỏ). Viết bảng *Input → Required State → Result*; mô hình FSM với entry/exit + cue cho mỗi chuyển trạng thái. Boolean chồng nhau → dùng enum/FSM.
- **Action logic:** check điều kiện → áp kết quả → cập nhật state → bắn event (SFX/anim) → chain state/cooldown tiếp. *"Action logic định nghĩa sự thật. Feedback định nghĩa cảm giác."*
- **Goal / Challenge / Reward** chia chung 3 cần gạt: **When** (thời điểm, nhịp), **Where** (vị trí), **What** (loại, hình thức). Challenge ≠ difficulty; là căng thẳng có mục đích. Reward loop: Action → Reward → Reinforcement → Re-engagement → Mastery → Deeper reward.

## Lớp Cognition

UX 5 khía cạnh: Clarity, Control, Feedback, Rhythm, Emotion. Chi tiết quy trình trong `gd-ux-audit`.

## Lớp Dynamics

- Mỗi loop phải cho người chơi: việc để làm **bây giờ**, mục tiêu **tiếp theo**, lý do **quay lại sau**.
- Thang loop: Core (giây–phút), Mid (phút–giờ), Meta (ngày–tuần), Emergent (người chơi tự tạo).
- Feedback dương (thưởng thành công, tăng tốc) vs âm (hạn chế bỏ xa, catch-up).
- Progression tốt làm người chơi *có thêm lựa chọn*; progression tệ = cùng gameplay với số to hơn.
- Regulators chi tiết: `gd-pacing-progression`, `gd-economy-balance`.

## Lớp Perception

- **Player fantasy** = Role + Power + Responsibility + Emotion; một loại fantasy phải chiếm ưu thế (Power, Nurture, Escape, Identity, Survival, Mystery).
- **Theme** phải phát biểu được trong 1 câu và được cảm nhận qua hành động, không qua cutscene. Đổi theme mà không vỡ gì → theme quá nông.
- **Feedback:** tức thì, rõ, nhiều lớp, **tỉ lệ với hệ quả** (boss chết > lính chết), nhất quán.
- **Game feel:** feedback trong ~100–200 ms sau input (với text/turn-based chấp nhận ≥150 ms nhưng cần cue tức thì).
- Narrative & emotion arc chi tiết: `gd-narrative-design`, `gd-pacing-progression`.
