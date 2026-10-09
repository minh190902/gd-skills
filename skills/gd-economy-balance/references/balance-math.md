# Balance math — công thức tham chiếu

Phần ×1.2, two-option audit, bottom-up framework lấy từ gamedesign.guide (CC BY 4.0). Các công thức còn lại là kiến thức chuẩn ngành (Schreiber & Romero, *Game Balance*) do site chỉ nêu tên mà không có công thức.

## Tăng trưởng theo tier
- **Hình học (mặc định):** `value_n = base × r^(n−1)`, r ≈ 1.2. Level 6 ≫ level 1 nhưng 5 vs 6 vẫn là trận công bằng.
- **Tuyến tính:** `value_n = base + k·(n−1)` — dùng khi muốn ý nghĩa mỗi bước giảm dần (tỉ lệ tăng tương đối giảm).
- **Đa thức:** `value_n = a·n^p` (p 1.5–2.5) — đường cong XP phổ biến.
- Chi phí nên tăng nhanh hơn sức mạnh một chút → efficiency (power/cost) giảm nhẹ theo tier, tạo lựa chọn giữa "nâng cái cũ" và "mua cái mới".

## Diminishing returns & soft cap
- **Hyperbolic:** `effect = x / (x + K)` → effect 50% khi x = K; không bao giờ đạt 100%. Tốt cho % né, % giảm sát thương, tỉ lệ crit.
- **Soft cap:** `effect = x` khi x ≤ C; `C + (x − C)·d` khi x > C (d ≈ 0.3–0.5).
- **Log:** `effect = a·ln(1 + x/b)` — tăng nhanh lúc đầu, chậm dần.

## Damage formula
- Trừ: `dmg = atk − def` → def cao có thể vô hiệu hóa hoàn toàn (cần sàn tối thiểu, vd. `max(dmg, atk·0.1)`).
- Tỉ lệ: `dmg = atk × K/(K + def)` → không bao giờ 0, mỗi điểm def có giá trị giảm dần. Với K = def "chuẩn" ở tier đó, giảm 50%.
- Time-to-kill: `TTK = HP / DPS`. Cân bằng role bằng TTK chứ không bằng chỉ số đơn lẻ.

## Kinh tế (Source → Pool → Sink)
- **Faucet/sink ratio** mỗi stage = tổng thu / tổng chi bắt buộc. <1 → nợ (vòng xoáy chết nếu không có catch-up); ≈1.0–1.3 → khắc nghiệt; >1.5 → dư dả, pillar "khắc nghiệt" mất tác dụng.
- **Lạm phát:** carry-over trung vị tăng đều mỗi stage → thêm sink có giá trị (đầu tư dài hạn, cosmetic, cải thiện thành) hoặc scale chi phí.
- **Catch-up (feedback âm):** khoản vay, hero rẻ, nhiệm vụ phụ cứu trợ — tránh để một stage thua dẫn tới thua cả game.
- **Snowball (feedback dương):** thắng → thưởng → mạnh hơn → thắng. Cần trần hoặc chi phí duy trì (lương là một chi phí duy trì tự nhiên).

## Tier table mẫu
| Tier | Cost | Power | Efficiency (P/C) | Ghi chú |
|---|---|---|---|---|

## Bottom-up framework
Đơn vị nguyên tử (1 đòn đánh, 1 gold) → trao đổi tài nguyên → kinh tế hệ thống → nhịp progression → chiến lược nổi lên. Cân bằng từ dưới lên; kiểm tra từ trên xuống bằng playtest.

## Deliberate imbalance
Được phép khi hệ sinh thái hấp thụ được (vũ khí mạnh nhưng có chi phí/ rủi ro, hero SSR đắt lương). Ghi rõ là chủ ý.

## Balance doc (khi cần tài liệu đầy đủ)
Exec summary · System overview (flow + biến chính) · Player model (archetype, difficulty curve, reward pacing) · Balance theo hệ thống (công thức, giá trị, mục tiêu) · Math models & cost curves · Analytics/A-B · Feedback loops · Asymmetry & meta (pick rate, counter, buff/nerf log) · Tools · Simulation guidance.
