import streamlit as st

st.title("⚡ Bifacial PV Output Estimation")
st.markdown("Estimate key electrical output parameters of a bifacial PV module.")
st.markdown("---")

# =========================
# INPUT SECTION
# =========================
st.subheader("📥 Module & Environmental Inputs")

col1, col2 = st.columns(2)

with col1:
    Pstc = st.number_input("Pmp at STC (W)", value=450.0)
    Voc_stc = st.number_input("Voc at STC (V)", value=49.5)
    Isc_stc = st.number_input("Isc at STC (A)", value=11.4)
    Vmp_stc = st.number_input("Vmp at STC (V)", value=41.5)
    Imp_stc = st.number_input("Imp at STC (A)", value=10.8)

with col2:
    G_front = st.number_input("Front Irradiance (W/m²)", value=800.0)
    G_rear = st.number_input("Rear Irradiance (W/m²)", value=100.0)
    Tcell = st.number_input("Cell Temperature (°C)", value=30.0)
    alpha_I = st.number_input("Current Temp Coeff α (%/°C)", value=0.05) / 100
    beta_V = st.number_input("Voltage Temp Coeff β (%/°C)", value=0.30) / 100

# =========================
# LOSS FACTORS
# =========================
st.subheader("⚙️ Correction Factors")

c1, c2, c3 = st.columns(3)

with c1:
    Fmm = st.number_input("Mismatch Factor (Fmm)", 0.80, 1.00, 0.98, 0.01)
    Fage = st.number_input("Aging Factor (Fage)", 0.80, 1.00, 0.95, 0.01)

with c2:
    Fclean = st.number_input("Cleaning Factor (Fclean)", 0.80, 1.00, 0.97, 0.01)
    Fshade = st.number_input("Shading Factor (Fshade)", 0.80, 1.00, 0.96, 0.01)

with c3:
    Fg = st.number_input("Glass/Soiling Factor (Fg)", 0.80, 1.00, 0.98, 0.01)

# =========================
# CALCULATION
# =========================
G_total = G_front + G_rear
temp_diff = Tcell - 25
loss_product = Fmm * Fage * Fclean * Fshade * Fg

Isc = Isc_stc * (G_total / 1000) * (1 + alpha_I * temp_diff)
Voc = Voc_stc * (1 - beta_V * temp_diff)

Imp = Imp_stc * (G_total / 1000) * (1 + alpha_I * temp_diff) * loss_product
Vmp = Vmp_stc * (1 - beta_V * temp_diff)
Pmp = Vmp * Imp

# =========================
# OUTPUT
# =========================
st.markdown("---")
st.subheader("📊 Estimated PV Output Parameters")

o1, o2, o3, o4, o5 = st.columns(5)

o1.metric("Voc (V)", f"{Voc:.2f}")
o2.metric("Isc (A)", f"{Isc:.2f}")
o3.metric("Vmp (V)", f"{Vmp:.2f}")
o4.metric("Imp (A)", f"{Imp:.2f}")
o5.metric("Pmp (W)", f"{Pmp:.2f}")

# Save for ABC / Results pages
st.session_state["Vmp"] = Vmp
st.session_state["Imp"] = Imp
st.session_state["Pmp"] = Pmp
