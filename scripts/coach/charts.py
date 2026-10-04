"""Graphs SVG du README, en variante claire et sombre (insérés via <picture>).

Règles (skill dataviz) : un seul axe par graph (plusieurs mesures = petits multiples),
barres fines à bout arrondi, lignes 2 px, grille discrète, texte jamais coloré par
la série, labels directs sélectifs. Couleurs validées contre les fonds GitHub
(#ffffff / #0d1117). Couleur = entité : bleu = course, orange = vélo.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.dates as mdates  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
import matplotlib.ticker as mticker  # noqa: E402
import pandas as pd  # noqa: E402
from matplotlib import font_manager  # noqa: E402
from matplotlib.axes import Axes  # noqa: E402
from matplotlib.figure import Figure  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from matplotlib.patches import FancyBboxPatch, PathPatch, Rectangle  # noqa: E402
from matplotlib.path import Path as MPath  # noqa: E402

from coach import metrics as m  # noqa: E402
from coach.util import FR_MONTHS, fmt_race_time, monday_of  # noqa: E402

for _font in ("/System/Library/Fonts/Avenir Next.ttc", "/System/Library/Fonts/HelveticaNeue.ttc"):
    if Path(_font).exists():
        font_manager.fontManager.addfont(_font)

plt.rcParams.update({
    "font.family": ["Avenir Next", "Helvetica Neue", "DejaVu Sans"],
    "svg.fonttype": "path",  # texte vectorisé : rendu identique partout
    "svg.hashsalt": "run-coach",  # ids stables : pas de diff si les données ne changent pas
    "axes.spines.top": False,
    "axes.spines.right": False,
})

W_IN = 8.6  # ~ largeur de la colonne README GitHub


@dataclass(frozen=True)
class Theme:
    name: str
    ink: str
    ink2: str
    muted: str
    grid: str
    axis: str
    empty: str
    run: str
    run_soft: str
    bike: str
    seq: tuple[str, ...]  # rampe séquentielle bleue, du plus faible au plus fort


LIGHT = Theme(
    "light", ink="#0b0b0b", ink2="#52514e", muted="#898781", grid="#e1e0d9", axis="#c3c2b7", empty="#ecebe6",
    run="#2a78d6", run_soft="#9ec5f4", bike="#eb6834",
    seq=("#cde2fb", "#86b6ef", "#3987e5", "#1c5cab", "#0d366b"),
)
DARK = Theme(
    "dark", ink="#ffffff", ink2="#c3c2b7", muted="#898781", grid="#262a30", axis="#3a3f46", empty="#1b2027",
    run="#3987e5", run_soft="#1c5cab", bike="#d95926",
    seq=("#104281", "#1c5cab", "#2a78d6", "#5598e7", "#9ec5f4"),
)
THEMES = (LIGHT, DARK)


# --- Outils communs ------------------------------------------------------------------


def _style(ax: Axes, t: Theme, ylabel: str = "") -> None:
    ax.set_facecolor("none")
    ax.grid(axis="y", color=t.grid, linewidth=0.8)
    ax.set_axisbelow(True)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_color(t.axis)
    ax.tick_params(colors=t.muted, labelsize=8.5, length=0)
    if ylabel:
        ax.set_ylabel(ylabel, color=t.muted, fontsize=8.5)


def _fig(height: float, nrows: int = 1, ratios: list[float] | None = None) -> tuple[Figure, list[Axes]]:
    fig, axes = plt.subplots(nrows, 1, figsize=(W_IN, height), sharex=True,
                             gridspec_kw={"height_ratios": ratios} if ratios else None)
    fig.patch.set_alpha(0)
    return fig, list(axes) if nrows > 1 else [axes]


def _px(ax: Axes) -> tuple[float, float]:
    """Pixels par unité de données (x, y), avec les limites déjà fixées."""
    ax.figure.canvas.draw()
    (x0, y0), (x1, y1) = ax.transData.transform([(0, 0), (1, 1)])
    return abs(x1 - x0), abs(y1 - y0)


def _rbar(ax: Axes, x: float, y0: float, h: float, w: float, color: str, r_px: float = 4) -> None:
    """Barre à bout arrondi (4 px), carrée côté base. Tracée comme un seul chemin (pas de jointure visible)."""
    if h <= 0:
        return
    pxx, pxy = _px(ax)
    rx = min(r_px / pxx, w / 2)
    ry = min(r_px / pxy, h / 2)
    x0, x1, top = x - w / 2, x + w / 2, y0 + h
    verts = [(x0, y0), (x1, y0), (x1, top - ry), (x1, top), (x1 - rx, top), (x0 + rx, top), (x0, top), (x0, top - ry),
             (x0, y0)]
    codes = [MPath.MOVETO, MPath.LINETO, MPath.LINETO, MPath.CURVE3, MPath.CURVE3, MPath.LINETO, MPath.CURVE3,
             MPath.CURVE3, MPath.CLOSEPOLY]
    ax.add_patch(PathPatch(MPath(verts, codes), facecolor=color, edgecolor="none"))


def _bar_width(ax: Axes, max_px: float = 20, slot: float = 0.62) -> float:
    pxx, _ = _px(ax)
    return min(slot, max_px / pxx)


def _label(ax: Axes, x: float, y: float, text: str, t: Theme, **kw: object) -> None:
    ax.annotate(text, (x, y), xytext=kw.pop("offset", (0, 4)), textcoords="offset points", ha=kw.pop("ha", "center"),
                va=kw.pop("va", "bottom"), fontsize=kw.pop("size", 8.5), color=kw.pop("color", t.ink2),
                fontweight=kw.pop("weight", "normal"))


def _save(fig: Figure, out: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, format="svg", bbox_inches="tight", pad_inches=0.08, transparent=True, metadata={"Date": None})
    plt.close(fig)


def _week_ticks(ax: Axes, mondays: list[date], step: int = 2) -> None:
    idx = list(range(len(mondays)))
    ax.set_xticks(idx[::-1][::step][::-1])
    ax.set_xticklabels([f"{mondays[i]:%d/%m}" for i in ax.get_xticks().astype(int)])


# --- 1. Volume hebdo (course km + vélo h, petits multiples) ---------------------------


def volume(acts: pd.DataFrame, today: date, t: Theme, weeks: int = 16) -> Figure:
    wk = m.weekly(acts, today, weeks)
    has_bike = wk["bike_min"].sum() > 0
    fig, axes = _fig(3.6 if has_bike else 2.6, 2 if has_bike else 1, [3, 1.3] if has_bike else None)
    ax = axes[0]
    n = len(wk)
    ax.set_xlim(-0.6, n - 0.4)
    ymax = max(wk["run_km"].max() * 1.22, 10)
    ax.set_ylim(0, ymax)
    _style(ax, t, "km course")
    w = _bar_width(ax)
    for i, row in wk.iterrows():
        current = i == n - 1
        _rbar(ax, i, 0, row["run_km"], w, t.run_soft if current else t.run)
    # Labels sélectifs : semaine en cours, dernière semaine complète, record de la période.
    best = int(wk["run_km"].iloc[:-1].idxmax()) if n > 1 else 0
    for i in sorted({n - 1, n - 2, best}):
        if 0 <= i < n and wk["run_km"].iloc[i] > 0:
            txt = f"{wk['run_km'].iloc[i]:.0f}" + (" (en cours)" if i == n - 1 else "")
            _label(ax, i, wk["run_km"].iloc[i], txt, t, weight="bold" if i != n - 1 else "normal")
    if has_bike:
        bx = axes[1]
        bx.set_xlim(-0.6, n - 0.4)
        bx.set_ylim(0, max(wk["bike_min"].max() / 60 * 1.35, 1))
        _style(bx, t, "h vélo")
        for i, row in wk.iterrows():
            _rbar(bx, i, 0, row["bike_min"] / 60, w, t.bike)
    _week_ticks(axes[-1], list(wk["monday"]))
    fig.align_ylabels(axes)
    return fig


# --- 2. Prédiction semi Garmin vs objectif ----------------------------------------------------


def prediction(metrics_df: pd.DataFrame, goal: dict, today: date, t: Theme) -> Figure | None:
    if metrics_df.empty or "pred_semi_s" not in metrics_df:
        return None
    df = metrics_df.dropna(subset=["pred_semi_s"])
    df = df[df["date"] >= pd.Timestamp(today - timedelta(days=180))]
    if len(df) < 2:
        return None
    target = goal.get("target_s")
    race_date = pd.Timestamp(goal["date"]) if goal.get("date") else None
    fig, (ax,) = _fig(2.6)
    _style(ax, t, "prédiction semi")
    ax.plot(df["date"], df["pred_semi_s"], color=t.run, linewidth=2, solid_capstyle="round", solid_joinstyle="round")
    last = df.iloc[-1]
    ax.scatter([last["date"]], [last["pred_semi_s"]], s=60, color=t.run, linewidths=0, zorder=3)
    _label(ax, mdates.date2num(last["date"]), last["pred_semi_s"], fmt_race_time(last["pred_semi_s"]), t,
           offset=(6, -3), ha="left", va="top", weight="bold", color=t.ink)
    lo, hi = df["pred_semi_s"].min(), df["pred_semi_s"].max()
    if target:
        lo, hi = min(lo, target), max(hi, target)
        ax.axhline(target, color=t.ink2, linewidth=1)
        ax.annotate(f"Objectif {fmt_race_time(target)}", (0.0, target), xycoords=("axes fraction", "data"),
                    xytext=(2, 3), textcoords="offset points", fontsize=8.5, color=t.ink2)
    pad = max((hi - lo) * 0.25, 60)
    ax.set_ylim(hi + pad, lo - pad)  # axe inversé : vers le haut = plus rapide
    right = race_date if race_date is not None and race_date > df["date"].max() else df["date"].max()
    ax.set_xlim(df["date"].min(), right + pd.Timedelta(days=3))
    if race_date is not None and race_date > df["date"].min():
        ax.axvline(race_date, color=t.axis, linewidth=1)
        ax.annotate("Jour J", (race_date, 1.0), xycoords=("data", "axes fraction"),
                    xytext=(-3, -10), textcoords="offset points", ha="right", fontsize=8.5, color=t.ink2)
    span = hi - lo + 2 * pad
    step = next(st for st in (60, 120, 300, 600, 1200) if span / st <= 6)
    ax.yaxis.set_major_locator(mticker.MultipleLocator(step))
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: fmt_race_time(v)))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m"))
    return fig


# --- 3. Distribution de l'intensité par semaine ------------------------------------------------


def intensity(acts: pd.DataFrame, today: date, t: Theme, weeks: int = 12) -> Figure | None:
    wk = m.weekly(acts, today, weeks)
    if wk["zone_min"].sum() == 0:
        return None
    fig, (ax,) = _fig(2.7)
    n = len(wk)
    ax.set_xlim(-0.6, n - 0.4)
    ax.set_ylim(0, 108)
    _style(ax, t, "% du temps")
    w = _bar_width(ax)
    _, pxy = _px(ax)
    gap = 2 / pxy
    colors = (t.seq[1], t.seq[2], t.seq[4]) if t.name == "light" else (t.seq[1], t.seq[3], t.seq[4])
    for i, row in wk.iterrows():
        if not row["zone_min"]:
            continue
        parts = [row["z12_pct"] or 0, row["z3_pct"] or 0, row["z45_pct"] or 0]
        y = 0.0
        for j, (p, c) in enumerate(zip(parts, colors)):
            if p <= 0:
                continue
            top = j == 2 or all(q <= 0 for q in parts[j + 1:])
            h = p - (0 if top else gap)
            if top:
                _rbar(ax, i, y, h, w, c)
            else:
                ax.add_patch(Rectangle((i - w / 2, y), w, h, facecolor=c, edgecolor="none"))
            y += p
    ax.axhline(80, color=t.ink2, linewidth=1)
    handles = [Rectangle((0, 0), 1, 1, color=c) for c in colors] + [Line2D([0], [0], color=t.ink2, linewidth=1)]
    ax.legend(handles, ["Z1-Z2 facile", "Z3 tempo", "Z4-Z5 dur", "cible 80 % en facile"], loc="lower left",
              bbox_to_anchor=(0, 1.0), ncol=4, frameon=False, fontsize=8.5, labelcolor=t.ink2, handlelength=1.2,
              handleheight=1)
    ax.set_yticks([0, 20, 40, 60, 80, 100])
    _week_ticks(ax, list(wk["monday"]))
    return fig


# --- 4. Charge aiguë vs chronique ---------------------------------------------------------------


def load(acts: pd.DataFrame, today: date, t: Theme, days: int = 120) -> Figure | None:
    ls, unit = m.load_series(acts, today, days)
    ls = ls.dropna(subset=["chronic"])
    if len(ls) < 14 or ls["chronic"].max() == 0:
        return None
    fig, (ax,) = _fig(2.6)
    _style(ax, t, f"{unit} / 7 j")
    x = ls.index
    ax.fill_between(x, ls["chronic"] * 0.8, ls["chronic"] * 1.3, color=t.run, alpha=0.10, linewidth=0)
    ax.plot(x, ls["chronic"], color=t.ink2, linewidth=2, solid_capstyle="round")
    ax.plot(x, ls["acute"], color=t.run, linewidth=2, solid_capstyle="round", solid_joinstyle="round")
    end = x[-1]
    ax.scatter([end], [ls["acute"].iloc[-1]], s=60, color=t.run, zorder=3)
    a, c = ls["acute"].iloc[-1], ls["chronic"].iloc[-1]
    _label(ax, mdates.date2num(end), a, f"aiguë {a:.0f}", t, offset=(7, 0), ha="left", va="center", color=t.ink, weight="bold")
    _label(ax, mdates.date2num(end), c, f"chronique {c:.0f}", t, offset=(7, -11 if a > c else 11), ha="left", va="center")
    ax.set_ylim(0, max(ls["acute"].max(), ls["chronic"].max() * 1.3) * 1.12)
    ax.set_xlim(x[0], end + pd.Timedelta(days=1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m"))
    ax.annotate("bande : 0,8 à 1,3 × la chronique", (0, 1), xycoords="axes fraction", xytext=(2, -2),
                textcoords="offset points", va="top", fontsize=8, color=t.muted)
    return fig


# --- 5. Forme : HRV, FC repos, sommeil (petits multiples) ---------------------------------------


def form(wellness: pd.DataFrame, today: date, t: Theme, days: int = 70) -> Figure | None:
    if wellness.empty:
        return None
    w = m.between(wellness, today - timedelta(days=days), today)
    panels = [(c, lbl) for c, lbl in (("hrv_night", "HRV nuit (ms)"), ("rhr", "FC repos (bpm)"), ("sleep_h", "Sommeil (h)"))
              if c in w and w[c].notna().sum() >= 5]
    if not panels:
        return None
    fig, axes = _fig(1.35 * len(panels) + 0.4, len(panels))
    for ax, (col, lbl) in zip(axes, panels):
        _style(ax, t)
        s = w.dropna(subset=[col])
        if col == "hrv_night" and "hrv_base_low" in s and s["hrv_base_low"].notna().any():
            ax.fill_between(s["date"], s["hrv_base_low"], s["hrv_base_high"], color=t.run, alpha=0.10, linewidth=0, step="mid")
        if col == "sleep_h":
            ax.axhline(7, color=t.axis, linewidth=1)
        roll = s.set_index("date")[col].rolling("7D").mean()
        ax.scatter(s["date"], s[col], s=9, color=t.run_soft, linewidths=0, zorder=2)
        ax.plot(roll.index, roll.values, color=t.run, linewidth=2, solid_capstyle="round", zorder=3)
        ax.annotate(lbl, (0, 1), xycoords="axes fraction", xytext=(0, 2), textcoords="offset points", fontsize=8.5,
                    color=t.ink2, va="bottom")
        _label(ax, mdates.date2num(roll.index[-1]), roll.iloc[-1], f"{roll.iloc[-1]:.0f}" if col != "sleep_h" else f"{roll.iloc[-1]:.1f}",
               t, offset=(6, 0), ha="left", va="center", color=t.ink, weight="bold")
        lo, hi = s[col].min(), s[col].max()
        pad = (hi - lo) * 0.2 or 1
        ax.set_ylim(lo - pad, hi + pad)
        ax.yaxis.set_major_locator(mticker.MaxNLocator(nbins=3, integer=col != "sleep_h"))
    axes[-1].xaxis.set_major_formatter(mdates.DateFormatter("%d/%m"))
    axes[-1].set_xlim(pd.Timestamp(today - timedelta(days=days)), pd.Timestamp(today) + pd.Timedelta(days=2))
    fig.subplots_adjust(hspace=0.55)
    return fig


# --- 6. Heatmap de régularité (façon contributions GitHub) ----------------------------------------


def heatmap(acts: pd.DataFrame, today: date, t: Theme, weeks: int = 53) -> Figure:
    acts = m.ensure_columns(acts)
    start = monday_of(today) - timedelta(weeks=weeks - 1)
    daily = m.between(acts, start, today).groupby("date")["duration_min"].sum()
    bins = [0, 30, 60, 90]  # minutes : 1-30, 31-60, 61-90, > 90
    fig, (ax,) = _fig(1.75)
    ax.set_xlim(-0.5, weeks - 0.5)
    ax.set_ylim(7.6, -1.6)
    ax.axis("off")
    cell = 0.78
    month_seen = set()
    for wi in range(weeks):
        mon = start + timedelta(weeks=wi)
        if mon.day <= 7 and (mon.year, mon.month) not in month_seen:
            month_seen.add((mon.year, mon.month))
            ax.text(wi - 0.4, -1.0, FR_MONTHS[mon.month - 1].rstrip("."), fontsize=7.5, color=t.muted, va="center")
        for di in range(7):
            d = mon + timedelta(days=di)
            if d > today:
                continue
            v = float(daily.get(pd.Timestamp(d), 0))
            if v <= 0:
                c = t.empty
            else:
                level = sum(v > b for b in bins)  # 1..4
                c = t.seq[level]
            ax.add_patch(FancyBboxPatch((wi - cell / 2, di - cell / 2), cell, cell,
                                        boxstyle="round,pad=0,rounding_size=0.16", facecolor=c, edgecolor="none"))
    for di, lbl in ((0, "Lu"), (2, "Me"), (4, "Ve"), (6, "Di")):
        ax.text(-1.0, di, lbl, fontsize=7.5, color=t.muted, ha="right", va="center")
    # Légende : moins → plus
    x0 = weeks - 9
    ax.text(x0 - 0.7, 8.4, "0 min", fontsize=7.5, color=t.muted, ha="right", va="center")
    for k, c in enumerate([t.empty, *t.seq[1:]]):
        ax.add_patch(FancyBboxPatch((x0 + k - cell / 2, 8.4 - cell / 2), cell, cell,
                                    boxstyle="round,pad=0,rounding_size=0.16", facecolor=c, edgecolor="none"))
    ax.text(x0 + 5 - 0.3, 8.4, "> 90 min", fontsize=7.5, color=t.muted, ha="left", va="center")
    ax.set_ylim(9.0, -1.6)
    return fig


# --- 7. Efficience aérobie -----------------------------------------------------------------------


def efficiency(acts: pd.DataFrame, today: date, t: Theme, days: int = 180) -> Figure | None:
    ef = m.aerobic_efficiency(acts)
    ef = ef[ef["date"] >= pd.Timestamp(today - timedelta(days=days))]
    if len(ef) < 10:  # en dessous, la tendance ne veut rien dire
        return None
    fig, (ax,) = _fig(2.4)
    _style(ax, t, "m / battement")
    ax.scatter(ef["date"], ef["ef"], s=22, color=t.run_soft, linewidths=0, zorder=2)
    roll = ef.set_index("date")["ef"].rolling("28D", min_periods=3).median().dropna()
    if len(roll):
        ax.plot(roll.index, roll.values, color=t.run, linewidth=2, solid_capstyle="round", zorder=3)
        _label(ax, mdates.date2num(roll.index[-1]), roll.iloc[-1], f"{roll.iloc[-1]:.2f}", t, offset=(6, 0), ha="left",
               va="center", color=t.ink, weight="bold")
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m"))
    return fig


# --- Rendu -------------------------------------------------------------------------------------------


def render_all(acts: pd.DataFrame, wellness: pd.DataFrame, metrics_df: pd.DataFrame, goal: dict,
               today: date, out_dir: Path) -> dict[str, bool]:
    """Écrit <nom>-light.svg et <nom>-dark.svg. Renvoie {nom: produit ?}."""
    builders = {
        "volume": lambda t: volume(acts, today, t),
        "prediction": lambda t: prediction(metrics_df, goal, today, t),
        "intensite": lambda t: intensity(acts, today, t),
        "charge": lambda t: load(acts, today, t),
        "forme": lambda t: form(wellness, today, t),
        "regularite": lambda t: heatmap(acts, today, t),
        "efficience": lambda t: efficiency(acts, today, t),
    }
    produced: dict[str, bool] = {}
    if acts.empty:
        return produced  # rien à tracer avant la première sync
    for name, build in builders.items():
        ok = False
        for t in THEMES:
            fig = build(t)
            if fig is None:
                break
            _save(fig, out_dir / f"{name}-{t.name}.svg")
            ok = True
        produced[name] = ok
    return produced
