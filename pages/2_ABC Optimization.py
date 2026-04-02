import streamlit as st
import random

st.title("🤖 ABC Optimization Tool")
st.markdown("Optimize PV output using Artificial Bee Colony (ABC)")

# ------------------ CHECK DATA ------------------

if "Pmax_calculated" not in st.session_state:
    st.warning("⚠ Please run the Computation Tool first.")
    st.stop()

# Retrieve data from previous page
Pmax = st.session_state["Pmax_calculated"]
Pmax_stc = st.session_state["Pmax_STC"]
Ftemp_Pmp = st.session_state["Ftemp_P"]
Fg = st.session_state["Fg"]

# User input for measured value
P_measured = st.number_input("Measured Pmax (W)", value=480.0)

# ------------------ OBJECTIVE FUNCTION ------------------

def objective_function(params):
    Fclean, Fshade, Fmm, Fage = params

    P_calc = Pmax_stc * Ftemp_Pmp * Fg * Fclean * Fshade * Fmm * Fage
    error = (P_calc - P_measured) ** 2

    return error

# ------------------ ABC FUNCTION ------------------

def abc_optimization(iterations=50, colony_size=20):

    bounds = [
        (0.90, 1.00),  # Fclean
        (0.90, 1.00),  # Fshade
        (0.95, 1.00),  # Fmm
        (0.85, 1.00)   # Fage
    ]

    population = [
        [random.uniform(b[0], b[1]) for b in bounds]
        for _ in range(colony_size)
    ]

    fitness = [objective_function(sol) for sol in population]

    best_solution = population[fitness.index(min(fitness))]
    best_error = min(fitness)

    for _ in range(iterations):
        for i in range(colony_size):

            new_solution = population[i].copy()
            index = random.randint(0, len(bounds)-1)

            phi = random.uniform(-1, 1)

            new_solution[index] = new_solution[index] + phi * (
                new_solution[index] - best_solution[index]
            )

            # Apply bounds
            new_solution[index] = max(bounds[index][0],
                                      min(bounds[index][1],
                                          new_solution[index]))

            new_error = objective_function(new_solution)

            if new_error < fitness[i]:
                population[i] = new_solution
                fitness[i] = new_error

        best_solution = population[fitness.index(min(fitness))]
        best_error = min(fitness)

    return best_solution, best_error

# ------------------ RUN OPTIMIZATION ------------------

if st.button("Run ABC Optimization"):

    best_params, best_error = abc_optimization()

    Fclean_opt, Fshade_opt, Fmm_opt, Fage_opt = best_params

    Pmax_opt = Pmax_stc * Ftemp_Pmp * Fg * Fclean_opt * Fshade_opt * Fmm_opt * Fage_opt

    error_before = (Pmax - P_measured) ** 2
    error_after = best_error

    # ------------------ OUTPUT ------------------

    st.markdown("---")
    st.subheader("📊 Optimization Results")

    st.write(f"Measured Pmax = {P_measured:.2f} W")

    st.write("### 🔹 Before Optimization")
    st.write(f"Calculated Pmax = {Pmax:.2f} W")
    st.write(f"Error = {error_before:.4f}")

    st.write("### 🔹 After Optimization")
    st.success(f"Optimized Pmax = {Pmax_opt:.2f} W")
    st.write(f"Error = {error_after:.4f}")

    st.write("### 🔧 Optimized Parameters")
    st.write(f"Fclean = {Fclean_opt:.3f}")
    st.write(f"Fshade = {Fshade_opt:.3f}")
    st.write(f"Fmm = {Fmm_opt:.3f}")
    st.write(f"Fage = {Fage_opt:.3f}")
