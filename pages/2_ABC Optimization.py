import streamlit as st
import random

st.title("🐝 ABC Algorithm — Pmax Error Minimizer")
st.markdown("Optimize controllable factors so that **calculated Pmax matches your measured Pmax** as closely as possible.")
st.markdown("---")

# ------------------ CHECK SESSION STATE ------------------
required_keys = ["Pmax_STC", "Ftemp_P", "Fg", "Fage"]
missing = [k for k in required_keys if k not in st.session_state]

if missing:
    st.warning(
        "⚠️ No data found from the Computational Tool. "
        "Please run the **Computational Tool page** first and click **Calculate Outputs**."
    )
    st.stop()

# ------------------ IMPORT FIXED VALUES ------------------
Pmax_stc = st.session_state["Pmax_STC"]
Ftemp_P  = st.session_state["Ftemp_P"]
Fg       = st.session_state["Fg"]
Fage     = st.session_state["Fage"]

st.subheader("📥 Imported Fixed Values (from Computational Tool)")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Pmax STC (W)", f"{Pmax_stc:.2f}")
col2.metric("Ftemp_Pmp",    f"{Ftemp_P:.4f}")
col3.metric("Fg",           f"{Fg:.4f}")
col4.metric("Fage",         f"{Fage:.4f}")

st.markdown("---")

# ------------------ 5 SETS OF MEASURED PMAX ------------------
st.subheader("📋 Measured Pmax (5 Sets)")

pmax_meas_list = []
cols = st.columns(5)
for i, col in enumerate(cols):
    with col:
        st.markdown(f"**Set {i+1}**")
        val = col.number_input(f"Measured Pmax (W)", min_value=0.0, value=0.0, format="%.4f", key=f"pmax_meas_{i}")
        pmax_meas_list.append(val)

if all(v <= 0 for v in pmax_meas_list):
    st.info("ℹ️ Enter at least one measured Pmax above to enable optimization.")
    st.stop()

st.markdown("---")

# ------------------ ABC PARAMETERS ------------------
st.subheader("⚙️ ABC Algorithm Parameters")

col_a, col_b, col_c = st.columns(3)
with col_a:
    num_bees   = st.number_input("Number of Bees", min_value=10, max_value=200, value=30,  step=5)
with col_b:
    max_cycles = st.number_input("Max Cycles",     min_value=10, max_value=500, value=100, step=10)
with col_c:
    limit      = st.number_input("Scout Limit",    min_value=1,  max_value=50,  value=5,   step=1)

st.markdown("---")

# ------------------ ABC ALGORITHM ------------------
def abc_optimize(Pmax_stc, Ftemp_P, Fg, Fage, Pmax_meas, num_bees, max_cycles, limit):
    BOUNDS = [
        (0.00, 0.35),
        (0.00, 20.0),
        (0.95, 1.00),
        (0.70, 1.00),
    ]
    DIM = len(BOUNDS)

    def compute_pmax(x):
        BG, dirt, Fmm, Fshade = x
        G_front = Fg * 1000
        G_total = G_front * (1 + BG)
        Fg_eff  = G_total / 1000
        Fclean  = (100 - dirt) / 100
        return Pmax_stc * Ftemp_P * Fg_eff * Fclean * Fshade * Fmm * Fage

    def objective(x):
        return abs(compute_pmax(x) - Pmax_meas)

    def random_solution():
        return [random.uniform(lo, hi) for lo, hi in BOUNDS]

    def clip(x):
        return [max(lo, min(hi, x[i])) for i, (lo, hi) in enumerate(BOUNDS)]

    solutions = [random_solution() for _ in range(num_bees)]
    fitness   = [objective(s) for s in solutions]
    trial     = [0] * num_bees
    error_history = []

    for cycle in range(max_cycles):

        for i in range(num_bees):
            k = random.randint(0, num_bees - 1)
            while k == i:
                k = random.randint(0, num_bees - 1)
            j       = random.randint(0, DIM - 1)
            phi     = random.uniform(-1, 1)
            new_sol = solutions[i][:]
            new_sol[j] = solutions[i][j] + phi * (solutions[i][j] - solutions[k][j])
            new_sol = clip(new_sol)
            new_fit = objective(new_sol)
            if new_fit < fitness[i]:
                solutions[i] = new_sol
                fitness[i]   = new_fit
                trial[i]     = 0
            else:
                trial[i] += 1

        prob       = [1 / (1 + f) for f in fitness]
        total_prob = sum(prob)
        prob       = [p / total_prob for p in prob]

        for i in range(num_bees):
            if random.random() < prob[i]:
                k = random.randint(0, num_bees - 1)
                while k == i:
                    k = random.randint(0, num_bees - 1)
                j       = random.randint(0, DIM - 1)
                phi     = random.uniform(-1, 1)
                new_sol = solutions[i][:]
                new_sol[j] = solutions[i][j] + phi * (solutions[i][j] - solutions[k][j])
                new_sol = clip(new_sol)
                new_fit = objective(new_sol)
                if new_fit < fitness[i]:
                    solutions[i] = new_sol
                    fitness[i]   = new_fit
                    trial[i]     = 0
                else:
                    trial[i] += 1

        for i in range(num_bees):
            if trial[i] > limit:
                solutions[i] = random_solution()
                fitness[i]   = objective(solutions[i])
                trial[i]     = 0

        best_idx = fitness.index(min(fitness))
        error_history.append(fitness[best_idx])

    best_idx  = fitness.index(min(fitness))
    best_sol  = solutions[best_idx]
    best_pmax = compute_pmax(best_sol)

    return best_sol, best_pmax, error_history


