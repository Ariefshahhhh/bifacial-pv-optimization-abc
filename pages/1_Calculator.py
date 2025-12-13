import streamlit as st

st.title("⚡ PV Output Power & Electrical Parameter Calculator")
st.markdown("Compute Pout, Voc, Isc, Vmp, and Imp with full temperature coefficients and correction factors.")
st.markdown("---")

# ------------------------
# INPUT COLUMNS
# ------------------------
col1, col2 = st.columns(2)

with col1:
    Pmax_stc = st.number_input("Pmax at STC (W)", value=450.0)
    Voc_stc = st.number_input("Voc at STC (V)", value=49.0)
    Isc_stc = st.number_input("Isc at STC (A)", value=10.5)
    Tcell = st.number_input("Cell Temperature (°C)", value=30.0)
    irr_front = st.number_input("Front Irradiance (W/m²)", value=800.0)
    irr_rear = st.number_input("Rear Irradiance (W/m²)", value=100.0)

with col2:
    gamma_pmax = st.number_input("γ Power Temp Coefficient (%/°C)", value=-0.35)  
    beta_voc = st.number_input("β Voc Temp Coefficient (%/°C)", value=-0.29)
    alpha_isc = st.number_input("α Isc Temp Coefficient (%/°C)", value=0.05)

    Fmm = st.number_input("Mismatch Factor Fmm", value=0.98, min_value=0.80, max_value=1.00, step=0.01)
    Fage = st.number_input("Aging Factor Fage", value=0.95, min_value=0.80, max_value=1.00, step=0.01)
    Fg = st.number_input("Glass/Soiling Factor Fg", value=0.97, min_value=0.80, max_value=1.00, step=0.01)
    Fclean = st.number_input("Cleaning Factor Fclean", value=0.98, min_value=0.80, max_value=1.00, step=0.01)
    Fshade = st.number_input("Shading Factor Fshade", value=0.95, min_value=0.80, max_value=1.00, step=0.01)

# ------------------------------------------------
# CALCULATIONS
# ------------------------------------------------
irr_total = irr_front + irr_rear
deltaT = Tcell - 25  # temperature change from STC

# TEMP COEFFICIENTS MUST BE CONVERTED FROM %/°C TO DECIMAL
gamma = gamma_pmax / 100
beta = beta_voc / 100
alpha = alpha_isc / 100

# 1) Adjusted Voc
Voc = Voc_stc * (1 + beta * deltaT)

# 2) Adjusted Isc
Isc = Isc_stc * (irr_total / 1000) * (1 + alpha * deltaT)

# 3) Approx Vmp & Imp
Vmp = 0.8 * Voc
Imp = 0.9 * Isc

# 4) Raw Pmp from temperature effect
Ptemp = Pmax_stc * (irr_total / 1000) * (1 + gamma * deltaT)

# 5) Apply ALL correction factors
Pout = Ptemp * Fmm * Fage * Fg * Fclean * Fshade

# ------------------------------------------------
# DISPLAY RESULTS
# ------------------------------------------------
st.markdown("---")
if st.button("Calculate All Parameters"):
    
    st.success(f"Adjusted Power Output (Pout): **{Pout:.2f} W**")
    st.info(f"Adjusted Voc: **{Voc:.2f} V**")
    st.info(f"Adjusted Isc: **{Isc:.2f} A**")
    st.info(f"Adjusted Vmp: **{Vmp:.2f} V**")
    st.info(f"Adjusted Imp: **{Imp:.2f} A**")

    # SAVE FOR OTHER PAGES
    st.session_state["P_calculated"] = Pout
    st.session_state["Voc"] = Voc
    st.session_state["Isc"] = Isc
    st.session_state["Vmp"] = Vmp
    st.session_state["Imp"] = Imp
    st.session_state["irr_total"] = irr_total
    st.session_state["Pmax_stc"] = Pmax_stc

    st.success("All parameters calculated successfully! Continue to ABC Optimization page.")
