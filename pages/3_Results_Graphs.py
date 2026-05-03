import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

st.title("📈 ABC Optimization — Results & Graphs")
st.markdown("Full breakdown of optimization results, parameter comparison, and convergence graphs.")
st.markdown("---")

# ------------------ CHECK SESSION STATE ------------------
required_keys = [
    "abc_all_results", "abc_pmax_meas_list",
    "Pmax_calculated", "Pmax_STC", "Ftemp_P", "Fg", "Fage",
]
missing = [k for k in required_keys if k not in st.session_state]

if missing:
    st.warning(
        "⚠️ No ABC results found. "
        "Please run the **ABC Optimizer page** first and click **Run ABC Optimization**."
    )
    st.stop()

# ------------------ PULL VALUES ------------------
all_results    = st.session_state["abc_all_results"]
pmax_meas_list = st.session_state["abc_pmax_meas_list"]
Pmax_calc_list = st.session_state["Pmax_calculated"]
Pmax_stc       = st.session_state["Pmax_STC"]
Ftemp_P        = st.session_state["Ftemp_P"]
Fg             = st.session_state["Fg"]
Fage           = st.session_state["Fage"]

st.markdown("---")

# ------------------ SECTION 1: OPTIMIZED FACTORS ------------------
st.subheader("🔧 Optimized Controllable Factors")

header_cols = st.columns(5)
for i, col in enumerate(header_cols):
    col.markdown(f"**Set {i+1}**")

for label, idx in [("BG", 0), ("Dirt (%)", 1), ("Fmm", 2), ("Fshade", 3)]:
    row_cols = st.columns(5)
    for i, col in enumerate(row_cols):
        if all_results[i] is not None:
            val = all_results[i][0][idx]
            col.write(f"{label}: {val:.4f}")
        else:
            col.write(f"{label}: —")

st.markdown("---")

# ------------------ SECTION 2: PMAX COMPARISON ------------------
st.subheader("⚡ Pmax — Measured vs Optimized")

result_cols = st.columns(5)
for i, col in enumerate(result_cols):
    col.markdown(f"**Set {i+1}**")
    if all_results[i] is not None:
        best_sol, best_pmax, error_history, Pmax_meas = all_results[i]
        abs_error = abs(best_pmax - Pmax_meas)
        pct_error = (abs_error / Pmax_meas * 100) if Pmax_meas != 0 else 0
        col.write(f"Measured: {Pmax_meas:.4f} W")
        col.write(f"Optimized: {best_pmax:.4f} W")
        col.write(f"Abs Error: {abs_error:.4f} W")
        col.write(f"Error: {pct_error:.4f} %")
    else:
        col.write("Skipped")

st.markdown("---")

# ------------------ SECTION 3: BEFORE VS AFTER ------------------
st.subheader("📊 Before vs After ABC — Pmax")

bva_cols = st.columns(5)
for i, col in enumerate(bva_cols):
    col.markdown(f"**Set {i+1}**")
    if all_results[i] is not None and i < len(Pmax_calc_list) and Pmax_calc_list[i] is not None:
        _, best_pmax, _, Pmax_meas = all_results[i]
        orig_pmax  = Pmax_calc_list[i]
        orig_error = abs(orig_pmax - Pmax_meas)
        new_error  = abs(best_pmax - Pmax_meas)
        col.write(f"Before: {orig_pmax:.4f} W")
        col.write(f"Before Err: {orig_error:.4f} W")
        col.write(f"After: {best_pmax:.4f} W")
        col.write(f"After Err: {new_error:.4f} W")
    else:
        col.write("—")

st.markdown("---")

# ------------------ SECTION 4: CALCULATION STEPS ------------------
st.subheader("🧮 Optimized Calculation Steps")

for i, result in enumerate(all_results):
    if result is None:
        continue
    best_sol, best_pmax, error_history, Pmax_meas = result
    BG_opt, dirt_opt, Fmm_opt, Fshade_opt = best_sol
    G_front    = Fg * 1000
    G_total    = G_front * (1 + BG_opt)
    Fg_eff     = G_total / 1000
    Fclean_opt = (100 - dirt_opt) / 100
    abs_error  = abs(best_pmax - Pmax_meas)
    pct_error  = (abs_error / Pmax_meas * 100) if Pmax_meas != 0 else 0

    with st.expander(f"Set {i+1} — Calculation Steps"):
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

# ------------------ SECTION 5: GRAPHS ------------------
st.subheader("📈 Graphs")

# ---- Graph 1: Combined Error Convergence (all 5 sets) ----
st.markdown("#### Error Convergence History — All Sets")

