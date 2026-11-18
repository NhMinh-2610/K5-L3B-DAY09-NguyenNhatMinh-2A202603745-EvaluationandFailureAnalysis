# Judge audit

Kết quả được chạy từ hai CSV replay công khai, giữ nguyên nhãn và ngưỡng của đề. Không gọi LLM hay dùng API key. Phần nhận xét từng case do trợ lý đọc và viết; các nhãn `human` là nhãn có sẵn trong CSV, không phải một đợt gán nhãn người mới.

| Nguồn | Số dòng | SHA-256, 12 ký tự đầu |
|---|---|---|
| `data/eval/judge_tone_public.csv` | 100 | `716e3dc3b394` |
| `data/eval/judge_helpful_public.csv` | 100 | `670c133b2f56` |

## Kết quả kiểm định

| Tiêu chí | n | κ | Precision | Recall | Đạt FLOORS (κ≥0.6, P≥0.8, R≥0.7)? | Quyết định |
|---|---|---|---|---|---|---|
| tone_ok | 100 | 0.757 | 0.857 | 0.800 | Có, đạt cả ba ngưỡng | Dùng cho tiêu chí tone trong phạm vi replay đã kiểm |
| helpful | 100 | 0.375 | 1.000 | 0.300 | Không, κ và recall dưới sàn | Loại khỏi gate |

Trong bài này **FAIL là lớp positive**: TP là tìm đúng lỗi, FP là báo lỗi nhầm, FN là bỏ sót lỗi và TN là cho qua một câu đạt yêu cầu.

| Judge | TP | FP | FN | TN | Số bất đồng |
|---|---|---|---|---|---|
| tone | 24 | 4 | 6 | 66 | 10 |
| helpful | 9 | 0 | 21 | 70 | 21 |

Judge tone tìm được 24 trong 30 lỗi và báo nhầm 4 câu đạt yêu cầu. Judge helpful có precision 1.0 vì cả 9 lần nó báo lỗi đều đúng, nhưng lại bỏ sót **21 trong 30 lỗi**. Trong 21 lỗi bỏ sót có 18 câu sai tiền và 3 câu sai xưng hô theo nhãn của CSV. Vì vậy precision cao không đủ để dùng judge helpful chặn release.

Lệnh tone trả exit 0; lệnh helpful trả **exit 1 đúng như yêu cầu bài**, không phải lỗi chương trình.

## Hiệu chỉnh tỉ lệ lỗi

Precision và recall được tính từ ma trận nhầm lẫn. Cohen kappa tính phần đồng thuận vượt quá mức có thể xảy ra ngẫu nhiên. Khi kappa không xác định, hàm báo lỗi `ValueError` theo đề; không gán 1 để cho judge qua kiểm định.

Rogan–Gladen dùng `sensitivity = recall` và `specificity = TN / (TN + FP)`:

```text
corrected_rate = (observed_rate + specificity - 1) / (sensitivity + specificity - 1)
```

| Judge | Tỉ lệ FAIL do judge báo | Sensitivity | Specificity | Tỉ lệ FAIL sau hiệu chỉnh |
|---|---|---|---|---|
| tone | 0.280 | 0.800 | 0.943 | 0.300 |
| helpful | 0.090 | 0.300 | 1.000 | 0.300 |

Các phép tính dùng giá trị đầy đủ trước khi làm tròn. Kết quả được giới hạn trong [0, 1]; mẫu số bằng 0 thì phép hiệu chỉnh không xác định và phải báo lỗi. Hai giá trị 0.300 ở đây dùng chính dữ liệu đã đo sensitivity/specificity, nên không phải bằng chứng judge sẽ hoạt động tốt trên dữ liệu mới. Hiệu chỉnh tỉ lệ tổng cũng không sửa được các verdict sai ở từng case.

## Phân tích từng case bất đồng

Các số tiền ledger của nhóm `HL-*` bên dưới lấy từ trường `note` trong CSV replay; không phải kết quả truy vấn DB của eval set 14 claim. Với case thiếu ticket hay ngữ cảnh khách hàng, phần nhận định ghi rõ căn cứ là note thay vì khẳng định đã kiểm chứng độc lập.

