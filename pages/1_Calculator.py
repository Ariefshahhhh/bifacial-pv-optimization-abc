import streamlit as st

st.title("⚡ Bifacial PV Output Computation Tool")
st.markdown("Module-level electrical output calculation with full loss modeling.")
st.markdown("---")

# -------------------- INPUTS --------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("🔆 Environmental Inputs")
    G_front = st.number_input("Front Irradiance G_front (W/m²)", value=800.0)
    BG = st.number_input("Bifacial Gain (BG)", value=0.10, format="%.2f")
    Tcell = st.number_input("Cell Temperature Tmod (°C)", value=30.0)

    st.subheader("📦 Module Electrical Data at STC")
    Pstc = st.number_input("Pmax,STC (W)", value=450.0)
    Vmp_stc = st.number_input("Vmp,STC (V)", value=41.0)
    Imp_stc = st.number_input("Imp,STC (A)", value=10.98)
    Voc_stc = st.number_input("Voc,STC (V)", value=49.5)
    Isc_stc = st.number_input("Isc,STC (A)", value=11.5)

with col2:
    st.subheader("🌡 Temperature Coefficients")
    alpha = st.number_input("α (Isc) %/°C", value=0.040, format="%.3f")
    beta = st.number_input("β (Voc & Vmp) %/°C", value=-0.280, format="%.3f")
    gamma = st.number_input("γ (Pmax) %/°C", value=-0.350, format="%.3f")

    st.subheader("⚙ Loss Inputs (User)")
    dirt = st.number_input("Dirt Level (%)", value=5.0)
    age_years = st.number_input("Module Age (years)", value=10)
    Fmm = st.number_input("Mismatch Factor Fmm", value=0.98, min_value=0.80, max_value=1.00)
    Funshade = st.number_input("Unshaded Factor Funshade", value=0.95, min_value=0.80, max_value=1.00)

# -------------------- CALCULATION --------------------
if st.button("Calculate Outputs"):

    # --- Irradiance ---
    G_rear = BG * G_front
    G_total = G_front + G_rear
    Fg = G_total / 1000

    # --- Temperature factors ---
    Ftemp_I = 1 + (alpha / 100) * (Tcell - 25)
    Ftemp_V = 1 + (beta / 100) * (Tcell - 25)
    Ftemp_P = 1 + (gamma / 100) * (Tcell - 25)

    # --- Loss factors ---
    Fclean = (100 - dirt) / 100
    degradation_rate = 0.005
    Fage = 1 - degradation_rate * age_years

    # --- Electrical outputs ---
    Isc = Isc_stc * Ftemp_I * Fg * Fclean * Funshade
    Voc = Voc_stc * Ftemp_V
    Vmp = Vmp_stc * Ftemp_V
    Imp = Imp_stc * Ftemp_I * Fg * Fclean * Funshade

    Pmax = (
        Pstc *
        Ftemp_P *
        Fg *
        Fclean *
        Funshade *
        Fmm *
        Fage
    )

    # -------------------- RESULTS --------------------
    st.markdown("---")
    st.subheader("📊 Calculated Electrical Outputs")

    colA, colB = st.columns(2)
    with colA:
        st.success(f"**Maximum Power Output (Pmax)** = {Pmax:.2f} W")
        st.success(f"**Voltage at Maximum Power (Vmp)** = {Vmp:.2f} V")
        st.success(f"**Open Circuit Voltage (Voc)** = {Voc:.2f} V")

    with colB:
        st.success(f"**Current at Maximum Power (Imp)** = {Imp:.2f} A")
        st.success(f"**Short Circuit Current (Isc)** = {Isc:.2f} A")

    # -------------------- CALCULATION STEPS --------------------
    st.markdown("### 🧮 Calculation Steps")

    st.write(f"1. Rear irradiance = BG × G_front = {BG} × {G_front} = {G_rear:.2f} W/m²")
    st.write(f"2. Total irradiance = {G_total:.2f} W/m² → Fg = {Fg:.3f}")

    st.write(
        f"3. Isc = {Isc_stc} × {Ftemp_I:.3f} × {Fg:.3f} × {Fclean:.3f} × {Funshade:.3f}"
        f" = {Isc:.2f} A"
    )

    st.write(
        f"4. Voc = {Voc_stc} × {Ftemp_V:.3f}"
        f" = {Voc:.2f} V"
    )

    st.write(
        f"5. Vmp = {Vmp_stc} × {Ftemp_V:.3f}"
        f" = {Vmp:.2f} V"
    )

    st.write(
        f"6. Imp = {Imp_stc} × {Ftemp_I:.3f} × {Fg:.3f} × {Fclean:.3f} × {Funshade:.3f}"
        f" = {Imp:.2f} A"
    )

    st.write(
        f"7. Pmax = {Pstc} × {Ftemp_P:.3f} × {Fg:.3f} × {Fclean:.3f} × "
        f"{Funshade:.3f} × {Fmm:.3f} × {Fage:.3f}"
        f" = {Pmax:.2f} W"
    )
