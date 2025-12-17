import streamlit as st

st.set_page_config(layout="wide")

st.title("⚡ Bifacial PV Output Computation Tool")
st.markdown("Module-level electrical output calculation with bifacial correction.")
st.markdown("---")

# ===================== INPUT SECTIONS =====================
col1, col2 = st.columns(2)

# ---------- ENVIRONMENT ----------
with col1:
    st.subheader("🔆 Environmental Inputs")

    G_front = st.number_input("Front Irradiance, G_front (W/m²)", value=800.0)
    BG = st.number_input("Bifacial Gain (BG)", value=0.10, format="%.2f")
    Tcell = st.number_input("Cell Temperature, Tmod (°C)", value=30.0)

    st.subheader("📦 Module Electrical Data at STC")

    Pmax_stc = st.number_input("Pmax,STC (W)", value=450.0)
    Vmp_stc = st.number_input("Vmp,STC (V)", value=41.0)
    Imp_stc = st.number_input("Imp,STC (A)", value=10.98)
    Voc_stc = st.number_input("Voc,STC (V)", value=49.5)
    Isc_stc = st.number_input("Isc,STC (A)", value=11.5)

# ---------- COEFFICIENTS & LOSSES ----------
with col2:
    st.subheader("🌡 Temperature Coefficients")

    alpha = st.number_input("α (Isc coeff, %/°C)", value=0.040, format="%.3f")
    beta  = st.number_input("β (Voc coeff, %/°C)", value=-0.280, format="%.3f")
    gamma = st.number_input("γ (Pmax coeff, %/°C)", value=-0.350, format="%.3f")

    st.subheader("⚙ Loss & Correction Factors")

    dirt = st.number_input("Dirt level (%)", value=5.0)
    years = st.number_input("Module age (years)", value=10)

    Fmm = st.number_input("Mismatch factor, Fmm", value=0.98, min_value=0.8, max_value=1.0)
    Fshade = st.number_input("Shading factor, Funshade", value=0.95, min_value=0.8, max_value=1.0)

# ===================== CALCULATION =====================
if st.button("Calculate Outputs"):

    # --- Irradiance ---
    G_rear = BG * G_front
    G_total = G_front + G_rear

    Fg = G_front / 1000
    Fclean = (100 - dirt) / 100
    Fage = 1 - (0.005 * years)

    # --- Temperature factors ---
    Ftemp_I = 1 + (alpha / 100) * (Tcell - 25)
    Ftemp_V = 1 + (beta  / 100) * (Tcell - 25)
    Ftemp_P = 1 + (gamma / 100) * (Tcell - 25)

    # --- Electrical outputs ---
    Isc = Isc_stc * Ftemp_I * Fg * Fclean * Fshade
    Voc = Voc_stc * Ftemp_V
    Vmp = Vmp_stc * Ftemp_V
    Imp = Imp_stc * Ftemp_I * Fg * Fclean * Fshade

    Pmax = (
        Pmax_stc
        * Ftemp_P
        * Fg
        * Fclean
        * Fshade
        * Fmm
        * Fage
    )

    # ===================== OUTPUT =====================
    st.markdown("---")
    st.subheader("📊 Calculated Module-Level Outputs")

    colA, colB = st.columns(2)
    with colA:
        st.success(f"**Maximum Power Output, Pmax = {Pmax:.2f} W**")
        st.success(f"**Voltage at MPP, Vmp = {Vmp:.2f} V**")
        st.success(f"**Open Circuit Voltage, Voc = {Voc:.2f} V**")

    with colB:
        st.success(f"**Current at MPP, Imp = {Imp:.2f} A**")
        st.success(f"**Short Circuit Current, Isc = {Isc:.2f} A**")

    # ===================== STEPS =====================
    st.markdown("---")
    st.markdown("### 🧮 Calculation Steps")

    st.write(f"1. Rear irradiance = BG × G_front = {BG:.2f} × {G_front:.1f} = {G_rear:.2f} W/m²")
    st.write(f"2. Glass factor, Fg = G_front / 1000 = {G_front:.1f} / 1000 = {Fg:.3f}")
    st.write(f"3. Cleaning factor, Fclean = (100 − {dirt:.1f}) / 100 = {Fclean:.3f}")
    st.write(f"4. Aging factor, Fage = 1 − 0.005 × {years} = {Fage:.3f}")

    st.write(f"5. Ftemp,I = {Ftemp_I:.3f}, Ftemp,V = {Ftemp_V:.3f}, Ftemp,P = {Ftemp_P:.3f}")

    st.write(
        f"6. Pmax = {Pmax_stc:.1f} × {Ftemp_P:.3f} × {Fg:.3f} × "
        f"{Fclean:.3f} × {Fshade:.3f} × {Fmm:.3f} × {Fage:.3f}"
    )
