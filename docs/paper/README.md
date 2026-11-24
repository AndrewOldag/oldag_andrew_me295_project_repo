# Final paper (IEEE conference format, 4 pages incl. AI Use Declaration)

- `main.tex`, `refs.bib`: source. Class `IEEEtran.cls` and `IEEEtran.bst` from CTAN (conference mode, US letter)
- `fig_design.dot` → `fig_design.png`: Fig. 1 (`dot -Tpng -Gdpi=300 fig_design.dot -o fig_design.png`)
- `fig_zone.py` → `fig_zone.pdf`: Fig. 2, data from `results/2026-11-23_zone_reference/curve.md`
- Build: `pdflatex main; bibtex main; pdflatex main; pdflatex main`
- Every number comes from a committed results README (freeze v4, held-out compound and supplement, integrated run, auditor check, zone reference)
