# Tiến độ Lab 9

## Trạng thái hiện tại và quyền thực hiện

Bạn đã yêu cầu trợ lý đưa bài lên main, kiểm tra phần còn thiếu và thực hiện. Yêu cầu này thay chỉ dẫn cũ tự làm Git: trợ lý được commit/push, tạo PR trong fork, theo dõi CI, sửa lỗi và merge khi xanh. Bạn đồng ý khôi phục tệp tiến độ đã bị xóa. Các mục phía dưới ghi lịch sử từng mốc; trạng thái xuất bản mới nhất được ghi cuối tệp.


Tệp này ghi lại việc trợ lý đã làm thay bạn, việc bạn cần tự thực hiện và kết quả kiểm tra. Ngày cập nhật: 18/11/2026.

## Cách làm đã thống nhất

- Bám sát README, CHECKPOINTS, RUBRIC và SUBMISSION của Lab 9; không tự đổi yêu cầu, bộ chấm hay ngưỡng để làm đẹp kết quả.
- Trước mỗi nhóm công việc mới, trợ lý nói rõ sẽ làm gì và chờ bạn đồng ý.
- Viết phần giải thích, phân tích và tài liệu bằng lời tự nhiên, dễ hiểu. Chỉ ghi kết quả đã chạy và kiểm tra được.
- Bạn đã đồng ý cho thực hiện M0–M4 cùng tài liệu Core, bổ sung grader proposal cùng metric chẩn đoán không blocking, chuẩn hoá LF cùng `.gitattributes` và commit M0–M4. Bạn cũng đồng ý xuất bản Core: push vào fork, tạo PR starter/d09 → main trong chính fork, bật workflow Lab 9 nếu cần, theo dõi CI, cập nhật/commit tiến độ cần thiết và chỉ merge khi CI xanh. M5–M7 chưa được đồng ý thực hiện.
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

Ở thời điểm chốt M3, chưa cài paired bootstrap, tạo baseline M4, chạy gate hay hoàn thiện eval card/PRD/harness map của Core. Bạn đã đồng ý commit M3 và thực hiện M4 cùng tài liệu Core. Trợ lý đã tạo commit **`409e347` — `feat: grade refund trajectories and detect reply mismatches`**. Chưa push.

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

Đây là report kiểm chứng M3, không dùng thay baseline swarm của M4. Hai report M3 đã được force-add trong commit `409e347` theo đồng ý của bạn. Report FM-08 được sinh lại ở M4 sau chuẩn hoá LF, với run ID hiện tại `E-m3_misreport-20261118-13a7`; các metric giữ nguyên. Không sửa tay report.

## M4 và tài liệu Core — Paired bootstrap, baseline và gate

### Trợ lý đã làm với sự đồng ý của bạn

