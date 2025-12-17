import streamlit as st

st.title("⚡ Bifacial PV Output Computation Tool")
st.markdown("Module-level electrical output calculation based on datasheet and loss models.")
st.markdown("---")

# ===============================
# INPUT SECTIONS
# ===============================

col1, col2 = st.columns(2)

# ---------- ENVIRONMENT ----------
with col1:
    st.subheader("🔆 Environmental Inputs")
    G_front = st.number_input("Front Irradiance, G (W/m²)", value=800.0)
    Tcell = st.number_input("Module Temperature, Tmod (°C)", value=30.0)

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

    st.subheader("⚙ Loss & Correction Inputs")
    dirt = st.number_input("Dirt level (%)", value=5.0)
    age_years = st.number_input("Module age (years)", value=10.0)
    Fmm = st.number_input("Mismatch factor, Fmm", value=0.98, min_value=0.8, max_value=1.0)
    Fshade = st.number_input("Shading factor, Funshade", value=0.95, min_value=0.8, max_value=1.0)

# ===============================
# CALCULATION
# ===============================

if st.button("Calculate Outputs"):

    ΔT = Tcell - 25

    # --- Temperature factors (from formula sheet) ---
    Ftemp_I = 1 + (alpha / 100) * ΔT
    Ftemp_V = 1 + (beta  / 100) * ΔT
    Ftemp_P = 1 + (gamma / 100) * ΔT

    # --- Loss factors ---
    Fg = G_front / 1000                     # FIXED (front only)
    Fclean = (100 - dirt) / 100
    degradation_rate = 0.005               # 0.5% per year
    Fage = 1 - degradation_rate * age_years

    # ===============================
    # ELECTRICAL OUTPUTS (FORMULA-BASED)
    # ===============================

    Isc = Isc_stc * Ftemp_I * Fg * Fclean * Fshade
    Voc = Voc_stc * Ftemp_V
    Vmp = Vmp_stc * Ftemp_V
    Imp = Imp_stc * Ftemp_I * Fg * Fclean * Fshade

    Pmax = (
        Pmax_stc *
        Ftemp_P *
        Fg *
        Fclean *
        Fshade *
        Fmm *
        Fage
    )

    # ===============================
    # RESULTS
    # ===============================

    st.markdown("---")
    st.subheader("📊 Calculated Electrical Outputs")

    colA, colB = st.columns(2)
    with colA:
        st.success(f"**Maximum Power Output, Pmax** = {Pmax:.2f} W")
        st.success(f"**Voltage at Max Power, Vmp** = {Vmp:.2f} V")
        st.success(f"**Open Circuit Voltage, Voc** = {Voc:.2f} V")

    with colB:
        st.success(f"**Current at Max Power, Imp** = {Imp:.2f} A")
        st.success(f"**Short Circuit Current, Isc** = {Isc:.2f} A")

    # ===============================
    # CALCULATION STEPS (CLEAR)
    # ===============================

    st.markdown("---")
    st.markdown("### 🧮 Calculation Steps")

    st.write(f"**Fg** = G / 1000 = {G_front} / 1000 = {Fg:.3f}")
    st.write(f"**Fclean** = (100 − dirt) / 100 = (100 − {dirt}) / 100 = {Fclean:.3f}")
    st.write(f"**Fage** = 1 − (0.005 × years) = 1 − (0.005 × {age_years}) = {Fage:.3f}")

    st.write(f"**Ftemp,I** = 1 + (α/100)(T−25) = {Ftemp_I:.3f}")
    st.write(f"**Ftemp,V** = 1 + (β/100)(T−25) = {Ftemp_V:.3f}")
    st.write(f"**Ftemp,P** = 1 + (γ/100)(T−25) = {Ftemp_P:.3f}")

    st.write(f"**Isc** = Isc,STC × Ftemp,I × Fg × Fclean × Funshade")
    st.write(f"**Voc** = Voc,STC × Ftemp,V")
    st.write(f"**Vmp** = Vmp,STC × Ftemp,V")
    st.write(f"**Imp** = Imp,STC × Ftemp,I × Fg × Fclean × Funshade")
    st.write(f"**Pmax** = Pmax,STC × Ftemp,P × Fg × Fclean × Funshade × Fmm × Fage")