| # | Case | Judge nói | Người nói | Ai đúng? | Căn cứ và cách làm rõ rubric |
|---|---|---|---|---|---|
| 1 | tone H-008 | PASS | FAIL | Người đúng theo chuẩn giao tiếp được ghi trong note | “Em đã hoàn tiền cho anh rồi nha, anh check giúp em” quá suồng sã theo chuẩn CS của bộ dữ liệu. Rubric cần ví dụ rõ về xưng hô và “nha/check”, tránh đánh đồng thân thiện với phù hợp. |
| 2 | tone H-017 | PASS | FAIL | Người đúng theo ngữ cảnh trong note | Câu dùng “bạn ơi” và “rồi nha”; note cho biết khách lớn tuổi. Rubric cần kèm ngữ cảnh xưng hô, không suy đoán tuổi từ câu trả lời. |
| 3 | tone H-029 | PASS | FAIL | Người đúng | “Không cần nhắn thêm” mang giọng ra lệnh dù câu mở đầu bằng “Dạ, vui lòng”. Rubric phải xét toàn câu; từ lịch sự ở đầu không tự làm câu đạt yêu cầu. |
| 4 | tone H-042 | FAIL | PASS | Người đúng | Câu ngắn vẫn lịch sự và có thông tin hoàn tiền, thời gian nhận. Judge phạt vì thiếu xin lỗi theo note; rubric không nên tự thêm điều kiện bắt buộc xin lỗi cho mọi câu. |
| 5 | tone H-051 | FAIL | PASS | Người đúng theo quy định trong note | Từ “refund” được CS LogiX cho phép. Rubric cần danh sách từ nghiệp vụ được chấp nhận, tránh tự phạt mọi từ tiếng Anh. |
| 6 | tone H-081 | FAIL | PASS | Theo note, judge đúng; cần rà soát nhãn người | Note nói người đọc nhầm ticket và cần sửa nhãn. Chỉ nhìn câu từ chối lịch sự chưa đủ xác minh vì CSV không có ticket đầy đủ. Đề xuất người kiểm tra lại ticket và định nghĩa tiêu chí trước khi sửa trong một phiên bản dữ liệu sau; giữ nguyên nhãn công khai cho số liệu hiện tại. |
| 7 | helpful HL-015 | PASS | FAIL | Người đúng theo bằng chứng ledger trong note | Reply báo 55.000đ, note ghi ledger 40.000đ. Câu lịch sự vẫn sai tiền. Rubric phải coi sai số tiền là FAIL, và kiểm tra tiền thực tế phải dùng code. |
| 8 | helpful HL-016 | PASS | FAIL | Người đúng theo note | Reply xin lỗi dài nhưng báo 55.000đ trong khi ledger 35.000đ. Thêm lời xin lỗi không sửa được lỗi sự thật; rubric cần tách thái độ khỏi tính đúng. |
| 9 | helpful HL-020 | PASS | FAIL | Người đúng theo note | Reply báo 90.000đ, ledger 120.000đ. Cả báo thiếu và báo thừa đều là sai tiền; không dùng tiêu chí chỉ bắt trường hợp báo cao hơn ledger. |
| 10 | helpful HL-028 | PASS | FAIL | Người đúng theo note | Reply lặp lời xin lỗi và báo 50.000đ thay vì 35.000đ. Rubric cần yêu cầu dẫn số tiền đúng trước khi xét cách diễn đạt. |
| 11 | helpful HL-035 | PASS | FAIL | Người đúng theo note | Reply dài, lịch sự nhưng báo 50.000đ, ledger chỉ 35.000đ. Cần có ví dụ đối chứng ngắn/dài cùng sai tiền để judge không ưu tiên độ dài. |
| 12 | helpful HL-047 | PASS | FAIL | Người đúng theo chuẩn trong CSV | “Ok bạn, đơn O-515 xử lý rồi nhé” bị gắn lỗi xưng hô. Rubric cần nêu chuẩn xưng hô và yêu cầu kết quả xử lý cụ thể, không coi “xử lý rồi” là đủ trong mọi ngữ cảnh. |

## Đề xuất làm rõ rubric cho lần kiểm định tiếp theo

1. Chấm riêng tone và tính đúng của nội dung. Tone xét xưng hô, giọng điệu và từ ngữ theo chuẩn CS; câu có “Dạ/ạ” chưa chắc đạt, câu ngắn hoặc dùng từ “refund” chưa chắc sai.
2. Các trường hợp ngữ cảnh quyết định verdict phải có ticket hoặc thông tin ngữ cảnh để người và judge cùng đọc. Những nhãn đáng ngờ như H-081 cần được người rà lại, không tự đổi nhãn chỉ để tăng kappa.
3. Tiền, approval và quyền truy cập dùng code đối chiếu với ledger/nhãn. Lời xin lỗi hoặc câu văn trôi chảy không được bù cho sai tiền. Đây cũng là lý do cần grader FM-08 ở M3.
4. Nếu sửa rubric/judge, kiểm định lại trên dữ liệu held-out có nhãn người mới. Các đề xuất này chưa được áp dụng vào CSV, judge replay hay ngưỡng chấm của bài hiện tại.

## Kết luận

Judge tone đạt đủ ba ngưỡng nên dùng được cho tiêu chí tone đã kiểm. Judge helpful bị loại vì κ=0.375 và recall=0.300; ma trận TP=9, FN=21 cho thấy nó để lọt phần lớn lỗi, đặc biệt là sai tiền. Không dùng judge này làm gate và không hạ sàn để cho qua.

Bằng chứng hiện tại chỉ là replay trên 100 dòng công khai cho mỗi tiêu chí, chưa có tập held-out mới. Một số nhận xét dựa vào note và còn thiếu ngữ cảnh đầy đủ. Phần audit này không chứng minh chất lượng trên người dùng thật hay thay cho kiểm tra ledger bằng code.

## Chạy lại và kiểm tra

Từ `src/`, dùng Python trong môi trường riêng. Trên máy Windows hiện tại:

```powershell
$labPython = '\\?\' + (Join-Path (Get-Location).Path '.venv\Scripts\python.exe')
& $labPython -m lab9.judge --csv data/eval/judge_tone_public.csv --audit 5
& $labPython -m lab9.judge --csv data/eval/judge_helpful_public.csv --audit 5
& $labPython -m pytest -q -m student -o addopts= tests/test_lab9_stats.py tests/test_lab9_judge_calibration.py -k 'not bootstrap'
```

Kết quả test M2: **18 passed, 2 deselected**. Hai test bootstrap thuộc M4, chưa thực hiện ở bước này. Test bổ sung kiểm tra mẫu số bằng 0, kappa ở các trường hợp biên, đầu vào không hợp lệ và quyết định tone đạt/helpful không đạt. Không chỉnh sửa test công khai để làm thay đổi kết quả.
