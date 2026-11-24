"""No real-root biology value in a tracked file (c033 audit S1-3, S1-4; task c036)."""
import shutil
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import mask_bio  # noqa: E402
from batch2_agents_report import mask  # noqa: E402


@pytest.mark.skipif(shutil.which("git") is None, reason="needs git")
def test_tracked_real_files_have_no_biology_values():
    hits = {}
    for f in mask_bio.tracked_files():
        text = mask_bio.read_text(f)
        if text and mask_bio.find_values(text):
            hits[f] = sorted(set(mask_bio.find_values(text)))
    assert not hits, f"biology values in {len(hits)} files (run scripts/mask_bio.py --apply): {list(hits)[:10]}"


def test_mask_text_keys_and_phrases():
    text = ('{"strain_rate_pct_per_h": [null, 1.1, -0.5], "negative_strain_rate_min_pct_per_h": -17.9, '
            '"closure": 0.945, "detail": "flank difference 33.99 %/h, predicted 167.56 %/h; REGR peak 55.5 %/h at 579 um"}')
    out = mask_bio.mask_text(text)
    assert not mask_bio.find_values(out)
    assert '"closure": 0.945' in out and "predicted 167.56" in out
    assert "17.9" not in out and "33.99" not in out and "55.5" not in out and "579" not in out
    escaped = '"result": "{\\"centre_peak_regr_pct_per_h\\": 55.51, \\"rigid_invariance\\": 8.83}"'
    assert mask_bio.mask_text(escaped) == '"result": "{\\"centre_peak_regr_pct_per_h\\": \\"[masked]\\", \\"rigid_invariance\\": 8.83}"'


def test_mask_text_leaves_dates_ids_positions():
    for text in ["REGR values (Andrew, 2026-10-25)", "flank difference (x): r35", "strain rate at s = 435 px",
                 "regression (2026-11-20)"]:
        assert mask_bio.mask_text(text) == text
    assert mask_bio.mask_text("growth zone 2-6 px/h") == "growth zone [masked] px/h"


def test_report_mask_covers_strain_rate_profile():
    m = mask({"strain_rate_pct_per_h": [1.0, 2.0], "negative_strain_rate_min_pct_per_h": -17.9, "closure": 1.2})
    assert m["strain_rate_pct_per_h"] == "[masked]" and m["negative_strain_rate_min_pct_per_h"] == "[masked]"
    assert m["closure"] == 1.2
