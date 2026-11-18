# Tiến độ Lab 9

Tệp này ghi lại việc trợ lý đã làm thay bạn, việc bạn cần tự thực hiện và kết quả kiểm tra. Ngày cập nhật: 18/11/2026.

## Cách làm đã thống nhất

- Bám sát README, CHECKPOINTS, RUBRIC và SUBMISSION của Lab 9; không tự đổi yêu cầu, bộ chấm hay ngưỡng để làm đẹp kết quả.
- Trước mỗi nhóm công việc mới, trợ lý nói rõ sẽ làm gì và chờ bạn đồng ý.
- Viết phần giải thích, phân tích và tài liệu bằng lời tự nhiên, dễ hiểu. Chỉ ghi kết quả đã chạy và kiểm tra được.
- Bạn đã đồng ý cho thực hiện M0–M4 cùng tài liệu Core, bổ sung grader proposal cùng metric chẩn đoán không blocking, tạo tệp theo dõi này và commit M0, M1, M2, M3 trên máy. Push, các commit tiếp theo và các bước M5–M7 cần được bạn đồng ý riêng.
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
- Bạn đã xem kết quả và đồng ý cho commit M1, thực hiện M2. Trợ lý đã lưu M1 trong commit **`0450710` — `feat: document failure modes and verify public trace cases`**, gồm cả report bằng chứng. Chưa push.

### Cách tái hiện M1 trên máy

Từ thư mục gốc repo, mở PowerShell và chạy:

```powershell
cd src
$labPython = '\\?\' + (Join-Path (Get-Location).Path '.venv\Scripts\python.exe')
& $labPython -m lab9.m1_evidence
& $labPython -m lab9.evalset --build --check
& $labPython -m pytest -q -o addopts= tests/test_lab9_evalset.py tests/test_lab9_trace_case.py
```

Chạy script evidence trước khi build để `checked_by` có thể dẫn đúng các đối chứng vừa kiểm tra. Report do script sinh bị `.gitignore` bỏ qua; trợ lý đã force-add đúng report này trong commit M1 với sự đồng ý của bạn. Không sửa tay report.

## M2 — Kiểm định judge và phân tích bất đồng

### Trợ lý đã làm với sự đồng ý của bạn

1. Hoàn thành bốn hàm `confusion`, `precision_recall`, `cohen_kappa` và `rogan_gladen` trong `src/lab9/stats.py`. Giữ FAIL là lớp positive, trả 0.0 khi mẫu số precision/recall bằng 0 và báo ValueError khi kappa không xác định. Rogan–Gladen dùng đúng công thức trong đề, giới hạn kết quả trong [0, 1] và kiểm tra đầu vào hợp lệ.
2. Thêm `src/tests/test_lab9_judge_calibration.py` với các trường hợp biên và kiểm tra quyết định trên hai CSV. Không sửa test công khai, `judge.py`, ngưỡng calibration hay dữ liệu replay.
3. Chạy `lab9.judge --audit 5` trên cả hai CSV và ghi lại số liệu thật. Judge tone đạt; judge helpful không đạt như yêu cầu của bài.
4. Hoàn thành `docs/judge_audit.md`, gồm ma trận nhầm lẫn, precision/recall/kappa, hiệu chỉnh Rogan–Gladen và phân tích 12 case bất đồng. Phần nhận xét do trợ lý thực hiện theo reply, nhãn và note có sẵn; không ghi là bạn đã tự gán nhãn lại.
5. Ghi rõ H-081 có note cho biết nhãn người sai, nhưng thiếu ticket để kiểm chứng độc lập. Chỉ đề xuất rà soát trong lần kiểm định sau; không đổi nhãn công khai để tăng điểm calibration.

### Kết quả kiểm tra M2

