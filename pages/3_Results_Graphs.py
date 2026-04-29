import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.title("📈 ABC Optimization — Results & Graphs")
st.markdown("Full breakdown of optimization results, parameter comparison, and convergence graphs.")
st.markdown("---")

# ------------------ CHECK SESSION STATE ------------------
required_keys = [
    "abc_best_pmax", "abc_best_sol", "abc_error_history",
    "abc_pmax_meas", "Pmax_calculated", "Pmax_STC",
    "Ftemp_P", "Fg", "Fage",
]
missing = [k for k in required_keys if k not in st.session_state]

if missing:
    st.warning(
        "⚠️ No ABC results found. "
        "Please run the **ABC Optimizer page** first and click **Run ABC Optimization**."
    )
    st.stop()

# ------------------ PULL VALUES ------------------
best_pmax     = st.session_state["abc_best_pmax"]
best_sol      = st.session_state["abc_best_sol"]
error_history = st.session_state["abc_error_history"]
Pmax_meas     = st.session_state["abc_pmax_meas"]
Pmax_orig     = st.session_state["Pmax_calculated"]
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

Pmax_meas_val = st.session_state.get("abc_pmax_meas", 0.0)
Vmp_meas      = st.session_state.get("abc_vmp_meas",  0.0)
Imp_meas      = st.session_state.get("abc_imp_meas",  0.0)
Voc_meas      = st.session_state.get("abc_voc_meas",  0.0)
Isc_meas      = st.session_state.get("abc_isc_meas",  0.0)

BG_opt, dirt_opt, Fmm_opt, Fshade_opt = best_sol

G_front    = Fg * 1000
G_total    = G_front * (1 + BG_opt)
Fg_eff     = G_total / 1000
Fclean_opt = (100 - dirt_opt) / 100

abs_error  = abs(best_pmax - Pmax_meas)
pct_error  = (abs_error / Pmax_meas * 100) if Pmax_meas != 0 else 0
orig_error = abs(Pmax_orig - Pmax_meas)
orig_pct   = (orig_error / Pmax_meas * 100) if Pmax_meas != 0 else 0
improvement = orig_error - abs_error

# ------------------ SECTION 1: OPTIMIZED FACTORS ------------------
st.subheader("🔧 Optimized Controllable Factors")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Optimal BG",           f"{BG_opt:.4f}")
col2.metric("Optimal Dirt (%)",     f"{dirt_opt:.4f}")
col3.metric("Optimal Fmm",         f"{Fmm_opt:.4f}")
col4.metric("Optimal Fshade",      f"{Fshade_opt:.4f}")

st.markdown("---")

# ------------------ SECTION 2: PMAX COMPARISON ------------------
st.subheader("⚡ Pmax — Measured vs Optimized")

col_a, col_b, col_c, col_d = st.columns(4)
col_a.metric("Measured Pmax (W)",   f"{Pmax_meas:.4f}")
col_b.metric("Optimized Pmax (W)",  f"{best_pmax:.4f}")
col_c.metric("Absolute Error (W)",  f"{abs_error:.4f}")
col_d.metric("Error (%)",           f"{pct_error:.4f} %")

st.markdown("---")

# ------------------ SECTION 3: BEFORE vs AFTER ------------------
st.subheader("📊 Before vs After ABC — Pmax")

col_e, col_f, col_g, col_h = st.columns(4)
col_e.metric("Before ABC — Pmax (W)",   f"{Pmax_orig:.4f}")
col_f.metric("Before ABC — Error (W)",  f"{orig_error:.4f}")
col_g.metric("After ABC — Pmax (W)",    f"{best_pmax:.4f}")
col_h.metric("After ABC — Error (W)",   f"{abs_error:.4f}",
             delta=f"{abs_error - orig_error:.4f} W", delta_color="inverse")

st.markdown("---")

# ------------------ SECTION 4: ALL FIVE OUTPUTS TABLE ------------------
st.subheader("📋 Measured vs Calculated — All Five Outputs")

rows = [("Pmax (W)", Pmax_meas, best_pmax)]

if Isc_stc:
    Isc_calc = Isc_stc * Ftemp_Isc * Fg_eff * Fclean_opt * Fshade_opt
    rows.append(("Isc (A)", Isc_meas, Isc_calc))
if Imp_stc:
    Imp_calc = Imp_stc * Ftemp_Imp * Fg_eff * Fclean_opt * Fshade_opt
    rows.append(("Imp (A)", Imp_meas, Imp_calc))
if Voc_stc:
    Voc_calc = Voc_stc * Ftemp_Voc
    rows.append(("Voc (V)", Voc_meas, Voc_calc))
