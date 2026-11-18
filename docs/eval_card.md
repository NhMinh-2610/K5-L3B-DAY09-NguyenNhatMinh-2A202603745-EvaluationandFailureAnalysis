# Eval card — LogiX-VN refund agent

Ngày chạy: **18/11/2026**. Card này mô tả kết quả Core trên máy, dùng MockLLM. Gate cho qua `fixed`, chặn `seeded_regression` và chặn case chỉ nói sai tiền trong reply. GitHub Actions chưa được chạy qua PR ở mốc chuẩn bị này.

## Phiên bản và nguồn dữ liệu

- **Eval set:** v1, SHA `13a7cc261af8`, 14 item từ ma trận `lab8_public`; nhãn tách riêng trong `data/eval/labels_v1.json`.
- **Seeds:** 11, 22, 33, 44, 55; mỗi report có 70 trial. Mỗi trial dùng một SQLite mới.
- **Agent và grader:** nền commit `409e347`; mã Day 8 lấy từ repo gốc giảng viên, commit `034c6c421c198dae67a9211d15e2587d5a378972`, giữ nguyên `src/lab8/`.
- **Bootstrap M4:** `lab9/stats.py`, Git blob `8627e4eb2667933de9e70051af1ebea440d1b633`; đây là phần bổ sung sau commit nền, được nộp cùng card và report.
- **Metric spec:** 1.2, `config/metric_spec.yaml`; harness map 1.2. Bảy metric gốc và ngưỡng của chúng giữ nguyên, thêm hai metric đã được chủ fork đồng ý.
- **Môi trường chạy:** Python 3.13.7, pydantic-evals 2.68.0, numpy 2.5.5, scipy 1.18.1. Không dùng API key, không bật dịch vụ quan sát Logfire/OTel.
- **Định dạng:** eval set và nhãn được ghi LF để SHA giống nhau trên Windows và Linux. Nội dung JSON giữ nguyên so với bản CRLF trước đó; fingerprint cũ `8b262652f4bf` chỉ khác cách xuống dòng.

| Vai trò | Report | Run ID |
|---|---|---|
| Baseline swarm | [baseline_v1.json](../src/reports/baseline_v1.json) | `E-swarm-20261118-13a7` |
| PR swarm chạy lại trên máy | [eval_pr.json](../src/reports/eval_pr.json) | `E-swarm-20261118-13a7` |
| Đối chứng fixed | [eval_fixed.json](../src/reports/eval_fixed.json) | `E-fixed-20261118-13a7` |
| Regression gài sẵn | [eval_seeded_regression.json](../src/reports/eval_seeded_regression.json) | `E-seeded_regression-20261118-13a7` |
| Kiểm chứng FM-08 | [eval_m3_misreport.json](../src/reports/eval_m3_misreport.json) | `E-m3_misreport-20261118-13a7` |

Baseline và lượt PR swarm là hai lần chạy riêng nhưng có cùng run ID theo quy tắc đặt tên có sẵn của harness; phân biệt bằng tên file. Hai report có metrics giống nhau, được `lab9.ci_check` xác nhận trên máy.

## Metric, ngưỡng và kết quả

Các tỉ lệ nằm trong [0, 1]. Hai metric an toàn là **số vi phạm**, không phải tỉ lệ trung bình.

| Metric | Ngưỡng trong spec | Blocking | Baseline | Fixed | Seeded regression |
|---|---|---|---|---|---|
| approval_bypass | max 0 | Có | 0 | 0 | 0 |
| secret_leak | max 0 | Có | 0 | 0 | 0 |
| db_fact_kept | min 0.95 | Không | 0.9857 | 1.0000 | 0.9286 |
| refund_amount_correct | min 0.95, không giảm có ý nghĩa | Có | 0.9857 | 1.0000 | 0.8571 |
| proposal_amount_correct | min 0.95, chẩn đoán | Không | 0.9857 | 1.0000 | 0.7857 |
| reply_ledger_consistent | min 1.0 | Có | 1.0000 | 1.0000 | 0.7857 |
| pass_rate | min 0.85, không giảm có ý nghĩa | Có | 0.9857 | 1.0000 | 0.7143 |
| pass_5 | min 0.80 | Không | 0.9286 | 1.0000 | 0.7143 |
| cost_per_success | tăng không quá 10% so baseline | Không | 49.5670 | 48.7157 | 81.2020 |

Chi phí là VND mô phỏng trên mỗi lần xử lý thành công, không phải hóa đơn API hay tiền đã chi thực tế. `pass_5` là tỉ lệ item đúng ở cả năm seed.

## Paired CI và quyết định gate

Lấy trung bình qua năm seed cho từng item, ghép cùng item của PR và baseline, rồi bootstrap **14 cặp item**. Không coi 70 trial là 70 quan sát độc lập. Cấu hình: 1.000 resample, percentile, RNG 2027, confidence 95%.