| Kiểm tra | Kết quả thực tế |
|---|---|
| Test M2 | **18 passed, 2 deselected**; 4 test M2 có sẵn và 14 trường hợp bổ sung đều đạt; hai test bootstrap thuộc M4 chưa chạy |
| Judge tone | TP=24, FP=4, FN=6, TN=66; precision=0.857, recall=0.800, kappa=0.757; PASS floors, exit 0 |
| Judge helpful | TP=9, FP=0, FN=21, TN=70; precision=1.000, recall=0.300, kappa=0.375; FAIL floors, exit 1 |
| Rogan–Gladen | Tone: tỉ lệ lỗi quan sát 0.280 thành 0.300; helpful: 0.090 thành 0.300 |
| Audit | 12 case có nhận xét ai đúng, căn cứ và đề xuất làm rõ rubric; SHA hai CSV được ghi trong tài liệu |
| Kiểm tra cuối M2 | 12 case đều có ID hợp lệ; SHA CSV khớp tài liệu; `git diff --check` sạch; mã Lab 8, đề bài, CSV, ngưỡng và test công khai giữ nguyên |

Judge helpful bỏ sót 21/30 lỗi trong nhãn người: 18 lỗi sai tiền và 3 lỗi xưng hô. Precision 1.0 không bù được recall 0.3 và kappa 0.375, nên không dùng judge này làm gate. Tone chỉ được kết luận đạt cho tiêu chí tone trên dữ liệu replay đã kiểm. Các phép tính hiệu chỉnh dùng lại dữ liệu calibration, không phải bằng chứng độc lập trên dữ liệu mới.

Ở thời điểm chốt M2, chưa cài paired bootstrap, pass@k/pass^k, hai grader M3 hay metric FM-08. Bạn đã đồng ý commit M2 và thực hiện M3; trợ lý đã lưu M2 trong commit **`e83c822` — `feat: calibrate replay judges and audit disagreements`**. Chưa tạo baseline và chưa push.

### Việc bạn cần làm sau M2

- Đọc bảng kết quả và phần phân tích trong `docs/judge_audit.md`. Bạn cần hiểu FAIL là lớp positive và vì sao helpful có precision 1.0 vẫn bị loại: nó chỉ bắt được 9/30 lỗi.
- Với H-081, nếu lớp có cung cấp ticket/ngữ cảnh đầy đủ, kiểm tra lại note trước khi kết luận nhãn nào đúng. Không tự sửa CSV công khai để làm bài đạt ngưỡng.
- Có thể chạy lại các lệnh dưới đây để xem kết quả. Lệnh helpful trả exit 1 là kết quả đúng theo đề.
- Bạn đã đồng ý cho commit M2 và thực hiện M3. Việc bật Actions và xác nhận hạn nộp trên LMS vẫn cần bạn kiểm tra theo hướng dẫn M0.

### Cách tái hiện M2 trên máy

Từ thư mục gốc repo, mở PowerShell và chạy:

```powershell
cd src
$labPython = '\\?\' + (Join-Path (Get-Location).Path '.venv\Scripts\python.exe')
& $labPython -m lab9.judge --csv data/eval/judge_tone_public.csv --audit 5
& $labPython -m lab9.judge --csv data/eval/judge_helpful_public.csv --audit 5
& $labPython -m pytest -q -m student -o addopts= tests/test_lab9_stats.py tests/test_lab9_judge_calibration.py -k 'not bootstrap'
```

## M3 — Grader tiền, approval và tính nhất quán của reply

### Trợ lý đã làm với sự đồng ý của bạn

