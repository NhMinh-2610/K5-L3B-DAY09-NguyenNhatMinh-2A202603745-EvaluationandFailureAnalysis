# Trace case — ticket ghi đè số ngày trong DB

Case được lấy từ report do `python -m lab9.m1_evidence` sinh ra. Đọc ledger trước cho thấy agent hoàn 20.000đ trong khi nhãn yêu cầu 0đ. Trace giúp tìm ra nguyên nhân trước khi thao tác ghi tiền diễn ra.

| Trường | Nội dung |
|---|---|
| Trial | `seeded_regression C-002@11`; trial run ID `R-seeded_regression-C-002-s11`; report `reports/m1_trace_evidence.json`, run ID `M1-trace-862f3ea8ac8f`. |
| Triệu chứng | Lab 8 FAIL: `status resolved != denied`. Agent báo đã hoàn 20.000đ và ledger thật sự ghi 20.000đ; nhãn yêu cầu `denied`, proposal 0đ, ledger 0đ. Đây là lỗi quyết định hoàn tiền, không phải lỗi reply lệch ledger. |
| Bước sai đầu tiên | Event **3**, `model_override`, payload `{"delay_days": 5}`. |
| Vì sao là bước đầu tiên | Event 1 chỉ giao việc với `principal_scope=owner_order_only`; event 2 trả order O-202 của đúng principal với `delay_days=2`. Cả hai chưa sai. Event 3 thay fact DB bằng con số 5 trong ticket. |
| Failure mode | **FM-03 — ticket_trust**, layer `model/prompt`. |
| Đối chứng | `fixed C-002@11`, run ID `R-fixed-C-002-s11`, giữ DB 2 ngày. Event 3 là quote `amount_vnd=0`, `reason=no_entitlement`; không có `model_override`, status `denied`, ledger 0đ và Lab 8 PASS. |
| Regression test | `tests/test_lab9_trace_case.py`: `test_lab9_trace_case_detects_ticket_override` kiểm tra `DbFactKept` trả False cho variant lỗi; `test_lab9_trace_case_fixed_keeps_db_fact` kiểm tra grader trả True và ledger 0đ cho `fixed`. Có thêm đối chứng `swarm` ở seed 11 và tái hiện lỗi `swarm` ở seed 55. |
| Chưa chắc chắn | Trace không giải thích được suy luận bên trong model. Đây là MockLLM và lỗi được gài sẵn; chưa suy rộng thành tỉ lệ lỗi của LLM thật hay người dùng thật. |

## Chuỗi nguyên nhân và hậu quả

Chính sách hiện hành yêu cầu trễ ít nhất 3 ngày. DB cho biết đơn chỉ trễ 2 ngày nên không có quyền hưởng bồi thường. Sau event 3, event 4 tính quote 20.000đ từ thông tin đã bị ghi đè. Approval của case vẫn hợp lệ ở mức 20.000đ nên host ghi khoản đó; kiểm tra approval không tự sửa được fact đầu vào sai. Event 5 đọc lịch sử hoàn tiền bằng 0 không phải nguyên nhân đầu tiên. Event 6 chỉ thông báo kết quả sai đã xảy ra.

Grader bước `DbFactKept` đã có sẵn trong đề, có thể bắt dấu `model_override`. Regression test dùng đúng grader đó và kiểm tra thêm trạng thái, ledger trên DB mới cho từng trial. Không sửa `swarm_reference.py` hay variant để làm test xanh. Trường hợp ghi đè âm thầm không có event này vẫn cần được các grader kết quả ở M3 kiểm tra.

## Cách chạy lại

Từ `src/`, dùng Python của môi trường riêng:

```powershell
$labPython = '\\?\' + (Join-Path (Get-Location).Path '.venv\Scripts\python.exe')
& $labPython -m lab9.trace_case --shape seeded_regression --claim C-002 --seed 11
& $labPython -m lab9.trace_case --shape fixed --claim C-002 --seed 11
& $labPython -m pytest -q -m student -o addopts= tests/test_lab9_trace_case.py
```

Test kiểm tra grader phải phát hiện đúng lỗi trên variant và không báo lỗi trên đối chứng. Vì vậy cả bộ test phải xanh, dù verdict của grader trên case lỗi là False. Kết quả chạy thực tế được cập nhật trong `TIEN_DO_LAB.md`. Chưa tạo baseline M4 ở bước này.
