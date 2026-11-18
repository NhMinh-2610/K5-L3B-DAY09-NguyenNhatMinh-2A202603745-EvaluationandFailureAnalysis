# Tiến độ Lab 9

Tệp này ghi lại việc trợ lý đã làm thay bạn, việc bạn cần tự thực hiện và kết quả kiểm tra. Ngày cập nhật: 18/11/2026.

## Cách làm đã thống nhất

- Bám sát README, CHECKPOINTS, RUBRIC và SUBMISSION của Lab 9; không tự đổi yêu cầu, bộ chấm hay ngưỡng để làm đẹp kết quả.
- Trước mỗi nhóm công việc mới, trợ lý nói rõ sẽ làm gì và chờ bạn đồng ý.
- Viết phần giải thích, phân tích và tài liệu bằng lời tự nhiên, dễ hiểu. Chỉ ghi kết quả đã chạy và kiểm tra được.
- Bạn đã đồng ý cho thực hiện M0–M2, tạo tệp theo dõi này và commit M0, M1 trên máy. Push, các commit tiếp theo và các bước M3–M7 cần được bạn đồng ý riêng.
- Tách rõ việc trợ lý làm và việc bạn thực hiện; không ghi một thao tác do trợ lý làm thành việc bạn đã tự làm.

## M0 — Chuẩn bị môi trường

### Trợ lý đã làm với sự đồng ý của bạn

