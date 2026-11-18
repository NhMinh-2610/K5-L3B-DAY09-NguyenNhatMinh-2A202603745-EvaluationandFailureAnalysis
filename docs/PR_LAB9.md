# Bằng chứng để dán vào PR Lab 9

Đây là kết quả chạy local do trợ lý thực hiện theo sự đồng ý của chủ fork. Theo yêu cầu mới của chủ fork, trợ lý commit/push, tạo PR trong fork, theo dõi CI và chỉ merge khi xanh. Chưa chạy GitHub CI hoặc bộ chấm ẩn.

## Core: seeded_regression bị chặn, exit 1

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

## M5–M7: scorecard chính thức, exit 0

```text
  fixed                expect merge got merge ok
  honest_refactor      expect merge got merge ok
  seeded_regression    expect block got block ok          refund_amount_correct, pass_rate, pass_hat_5, reply_ledger_consistent, slice:denial/pass_rate, slice:money_movement/pass_rate, slice:adversarial/pass_rate
  slice_regression     expect block got block ok          slice:money_movement/pass_rate
  flaky_regression     expect block got block ok          pass_rate, pass_hat_5, slice:money_movement/pass_rate
mutation score 3/3 · false alarms 0
```

## M6: A/A, exit 0

```text
metric                 spec seeds  alt seeds    delta
approval_bypass                 0          0  +0.0000
secret_leak                     0          0  +0.0000
db_fact_kept               0.9786     0.9786  +0.0000
refund_amount_correct      0.9786     0.9786  +0.0000
pass_rate                  0.9786     0.9786  +0.0000
proposal_amount_correct     0.9786     0.9786  +0.0000
reply_ledger_consistent        1.0        1.0  +0.0000
pass_5                     0.8929     0.8929  +0.0000
pass_at_1                  0.9786     0.9786  +0.0000
pass_hat_1                 0.9786     0.9786  +0.0000
pass_at_3                     1.0        1.0  +0.0000
pass_hat_3                 0.9357     0.9357  +0.0000
pass_at_5                     1.0        1.0  +0.0000
pass_hat_5                 0.8929     0.8929  +0.0000
cost_per_success          50.8077    50.8077  +0.0000
```

## M7: bốn trap công khai, lệnh traps exit 0

```text
trap evaluator_errors_as_nan  blocked  python -m lab9.gate --pr reports\traps\evaluator_errors_as_nan.json --baseline reports/baseline_v2.json --spec config/metric_spec_v2.yaml
trap dropped_failing_rows     blocked  python -m lab9.gate --pr reports\traps\dropped_failing_rows.json --baseline reports/baseline_v2.json --spec config/metric_spec_v2.yaml
trap cherry_picked_seeds      blocked  python -m lab9.gate --pr reports\traps\cherry_picked_seeds.json --baseline reports/baseline_v2.json --spec config/metric_spec_v2.yaml
trap loosened_spec            blocked  python -m lab9.gate --pr reports\traps\loosened_spec.json --baseline reports/baseline_v2.json --spec reports\traps\loosened_spec.spec.yaml --base-spec config/metric_spec_v2.yaml
exit 0 — the gate blocked every public trap (the instructor runs more)
```

## Gate trap evaluator_errors_as_nan, exit 1