# ------------------ RUN ------------------
if st.button("🐝 Run ABC Optimization"):

    all_results = []

    with st.spinner("Bees are minimizing the error between calculated and measured Pmax..."):
        for i, Pmax_meas in enumerate(pmax_meas_list):
            if Pmax_meas <= 0:
                all_results.append(None)
                continue
            best_sol, best_pmax, error_history = abc_optimize(
                Pmax_stc, Ftemp_P, Fg, Fage,
                Pmax_meas,
                int(num_bees), int(max_cycles), int(limit)
            )
            all_results.append((best_sol, best_pmax, error_history, Pmax_meas))

    # --- SAVE FOR PAGE 3 ---
    st.session_state["abc_all_results"]  = all_results
    st.session_state["abc_pmax_meas_list"] = pmax_meas_list

    st.markdown("---")
    st.subheader("🏆 Optimization Results")

    Pmax_calc_list = st.session_state.get("Pmax_calculated", [None]*5)

    # --- Optimized factors per set ---
    st.markdown("#### Optimized Controllable Factors")
    header_cols = st.columns(5)
    for i, col in enumerate(header_cols):
        col.markdown(f"**Set {i+1}**")

    for label, idx in [("BG", 0), ("Dirt %", 1), ("Fmm", 2), ("Fshade", 3)]:
        row_cols = st.columns(5)
        for i, col in enumerate(row_cols):
            if all_results[i] is not None:
                val = all_results[i][0][idx]
                col.write(f"{label}: {val:.4f}")
            else:
                col.write(f"{label}: —")

    st.markdown("---")

    # --- Pmax comparison per set ---
    st.markdown("#### Pmax Comparison")
    result_cols = st.columns(5)
    for i, col in enumerate(result_cols):
        if all_results[i] is not None:
            best_sol, best_pmax, error_history, Pmax_meas = all_results[i]
            abs_error = abs(best_pmax - Pmax_meas)
            pct_error = (abs_error / Pmax_meas) * 100 if Pmax_meas != 0 else 0
            col.markdown(f"**Set {i+1}**")
            col.write(f"Measured: {Pmax_meas:.4f} W")
            col.write(f"Optimized: {best_pmax:.4f} W")
            col.write(f"Abs Error: {abs_error:.4f} W")
            col.write(f"Error: {pct_error:.4f} %")
        else:
            col.markdown(f"**Set {i+1}**")
            col.write("Skipped (Pmax = 0)")

    st.markdown("---")

    # --- Before vs After ABC ---
    st.markdown("#### Before vs After ABC")
    bva_cols = st.columns(5)
    for i, col in enumerate(bva_cols):
        if all_results[i] is not None and i < len(Pmax_calc_list) and Pmax_calc_list[i] is not None:
            _, best_pmax, _, Pmax_meas = all_results[i]
            orig_pmax  = Pmax_calc_list[i]
            orig_error = abs(orig_pmax - Pmax_meas)
            new_error  = abs(best_pmax - Pmax_meas)
            col.markdown(f"**Set {i+1}**")
            col.write(f"Before: {orig_pmax:.4f} W")
            col.write(f"Before Error: {orig_error:.4f} W")
            col.write(f"After: {best_pmax:.4f} W")
            col.write(f"After Error: {new_error:.4f} W")
        else:
            col.markdown(f"**Set {i+1}**")
            col.write("—")

    st.info(
        "ABC tuned BG, dirt, Fmm, and Fshade to minimise |Pmax_calc − Pmax_measured|. "
        "Voc and Vmp are temperature-only and are not affected by the optimized factors."
    )
