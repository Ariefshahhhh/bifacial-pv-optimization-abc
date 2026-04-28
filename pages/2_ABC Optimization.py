import random

st.markdown("---")
st.subheader("🐝 ABC Optimization (Match Target Pmax)")

target_pmax = st.number_input("Enter Target Pmax (W)", value=400.0)
num_bees = st.slider("Number of Bees", 5, 100, 30)

if "Pmax_STC" not in st.session_state:
    st.warning("⚠ Please click 'Calculate Outputs' first.")
else:

    if st.button("Run ABC Optimization"):

        # Retrieve stored values
        Pmax_stc = st.session_state["Pmax_STC"]
        Ftemp_Pmp = st.session_state["Ftemp_P"]
        Fg = st.session_state["Fg"]
        Fclean = st.session_state["Fclean"]
        Fshade = st.session_state["Fshade"]
        Fmm_init = st.session_state["Fmm"]
        Fage = st.session_state["Fage"]

        # Objective function
        def objective(Fmm_candidate):
            P_test = (
                Pmax_stc
                * Ftemp_Pmp
                * Fg
                * Fclean
                * Fshade
                * Fmm_candidate
                * Fage
            )
            return abs(P_test - target_pmax)

        # Random solution
        def random_solution():
            return random.uniform(0.95, 1.0)

        # Initialize
        solutions = [random_solution() for _ in range(num_bees)]
        fitness = [objective(sol) for sol in solutions]
        trial = [0] * num_bees

        limit = 10
        max_cycles = 100

        for cycle in range(max_cycles):

            # Employed bees
            for i in range(num_bees):
                k = random.randint(0, num_bees - 1)
                while k == i:
                    k = random.randint(0, num_bees - 1)

                phi = random.uniform(-1, 1)
                new_sol = solutions[i] + phi * (solutions[i] - solutions[k])
                new_sol = max(0.95, min(1.0, new_sol))

                new_fit = objective(new_sol)

                if new_fit < fitness[i]:
                    solutions[i] = new_sol
                    fitness[i] = new_fit
                    trial[i] = 0
                else:
                    trial[i] += 1

            # Onlooker bees
            prob = [1 / (1 + f) for f in fitness]
            total_prob = sum(prob)
            prob = [p / total_prob for p in prob]

            for i in range(num_bees):
                if random.random() < prob[i]:
                    k = random.randint(0, num_bees - 1)
                    while k == i:
                        k = random.randint(0, num_bees - 1)

                    phi = random.uniform(-1, 1)
                    new_sol = solutions[i] + phi * (solutions[i] - solutions[k])
                    new_sol = max(0.95, min(1.0, new_sol))

                    new_fit = objective(new_sol)

                    if new_fit < fitness[i]:
                        solutions[i] = new_sol
                        fitness[i] = new_fit
                        trial[i] = 0
                    else:
                        trial[i] += 1

            # Scout bees
            for i in range(num_bees):
                if trial[i] > limit:
                    solutions[i] = random_solution()
                    fitness[i] = objective(solutions[i])
                    trial[i] = 0

        # Best solution
        best_index = fitness.index(min(fitness))
        best_Fmm = solutions[best_index]

        optimized_Pmax = (
            Pmax_stc
            * Ftemp_Pmp
            * Fg
            * Fclean
            * Fshade
            * best_Fmm
            * Fage
        )

        st.success(f"Optimal Fmm = {best_Fmm:.4f}")
        st.success(f"Optimized Pmax = {optimized_Pmax:.4f} W")
        st.write(f"Target Pmax = {target_pmax:.4f} W")
