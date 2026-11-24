# Detection curve on the clean reference windows (inbox 34; report-only, thresholds unchanged)

Windows: 130 labelled clean by Andrew. Thresholds `config/zone_reference_thresholds.yaml`: `pp_shape_rel` 0.14, `pp_common_rel` 0.5. Counts read `caught of computable`

| Check | Injection | Size | Caught | Fraction |
| :-- | :-- | --: | --: | --: |
| shape | none (false alarms) | 0 | 0 of 130 | 0.00 |
| common | none (false alarms) | 0 | 1 of 130 | 0.01 |
| shape | profile shifted along s | -90 px | 101 of 130 | 0.78 |
| shape | profile shifted along s | -60 px | 10 of 130 | 0.08 |
| shape | profile shifted along s | -30 px | 2 of 130 | 0.02 |
| shape | profile shifted along s | -15 px | 2 of 130 | 0.02 |
| shape | profile shifted along s | +15 px | 2 of 130 | 0.02 |
| shape | profile shifted along s | +30 px | 2 of 130 | 0.02 |
| shape | profile shifted along s | +60 px | 10 of 130 | 0.08 |
| shape | profile shifted along s | +90 px | 101 of 130 | 0.78 |
| common | whole chain slid along s | -4 patch spacings | 90 of 130 | 0.69 |
| common | whole chain slid along s | -2 patch spacings | 18 of 130 | 0.14 |
| common | whole chain slid along s | -1 patch spacings | 4 of 130 | 0.03 |
| common | whole chain slid along s | -0.5 patch spacings | 2 of 130 | 0.02 |
| common | whole chain slid along s | +0.5 patch spacings | 2 of 130 | 0.02 |
| common | whole chain slid along s | +1 patch spacings | 2 of 130 | 0.02 |
| common | whole chain slid along s | +2 patch spacings | 2 of 130 | 0.02 |
| common | whole chain slid along s | +4 patch spacings | 11 of 130 | 0.08 |

Smallest size caught in at least 90 % of computable windows, in both directions: shape none up to 90 px; common none up to 4 patch spacings (1 patch spacing = 15 px)
