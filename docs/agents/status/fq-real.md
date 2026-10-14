# fq-real
Updated: 2026-10-13 23:20 (local)
Lane: course
Branch: wip/fq-real
Last inbox item done: 4
State: waiting on Andrew
Now: labeling set rebuilt to the usable-window rule; B4 starts when an inbox item says the labels are done
Done since last update:
- Item 2: 7 windows broke the rule, all on include (not yes); none outside usable hours. Replaced: fq03, fq10, fq19, fq25, fq27 (include unsure), fq23, fq28 (include no). New: fq31-fq37, likely-poor windows from include-yes roots inside usable hours
- Item 2: column 3, bottom row of the overlay grid was fq28 (include no, dark region of the plate). Replaced
- Item 2: replaced windows removed from the VM labeling folder and labels.csv; no labels had been written
- Fix: labels.csv had only 4 rows since the first build; now 30 rows
- Item 3: segmentation band kept; border fix removed off-root patches in 4 windows; all 30 overlays checked by eye. Real reference will be marked provisional in config at B4
- Item 4: B4 stop rule "clean below synthetic lowest" dropped; clean vs not_clean separation check kept
Needs Andrew:
- Label 30 windows: staging/fq_real_labeling/ in the main repo folder; view/<id>.png, write clean, not_clean or unsure in labels.csv (HOW_TO_LABEL.txt)
- Band leaves the root in fq34: it runs past the tip and widens in a dark patch. Keep fq34 in the reference with this band, or leave it out