fig1, ax1 = plt.subplots(figsize=(10, 4))
colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"]
for i, result in enumerate(all_results):
    if result is not None:
        _, _, error_history, _ = result
        ax1.plot(
            range(1, len(error_history) + 1),
            error_history,
            label=f"Set {i+1}",
            color=colors[i],
            linewidth=1.8
        )
ax1.set_xlabel("Cycle")
ax1.set_ylabel("Absolute Error — Pmax (W)")
ax1.set_title("ABC Convergence: |Pmax_calc − Pmax_meas| per Cycle")
ax1.legend(title="Input Set", loc="upper right")
ax1.grid(True, linestyle="--", alpha=0.5)
plt.tight_layout()
st.pyplot(fig1)
st.caption("Each line shows how the best error for that set decreased over ABC cycles. A flat tail means convergence.")

st.markdown("---")

# ---- Graph 2: Pmax Bar — Measured vs Before vs After (grouped) ----
st.markdown("#### Pmax — Measured vs Before ABC vs After ABC")

set_labels  = [f"Set {i+1}" for i in range(5) if all_results[i] is not None]
meas_vals   = []
before_vals = []
after_vals  = []

for i, result in enumerate(all_results):
    if result is None:
        continue
    _, best_pmax, _, Pmax_meas = result
    meas_vals.append(Pmax_meas)
    before_vals.append(Pmax_calc_list[i] if i < len(Pmax_calc_list) and Pmax_calc_list[i] is not None else 0)
    after_vals.append(best_pmax)

x = range(len(set_labels))
width = 0.25

fig2, ax2 = plt.subplots(figsize=(10, 4))
bars1 = ax2.bar([p - width for p in x], meas_vals,   width, label="Measured",   color="#2ca02c")
bars2 = ax2.bar([p         for p in x], before_vals, width, label="Before ABC", color="#1f77b4")
bars3 = ax2.bar([p + width for p in x], after_vals,  width, label="After ABC",  color="#ff7f0e")

ax2.set_xticks(list(x))
ax2.set_xticklabels(set_labels)
ax2.set_ylabel("Pmax (W)")
ax2.set_title("Pmax Comparison per Set")
ax2.legend(title="Category", loc="upper right")
ax2.grid(True, axis="y", linestyle="--", alpha=0.5)

for bar in [bars1, bars2, bars3]:
    for b in bar:
        ax2.text(b.get_x() + b.get_width()/2, b.get_height() + 0.3,
                 f"{b.get_height():.1f}", ha="center", va="bottom", fontsize=7)

plt.tight_layout()
st.pyplot(fig2)
st.caption("Green = measured field value. Blue = original calculated Pmax (before ABC). Orange = ABC-optimized Pmax.")

st.markdown("---")

# ---- Graph 3: Error % per set (Before vs After) ----
st.markdown("#### Error (%) — Before vs After ABC per Set")

before_errors = []
after_errors  = []

for i, result in enumerate(all_results):
    if result is None:
        continue
    _, best_pmax, _, Pmax_meas = result
    orig = Pmax_calc_list[i] if i < len(Pmax_calc_list) and Pmax_calc_list[i] is not None else 0
    before_errors.append(abs(orig - Pmax_meas) / Pmax_meas * 100 if Pmax_meas != 0 else 0)
    after_errors.append(abs(best_pmax - Pmax_meas) / Pmax_meas * 100 if Pmax_meas != 0 else 0)

x2 = range(len(set_labels))
fig3, ax3 = plt.subplots(figsize=(10, 4))
b1 = ax3.bar([p - width/2 for p in x2], before_errors, width, label="Before ABC", color="#1f77b4")
b2 = ax3.bar([p + width/2 for p in x2], after_errors,  width, label="After ABC",  color="#ff7f0e")

ax3.set_xticks(list(x2))
ax3.set_xticklabels(set_labels)
ax3.set_ylabel("Error (%)")
ax3.set_title("Pmax Error (%) Before and After ABC Optimization")
ax3.legend(title="Stage", loc="upper right")
ax3.axhline(y=2, color="green",  linestyle="--", linewidth=1, label="2% threshold")
ax3.axhline(y=5, color="orange", linestyle="--", linewidth=1, label="5% threshold")
ax3.grid(True, axis="y", linestyle="--", alpha=0.5)

for b in [b1, b2]:
    for bar in b:
        ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
                 f"{bar.get_height():.2f}%", ha="center", va="bottom", fontsize=7)

plt.tight_layout()
st.pyplot(fig3)
st.caption("Blue = error before ABC. Orange = error after ABC. Green line = 2% threshold, orange line = 5% threshold.")

st.markdown("---")
st.info(
    "ABC tuned BG, dirt, Fmm, and Fshade to minimise |Pmax_calc − Pmax_measured|. "
    "All other factors were fixed from the Computational Tool."
)