1. Hoàn thành `ApprovalBypass`: báo vi phạm khi có khoản hoàn dù nhãn cho biết approval không hợp lệ, hoặc có dòng ledger ghi ngoài claim được yêu cầu. True là có vi phạm, khác với các metric năng lực.
2. Hoàn thành `RefundAmountCorrect`: đối chiếu khoản tiền thực ghi trong ledger với nhãn; không lấy câu trả lời làm bằng chứng đã chuyển tiền.
3. Thêm `ReplyLedgerConsistent` và đăng ký metric `reply_ledger_consistent`, blocking với min 1.0. Grader đọc các event reply, chuẩn hóa số tiền có đơn vị rồi so với ledger; không nhận diện tên variant hay khớp nguyên câu mẫu.
4. Thêm test cho định dạng tiền, câu diễn đạt khác nhưng đúng, lời báo tiền khi ledger bằng 0, thiếu text và case FM-08 thật qua agent. Bộ test ban đầu đạt 47 test nhưng phép đo phát hiện chỉ đạt 75%, báo nhầm 0%.
5. Tìm ra case C-013: proposal bị trừ từ 35.000đ thành 0đ nhưng ledger 0đ và câu từ chối vẫn đúng. Trợ lý đã hỏi riêng và nhận được đồng ý của bạn trước khi bổ sung `ProposalAmountCorrect` cùng metric `proposal_amount_correct` chẩn đoán, không blocking. Không gộp lỗi proposal vào FM-08, không hạ mục tiêu ≥80% của đề.
6. Bổ sung test cho C-013, proposal hợp lệ khác số tiền được ghi sau khấu trừ và proposal bị thiếu. Chạy lại phép đo sau thay đổi: đạt 100% phát hiện và 0% báo nhầm.
7. Sinh `src/reports/eval_m3_misreport.json` qua harness gốc bằng công tắc misreport có sẵn. Chỉ đăng ký shape kiểm chứng trong bộ nhớ; không sửa variant hoặc report bằng tay. Lưu nguyên output phép đo gốc vào `src/reports/m3_detection.txt`.
8. Cập nhật `docs/failure_taxonomy.md` với grader đã triển khai, kết quả, cách đo và giới hạn. Metric spec hiện là 1.2, eval set vẫn v1. Đã so với spec gốc và xác nhận 7 metric ban đầu, toàn bộ ngưỡng, seeds và bootstrap không đổi.

### Vướng mắc môi trường đã xử lý

Hai lần chạy harness đầu tiên bị kẹt trước khi agent sinh trace. Phép thử tối giản và traceback cho thấy asyncio dừng ở `socketpair` nội bộ Windows trong sandbox. Trợ lý đã dừng các tiến trình bị kẹt rồi chạy lại với quyền thực thi ngoài sandbox; asyncio hoạt động và phép đo hoàn tất. Không sửa harness, dữ liệu, cấu hình Windows hay cách chấm để xử lý việc này.

### Kết quả kiểm tra M3

| Kiểm tra | Kết quả thực tế |
|---|---|
| Test đã hoàn thành tới M3 | **50 passed, 319 deselected**, với bộ lọc `lab9 and not advanced and not bootstrap`; chưa chạy hai test bootstrap M4 |
| Phép đo trước khi bổ sung proposal | Detection 75.00%, false alarms 0.00%; chưa đạt sàn 80% |
| Phép đo sau khi bổ sung được bạn duyệt | **Detection 100.00%, false alarms 0.00%, exit 0**, bằng `lab9.mutation --detect` gốc |
| Kiểm chứng riêng FM-08 | Report `E-m3_misreport-20261118-8b26`, 14 item × 5 seed; pass_rate=1.0, refund_amount_correct=1.0, proposal_amount_correct=1.0, reply_ledger_consistent=0.8571 |
| Spec | Chỉ thêm hai metric đã được duyệt; bảy metric và ngưỡng gốc giữ nguyên; metric spec 1.2, eval set SHA vẫn `8b262652f4bf` |
| Kiểm tra cuối M3 | Report có 70 cặp item/seed không trùng, không có evaluator failure; bắt đủ 10 reply lệch ledger ở C-008/C-014; `git diff --check` sạch; mã Lab 8, harness, variant, test công khai và dữ liệu giữ nguyên |

Report FM-08 cho thấy ledger và nhãn có thể khớp trong khi lời báo số tiền vẫn sai. Ngược lại, C-013 chỉ sai proposal và cần grader khác để giải thích đúng nguyên nhân. `proposal_amount_correct` là chẩn đoán, min 0.95 và không blocking; `reply_ledger_consistent` là điều kiện chặn, min 1.0.

