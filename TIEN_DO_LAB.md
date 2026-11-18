# Tiến độ Lab 9

Tệp này ghi lại việc trợ lý đã làm thay bạn, việc bạn cần tự thực hiện và kết quả kiểm tra. Ngày cập nhật: 18/11/2026.

## Cách làm đã thống nhất

- Bám sát README, CHECKPOINTS, RUBRIC và SUBMISSION của Lab 9; không tự đổi yêu cầu, bộ chấm hay ngưỡng để làm đẹp kết quả.
- Trước mỗi nhóm công việc mới, trợ lý nói rõ sẽ làm gì và chờ bạn đồng ý.
- Viết phần giải thích, phân tích và tài liệu bằng lời tự nhiên, dễ hiểu. Chỉ ghi kết quả đã chạy và kiểm tra được.
- Bạn đã đồng ý cho thực hiện M0, tạo tệp theo dõi này, commit M0 trên máy và thực hiện M1. Push, các commit tiếp theo và các bước M2–M7 cần được bạn đồng ý riêng.
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

Chưa chạy `evalset --check` vì việc điền `failure_modes` thuộc M1. Chưa sinh baseline M4 và chưa push. Bạn đã duyệt việc commit các tệp M0 trên nhánh `starter/d09`; kết quả commit sẽ được ghi lại ở lần cập nhật tiếp theo.

### Việc bạn cần làm

- Kiểm tra GitHub Actions đã được bật: mở https://github.com/NhMinh-2610/K5-L3B-DAY09-NguyenNhatMinh-2A202603745-EvaluationandFailureAnalysis/actions. Nếu có nút “I understand my workflows, go ahead and enable them”, bấm nút đó. Nếu đã thấy danh sách workflow thì không cần bấm gì thêm. Trợ lý chưa xác minh trạng thái này trên GitHub.
- Xem hạn nộp của ca học trên LMS. Đề không cho một hạn chung cho mọi ca; không lấy mốc giờ minh họa trong README làm hạn nộp của bạn.
- Khi trợ lý báo xong M0, xem kết quả và quyết định có đồng ý cho thực hiện M1 hay không.

### Cách chạy lại kiểm tra trên máy

Mở PowerShell tại thư mục gốc repo, rồi chạy:

```powershell
cd src
$labPython = '\\?\' + (Join-Path (Get-Location).Path '.venv\Scripts\python.exe')
& $labPython -m lab9.smoke
& $labPython -m lab9.evalset --build
```

Tiền tố đường dẫn mở rộng giúp chạy môi trường trong thư mục hiện tại của bạn mà không cần sửa thiết lập Windows. Hai lệnh phải trả exit 0. Ở M0, `failure_modes` còn rỗng là đúng theo đề; việc gắn mã lỗi thuộc M1. Không sửa tay tệp nhãn.

## Các bước tiếp theo — chưa thực hiện

| Bước | Việc cần làm theo đề | Trạng thái |
|---|---|---|
| M1 | Taxonomy ít nhất 5 FM, phân tích trace, gắn failure_modes và kiểm tra eval set | Bạn đã đồng ý; chuẩn bị thực hiện sau commit M0 |
| M2 | Confusion, precision/recall, kappa, Rogan–Gladen và audit ít nhất 5 bất đồng | Chưa xin phép thực hiện |
| M3 | Hai grader TODO, metric FM-08 và regression test cho trace case | Chưa xin phép thực hiện |
| M4 | Paired bootstrap, baseline swarm, fixed qua gate, seeded_regression bị chặn | Chưa xin phép thực hiện |
| Tài liệu Core | Eval card, PRD v1.1 và section eval trong harness_map | Chưa xin phép thực hiện |
| M5–M6 | Eval set v2, slice gate, pass@k/pass^k và A/A | Chưa xin phép thực hiện |
| M7 | Integrity check, ratchet và kiểm tra traps | Chưa xin phép thực hiện |
| Nộp bài | Commit report, push, PR trong fork, CI xanh, merge main và nộp link trên LMS | Chưa xin phép thực hiện |

Không chỉnh sửa `src/lab8/` sau khi chép từ nguồn gốc; không sửa tay report; không đưa nhãn đáp án vào item. Chỉ sinh baseline sau khi đã hoàn thành các bước cần thiết của Core.
