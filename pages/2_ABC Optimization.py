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
Pmax_stc  = st.session_state["Pmax_STC"]
Ftemp_P   = st.session_state["Ftemp_P"]
Fg        = st.session_state["Fg"]
Fage      = st.session_state["Fage"]

Ftemp_Isc = st.session_state.get("Ftemp_Isc", 1.0)
Ftemp_Imp = st.session_state.get("Ftemp_Imp", 1.0)
Ftemp_Voc = st.session_state.get("Ftemp_Voc", 1.0)
Ftemp_Vmp = st.session_state.get("Ftemp_Vmp", 1.0)
Isc_stc   = st.session_state.get("Isc_stc",   None)
Imp_stc   = st.session_state.get("Imp_stc",   None)
Voc_stc   = st.session_state.get("Voc_stc",   None)
Vmp_stc   = st.session_state.get("Vmp_stc",   None)

st.subheader("📥 Imported Fixed Values (from Computational Tool)")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Pmax STC (W)",  f"{Pmax_stc:.2f}")
col2.metric("Ftemp_Pmp",     f"{Ftemp_P:.4f}")
col3.metric("Fg",            f"{Fg:.4f}")
col4.metric("Fage",          f"{Fage:.4f}")

st.markdown("---")

# ------------------ MEASURED DATA INPUT ------------------
st.subheader("📋 Measured Data (Field Measurements)")
st.markdown("Enter the values measured from your actual PV module in the field.")

col_m1, col_m2 = st.columns(2)
with col_m1:
    Pmax_meas = st.number_input("Measured Pmax (W)",  min_value=0.0, value=0.0, format="%.4f")
    Vmp_meas  = st.number_input("Measured Vmp (V)",   min_value=0.0, value=0.0, format="%.4f")
    Isc_meas  = st.number_input("Measured Isc (A)",   min_value=0.0, value=0.0, format="%.4f")
with col_m2:
    Imp_meas  = st.number_input("Measured Imp (A)",   min_value=0.0, value=0.0, format="%.4f")
    Voc_meas  = st.number_input("Measured Voc (V)",   min_value=0.0, value=0.0, format="%.4f")

if Pmax_meas <= 0:
    st.info("ℹ️ Enter your measured Pmax above to enable optimization.")
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
    """
    Optimize 4 controllable factors to minimise |Pmax_calc - Pmax_meas|.

    Variables (solution vector):
        x[0] = BG      — bifacial gain       [0.00, 0.35]
        x[1] = dirt    — dirt level %        [0.00, 20.0]
        x[2] = Fmm     — mismatch factor     [0.95,  1.0]
        x[3] = Fshade  — shading factor      [0.70,  1.0]

    Fixed (from session_state):
        Pmax_stc, Ftemp_P, Fg, Fage

    Objective: minimise |Pmax_calc - Pmax_meas|
    """

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

    # ---- Initialise ----
    solutions = [random_solution() for _ in range(num_bees)]
    fitness   = [objective(s) for s in solutions]
    trial     = [0] * num_bees
    error_history = []

    for cycle in range(max_cycles):

        # ---- Employed Bees ----
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

        # ---- Onlooker Bees ----
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

        # ---- Scout Bees ----
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

    with st.spinner("Bees are minimizing the error between calculated and measured Pmax..."):
        best_sol, best_pmax, error_history = abc_optimize(
            Pmax_stc, Ftemp_P, Fg, Fage,
            Pmax_meas,
            int(num_bees), int(max_cycles), int(limit)
        )

    BG_opt, dirt_opt, Fmm_opt, Fshade_opt = best_sol
    
    # --- SAVE RESULTS FOR PAGE 3 ---
    st.session_state["abc_best_pmax"] = best_pmax
    st.session_state["abc_best_sol"] = best_sol
    st.session_state["abc_error_history"] = error_history
    st.session_state["abc_pmax_meas"] = Pmax_meas
    
    # Optional (for full table in Page 3)
    st.session_state["abc_vmp_meas"] = Vmp_meas
    st.session_state["abc_imp_meas"] = Imp_meas
    st.session_state["abc_voc_meas"] = Voc_meas
    st.session_state["abc_isc_meas"] = Isc_meas

    G_front    = Fg * 1000
    G_total    = G_front * (1 + BG_opt)
    Fg_eff     = G_total / 1000
    Fclean_opt = (100 - dirt_opt) / 100

    abs_error = abs(best_pmax - Pmax_meas)
    pct_error = (abs_error / Pmax_meas) * 100 if Pmax_meas != 0 else 0

    Pmax_calc_original = st.session_state.get("Pmax_calculated", None)

    st.markdown("---")
    st.subheader("🏆 Optimization Results")

    # --- Optimal factors ---
    st.markdown("#### Optimized Controllable Factors")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Optimal BG",     f"{BG_opt:.4f}")
    col2.metric("Optimal Dirt %", f"{dirt_opt:.4f}")
    col3.metric("Optimal Fmm",    f"{Fmm_opt:.4f}")
    col4.metric("Optimal Fshade", f"{Fshade_opt:.4f}")

    # --- Pmax comparison ---
    st.markdown("#### Pmax Comparison")
    col_a, col_b, col_c, col_d = st.columns(4)
    col_a.metric("Measured Pmax (W)",  f"{Pmax_meas:.4f}")
    col_b.metric("Optimized Pmax (W)", f"{best_pmax:.4f}")
    col_c.metric("Absolute Error (W)", f"{abs_error:.4f}")
    col_d.metric("Error (%)",          f"{pct_error:.4f} %")

    # --- Before vs after ABC ---
    if Pmax_calc_original is not None:
        orig_error     = abs(Pmax_calc_original - Pmax_meas)
        orig_pct_error = (orig_error / Pmax_meas) * 100 if Pmax_meas != 0 else 0
        st.markdown("#### Before vs After ABC")
        col_e, col_f, col_g, col_h = st.columns(4)
        col_e.metric("Before ABC — Pmax (W)",    f"{Pmax_calc_original:.4f}")
        col_f.metric("Before ABC — Error (W)",   f"{orig_error:.4f}")
        col_g.metric("After ABC  — Pmax (W)",    f"{best_pmax:.4f}")
        col_h.metric("After ABC  — Error (W)",   f"{abs_error:.4f}",
                     delta=f"{abs_error - orig_error:.4f} W", delta_color="inverse")

    # --- Full output table ---
    st.markdown("#### 📊 Measured vs Calculated — All Five Outputs")

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

    # --- Convergence ---
    st.markdown("#### 📈 Error Convergence History")
    st.line_chart({"Absolute Error — Pmax (W)": error_history})

    # --- Steps ---
    st.markdown("#### 🧮 Optimized Calculation Steps")
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
    st.info(
        "ABC tuned BG, dirt, Fmm, and Fshade to minimise |Pmax_calc − Pmax_measured|. "
        "Voc and Vmp are temperature-only and are not affected by the optimized factors."
    )