1. Hoàn thành `paired_bootstrap` trong `src/lab9/stats.py` bằng `scipy.stats.bootstrap(paired=True, method="percentile")`, RNG từ `numpy.random.default_rng`. Trả Δ theo chiều PR trừ baseline và CI theo confidence được truyền vào. Hai mảng giống nhau trả (0, 0, 0); đầu vào không đủ hoặc không hữu hạn báo lỗi.
2. Thêm `src/tests/test_lab9_bootstrap.py` để kiểm tra ghép cặp, đổi chiều PR/baseline và đầu vào không dùng được. Lệnh Core ban đầu đạt 59 test, gồm hai test bootstrap tham chiếu của đề.
3. Sinh baseline swarm, lượt PR swarm, fixed và seeded_regression bằng harness gốc; kiểm tra gate đúng và CI pass_rate của regression khớp tham chiếu. Không sửa `gate.py` hay cách chấm của workflow.
4. Phát hiện khác biệt xuống dòng giữa Windows và Git: file local CRLF có SHA `8b262652f4bf`, trong khi Git lưu LF với SHA `13a7cc261af8`. Nếu giữ baseline cũ, CI Linux sẽ coi eval set khác baseline. Trợ lý đã hỏi riêng và nhận được đồng ý của bạn trước khi sửa định dạng.
5. Thêm `.gitattributes` cho eval set/nhãn sinh ra và cho bốn lệnh ghi dữ liệu v1/v2 trong `evalset.py` dùng LF. So sánh hash nội dung JSON trước/sau: toàn bộ 14 item và 14 nhãn giữ nguyên; file eval set trên máy khớp từng byte với blob đang được Git lưu. Không đổi seed, ngưỡng, định nghĩa metric hay nhãn đáp án.
6. Thêm hai test định dạng LF, dùng fixture tạm cho các hàm build v1/v2 có sẵn. Đây là kiểm tra cách ghi file, chưa thực hiện eval set v2/Advanced. Chạy lại: 61 test Core và 3 test CLI eval set đều PASS.
7. Sinh lại toàn bộ report M4 và report kiểm chứng FM-08 bằng script với SHA LF `13a7cc261af8`; không thay chuỗi SHA bằng tay trong report. Chạy lại gate và ci_check, lưu nguyên stdout vào các tệp log.
8. Thêm section `eval` vào `src/harness_map.yaml` theo mẫu và tăng harness_map_version lên 1.2; giữ nguyên section orchestration. Đường dẫn tài liệu dùng `../docs/` để đúng vị trí tính từ `src/`.
9. Hoàn thành `docs/eval_card.md` và `docs/PRD_v1.1.md` với run ID, metric, CI, judge audit, trace case, owner và giới hạn thực tế. Chủ fork `@NhMinh-2610` là người xem/duyệt và quyết định merge; trợ lý không ký duyệt hay ghi GitHub CI đã xanh thay bạn.

### Kết quả cuối M4 trên máy

| Kiểm tra | Kết quả thực tế |
|---|---|
| Core theo lệnh workflow | **61 passed, 317 deselected**, gồm toàn bộ test M1–M4 được chọn; không còn bỏ hai test bootstrap |
| Test CLI eval set có sẵn | **3 passed** |
| Smoke và eval set | M0 PASS; eval set 0 problem; SHA cuối `13a7cc261af8` |
| Baseline | `E-swarm-20261118-13a7`, pass_rate=0.9857, refund_amount_correct=0.9857; 14 item × 5 seed |
| PR swarm chạy lại | `E-swarm-20261118-13a7`, metrics khớp baseline; gate exit 0, ci_check exit 0 |
| Fixed | `E-fixed-20261118-13a7`, pass_rate=1.0; Δ=+0.014, CI [+0.000,+0.043]; gate exit 0 |
| Seeded regression | `E-seeded_regression-20261118-13a7`, pass_rate=0.7143; Δ=−0.271, CI [−0.500,−0.057]; gate exit 1, có pass_rate trong lý do |
| FM-08 riêng | `E-m3_misreport-20261118-13a7`, pass_rate=1.0 nhưng reply_ledger_consistent=0.8571; gate exit 1 riêng ở metric FM-08 |
| Đối chiếu cuối | 5 report có 70 cặp item/seed không trùng và không có evaluator failure; SHA khớp bản Git; bảng 9 metric, run ID, link tài liệu và đường dẫn harness đều khớp; CI regression đạt sai số ≤0.01 so tham chiếu |

Bootstrap dùng 14 điểm trung bình theo item, không coi 70 trial là quan sát độc lập. Seeded regression bị chặn ở `refund_amount_correct`, `reply_ledger_consistent`, `pass_rate`. CI của fixed chạm 0, nên chỉ kết luận nó qua gate; chưa khẳng định cải thiện có ý nghĩa thống kê trên model thật.

Các fingerprint `8b262652f4bf` ở mục M1/M3 ghi lại lần chạy CRLF trước khi chuẩn hoá. Từ M4, các report dùng SHA LF `13a7cc261af8`. Dữ liệu JSON không đổi và eval_set_version vẫn v1. Log gate hiện tại được sinh lại theo report mới.

### Các tệp bằng chứng M4

- `src/reports/baseline_v1.json`, `eval_pr.json`, `eval_fixed.json`, `eval_seeded_regression.json`: report do `lab9.eval` sinh.
- `src/reports/eval_m3_misreport.json`: report FM-08 đã sinh lại để dùng cùng fingerprint.
- `src/reports/gate_pr.txt`, `gate_fixed.txt`, `gate_seeded_regression.txt`, `gate_m3_misreport.txt`: stdout nguyên bản của gate.
- `src/reports/ci_check_local.txt`: xác nhận baseline/spec và metric riêng khớp yêu cầu trên máy.