1. Kiểm tra Git: repo ban đầu ở nhánh `main`, không có thay đổi chưa commit; đã có `origin` trỏ tới fork cá nhân và `upstream` trỏ tới repo Lab 9 của giảng viên.
2. Kiểm tra Python: máy có Python 3.13.7, nằm trong khoảng 3.11–3.13 mà đề yêu cầu.
3. Kiểm tra thư mục Lab 8 bạn cung cấp: `C:\Users\nnhat\OneDrive - Hanoi University of Science and Technology\Documents\Nguyen_Nhat_Minh\HUST\Git\K5-L3B-DAY08-HVM-FromWorkflowsToAgents`. Repo này có mã Lab 8 và requirements, nhưng đề Lab 9 yêu cầu dùng mã gốc của giảng viên.
4. Tạo nhánh làm bài `starter/d09`.
5. Tải repo gốc Day 8 vào thư mục tạm và chép 63 tệp trong `src/` sang Lab 9. Nguồn: https://github.com/VinUni-AI20k/K5-Day8-From-Workflows-to-Agents, commit `034c6c421c198dae67a9211d15e2587d5a378972`. Không có tệp nguồn nào trùng với tệp Lab 9 đã có; sau khi chép đã so SHA-256 và tất cả đều khớp.
6. Tạo môi trường Python tại `src/.venv`. Bước cài pip ban đầu gặp lỗi vì đường dẫn dài và máy đang có `LongPathsEnabled=0`. Đã cài pip thành công bằng cách gọi Python với tiền tố đường dẫn mở rộng `\\?\`; không thay đổi thiết lập Windows.
7. Cài xong thư viện theo đúng `src/requirements.txt` và `src/requirements-lab9.txt` vào môi trường riêng. Các gói chính: pydantic-evals 2.68.0, numpy 2.5.5, scipy 1.18.1, pytest 8.4.2 và PyYAML 6.0.3.
8. Chạy kiểm tra thư viện, smoke và sinh eval set v1; cả ba lệnh đều trả exit 0.
9. Đọc lại dữ liệu vừa sinh: có 14 item không trùng ID, 14 nhãn tách riêng, mọi claim đều có nhãn và `failure_modes` còn rỗng đúng yêu cầu M0.
10. Kiểm tra lại sau khi chạy: 63 tệp nguồn Day 8 vẫn khớp SHA-256 với bản gốc; không có thay đổi trong các tệp đề bài và mã Lab 9 đã được theo dõi từ đầu. `.venv` được Git bỏ qua đúng như cấu hình sẵn.

### Kết quả kiểm tra M0

Phần chuẩn bị và kiểm tra trên máy của M0 đã đạt. Trạng thái bật GitHub Actions vẫn cần bạn xác nhận.

| Kiểm tra | Kết quả thực tế |
|---|---|
| `python -m pip check` trong môi trường riêng | `No broken requirements found.`, exit 0 |
| `python -m lab9.smoke` | `M0 PASS`, exit 0 |
| `python -m lab9.evalset --build` | Sinh `eval_set_v1.jsonl` gồm 14 item và `labels_v1.json` gồm 14 nhãn, exit 0 |
| Nguồn Day 8 sau khi chạy | 63/63 tệp khớp bản gốc |

Ở thời điểm chốt M0, chưa chạy `evalset --check` vì việc điền `failure_modes` thuộc M1. Bạn đã duyệt việc commit các tệp M0 trên nhánh `starter/d09`; trợ lý đã tạo commit **`dc209ad` — `chore: prepare Lab 9 environment and eval set v1`**. Chưa push và chưa sinh baseline M4.

### Việc bạn cần làm

- Kiểm tra GitHub Actions đã được bật: mở https://github.com/NhMinh-2610/K5-L3B-DAY09-NguyenNhatMinh-2A202603745-EvaluationandFailureAnalysis/actions. Nếu có nút “I understand my workflows, go ahead and enable them”, bấm nút đó. Nếu đã thấy danh sách workflow thì không cần bấm gì thêm. Trợ lý chưa xác minh trạng thái này trên GitHub.
- Xem hạn nộp của ca học trên LMS. Đề không cho một hạn chung cho mọi ca; không lấy mốc giờ minh họa trong README làm hạn nộp của bạn.
- Bạn đã đồng ý cho thực hiện M1. Phần M1 được ghi bên dưới; các bước tiếp theo vẫn cần bạn duyệt.

### Cách chạy lại kiểm tra trên máy

Mở PowerShell tại thư mục gốc repo, rồi chạy:

```powershell
cd src
$labPython = '\\?\' + (Join-Path (Get-Location).Path '.venv\Scripts\python.exe')
& $labPython -m lab9.smoke
& $labPython -m lab9.evalset --build
```

Tiền tố đường dẫn mở rộng giúp chạy môi trường trong thư mục hiện tại của bạn mà không cần sửa thiết lập Windows. Hai lệnh phải trả exit 0. Lúc mới hoàn thành M0, `failure_modes` còn rỗng đúng theo đề. Sau M1, lệnh build giữ lại các mã đã gắn trong code. Không sửa tay tệp nhãn.

## M1 — Taxonomy, gắn mã lỗi và trace case

### Trợ lý đã làm với sự đồng ý của bạn

1. Đọc trace của agent gốc và các cấu hình gài lỗi công khai, so sánh với nhãn và ledger. Giữ nguyên `src/lab8/`, các variant và bộ chấm của đề.
2. Thêm `src/lab9/m1_evidence.py` để chạy lại các case và sinh report bằng script. Các tên `m1_*` chỉ đăng ký công tắc lỗi có sẵn trong bộ nhớ; không phải logic để gate nhận diện tên variant.
3. Sinh `src/reports/m1_trace_evidence.json`, run ID `M1-trace-862f3ea8ac8f`: 12 case chẩn đoán cho FM-01 đến FM-08, cùng 15 đối chứng fixed. Các đối chứng gồm toàn bộ 14 claim ở seed 11 và C-002 ở seed 55; tất cả đều PASS bộ chấm Lab 8.
4. Hoàn thành `docs/failure_taxonomy.md`: định nghĩa, layer, bằng chứng, event sai đầu tiên và grader/metric dự kiến cho 8 kiểu lỗi đã tái hiện. FM-09 được giữ đúng mã và tên của đề; hiện chỉ có đối chứng chặn truy cập ở C-005, chưa nhận là đã tái hiện lỗi v2.
5. Điền mã lỗi theo ma trận trong `src/lab9/evalset.py`, build lại 14 item và giữ nguyên nhãn riêng. `checked_by` ghi rõ trợ lý replay trace nào; chỉ điền khi có report khớp SHA của nguồn. Không thay đổi các quy tắc kiểm tra của đề.
6. Hoàn thành `docs/trace_case.md` cho `seeded_regression C-002@11`: event 3 ghi đè DB từ 2 ngày thành 5 ngày, dẫn tới hoàn 20.000đ thay vì 0đ. Đối chứng fixed giữ đúng DB và từ chối hoàn tiền.
7. Thêm `src/tests/test_lab9_trace_case.py`, dùng grader `DbFactKept` đã có sẵn. Test phát hiện đúng trace lỗi ở seeded_regression/11 và swarm/55, đồng thời cho qua fixed/11, fixed/55 và swarm/11.

### Kết quả kiểm tra M1

| Kiểm tra | Kết quả thực tế |
|---|---|
| `python -m lab9.m1_evidence` | Exit 0; sinh report; 15/15 đối chứng fixed PASS |
| `python -m lab9.evalset --build --check` | 14 item, 14 nhãn; `0 problem(s)`; SHA eval set `8b262652f4bf` |
| `python -m pytest -q -o addopts= tests/test_lab9_evalset.py tests/test_lab9_trace_case.py` | **8 passed**: 3 test eval set có sẵn và 5 trường hợp regression mới |
| Kiểm tra cuối M1 | 14/14 item có mã FM và checked_by; nhãn giữ nguyên; 63/63 tệp nguồn Day 8 khớp bản gốc; `git diff --check` sạch |

Điểm đáng chú ý: FM-08 ở C-008 báo đã hoàn 35.000đ nhưng ledger chỉ ghi 20.000đ. Bộ chấm Lab 8 vẫn PASS case này. Đây là bằng chứng cần thêm grader kiểm tra reply với ledger ở M3, không phải kết luận metric đó đã hoàn thành.

Đề nhắc tới 5 anchor được đối chiếu bằng `instructor/coding_sheet_anchor_key.csv`, nhưng key này không có trong repo công khai. Trợ lý đã ghi rõ event và mã FM cho các case đã chạy, chưa khẳng định đối chiếu được key riêng của giảng viên.

### Việc bạn cần làm sau M1

- Đọc bảng trong `docs/trace_case.md` để hiểu vì sao event 3 là bước sai đầu tiên, còn việc ghi tiền là hậu quả. Có thể tự chạy lại hai lệnh trace trong tài liệu để kiểm tra.
- Nếu lớp có phát phiếu hoặc danh sách 5 anchor riêng, đối chiếu các claim/seed trong phiếu với bảng taxonomy. Không tự đánh dấu đã khớp key khi chưa có thông tin đó.
- Xác nhận đã bật GitHub Actions và kiểm tra hạn nộp trên LMS như hướng dẫn M0.
- Bạn đã xem kết quả và đồng ý cho commit M1, thực hiện M2. Trợ lý sẽ lưu M1 trên máy trước khi sửa phần M2; chưa push.

### Cách tái hiện M1 trên máy

Từ thư mục gốc repo, mở PowerShell và chạy:

```powershell
cd src
$labPython = '\\?\' + (Join-Path (Get-Location).Path '.venv\Scripts\python.exe')
& $labPython -m lab9.m1_evidence
& $labPython -m lab9.evalset --build --check
& $labPython -m pytest -q -o addopts= tests/test_lab9_evalset.py tests/test_lab9_trace_case.py
```

Chạy script evidence trước khi build để `checked_by` có thể dẫn đúng các đối chứng vừa kiểm tra. Report do script sinh bị `.gitignore` bỏ qua; bạn đã đồng ý force-add đúng report này khi commit M1. Không sửa tay report.

## Trạng thái các mốc

| Bước | Việc cần làm theo đề | Trạng thái |
|---|---|---|
| M1 | Taxonomy ít nhất 5 FM, phân tích trace, gắn failure_modes và kiểm tra eval set | Các kiểm tra công khai đã đạt; chưa đối chiếu key 5 anchor riêng; bạn đã duyệt commit |
| M2 | Confusion, precision/recall, kappa, Rogan–Gladen và audit ít nhất 5 bất đồng | Bạn đã đồng ý; chuẩn bị thực hiện sau commit M1 |
| M3 | Hai grader TODO và metric FM-08; regression test FM-03 đã có ở M1 | Chưa xin phép thực hiện grader/metric |
| M4 | Paired bootstrap, baseline swarm, fixed qua gate, seeded_regression bị chặn | Chưa xin phép thực hiện |
| Tài liệu Core | Eval card, PRD v1.1 và section eval trong harness_map | Chưa xin phép thực hiện |
| M5–M6 | Eval set v2, slice gate, pass@k/pass^k và A/A | Chưa xin phép thực hiện |
| M7 | Integrity check, ratchet và kiểm tra traps | Chưa xin phép thực hiện |
| Nộp bài | Commit report, push, PR trong fork, CI xanh, merge main và nộp link trên LMS | Chưa xin phép thực hiện |

Không chỉnh sửa `src/lab8/` sau khi chép từ nguồn gốc; không sửa tay report; không đưa nhãn đáp án vào item. Chỉ sinh baseline sau khi đã hoàn thành các bước cần thiết của Core.
