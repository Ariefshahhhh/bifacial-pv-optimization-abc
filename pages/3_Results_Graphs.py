import streamlit as st
import matplotlib.pyplot as plt

st.title("📊 Results & Graph Analysis")
st.markdown("Visualization of PV output before and after ABC optimization")

# ------------------ CHECK DATA ------------------

if "Pmax_calculated" not in st.session_state:
    st.warning("⚠ Please run the Computation Tool first.")
    st.stop()

if "Pmax_optimized" not in st.session_state:
    st.warning("⚠ Please run ABC Optimization first.")
    st.stop()

# Retrieve data
Pmax_calc = st.session_state["Pmax_calculated"]
Pmax_opt = st.session_state["Pmax_optimized"]
P_measured = st.session_state["P_measured"]

# ------------------ BAR CHART ------------------

st.subheader("🔋 Power Comparison")

labels = ["Measured", "Calculated", "Optimized"]
values = [P_measured, Pmax_calc, Pmax_opt]

fig, ax = plt.subplots()
ax.bar(labels, values)
ax.set_title("Pmax Comparison")
ax.set_ylabel("Power (W)")

st.pyplot(fig)

# ------------------ ERROR ANALYSIS ------------------

error_before = abs(Pmax_calc - P_measured)
error_after = abs(Pmax_opt - P_measured)

reduction = ((error_before - error_after) / error_before) * 100 if error_before != 0 else 0

st.subheader("📉 Error Analysis")

st.write(f"Error Before Optimization = {error_before:.2f} W")
st.write(f"Error After Optimization = {error_after:.2f} W")
st.success(f"Error Reduction = {reduction:.2f}%")

# ------------------ ERROR BAR CHART ------------------

st.subheader("📊 Error Comparison")

error_labels = ["Before", "After"]
error_values = [error_before, error_after]

fig2, ax2 = plt.subplots()
ax2.bar(error_labels, error_values)
ax2.set_title("Error Reduction")
ax2.set_ylabel("Error (W)")

st.pyplot(fig2)

# ------------------ OPTIONAL: CONVERGENCE ------------------

if "abc_history" in st.session_state:

    st.subheader("📈 ABC Convergence Curve")

    history = st.session_state["abc_history"]

    fig3, ax3 = plt.subplots()
    ax3.plot(history)
    ax3.set_title("ABC Convergence")
    ax3.set_xlabel("Iteration")
    ax3.set_ylabel("Error")

    st.pyplot(fig3)