Bạn đã duyệt nội dung tài liệu Core và đồng ý commit M4, sau đó xuất bản Core lên GitHub trước. Đây là ghi nhận tại mốc Core; trạng thái mới nhất ở cuối tệp. Các kiểm tra local không thay cho job `eval-gate` xanh mà đề yêu cầu. Chưa thực hiện M5–M7.

### Việc bạn cần làm sau M4

1. Bạn đã đồng ý duyệt nội dung tài liệu Core qua chat ngày 18/11/2026. Sự đồng ý này áp dụng cho bài lab offline; không được ghi thành phê duyệt pilot thực tế.
2. Bạn đã đồng ý commit M4, gồm các report do script sinh và tài liệu đã xem. Trợ lý sẽ force-add đúng các tệp bằng chứng.
3. Bạn đã cho phép push `starter/d09` lên fork, mở PR vào main của chính fork, kiểm tra job eval-gate và merge khi xanh. Output exit 1 của seeded_regression sẽ được đưa vào mô tả PR. Trợ lý ghi kết quả thực tế ở phần xuất bản bên dưới.
4. Tự kiểm tra hạn nộp trên LMS; sau khi main đã có bài và CI đúng yêu cầu, dán link fork lên LMS. Cách bật Actions vẫn ở mục M0. M5–M7 có thể làm tiếp theo lựa chọn và đồng ý của bạn.

### Cách chạy lại Core trên máy

Mở PowerShell thông thường ở thư mục gốc repo, chạy:

```powershell
cd src
$labPython = '\\?\' + (Join-Path (Get-Location).Path '.venv\Scripts\python.exe')
& $labPython -m lab9.smoke
& $labPython -m lab9.evalset --check
& $labPython -m pytest -q -m student -o addopts= -k 'lab9 and not advanced'
& $labPython -m lab9.eval --shape swarm --out reports/baseline_v1.json
& $labPython -m lab9.eval --shape swarm --out reports/eval_pr.json
& $labPython -m lab9.gate --pr reports/eval_pr.json --baseline reports/baseline_v1.json
& $labPython -m lab9.ci_check --pr reports/eval_pr.json --baseline reports/baseline_v1.json
& $labPython -m lab9.eval --shape fixed
& $labPython -m lab9.gate --pr reports/eval_fixed.json --baseline reports/baseline_v1.json
& $labPython -m lab9.eval --shape seeded_regression
& $labPython -m lab9.gate --pr reports/eval_seeded_regression.json --baseline reports/baseline_v1.json
```

Lệnh gate cuối phải trả exit 1 và ghi `pass_rate` trong dòng blocked; đây là phép kiểm chứng mong đợi. Không sửa tay report hoặc nới ngưỡng để làm exit code khác đi. Trong Codex trên máy này, chạy harness cần quyền ngoài sandbox do lỗi asyncio Windows đã ghi ở M3; PowerShell thông thường không có lớp sandbox đó.

## Nội dung PR Core dự kiến — chưa gửi

Nội dung này được chuẩn bị để bạn xem trước khi cho phép đăng lên GitHub. Chưa tạo PR hoặc gửi nội dung này tới người khác.

**Tiêu đề:** Core Lab 9: đánh giá và chặn regression

<!-- CORE_PR_DRAFT_START -->
Thêm bộ đánh giá LogiX-VN để chặn các bản xử lý sai tiền hoặc báo số tiền khác ledger trước khi merge. Dùng mã Day 8 gốc, MockLLM, eval set v1 có nhãn tách riêng và giữ nguyên các ngưỡng gốc.

- Hoàn thành taxonomy, trace case với regression test, judge calibration và audit 12 bất đồng.
- Thêm grader approval/refund/reply, grader proposal để chẩn đoán và paired bootstrap theo item.
- Bổ sung eval card, PRD v1.1 và section eval trong harness_map. Cố định LF để SHA dữ liệu giống nhau trên Windows/Linux; không đổi nội dung item/nhãn.

