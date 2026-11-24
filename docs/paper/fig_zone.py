"""Fig. 2: zone-check detection curve. Data: results/2026-11-23_zone_reference/curve.md"""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"font.family": "serif", "font.serif": ["Nimbus Roman", "Times New Roman", "DejaVu Serif"], "font.size": 8, "pdf.fonttype": 42})
shape = {-90: .78, -60: .08, -30: .02, -15: .02, 0: 0.0, 15: .02, 30: .02, 60: .08, 90: .78}
common = {-60: .69, -30: .14, -15: .03, -7.5: .02, 0: .01, 7.5: .02, 15: .02, 30: .02, 60: .08}
fig, ax = plt.subplots(figsize=(3.4, 1.7))
for d, lab, m, c in [(shape, "shape: profile shifted", "o", "#1f5aa6"), (common, "common: chain slid", "s", "#c0632b")]:
    x = sorted(d); ax.plot(x, [d[k] for k in x], marker=m, ms=3.5, lw=1, color=c, label=lab)
ax.set_xlabel("Injected shift along the root (px)"); ax.set_ylabel("Fraction caught")
ax.set_ylim(-0.03, 1); ax.set_xticks([-90, -60, -30, 0, 30, 60, 90])
ax.spines[["top", "right"]].set_visible(False); ax.legend(frameon=False, loc="upper center")
fig.tight_layout(pad=0.2); fig.savefig("fig_zone.pdf")
