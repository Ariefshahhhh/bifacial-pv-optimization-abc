import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np

st.set_page_config(page_title="ABC Results & Graphs", layout="wide")

st.markdown("""
<style>
    html, body, [class*="css"] { font-family: 'Segoe UI', sans-serif; }

    .page-title { font-size: 1.75rem; font-weight: 700; color: #1e293b; margin-bottom: 0.15rem; }
    .page-sub   { font-size: 0.85rem; color: #64748b; margin-bottom: 0.5rem; }

    .section-header {
        font-size: 0.68rem; font-weight: 700; letter-spacing: 0.13em;
        text-transform: uppercase; color: #2563eb;
        border-bottom: 2px solid #2563eb;
        padding-bottom: 4px; margin: 1.4rem 0 0.75rem 0;
    }

    hr { border: none; border-top: 1px solid #e5e7eb; margin: 1.2rem 0; }

    /* ── Summary cards ── */
    .card-row {
        display: grid; gap: 0.75rem; margin: 0.75rem 0 1.2rem 0;
    }
    .card-row-4 { grid-template-columns: repeat(4, 1fr); }
    .card-row-3 { grid-template-columns: repeat(3, 1fr); }
    .card-row-5 { grid-template-columns: repeat(5, 1fr); }

    .card {
        background: #f8fafc; border: 1px solid #e2e8f0;
        border-top: 3px solid #2563eb; border-radius: 8px;
        padding: 0.85rem 1rem; text-align: center;
    }
    .card.blue  { background: #eff6ff; border-top-color: #1d4ed8; }
    .card.green { background: #f0fdf4; border-top-color: #16a34a; }
    .card.amber { background: #fffbeb; border-top-color: #d97706; }
    .card.red   { background: #fef2f2; border-top-color: #dc2626; }

    .c-label {
        font-size: 0.67rem; font-weight: 700; letter-spacing: 0.1em;
        text-transform: uppercase; color: #6b7280; margin-bottom: 0.3rem;
    }
    .c-value { font-size: 1.4rem; font-weight: 700; color: #1e293b; line-height: 1.1; }
    .card.blue  .c-value { color: #1d4ed8; }
    .card.green .c-value { color: #16a34a; }
    .card.amber .c-value { color: #d97706; }
    .card.red   .c-value { color: #dc2626; }
    .c-unit { font-size: 0.7rem; color: #94a3b8; margin-top: 0.2rem; }

    /* ── Table ── */
    .tbl { width: 100%; border-collapse: collapse; font-size: 0.82rem; margin-top: 0.5rem; }
    .tbl th {
        background: #f1f5f9; color: #374151; font-weight: 600;
        text-align: left; padding: 0.55rem 0.9rem;
        border-bottom: 2px solid #e2e8f0; font-size: 0.75rem;
        letter-spacing: 0.05em; text-transform: uppercase;
    }
    .tbl td { padding: 0.55rem 0.9rem; border-bottom: 1px solid #e2e8f0; color: #374151; }
    .tbl tr:last-child td { border-bottom: none; }
    .tbl tr:nth-child(even) td { background: #f8fafc; }
    .tbl td.bold { font-weight: 700; color: #1e293b; }
    .tbl td.good { color: #16a34a; font-weight: 600; }
    .tbl td.warn { color: #d97706; font-weight: 600; }
    .tbl td.bad  { color: #dc2626; font-weight: 600; }

    /* ── Steps ── */
    .steps-wrap {
        background: #f8fafc; border: 1px solid #e2e8f0;
        border-radius: 8px; overflow: hidden; margin-top: 0.5rem;
    }
    .step-row {
        display: flex; align-items: flex-start; gap: 0.9rem;
        padding: 0.65rem 1.1rem; border-bottom: 1px solid #e2e8f0;
        font-size: 0.82rem; color: #374151; line-height: 1.65;
    }
    .step-row:last-child { border-bottom: none; }
    .step-row:nth-child(even) { background: #ffffff; }
    .step-n {
        min-width: 22px; height: 22px; background: #2563eb; color: #fff;
        border-radius: 50%; font-size: 0.65rem; font-weight: 700;
        display: flex; align-items: center; justify-content: center;
        margin-top: 2px; flex-shrink: 0;
    }
    .step-row b { color: #1e293b; }

    .info-note {
        font-size: 0.78rem; color: #1d4ed8; background: #eff6ff;
        border: 1px solid #bfdbfe; border-radius: 6px;
        padding: 0.6rem 1rem; margin-top: 1rem;
    }
    .warn-note {
        font-size: 0.78rem; color: #92400e; background: #fffbeb;
        border: 1px solid #fcd34d; border-radius: 6px;
        padding: 0.6rem 1rem; margin-top: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown('<div class="page-title">📈 ABC Optimization — Results & Graphs</div>', unsafe_allow_html=True)
st.markdown('<div class="page-sub">Detailed results, comparison table, and convergence analysis from the ABC run.</div>', unsafe_allow_html=True)
st.markdown('<hr>', unsafe_allow_html=True)

# ── Guard: check session state ────────────────────────────────────────────────
required = [
    "abc_best_pmax", "abc_best_sol", "abc_error_history",
    "abc_pmax_meas", "Pmax_calculated", "Pmax_STC",
    "Ftemp_P", "Fg", "Fage",
]
missing = [k for k in required if k not in st.session_state]

if missing:
    st.warning(
        "⚠️ No ABC results found. Please run the **ABC Optimizer page** first."
    )
    st.stop()

# ── Pull values ───────────────────────────────────────────────────────────────
best_pmax     = st.session_state["abc_best_pmax"]
best_sol      = st.session_state["abc_best_sol"]          # [BG, dirt, Fmm, Fshade]
error_history = st.session_state["abc_error_history"]
Pmax_meas     = st.session_state["abc_pmax_meas"]
Pmax_calc_orig= st.session_state["Pmax_calculated"]
Pmax_stc      = st.session_state["Pmax_STC"]
Ftemp_P       = st.session_state["Ftemp_P"]
Fg            = st.session_state["Fg"]
Fage          = st.session_state["Fage"]

Ftemp_Isc = st.session_state.get("Ftemp_Isc", 1.0)
Ftemp_Imp = st.session_state.get("Ftemp_Imp", 1.0)
Ftemp_Voc = st.session_state.get("Ftemp_Voc", 1.0)
Ftemp_Vmp = st.session_state.get("Ftemp_Vmp", 1.0)
Isc_stc   = st.session_state.get("Isc_stc", None)
Imp_stc   = st.session_state.get("Imp_stc", None)
Voc_stc   = st.session_state.get("Voc_stc", None)
Vmp_stc   = st.session_state.get("Vmp_stc", None)

Vmp_meas = st.session_state.get("abc_vmp_meas", 0.0)
Imp_meas = st.session_state.get("abc_imp_meas", 0.0)
Voc_meas = st.session_state.get("abc_voc_meas", 0.0)
Isc_meas = st.session_state.get("abc_isc_meas", 0.0)

BG_opt, dirt_opt, Fmm_opt, Fshade_opt = best_sol

G_front    = Fg * 1000
G_total    = G_front * (1 + BG_opt)
Fg_eff     = G_total / 1000
Fclean_opt = (100 - dirt_opt) / 100

abs_error  = abs(best_pmax - Pmax_meas)
pct_error  = (abs_error / Pmax_meas * 100) if Pmax_meas != 0 else 0
orig_error = abs(Pmax_calc_orig - Pmax_meas)
orig_pct   = (orig_error / Pmax_meas * 100) if Pmax_meas != 0 else 0
improvement= orig_error - abs_error

def err_class(pct):
    if pct < 2:   return "good"
    if pct < 5:   return "warn"
    return "bad"

# ── 1. Optimized Factors ──────────────────────────────────────────────────────
st.markdown('<div class="section-header">🔧 Optimized Controllable Factors</div>', unsafe_allow_html=True)
st.markdown(f"""
<div class="card-row card-row-4">
    <div class="card blue">
        <div class="c-label">Bifacial Gain (BG)</div>
        <div class="c-value">{BG_opt:.4f}</div>
        <div class="c-unit">optimized</div>
    </div>
    <div class="card">
        <div class="c-label">Dirt Level</div>
        <div class="c-value">{dirt_opt:.4f}</div>
        <div class="c-unit">%</div>
    </div>
    <div class="card">
        <div class="c-label">Mismatch Factor (Fmm)</div>
        <div class="c-value">{Fmm_opt:.4f}</div>
        <div class="c-unit">optimized</div>
    </div>
    <div class="card">
        <div class="c-label">Shading Factor (Fshade)</div>
        <div class="c-value">{Fshade_opt:.4f}</div>
        <div class="c-unit">optimized</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── 2. Pmax Summary ───────────────────────────────────────────────────────────
st.markdown('<div class="section-header">⚡ Pmax — Measured vs Calculated</div>', unsafe_allow_html=True)
st.markdown(f"""
<div class="card-row card-row-4">
    <div class="card">
        <div class="c-label">Measured Pmax</div>
        <div class="c-value">{Pmax_meas:.4f}</div>
        <div class="c-unit">W · field measurement</div>
    </div>
    <div class="card green">
        <div class="c-label">ABC Optimized Pmax</div>
        <div class="c-value">{best_pmax:.4f}</div>
        <div class="c-unit">W · after optimization</div>
    </div>
    <div class="card {'green' if pct_error < 2 else 'amber' if pct_error < 5 else 'red'}">
        <div class="c-label">Absolute Error</div>
        <div class="c-value">{abs_error:.4f}</div>
        <div class="c-unit">W · {pct_error:.3f}%</div>
    </div>
    <div class="card {'green' if improvement > 0 else 'amber'}">
        <div class="c-label">Error Reduction</div>
        <div class="c-value">{improvement:.4f}</div>
        <div class="c-unit">W improvement over original</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── 3. Before vs After ────────────────────────────────────────────────────────
st.markdown('<div class="section-header">📊 Before vs After ABC — Pmax</div>', unsafe_allow_html=True)
st.markdown(f"""
<div class="card-row card-row-3">
    <div class="card">
        <div class="c-label">Before ABC (Original Calc)</div>
        <div class="c-value">{Pmax_calc_orig:.4f} W</div>
        <div class="c-unit">Error = {orig_error:.4f} W ({orig_pct:.3f}%)</div>
    </div>
    <div class="card green">
        <div class="c-label">After ABC (Optimized)</div>
        <div class="c-value">{best_pmax:.4f} W</div>
        <div class="c-unit">Error = {abs_error:.4f} W ({pct_error:.3f}%)</div>
    </div>
    <div class="card blue">
        <div class="c-label">Measured (Reference)</div>
        <div class="c-value">{Pmax_meas:.4f} W</div>
        <div class="c-unit">field measurement</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── 4. Full Output Comparison Table ──────────────────────────────────────────
st.markdown('<div class="section-header">📋 All Five Outputs — Measured vs Calculated</div>', unsafe_allow_html=True)

rows = []
rows.append(("Pmax", "W", Pmax_meas, best_pmax))
if Isc_stc:
    Isc_calc = Isc_stc * Ftemp_Isc * Fg_eff * Fclean_opt * Fshade_opt
    rows.append(("Isc", "A", Isc_meas, Isc_calc))
if Imp_stc:
    Imp_calc = Imp_stc * Ftemp_Imp * Fg_eff * Fclean_opt * Fshade_opt
    rows.append(("Imp", "A", Imp_meas, Imp_calc))
if Voc_stc:
    Voc_calc = Voc_stc * Ftemp_Voc
    rows.append(("Voc", "V", Voc_meas, Voc_calc))
if Vmp_stc:
    Vmp_calc = Vmp_stc * Ftemp_Vmp
    rows.append(("Vmp", "V", Vmp_meas, Vmp_calc))

table_rows = ""
for param, unit, meas, calc in rows:
    diff   = calc - meas
    pct    = abs(diff / meas * 100) if meas != 0 else 0
    cls    = err_class(pct)
    sign   = "+" if diff >= 0 else ""
    table_rows += f"""
    <tr>
        <td class="bold">{param}</td>
        <td>{unit}</td>
        <td>{meas:.4f}</td>
        <td>{calc:.4f}</td>
        <td>{sign}{diff:.4f}</td>
        <td class="{cls}">{pct:.3f}%</td>
    </tr>"""

st.markdown(f"""
<table class="tbl">
    <thead>
        <tr>
            <th>Parameter</th><th>Unit</th>
            <th>Measured</th><th>Calculated</th>
            <th>Difference</th><th>Error (%)</th>
        </tr>
    </thead>
    <tbody>{table_rows}</tbody>
</table>
<div class="warn-note">
    ℹ Voc and Vmp errors reflect temperature-only correction — they are not affected by the optimized factors.
</div>
""", unsafe_allow_html=True)

# ── 5. Calculation Steps ──────────────────────────────────────────────────────
st.markdown('<div class="section-header">🧮 Optimized Calculation Steps</div>', unsafe_allow_html=True)
st.markdown(f"""
<div class="steps-wrap">
    <div class="step-row">
        <div class="step-n">1</div>
        <div>G_front (from Fg) = {Fg:.4f} × 1000 = <b>{G_front:.2f} W/m²</b></div>
    </div>
    <div class="step-row">
        <div class="step-n">2</div>
        <div>Total irradiance with optimal BG = {G_front:.2f} × (1 + {BG_opt:.4f}) = <b>{G_total:.2f} W/m²</b></div>
    </div>
    <div class="step-row">
        <div class="step-n">3</div>
        <div>Effective Fg = {G_total:.2f} / 1000 = <b>{Fg_eff:.4f}</b></div>
    </div>
    <div class="step-row">
        <div class="step-n">4</div>
        <div>Fclean = (100 − {dirt_opt:.4f}) / 100 = <b>{Fclean_opt:.4f}</b></div>
    </div>
    <div class="step-row">
        <div class="step-n">5</div>
        <div>
            Pmax = {Pmax_stc:.2f} × {Ftemp_P:.4f} × {Fg_eff:.4f} ×
            {Fclean_opt:.4f} × {Fshade_opt:.4f} × {Fmm_opt:.4f} × {Fage:.4f}
            = <b>{best_pmax:.4f} W</b>
        </div>
    </div>
    <div class="step-row">
        <div class="step-n">6</div>
        <div>Absolute error = |{best_pmax:.4f} − {Pmax_meas:.4f}| = <b>{abs_error:.4f} W ({pct_error:.4f}%)</b></div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── 6. Graphs ─────────────────────────────────────────────────────────────────
st.markdown('<hr>', unsafe_allow_html=True)
st.markdown('<div class="section-header">📈 Graphs</div>', unsafe_allow_html=True)

cycles = list(range(1, len(error_history) + 1))

# Style
plt.rcParams.update({
    "font.family":       "DejaVu Sans",
    "axes.spines.top":   False,
    "axes.spines.right": False,
    "axes.grid":         True,
    "grid.color":        "#e5e7eb",
    "grid.linewidth":    0.8,
    "axes.facecolor":    "#f8fafc",
    "figure.facecolor":  "#ffffff",
})

col_g1, col_g2 = st.columns(2)

# ── Graph 1: Error convergence ────────────────────────────────────────────────
with col_g1:
    st.markdown("**Error Convergence History**")
    fig1, ax1 = plt.subplots(figsize=(6, 3.8))
    ax1.plot(cycles, error_history, color="#2563eb", linewidth=1.8, label="Abs Error (W)")
    ax1.fill_between(cycles, error_history, alpha=0.08, color="#2563eb")
    ax1.axhline(min(error_history), color="#16a34a", linewidth=1.2,
                linestyle="--", label=f"Min error = {min(error_history):.4f} W")
    ax1.set_xlabel("Cycle", fontsize=9, color="#374151")
    ax1.set_ylabel("Absolute Error (W)", fontsize=9, color="#374151")
    ax1.set_title("ABC Convergence — Pmax Error per Cycle", fontsize=10, color="#1e293b", fontweight="bold")
    ax1.legend(fontsize=8)
    ax1.tick_params(labelsize=8, colors="#6b7280")
    plt.tight_layout()
    st.pyplot(fig1)
    plt.close(fig1)

# ── Graph 2: Measured vs Calculated bar ───────────────────────────────────────
with col_g2:
    st.markdown("**Measured vs Calculated Pmax**")
    fig2, ax2 = plt.subplots(figsize=(6, 3.8))
    labels = ["Measured", "Before ABC", "After ABC"]
    values = [Pmax_meas, Pmax_calc_orig, best_pmax]
    colors = ["#64748b", "#f59e0b", "#2563eb"]
    bars   = ax2.bar(labels, values, color=colors, width=0.45, zorder=3)
    for bar, val in zip(bars, values):
        ax2.text(bar.get_x() + bar.get_width() / 2,
                 bar.get_height() + max(values) * 0.005,
                 f"{val:.2f} W", ha="center", va="bottom", fontsize=8.5,
                 color="#1e293b", fontweight="600")
    ax2.set_ylabel("Pmax (W)", fontsize=9, color="#374151")
    ax2.set_title("Pmax — Measured vs Before/After ABC", fontsize=10, color="#1e293b", fontweight="bold")
    ax2.tick_params(labelsize=9, colors="#6b7280")
    y_min = min(values) * 0.97
    y_max = max(values) * 1.04
    ax2.set_ylim(y_min, y_max)
    plt.tight_layout()
    st.pyplot(fig2)
    plt.close(fig2)

# ── Graph 3: Error % per parameter ───────────────────────────────────────────
if len(rows) > 1:
    col_g3, col_g4 = st.columns(2)

    with col_g3:
        st.markdown("**Error (%) per Output Parameter**")
        fig3, ax3 = plt.subplots(figsize=(6, 3.8))
        params  = [r[0] for r in rows]
        errors  = [abs((r[3] - r[2]) / r[2] * 100) if r[2] != 0 else 0 for r in rows]
        bar_clr = ["#16a34a" if e < 2 else "#f59e0b" if e < 5 else "#dc2626" for e in errors]
        ax3.barh(params, errors, color=bar_clr, height=0.45, zorder=3)
        ax3.axvline(2, color="#f59e0b", linewidth=1.1, linestyle="--", label="2% threshold")
        ax3.axvline(5, color="#dc2626", linewidth=1.1, linestyle="--", label="5% threshold")
        for i, (p, e) in enumerate(zip(params, errors)):
            ax3.text(e + 0.05, i, f"{e:.3f}%", va="center", fontsize=8.5, color="#1e293b")
        ax3.set_xlabel("Error (%)", fontsize=9, color="#374151")
        ax3.set_title("Parameter-wise Percentage Error", fontsize=10, color="#1e293b", fontweight="bold")
        ax3.legend(fontsize=8)
        ax3.tick_params(labelsize=9, colors="#6b7280")
        plt.tight_layout()
        st.pyplot(fig3)
        plt.close(fig3)

    # ── Graph 4: Measured vs Calculated per parameter ─────────────────────────
    with col_g4:
        st.markdown("**Measured vs Calculated — All Parameters**")
        fig4, ax4 = plt.subplots(figsize=(6, 3.8))
        x      = np.arange(len(rows))
        width  = 0.35
        meas_v = [r[2] for r in rows]
        calc_v = [r[3] for r in rows]
        b1 = ax4.bar(x - width/2, meas_v, width, label="Measured",   color="#64748b", zorder=3)
        b2 = ax4.bar(x + width/2, calc_v, width, label="Calculated", color="#2563eb", zorder=3)
        ax4.set_xticks(x)
        ax4.set_xticklabels([r[0] for r in rows], fontsize=9)
        ax4.set_ylabel("Value", fontsize=9, color="#374151")
        ax4.set_title("Measured vs Calculated — All Outputs", fontsize=10, color="#1e293b", fontweight="bold")
        ax4.legend(fontsize=8)
        ax4.tick_params(labelsize=8, colors="#6b7280")
        plt.tight_layout()
        st.pyplot(fig4)
        plt.close(fig4)

st.markdown("""
<div class="info-note">
    ℹ ABC optimized BG, dirt, Fmm, and Fshade to minimise |Pmax_calc − Pmax_measured|.
    Voc and Vmp are temperature-only — not affected by the optimized factors.
</div>
""", unsafe_allow_html=True)