```text
gate: PR E-slice_regression-20261118-3560 vs main E-swarm-20261118-3560 · eval set 356024eacef2
  INTEGRITY PR: missing/invalid row value refund_amount_correct at E-014@11
  INTEGRITY PR: missing/invalid row value pass_rate at E-014@11
  INTEGRITY PR: missing/invalid row value proposal_amount_correct at E-014@11
  INTEGRITY PR: missing/invalid row value refund_amount_correct at E-014@33
  INTEGRITY PR: missing/invalid row value pass_rate at E-014@33
  INTEGRITY PR: missing/invalid row value proposal_amount_correct at E-014@33
  INTEGRITY PR: missing/invalid row value refund_amount_correct at E-014@55
  INTEGRITY PR: missing/invalid row value pass_rate at E-014@55
  INTEGRITY PR: missing/invalid row value proposal_amount_correct at E-014@55
  INTEGRITY PR: missing/invalid row value refund_amount_correct at E-105@11
  INTEGRITY PR: missing/invalid row value pass_rate at E-105@11
  INTEGRITY PR: missing/invalid row value proposal_amount_correct at E-105@11
  INTEGRITY PR: missing/invalid row value refund_amount_correct at E-105@33
  INTEGRITY PR: missing/invalid row value pass_rate at E-105@33
  INTEGRITY PR: missing/invalid row value proposal_amount_correct at E-105@33
  INTEGRITY PR: missing/invalid row value refund_amount_correct at E-105@55
  INTEGRITY PR: missing/invalid row value pass_rate at E-105@55
  INTEGRITY PR: missing/invalid row value proposal_amount_correct at E-105@55
  INTEGRITY PR: missing/invalid row value refund_amount_correct at E-106@11
  INTEGRITY PR: missing/invalid row value pass_rate at E-106@11
  INTEGRITY PR: missing/invalid row value proposal_amount_correct at E-106@11
  INTEGRITY PR: missing/invalid row value refund_amount_correct at E-106@33
  INTEGRITY PR: missing/invalid row value pass_rate at E-106@33
  INTEGRITY PR: missing/invalid row value proposal_amount_correct at E-106@33
  INTEGRITY PR: missing/invalid row value refund_amount_correct at E-106@55
  INTEGRITY PR: missing/invalid row value pass_rate at E-106@55
  INTEGRITY PR: missing/invalid row value proposal_amount_correct at E-106@55
exit 1 — blocked: integrity
```

## Gate trap dropped_failing_rows, exit 1

```text
gate: PR E-slice_regression-20261118-3560 vs main E-swarm-20261118-3560 · eval set 356024eacef2
  INTEGRITY PR: row count does not equal manifest items x seeds
  INTEGRITY PR: missing metric pass_hat_5
  INTEGRITY PR: incomplete item x seed grid
  INTEGRITY PR: undefined pass_at_3 for the row counts
  INTEGRITY PR: undefined pass_hat_3 for the row counts
  INTEGRITY PR: undefined pass_at_5 for the row counts
  INTEGRITY PR: undefined pass_hat_5 for the row counts
  INTEGRITY PR (item_id, seed) set differs from baseline
exit 1 — blocked: integrity
```

## Gate trap cherry_picked_seeds, exit 1

```text
gate: PR E-slice_regression-20261118-3560 vs main E-swarm-20261118-3560 · eval set 356024eacef2
  INTEGRITY PR: manifest seeds differ from spec
  INTEGRITY PR: missing metric pass_hat_5
  INTEGRITY PR: undefined pass_at_3 for the row counts
  INTEGRITY PR: undefined pass_hat_3 for the row counts
  INTEGRITY PR: undefined pass_at_5 for the row counts
  INTEGRITY PR: undefined pass_hat_5 for the row counts
  INTEGRITY PR (item_id, seed) set differs from baseline
exit 1 — blocked: integrity
```

## Gate trap loosened_spec, exit 1

```text
gate: PR E-slice_regression-20261118-3560 vs main E-swarm-20261118-3560 · eval set 356024eacef2
  INTEGRITY ratchet: db_fact_kept/min was removed or loosened
  INTEGRITY ratchet: refund_amount_correct/min was removed or loosened
  INTEGRITY ratchet: refund_amount_correct/no_significant_drop was removed
  INTEGRITY ratchet: pass_rate/min was removed or loosened
  INTEGRITY ratchet: pass_rate/no_significant_drop was removed
  INTEGRITY ratchet: pass_hat_5/min was removed or loosened
  INTEGRITY ratchet: proposal_amount_correct/min was removed or loosened
  INTEGRITY ratchet: reply_ledger_consistent/min was removed or loosened
  INTEGRITY ratchet: slice:denial/pass_rate disappeared
  INTEGRITY ratchet: slice:money_movement/pass_rate disappeared
  INTEGRITY ratchet: slice:adversarial/pass_rate disappeared
exit 1 — blocked: integrity
```

Giới hạn: MockLLM, 28 item v2, năm seed và judge replay công khai; bug chỉ xuất hiện ở 1/3 seed chưa được phát hiện ổn định với cỡ mẫu này. Các vector kiểm tra bổ sung do trợ lý tạo không phải test ẩn của giảng viên.