| So với baseline swarm | Metric | Δ (PR − baseline) | CI 95% | Quyết định |
|---|---|---|---|---|
| PR swarm | pass_rate | +0.000 | [+0.000, +0.000] | Exit 0 |
| fixed | pass_rate | +0.014 | [+0.000, +0.043] | Exit 0 |
| seeded_regression | pass_rate | −0.271 | [−0.500, −0.057] | Exit 1, có `pass_rate` |
| seeded_regression | refund_amount_correct | −0.129 | [−0.315, +0.000] | Dưới sàn 0.95 nên vẫn bị chặn |
| m3_misreport | pass_rate | +0.014 | [+0.000, +0.043] | Vẫn exit 1 vì FM-08 |

`fixed` đạt 70/70 trial, baseline đạt 69/70. CI của chênh lệch fixed chạm 0 nên chưa dùng số liệu này để khẳng định cải thiện có ý nghĩa thống kê. Nó được cho qua vì đạt các sàn và không có bằng chứng giảm chất lượng theo quy tắc gate.

`seeded_regression` bị chặn ở `refund_amount_correct`, `reply_ledger_consistent` và `pass_rate`. CI pass_rate khớp mốc tham chiếu của đề khi làm tròn ba chữ số. Case FM-08 có pass_rate và refund_amount_correct đều 1.0 nhưng reply_ledger_consistent chỉ 0.8571, nên bị chặn riêng ở metric này.

Log nguyên bản: [gate PR](../src/reports/gate_pr.txt), [gate fixed](../src/reports/gate_fixed.txt), [gate seeded regression](../src/reports/gate_seeded_regression.txt), [gate FM-08](../src/reports/gate_m3_misreport.txt), [kiểm tra baseline/spec trên máy](../src/reports/ci_check_local.txt). Report và log được sinh bằng script, không sửa tay.

## Judge và trace case

Tone đạt κ=0.757, precision=0.857, recall=0.800. Helpful bị loại vì κ=0.375 và recall=0.300; precision 1.000 không bù được 21/30 lỗi bị bỏ sót. Đây là kết quả replay CSV, dùng nguyên nhãn công khai. Xem [judge audit](judge_audit.md) với 12 bất đồng đã phân tích.

[Trace case C-002](trace_case.md) xác định event 3 `model_override` là bước sai đầu tiên: DB ghi trễ 2 ngày nhưng agent lấy 5 ngày trong ticket. `tests/test_lab9_trace_case.py` dùng `DbFactKept` và kiểm tra ledger trên variant lỗi cùng đối chứng fixed. Baseline vẫn có lỗi này ở C-002, seed 55; mã Lab 8 được giữ nguyên theo đề.

Phép đo M3 gốc đạt detection 100%, false alarms 0% trên seeded_regression/fixed. Grader proposal giải thích riêng C-013, không đổi định nghĩa FM-08. Xem [taxonomy](failure_taxonomy.md) và [output detection](../src/reports/m3_detection.txt).

## Chủ gate và phạm vi pilot

**Gate owner:** chủ fork cá nhân `@NhMinh-2610`. Khi một PR thật có gate exit 1, chủ fork xem metric, trace và report trước khi quyết định sửa; trợ lý chỉ thực hiện công việc đã được đồng ý. Report regression bị chặn trong bước kiểm chứng là kết quả mong đợi, không phải lý do hạ ngưỡng.

Phạm vi hiện tại là pilot offline của bài lab: claim hoàn tiền trong 14 case công khai, SQLite tạm, chính sách và approval của host gốc. Bao gồm đối chứng cần hỏi thêm mã đơn, từ chối hoặc chuyển chuyên viên khi không đủ điều kiện/phạm vi. Chưa đo trên người dùng thật, thanh toán thật hay các claim ngoài tập này.

## Giới hạn và điều kiện đánh giá lại

- MockLLM và seed cố định giúp tái hiện nhưng không đại diện cho lỗi hay nhiễu của LLM thật.
- Chỉ có 14 item nên CI còn rộng; Core chưa chứng minh phát hiện ổn định regression nhỏ hoặc chỉ nằm trong một slice.
- Judge replay dùng dữ liệu công khai; một số nhãn/note cần ngữ cảnh bổ sung, chưa có held-out mới.
- Grader FM-08 hỗ trợ số nguyên VND có đơn vị và cách phân nhóm hàng nghìn thông thường trong reply của lab. Chưa diễn giải tiền bằng chữ hoặc nhiều khoản tiền có vai trò khác nhau.
- Swarm gốc không có event reply; giá trị 1.0 của reply_ledger_consistent ở baseline nghĩa là không thấy khẳng định tiền để đối chiếu, không phải đã kiểm chứng lời văn đầy đủ.
- Slice gate, pass@k/pass^k, integrity check và ratchet tự động thuộc M5–M7, chưa triển khai ở Core này. Core chưa chứng minh chống được report bị sửa hoặc bị bỏ dòng.
- GitHub Actions, merge vào main và nộp LMS còn cần được thực hiện sau khi chủ fork đồng ý. Kiểm tra local không được ghi thành CI GitHub đã xanh.

Đổi nội dung/tập item hoặc nhãn phải tăng eval_set_version và tạo baseline tương ứng. Đổi metric/ngưỡng phải tăng metric_spec_version; cùng một eval-set version chỉ giữ nguyên hoặc siết các ngưỡng đã có. Chuẩn hoá LF lần này giữ nguyên dữ liệu JSON, chỉ cố định fingerprint giữa các hệ điều hành.
