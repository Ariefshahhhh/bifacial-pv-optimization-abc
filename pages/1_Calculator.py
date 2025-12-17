import streamlit as st

st.title("⚡ Bifacial PV Module Output Computation Tool")
st.markdown("Module-level calculation of Pmax, Vmp, Imp, Isc, Voc using datasheet parameters.")
st.markdown("---")

# ================= INPUTS =================
col1, col2 = st.columns(2)

with col1:
    st.subheader("🔆 Irradiance & Temperature")
    G_front = st.number_input("Front Irradiance G_front (W/m²)", value=800.0)
    BG = st.number_input("Bifacial Gain BG (decimal)", value=0.10, step=0.01)
    Tmod = st.number_input("Module Temperature Tmod (°C)", value=30.0)

    st.subheader("📦 Module STC Data")
    Pstc = st.number_input("Pmax at STC (W)", value=600.0)
    Vmp_stc = st.number_input("Vmp at STC (V)", value=41.0)
    Imp_stc = st.number_input("Imp at STC (A)", value=14.6)
    Voc_stc = st.number_input("Voc at STC (V)", value=49.5)
    Isc_stc = st.number_input("Isc at STC (A)", value=15.2)

with col2:
    st.subheader("🌡 Temperature Coefficients")
    alpha = st.number_input("α (Isc coeff %/°C)", value=0.050, format="%.3f")
    beta = st.number_input("β (Voc coeff %/°C)", value=-0.280, format="%.3f")
    gamma = st.number_input("γ (Pmax coeff %/°C)", value=-0.350, format="%.3f")

    st.subheader("⚙ Loss Factors")
    Fg = st.number_input("Glass Factor Fg", value=0.97)
    Fclean = st.number_input("Cleaning Factor Fclean", value=0.98)
    Funshade = st.number_input("Unshaded Factor Funshade", value=0.95)
    Fmm = st.number_input("Mismatch Factor Fmm", value=0.98)
    Fage = st.number_input("Aging Factor Fage", value=0.95)

# ================= CALCULATION =================
if st.button("Calculate Module Outputs"):

    # Step 1: Bifacial irradiance
    G_rear = BG * G_front
    G_total = G_front + G_rear
    FG = G_total / 1000

    # Step 2: Temperature factors
    Ftemp_I = 1 + (alpha / 100) * (Tmod - 25)
    Ftemp_V = 1 + (beta / 100) * (Tmod - 25)
    Ftemp_P = 1 + (gamma / 100) * (Tmod - 25)

    # Step 3: Electrical outputs
    Pmax = Pstc * FG * Ftemp_P * Fg * Fclean * Funshade * Fmm * Fage
    Imp = Imp_stc * Ftemp_I * Fg * Fclean * Funshade
    Vmp = Vmp_stc * Ftemp_V
    Isc = Isc_stc * Ftemp_I * Fg * Fclean * Funshade
    Voc = Voc_stc * Ftemp_V

    # ================= OUTPUT =================
    st.markdown("---")
    st.subheader("📊 Module-Level Results")

    colA, colB = st.columns(2)
    with colA:
        st.success(f"**Maximum Power (Pmax)** = {Pmax:.2f} W")
        st.success(f"**Voltage at MPP (Vmp)** = {Vmp:.2f} V")
        st.success(f"**Open Circuit Voltage (Voc)** = {Voc:.2f} V")

    with colB:
        st.success(f"**Current at MPP (Imp)** = {Imp:.2f} A")
        st.success(f"**Short Circuit Current (Isc)** = {Isc:.2f} A")

    # ================= STEP DISPLAY =================
st.markdown("### 🧮 Calculation Steps")

st.write(
    f"1️⃣ **Short-Circuit Current (Isc)**\n\n"
    f"Isc = Isc_STC × Ftemp,I × Fg × Fclean × Funshade\n\n"
    f"Isc = {Isc_stc:.3f} × {Ftemp_I:.3f} × {Fg:.3f} × {Fclean:.3f} × {Fshade:.3f} "
    f"= **{Isc_T:.3f} A**"
)

st.write(
    f"2️⃣ **Open-Circuit Voltage (Voc)**\n\n"
    f"Voc = Voc_STC × Ftemp,V\n\n"
    f"Voc = {Voc_stc:.3f} × {Ftemp_V:.3f} "
    f"= **{Voc_T:.3f} V**"
)

st.write(
    f"3️⃣ **Voltage at Maximum Power (Vmp)**\n\n"
    f"Vmp = Vmp_STC × Ftemp,V\n\n"
    f"Vmp = {Vmp_stc:.3f} × {Ftemp_V:.3f} "
    f"= **{Vmp_T:.3f} V**"
)

st.write(
    f"4️⃣ **Current at Maximum Power (Imp)**\n\n"
    f"Imp = Imp_STC × Ftemp,I × Fg × Fclean × Funshade\n\n"
    f"Imp = {Imp_stc:.3f} × {Ftemp_I:.3f} × {Fg:.3f} × {Fclean:.3f} × {Fshade:.3f} "
    f"= **{Imp_T:.3f} A**"
)

st.write(
    f"5️⃣ **Maximum Output Power (Pmax)**\n\n"
    f"Pmax = Pmax_STC × Ftemp,P × Fg × Fclean × Funshade × Fmm × Fage\n\n"
    f"Pmax = {Pmax_stc:.2f} × {Ftemp_P:.3f} × {Fg:.3f} × {Fclean:.3f} × "
    f"{Fshade:.3f} × {Fmm:.3f} × {Fage:.3f} "
    f"= **{Pout:.2f} W**"
)