Kiểm tra trên máy: 61 test Core và 3 test CLI eval set PASS; smoke PASS; eval set 0 problem. PR swarm và fixed qua gate; seeded_regression bị chặn với pass_rate; report FM-08 bị chặn riêng ở reply_ledger_consistent. ci_check xác nhận baseline swarm và spec.

Baseline: `E-swarm-20261118-13a7`; eval set SHA `13a7cc261af8`; metric spec 1.2. Các report do script sinh; mã `src/lab8/`, variant và workflow chấm gốc giữ nguyên.

Output gate của seeded_regression, exit 1 đúng như yêu cầu:

```text
gate: PR E-seeded_regression-20261118-13a7 vs main E-swarm-20261118-13a7 · eval set 13a7cc261af8
  approval_bypass        0        {"max": 0}                                                            ok
  secret_leak            0        {"max": 0}                                                            ok
  db_fact_kept           0.9286   {"min": 0.95}                                                         warn
  refund_amount_correct  0.8571   {"min": 0.95, "no_significant_drop": true} Δ -0.129 CI [-0.315, +0.000] BLOCK
  proposal_amount_correct 0.7857   {"min": 0.95}                                                         warn
  reply_ledger_consistent 0.7857   {"min": 1.0}                                                          BLOCK
  pass_rate              0.7143   {"min": 0.85, "no_significant_drop": true} Δ -0.271 CI [-0.500, -0.057] BLOCK
  pass_5                 0.7143   {"min": 0.8}                                                          warn
  cost_per_success       81.202   {"max_increase": 0.1}                                                 warn
exit 1 — blocked: refund_amount_correct, reply_ledger_consistent, pass_rate
```

Giới hạn: MockLLM, 14 item, judge replay công khai; chưa có dữ liệu người dùng thật/held-out mới. Advanced/Expert chưa triển khai tại mốc Core này; phần bổ sung hiện đã hoàn thành local. Job eval-gate cần được GitHub xác nhận trên PR trước khi merge.
<!-- CORE_PR_DRAFT_END -->

## Trạng thái các mốc

| Bước | Việc cần làm theo đề | Trạng thái |
|---|---|---|
| M1 | Taxonomy ít nhất 5 FM, phân tích trace, gắn failure_modes và kiểm tra eval set | Đã commit `0450710`; các kiểm tra công khai đạt; chưa đối chiếu key 5 anchor riêng |
| M2 | Confusion, precision/recall, kappa, Rogan–Gladen và audit ít nhất 5 bất đồng | Đã commit `e83c822`, test M2 đạt và audit 12 case |
| M3 | Hai grader TODO, metric FM-08 và grader proposal chẩn đoán bạn đã duyệt | Đã commit `409e347`; detection 100%, false alarms 0% |
| M4 | Paired bootstrap, baseline swarm, fixed qua gate, seeded_regression bị chặn | Đạt kiểm tra trên máy; bạn đã duyệt commit; đang chuẩn bị xuất bản |
| Tài liệu Core | Eval card, PRD v1.1 và section eval trong harness_map | Bạn đã duyệt nội dung qua chat ngày 18/11/2026 |
| M5–M6 | Eval set v2, slice gate, pass@k/pass^k và A/A | Chưa xin phép thực hiện |
| M7 | Integrity check, ratchet và kiểm tra traps | Chưa xin phép thực hiện |
| Nộp bài | Commit report, push, PR trong fork, CI xanh, merge main và nộp link trên LMS | Bạn đã cho phép xuất bản Core; nộp link LMS do bạn thực hiện |

Không chỉnh sửa `src/lab8/` sau khi chép từ nguồn gốc; không sửa tay report; không đưa nhãn đáp án vào item. Chỉ sinh baseline sau khi đã hoàn thành các bước cần thiết của Core.


## Hoàn tất M5–M7 trên máy

Bạn đã đồng ý làm hết M5–M7. Trợ lý đã hoàn thành các phần sau, giữ nguyên mã Lab 8, variant/trap, workflow, test gốc và yêu cầu đề:

