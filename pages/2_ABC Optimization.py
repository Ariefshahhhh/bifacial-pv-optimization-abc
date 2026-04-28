import streamlit as st
import random

st.title("🐝 ABC Algorithm — Pmax Optimizer")
st.markdown("Optimize controllable factors to **maximize Pmax** using values from the Computational Tool.")
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

st.subheader("📥 Imported Fixed Values (from Computational Tool)")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Pmax STC (W)",   f"{Pmax_stc:.2f}")
col2.metric("Ftemp_Pmp",      f"{Ftemp_P:.4f}")
col3.metric("Fg",             f"{Fg:.4f}")
col4.metric("Fage",           f"{Fage:.4f}")

st.markdown("---")

# ------------------ ABC PARAMETERS ------------------
st.subheader("⚙️ ABC Algorithm Parameters")

col_a, col_b, col_c = st.columns(3)
with col_a:
    num_bees   = st.number_input("Number of Bees",   min_value=10, max_value=200, value=30, step=5)
with col_b:
    max_cycles = st.number_input("Max Cycles",       min_value=10, max_value=500, value=100, step=10)
with col_c:
    limit      = st.number_input("Scout Limit",      min_value=1,  max_value=50,  value=5,  step=1)

st.markdown("---")

# ------------------ ABC ALGORITHM ------------------
def abc_optimize_pmax(Pmax_stc, Ftemp_P, Fg, Fage, num_bees, max_cycles, limit):
    """
    Optimize 4 controllable factors to maximise Pmax.

    Variables (solution vector):
        x[0] = BG      — bifacial gain         [0.0,  0.35]
        x[1] = dirt    — dirt level %           [0.0, 20.0]
        x[2] = Fmm     — mismatch factor        [0.95,  1.0]
        x[3] = Fshade  — shading factor         [0.70,  1.0]

    Fixed (imported from session_state):
        Pmax_stc, Ftemp_P, Fg, Fage

    Objective: MAXIMISE Pmax, so fitness = -Pmax (ABC minimises).
    """

    BOUNDS = [
        (0.0,  0.35),   # BG
        (0.0,  20.0),   # dirt
        (0.95, 1.0),    # Fmm
        (0.70, 1.0),    # Fshade
    ]
    DIM = len(BOUNDS)

    def compute_pmax(x):
        BG, dirt, Fmm, Fshade = x
        G_front = Fg * 1000                        # recover G_front from Fg
        G_total = G_front * (1 + BG)               # total irradiance with bifacial gain
        Fg_eff  = G_total / 1000                   # effective irradiance factor
        Fclean  = (100 - dirt) / 100
        return Pmax_stc * Ftemp_P * Fg_eff * Fclean * Fshade * Fmm * Fage

    def objective(x):
        return -compute_pmax(x)                    # minimise negative → maximise Pmax

    def random_solution():
        return [random.uniform(lo, hi) for lo, hi in BOUNDS]

    def clip(x):
        return [max(lo, min(hi, x[i])) for i, (lo, hi) in enumerate(BOUNDS)]

    # ---- Initialise ----
    solutions = [random_solution() for _ in range(num_bees)]
    fitness   = [objective(s) for s in solutions]
    trial     = [0] * num_bees
    best_history = []

    for cycle in range(max_cycles):

        # ---- Employed Bees ----
        for i in range(num_bees):
            k = random.randint(0, num_bees - 1)
            while k == i:
                k = random.randint(0, num_bees - 1)

            j   = random.randint(0, DIM - 1)
            phi = random.uniform(-1, 1)
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

                j   = random.randint(0, DIM - 1)
                phi = random.uniform(-1, 1)
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

        # Track best each cycle
        best_idx = fitness.index(min(fitness))
        best_history.append(-fitness[best_idx])

    best_idx  = fitness.index(min(fitness))
    best_sol  = solutions[best_idx]
    best_pmax = compute_pmax(best_sol)

    return best_sol, best_pmax, best_history


# ------------------ RUN ------------------
if st.button("🐝 Run ABC Optimization"):

    with st.spinner("Bees are searching for the optimal solution..."):
        best_sol, best_pmax, history = abc_optimize_pmax(
            Pmax_stc, Ftemp_P, Fg, Fage,
            int(num_bees), int(max_cycles), int(limit)
        )

    BG_opt, dirt_opt, Fmm_opt, Fshade_opt = best_sol

    st.markdown("---")
    st.subheader("🏆 Optimized Results")

    st.success(f"**Optimal Pmax = {best_pmax:.4f} W**")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Optimal BG",     f"{BG_opt:.4f}")
    col2.metric("Optimal Dirt %", f"{dirt_opt:.4f}")
    col3.metric("Optimal Fmm",    f"{Fmm_opt:.4f}")
    col4.metric("Optimal Fshade", f"{Fshade_opt:.4f}")

    # ---- Comparison ----
    Pmax_original = st.session_state.get("Pmax_calculated", None)
    if Pmax_original is not None:
        improvement = best_pmax - Pmax_original
        st.markdown("### 📊 Comparison")
        col_a, col_b, col_c = st.columns(3)
        col_a.metric("Original Pmax (W)",  f"{Pmax_original:.4f}")
        col_b.metric("Optimized Pmax (W)", f"{best_pmax:.4f}")
        col_c.metric("Improvement (W)",    f"{improvement:.4f}",
                     delta=f"{improvement:.4f} W")

    # ---- Convergence chart ----
    st.markdown("### 📈 Convergence History")
    st.line_chart({"Pmax (W)": history})

    # ---- Calculation breakdown ----
    G_front    = Fg * 1000
    G_total    = G_front * (1 + BG_opt)
    Fg_eff     = G_total / 1000
    Fclean_opt = (100 - dirt_opt) / 100

    st.markdown("### 🧮 Optimized Calculation Steps")
    st.write(f"1️⃣ G_front (from Fg) = {Fg:.3f} × 1000 = **{G_front:.2f} W/m²**")
    st.write(f"2️⃣ Total irradiance = {G_front:.2f} × (1 + {BG_opt:.4f}) = **{G_total:.2f} W/m²**")
    st.write(f"3️⃣ Effective Fg = {G_total:.2f} / 1000 = **{Fg_eff:.4f}**")
    st.write(f"4️⃣ Fclean = (100 − {dirt_opt:.4f}) / 100 = **{Fclean_opt:.4f}**")
    st.write(
        f"5️⃣ Pmax = {Pmax_stc:.2f} × {Ftemp_P:.4f} × {Fg_eff:.4f} × "
        f"{Fclean_opt:.4f} × {Fshade_opt:.4f} × {Fmm_opt:.4f} × {Fage:.4f} "
        f"= **{best_pmax:.4f} W**"
    )
    st.info("ABC optimized BG, dirt, Fmm, and Fshade. All other factors were fixed from the Computational Tool.")
