# fq-real
Updated: 2026-10-13 (local)
Lane: course
Branch: wip/fq-real
Last inbox item done: 4
State: working
Now: inbox item 5: provisional real reference in config, info.py, tests
Done since last update:
- Labels read (Andrew, in chat): 24 clean, 5 unsure, 1 not_clean. fq34 left out on Andrew's instruction
- Reference candidate from 24 clean windows (72 frames): texture_contrast median 0.0648, lowest 0.0439; focus median 0.0286, lowest 0.0213
- Separation: the only not_clean window (fq12) is above the clean lowest on both measures, in all 3 frames, and above the clean median. Stop condition of B4. Config and measure/info.py unchanged
Needs Andrew:
- The measures do not mark fq12 as poor. Its problem (bad lighting, debris) raises texture_contrast rather than lowering it. One not_clean window is too few to judge separation either way
- Options: (a) write the reference anyway, provisional, and record that it catches low texture and blur but not lighting or debris; (b) label more poor windows from inside usable windows first; (c) add a measure aimed at lighting and debris (needs a planning decision)