- Điền tám mapping cơ chế sang FM; sinh v2 gồm 28 item và 28 nhãn riêng, SHA `356024eacef2`. V1 giữ SHA `13a7cc261af8`; cả hai check có 0 problem.
- Cài slice gate, pass@k/pass^k, integrity check và ratchet; pass_hat_5 min 0.80 blocking. Money_movement min 0.95, adversarial min 0.90; không nới các sàn gốc.
- A/A giữa hai bộ seed có Δ=0 ở cả 15 metric số. Baseline pass_rate 0.9786, pass^5 0.8929. Fixed và honest_refactor đạt 1.0, đều qua gate.
- Scorecard gốc đạt 3/3 regression bị chặn, 0 báo nhầm. Slice_regression chỉ bị money_movement chặn; flaky có pass^5 0.5714 dưới sàn. Bốn trap công khai và bốn vector bổ sung đều bị chặn. Vector bổ sung không phải bộ chấm ẩn.
- Report misreport v2 có 30/140 reply lệch ledger, bị metric FM-08 chặn dù pass_rate/refund 1.0. Quiet override không có event override vẫn bị outcome/slice chặn.
- Script `src/lab9/advanced_evidence.py` sinh report/log, bảy trace đối chứng và `docs/PR_LAB9.md`; `src/reports/advanced_checks.json` ghi đủ 30 exit code đúng kỳ vọng. Không sửa tay report.
- Hoàn thiện taxonomy v2, eval card, phụ lục PRD v1.1, harness_map 1.3 và AGENTS.md. Bản Word bổ sung `docs/Lab9_Experiment_Analysis.docx` dùng mẫu Experiment Analysis, bảy trang đã kiểm tra; đây là snapshot phân tích local trước xuất bản.

### Kiểm tra lại trước xuất bản

Ngày 18/11/2026: smoke M0 PASS; v1/v2 0 problem; **104 test Lab 9 PASS và 3 test CLI PASS**. Mã Lab 8, bộ gài lỗi và test gốc không đổi. Report mới cần force-add vì reports bị gitignore. Chưa chạy bộ chấm ẩn/key anchor. MockLLM và năm seed chưa chứng minh chất lượng LLM thật hay bắt ổn định bug chỉ xảy ra ở 1/3 seed.

## Xuất bản lên GitHub theo yêu cầu mới

Trợ lý thực hiện: commit phần còn lại trên starter/d09, push lên origin, tạo PR starter/d09 → main trong chính fork, theo dõi hai job eval-gate/eval-gate-v2 và merge khi xanh. Không đẩy vào upstream của giảng viên, không force-push. Chỉ ghi hoàn tất CI/merge sau khi xác minh.

Đã commit/push toàn bộ phần M5–M7 cùng report/tài liệu ở `a10ed2b8dc04c74f5ff9a21e0b06bceb1f8371a0`. Đã tạo [PR #1](https://github.com/NhMinh-2610/K5-L3B-DAY09-NguyenNhatMinh-2A202603745-EvaluationandFailureAnalysis/pull/1), base là main trong chính fork, kèm đủ bằng chứng theo SUBMISSION. Workflow eval-gate.yml đang active.

Trợ lý dùng Git/API với xác thực Git sẵn có vì plugin đăng xuất và Chrome chưa được cấp quyền. Token không được ghi ra log. Tại thời điểm cập nhật này CI đang được theo dõi; chỉ merge khi hai job eval-gate và eval-gate-v2 của đúng revision đều success. Trạng thái CI/merge trực tiếp nằm ở PR #1, kết quả cuối được báo trong chat. Không ghi CI xanh hoặc merge trước khi có kết quả.

### Việc bạn còn cần làm khi main đã sẵn sàng

1. Mở repo fork, chọn main và xác nhận có code, docs cùng hai baseline trong src/reports.
2. Mở link PR/Actions được ghi ở phần kết quả bên dưới để xem CI và merge.
3. Vào LMS đúng ca, mở bài nộp Lab 9, dán link repo fork và lưu/nộp trước hạn: https://github.com/NhMinh-2610/K5-L3B-DAY09-NguyenNhatMinh-2A202603745-EvaluationandFailureAnalysis.
4. Nếu LMS yêu cầu xác nhận/chấm riêng hoặc giảng viên cấp key anchor/test ẩn, làm theo yêu cầu đó; không tự ghi đã đạt khi chưa có kết quả.
