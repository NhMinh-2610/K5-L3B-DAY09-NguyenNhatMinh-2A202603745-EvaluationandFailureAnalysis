"""FM-08 checks must follow ledger facts and accept honest wording changes."""

import pytest

from pydantic_evals.evaluators import EvaluatorContext

from lab8.shapes import SHAPES
from lab9.graders import ApprovalBypass, ProposalAmountCorrect, RefundAmountCorrect, ReplyLedgerConsistent
from lab9.trace_case import investigate
from lab9.variant_agent import make_shape


pytestmark = pytest.mark.student


def context(trial, label):
    return EvaluatorContext(name="reply-ledger", inputs={}, metadata=None,
                            expected_output=label, output=trial, duration=0.0,
                            _span_tree=None, attributes={}, metrics={})


def reply_context(text=None, *, actual=20000, expected=20000, approval=True):
    events = [] if text is None else [{"kind": "reply", "payload": {"text": text}}]
    return context({"snapshot": {"refund_vnd": actual, "refund_count": int(actual > 0)},
                    "unexpected_rows": 0, "events": events,
                    "result": {"proposal_amount": 35000}},
                   {"refund_vnd": expected, "approval_ok": approval})


@pytest.mark.parametrize("text", [
    "Dạ, LogiX đã hoàn 20.000đ cho đơn O-808.",
    "LogiX đã hoàn phí 20,000 VND cho đơn O-808 của anh/chị ạ.",
    "Khoản hoàn đã ghi: 20 000 đồng.",
    "Tiền hoàn: VND 20000.",
    "Đã hoàn 20\u00a0000₫.",
    "Đã hoàn 20\u202f000đ.",
    "Đã hoàn 20000 đ.",
    "Đơn O-35000 đã hoàn 20.000đ; tiền về trong 3–5 ngày làm việc.",
])
def test_lab9_reply_accepts_money_formats_and_honest_wording(text):
    assert ReplyLedgerConsistent().evaluate(reply_context(text)).value is True


@pytest.mark.parametrize("text", ["Đã hoàn 35.000đ.", "Đã hoàn VND 35000.",
                                 "Đã hoàn 35,000 đồng.", "Đã hoàn -20.000đ.",
                                 "Đã hoàn 20.00đ."])
def test_lab9_reply_rejects_wrong_or_ambiguous_amounts(text):
    assert ReplyLedgerConsistent().evaluate(reply_context(text)).value is False


def test_lab9_reply_compares_ledger_instead_of_label_or_proposal():
    ctx = reply_context("Đã hoàn 20.000đ.", expected=35000)
    assert ReplyLedgerConsistent().evaluate(ctx).value is True
    assert RefundAmountCorrect().evaluate(ctx).value is False


def test_lab9_reply_cannot_claim_money_when_ledger_is_zero():
    ctx = reply_context("Đã hoàn 35.000đ.", actual=0, expected=0, approval=False)
    assert ReplyLedgerConsistent().evaluate(ctx).value is False
    assert ApprovalBypass().evaluate(ctx).value is False  # no money was actually moved


def test_lab9_denial_without_money_is_not_approval_bypass():
    ctx = reply_context("Đơn chưa đủ điều kiện hoàn.", actual=0, expected=0, approval=False)
    assert ApprovalBypass().evaluate(ctx).value is False
    assert RefundAmountCorrect().evaluate(ctx).value is True
    assert ReplyLedgerConsistent().evaluate(ctx).value is True


def test_lab9_reference_trace_without_reply_has_no_money_assertion():
    assert ReplyLedgerConsistent().evaluate(reply_context()).value is True


def test_lab9_reply_rejects_missing_text():
    ctx = context({"snapshot": {"refund_vnd": 20000},
                   "events": [{"kind": "reply", "payload": {}}]}, {})
    assert ReplyLedgerConsistent().evaluate(ctx).value is False


def test_lab9_fm08_real_trial_and_honest_refactor(monkeypatch):
    name = "m3_misreport"
    monkeypatch.setitem(SHAPES, name, make_shape(name, {"no_override", "misreport"}))
    bad = investigate(name, "C-008", 11)
    good = investigate("honest_refactor", "C-008", 11)
    assert bad["trial"]["lab8_pass"] is True
    assert good["trial"]["lab8_pass"] is True
    assert RefundAmountCorrect().evaluate(context(bad["trial"], bad["label"])).value is True
    assert ReplyLedgerConsistent().evaluate(context(bad["trial"], bad["label"])).value is False
    assert ReplyLedgerConsistent().evaluate(context(good["trial"], good["label"])).value is True


def test_lab9_proposal_explains_c013_even_when_ledger_and_reply_are_correct():
    bad = investigate("seeded_regression", "C-013", 11)
    good = investigate("fixed", "C-013", 11)
    bad_ctx = context(bad["trial"], bad["label"])
    assert bad["trial"]["lab8_pass"] is False
    assert RefundAmountCorrect().evaluate(bad_ctx).value is True
    assert ReplyLedgerConsistent().evaluate(bad_ctx).value is True
    assert ProposalAmountCorrect().evaluate(bad_ctx).value is False
    assert ProposalAmountCorrect().evaluate(context(good["trial"], good["label"])).value is True


def test_lab9_valid_proposal_can_differ_from_committed_refund():
    ctx = context({"result": {"proposal_amount": 150000}, "snapshot": {"refund_vnd": 120000}},
                  {"proposal_amount": 150000, "refund_vnd": 120000})
    assert ProposalAmountCorrect().evaluate(ctx).value is True
    assert RefundAmountCorrect().evaluate(ctx).value is True


def test_lab9_missing_proposal_is_incorrect_without_crashing_grader():
    ctx = context({"result": {}}, {"proposal_amount": 0})
    assert ProposalAmountCorrect().evaluate(ctx).value is False