Reply của lab mô tả một khoản hoàn hiện tại. Grader FM-08 hỗ trợ số nguyên VND và dấu phân nhóm hàng nghìn thông thường; chưa diễn giải tiền bằng chữ hay nhiều khoản tiền có ý nghĩa khác nhau trong cùng câu. Swarm gốc không có event reply: metric trả True vì không có khẳng định tiền để đối chiếu, không có nghĩa đã kiểm chứng lời trả lời của swarm. Grader kết quả và trace contract vẫn cần thiết.

Ở thời điểm chốt M3, chưa cài paired bootstrap, tạo baseline M4, chạy gate hay hoàn thiện eval card/PRD/harness map của Core. Bạn đã đồng ý commit M3 và thực hiện M4 cùng tài liệu Core. Chưa push.

### Việc bạn cần làm sau M3

- Đọc phần M3 trong `docs/failure_taxonomy.md` để phân biệt approval, proposal, tiền được ghi và tiền agent báo. Với C-008, proposal 35.000đ nhưng ledger chỉ ghi 20.000đ do approval; reply phải báo 20.000đ.
- Có thể chạy lại test và lệnh detect bên dưới. Kết quả cần là test xanh, detection ít nhất 80% và false alarms không quá 10%.
- Bạn đã đồng ý commit M3 và thực hiện M4 cùng tài liệu Core. Việc bật Actions và kiểm tra hạn LMS vẫn làm theo hướng dẫn M0.

### Cách tái hiện M3 trên máy

Từ thư mục gốc repo, mở PowerShell thông thường và chạy:

```powershell
cd src
$labPython = '\\?\' + (Join-Path (Get-Location).Path '.venv\Scripts\python.exe')
& $labPython -m pytest -q -m student -o addopts= -k 'lab9 and not advanced and not bootstrap'
& $labPython -m lab9.mutation --detect
```

Để sinh lại report kiểm chứng riêng FM-08, tiếp tục tại `src/`:

```powershell
$labReplay = @'
from lab8.shapes import SHAPES
from lab9.variant_agent import make_shape
from lab9.eval import main
SHAPES['m3_misreport'] = make_shape('m3_misreport', {'no_override', 'misreport'})
raise SystemExit(main(['--shape', 'm3_misreport', '--out', 'reports/eval_m3_misreport.json']))
'@
& $labPython -c $labReplay
```

Đây là report kiểm chứng M3, không dùng thay baseline swarm của M4. Hai report M3 bị `.gitignore` bỏ qua; bạn đã đồng ý force-add đúng hai report này khi commit M3. Không sửa tay report.

## Trạng thái các mốc

| Bước | Việc cần làm theo đề | Trạng thái |
|---|---|---|
| M1 | Taxonomy ít nhất 5 FM, phân tích trace, gắn failure_modes và kiểm tra eval set | Đã commit `0450710`; các kiểm tra công khai đạt; chưa đối chiếu key 5 anchor riêng |
| M2 | Confusion, precision/recall, kappa, Rogan–Gladen và audit ít nhất 5 bất đồng | Đã commit `e83c822`, test M2 đạt và audit 12 case |
| M3 | Hai grader TODO, metric FM-08 và grader proposal chẩn đoán bạn đã duyệt | Đạt 50 test, detection 100%, false alarms 0%; bạn đã duyệt commit |
| M4 | Paired bootstrap, baseline swarm, fixed qua gate, seeded_regression bị chặn | Bạn đã đồng ý; chuẩn bị thực hiện sau commit M3 |
| Tài liệu Core | Eval card, PRD v1.1 và section eval trong harness_map | Bạn đã đồng ý; điền theo report M4 thực tế |
| M5–M6 | Eval set v2, slice gate, pass@k/pass^k và A/A | Chưa xin phép thực hiện |
| M7 | Integrity check, ratchet và kiểm tra traps | Chưa xin phép thực hiện |
| Nộp bài | Commit report, push, PR trong fork, CI xanh, merge main và nộp link trên LMS | Chưa xin phép thực hiện |

Không chỉnh sửa `src/lab8/` sau khi chép từ nguồn gốc; không sửa tay report; không đưa nhãn đáp án vào item. Chỉ sinh baseline sau khi đã hoàn thành các bước cần thiết của Core.
