import streamlit as st
import numpy as np

st.title("🐝 Artificial Bee Colony (ABC) Optimization")
st.markdown("Optimize correction factors to minimize error between calculated and measured **Pmax**.")
st.markdown("---")

# ===============================
# 1️⃣ CHECK REQUIRED VALUES
# ===============================
required_keys = [
    "Pmax_calculated",
    "Pmax_stc",
    "Ftemp_P",
    "Fg",
    "Fclean",
    "Fshade",
    "Fmm",
    "Fage"
]

missing = [k for k in required_keys if k not in st.session_state]

if missing:
    st.error("❌ Please complete the **Calculator page** first.")
    st.stop()

# ===============================
# 2️⃣ READ VALUES FROM CALCULATOR
# ===============================
Pmax_STC = st.session_state["Pmax_STC"]
Ftemp_P = st.session_state["Ftemp_P"]
Fg = st.session_state["Fg"]
Fclean = st.session_state["Fclean"]
Fshade = st.session_state["Fshade"]
Fmm_base = st.session_state["Fmm"]
Fage_base = st.session_state["Fage"]

# ===============================
# 3️⃣ MEASURED INPUT
# ===============================
st.subheader("📏 Measured Data Input")
P_measured = st.number_input(
    "Measured Maximum Power, Pmax_measured (W)",
    value=Pcalc,
    step=1.0
)

# ===============================
# 4️⃣ ABC PARAMETERS
# ===============================
st.subheader("🐝 ABC Parameters")
iterations = st.slider("Number of Iterations", 50, 500, 200)
colony_size = st.slider("Number of Bees", 10, 100, 30)

# ===============================
# 5️⃣ ABC FUNCTIONS
# ===============================
def calculate_pmax(factors):
    Fmm_i, Fclean_i, Fshade_i = factors
    return (
        Pmax_stc
        * Ftemp_P
        * Fg
        * Fclean_i
        * Fshade_i
        * Fmm_i
        * Fage
    )

def objective_function(factors):
    return abs(calculate_pmax(factors) - P_measured)

def abc_optimize():
    solutions = np.random.uniform(0.8, 1.0, (colony_size, 3))
    best_solution = None
    best_error = float("inf")
    history = []

    for _ in range(iterations):
        for i in range(colony_size):
            error = objective_function(solutions[i])
            if error < best_error:
                best_error = error
                best_solution = solutions[i].copy()

            solutions[i] += np.random.uniform(-0.01, 0.01, 3)
            solutions[i] = np.clip(solutions[i], 0.8, 1.0)

        history.append(best_error)

    return best_solution, best_error, history

# ===============================
# 6️⃣ RUN ABC
# ===============================
if st.button("🚀 Run ABC Optimization"):

    best_factors, best_error, history = abc_optimize()
    Fmm_opt, Fclean_opt, Fshade_opt = best_factors

    P_optimized = calculate_pmax(best_factors)

    # ===============================
    # 7️⃣ SAVE RESULTS
    # ===============================
    st.session_state["Pmax_optimized"] = P_optimized
    st.session_state["ABC_error_before"] = abs(Pcalc - P_measured)
    st.session_state["ABC_error_after"] = best_error

    # ===============================
    # 8️⃣ DISPLAY RESULTS
    # ===============================
    st.markdown("---")
    st.subheader("📊 Optimization Results")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Calculated Pmax (W)", f"{Pcalc:.2f}")

    with col2:
        st.metric(
            "Optimized Pmax (W)",
            f"{P_optimized:.2f}",
            delta=f"{P_optimized - Pcalc:.2f}"
        )

    with col3:
        st.metric(
            "Measured Pmax (W)",
            f"{P_measured:.2f}"
        )

    st.markdown("### 🔧 Optimized Correction Factors")

    st.write(f"• **Mismatch Factor (Fmm)** = {Fmm_opt:.3f}")
    st.write(f"• **Cleaning Factor (Fclean)** = {Fclean_opt:.3f}")
    st.write(f"• **Shading Factor (Fshade)** = {Fshade_opt:.3f}")

    st.markdown("### 📉 Error Comparison")

    colA, colB = st.columns(2)
    with colA:
        st.metric("Error Before ABC (W)", f"{abs(Pcalc - P_measured):.3f}")
    with colB:
        st.metric(
            "Error After ABC (W)",
            f"{best_error:.3f}",
            delta=f"-{abs(Pcalc - P_measured - best_error):.3f}"
        )

    st.success("✅ ABC Optimization completed successfully.")



