"""Generated eval data must keep the same bytes after a Git checkout on any OS."""

import json

import pytest

from lab9 import evalset


pytestmark = pytest.mark.student


@pytest.mark.parametrize("version", [1, 2])
def test_lab9_evalset_generated_files_use_lf_without_changing_labels(tmp_path, monkeypatch, version):
    monkeypatch.chdir(tmp_path)
    expected = {"status": "resolved", "refund_vnd": 35000}
    claim = {"claim_id": "C-001", "matrix_id": "T01", "expected": expected}
    evalset.SOURCE.parent.mkdir(parents=True)
    evalset.SOURCE.write_text(json.dumps(claim) + "\n", encoding="utf-8", newline="\n")
    evalset.build()
    items_path, labels_path = evalset.ITEMS, evalset.LABELS
    if version == 2:
        extra_expected = {"status": "denied", "refund_vnd": 0}
        pack = {"claims": [{"claim_id": "C-105", "mechanisms": ["ticket_over_db"],
                            "attack": "test_fixture", "expected": extra_expected}]}
        evalset.PACK.write_text(json.dumps(pack), encoding="utf-8", newline="\n")
        evalset.FM_MAP.parent.mkdir()
        evalset.FM_MAP.write_text("ticket_over_db: FM-03\n", encoding="utf-8", newline="\n")
        evalset.build_v2()
        items_path, labels_path = evalset.ITEMS_V2, evalset.LABELS_V2
    assert b"\r" not in items_path.read_bytes()
    assert b"\r" not in labels_path.read_bytes()
    items = evalset.load_jsonl(items_path)
    labels = json.loads(labels_path.read_text(encoding="utf-8"))
    assert items[0]["claim_id"] == "C-001"
    assert "expected" not in items[0] and "label" not in items[0]
    assert labels["C-001"] == expected
    if version == 2:
        assert labels["C-105"] == extra_expected
