"""Public report of the c022 agent run: no number from the auditor's text, no per-condition block."""
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("fbr", ROOT / "scripts" / "full_batch_agents_report.py")
FBR = importlib.util.module_from_spec(spec)
spec.loader.exec_module(FBR)

REPORT = ("Batch: 12 runs, 11 accepted.\n\nFlagged:\n- summary_outlier, narrow (2): r08, r09. The growth zone is "
          "53 um against 737 um.\n\nWhat the flagged runs share: 2 of the 2 passed closure (13.2 vs 19 px/h).\n\n"
          "Cleared runs by condition (approximate medians):\n- control (n=5): REGR peak about 41 %/h.\n"
          "- mannitol (n=4): REGR peak about 32 %/h. Growth is slower.\n\nFlank differences mostly lie within "
          "-80 %/h. These differences between conditions are measurement results, not faults.")


def test_auditor_public_masks_numbers_and_withholds_condition_block():
    text = "\n".join(FBR.auditor_public(REPORT))
    assert "r08, r09" in text and "not faults" in text and "withheld" in text
    for leak in ("53", "737", "13.2", "41", "32", "80", "REGR peak", "slower", "growth zone is"):
        assert leak not in text


def test_remedy_cells_split_tried_and_rolled_back():
    rem = ["frames registered on the non-growing tissue (from 1015 px from the tip) before tracking",
           "rolled back: frames registered on the non-growing tissue (from 1015 px from the tip) before tracking"]
    assert FBR.remedy_cells(rem) == ("frames registered on the non-growing tissue",
                                     "frames registered on the non-growing tissue")