if Vmp_stc:
    Vmp_calc = Vmp_stc * Ftemp_Vmp
    rows.append(("Vmp (V)", Vmp_meas, Vmp_calc))

header = st.columns(4)
header[0].markdown("**Parameter**")
header[1].markdown("**Measured**")
header[2].markdown("**Calculated**")
header[3].markdown("**Error (%)**")

for param, meas, calc in rows:
    err_p = abs(calc - meas) / meas * 100 if meas != 0 else 0
    c1, c2, c3, c4 = st.columns(4)
    c1.write(param)
    c2.write(f"{meas:.4f}")
    c3.write(f"{calc:.4f}")
    c4.write(f"{err_p:.4f} %")

st.info(
    "Voc and Vmp errors reflect temperature correction only — "
    "they are not affected by the optimized factors (BG, dirt, Fmm, Fshade)."
)

st.markdown("---")

# ------------------ SECTION 5: CALCULATION STEPS ------------------
st.subheader("🧮 Optimized Calculation Steps")

st.write(f"1️⃣ G_front (from Fg) = {Fg:.4f} × 1000 = **{G_front:.2f} W/m²**")
st.write(f"2️⃣ Total irradiance with optimal BG = {G_front:.2f} × (1 + {BG_opt:.4f}) = **{G_total:.2f} W/m²**")
st.write(f"3️⃣ Effective Fg = {G_total:.2f} / 1000 = **{Fg_eff:.4f}**")
st.write(f"4️⃣ Fclean = (100 − {dirt_opt:.4f}) / 100 = **{Fclean_opt:.4f}**")
st.write(
    f"5️⃣ Pmax = {Pmax_stc:.2f} × {Ftemp_P:.4f} × {Fg_eff:.4f} × "
    f"{Fclean_opt:.4f} × {Fshade_opt:.4f} × {Fmm_opt:.4f} × {Fage:.4f} "
    f"= **{best_pmax:.4f} W**"
)
st.write(
    f"6️⃣ Absolute error = |{best_pmax:.4f} − {Pmax_meas:.4f}| "
    f"= **{abs_error:.4f} W ({pct_error:.4f}%)**"
)

st.markdown("---")

# ------------------ SECTION 6: GRAPHS ------------------
st.subheader("📈 Graphs")

cycles = list(range(1, len(error_history) + 1))

col_g1, col_g2 = st.columns(2)

# ---- Graph 1: Error Convergence ----
with col_g1:
    st.markdown("#### Error Convergence History")
    st.line_chart({"Absolute Error — Pmax (W)": error_history})
    st.caption(
        "Each point = best |Pmax_calc − Pmax_meas| found up to that cycle. "
        "A flat tail means the algorithm has converged."
    )

# ---- Graph 2: Pmax Bar Comparison ----
with col_g2:
    st.markdown("#### Pmax — Measured vs Before/After ABC")
    bar_data = {
        "Pmax (W)": [Pmax_meas, Pmax_orig, best_pmax]
    }
    import pandas as pd
    df_bar = pd.DataFrame(bar_data, index=["Measured", "Before ABC", "After ABC"])
    st.bar_chart(df_bar)
    st.caption("Compares the measured Pmax against the original calculated value and the ABC-optimized value.")

# ---- Graph 3 & 4 (only if more than Pmax) ----
if len(rows) > 1:
    col_g3, col_g4 = st.columns(2)

    # ---- Graph 3: Error % per parameter ----
    with col_g3:
        st.markdown("#### Error (%) per Output Parameter")
        params = [r[0] for r in rows]
        errors = [abs((r[2] - r[1]) / r[1] * 100) if r[1] != 0 else 0 for r in rows]
        df_err = pd.DataFrame({"Error (%)": errors}, index=params)
        st.bar_chart(df_err)
        st.caption("Lower is better. Green threshold = 2%, amber = 5%.")

    # ---- Graph 4: Measured vs Calculated per parameter ----
    with col_g4:
        st.markdown("#### Measured vs Calculated — All Parameters")
        df_compare = pd.DataFrame(
            {
                "Measured":   [r[1] for r in rows],
                "Calculated": [r[2] for r in rows],
            },
            index=[r[0] for r in rows]
        )
        st.bar_chart(df_compare)
        st.caption("Side-by-side comparison of measured field values vs ABC-optimized calculated values.")

st.markdown("---")
st.info(
    "ABC tuned BG, dirt, Fmm, and Fshade to minimise |Pmax_calc − Pmax_measured|. "
    "All other factors were fixed from the Computational Tool."
)
