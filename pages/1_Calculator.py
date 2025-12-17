import streamlit as st

st.title("⚡ Bifacial PV Output Computation Tool (Module Level)")
st.markdown(
    "This tool computes **Pmax, Vmp, Imp, Voc, and Isc** for a **bifacial PV module** "
    "using datasheet values, bifacial gain (BG), temperature coefficients, and loss factors."
)
st.markdown("---")

# ===============================
# INPUT SECTION
# ===============================

col1, col2 = st.columns(2)

# ---------- LEFT COLUMN ----------
with col1:
    st.subheader("🔆 Environmental Inputs")

    G_front = st.number_input("Front Irradiance, G_front (W/m²)", value=800.0)
    BG = st.number_input("Bifacial Gain, BG (–)", value=0.15, step=0.01, format="%.2f")
    Tcell = st.number_input("Module Temperature, Tmod (°C)", value=30.0)

    st.subheader("📦 Module Electrical Data at STC")

    Pmax_stc = st.number_input("Pmax,STC (W)", value=600.0)
    Vmp_stc = st.number_input("Vmp,STC (V)", value=41.0, step=0.1)
    Imp_stc = st.number_input("Imp,STC (A)", value=14.6, step=0.01)
    Voc_stc = st.number_input("Voc,STC (V)", value=49.5, step=0.1)
    Isc_stc = st.number_input("Isc,STC (A)", value=15.2, step=0.01)

# ---------- RIGHT COLUMN ----------
with col2:
    st.subheader("🌡 Temperature Coefficients (Datasheet)")

    alpha = st.number_input("α (Isc coefficient, %/°C)", value=0.050, format="%.3f")
    beta = st.number_input("β (Voc coefficient, %/°C)", value=-0.280, format="%.3f")
    gamma = st.number_input("γ (Pmax coefficient, %/°C)", value=-0.350, format="%.3f")

    st.subheader("⚙ Loss / Correction Factors")

    Fg = st.number_input("Glass / Optical Factor, Fg", value=0.97, min_value=0.80, max_value=1.00, step=0.01)
    Fclean = st.number_input("Cleaning Factor, Fclean", value=0.98, min_value=0.80, max_value=1.00, step=0.01)
    Fshade = st.number_input("Shading / Unshaded Factor, Funshade", value=0.95, min_value=0.80, max_value=1.00, step=0.01)
    Fmm = st.number_input("Mismatch Factor, Fmm", value=0.98, min_value=0.80, max_value=1.00, step=0.01)
    Fage = st.number_input("Aging Factor, Fage", value=0.95, min_value=0.80, max_value=1.00, step=0.01)

# ===============================
# CALCULATION
# ===============================

if st.button("Calculate Electrical Outputs"):

    # ---- Bifacial Irradiance ----
    G_rear = BG * G_front
    G_total = G_front + G_rear

    # ---- Temperature Factors (from formula PDF) ----
    Ftemp_I = 1 + (alpha / 100) * (Tcell - 25)
    Ftemp_V = 1 + (beta / 100) * (Tcell - 25)
    Ftemp_P = 1 + (gamma / 100) * (Tcell - 25)

    # ---- Electrical Outputs ----
    Isc = Isc_stc * Ftemp_I * Fg * Fclean * Fshade
    Voc = Voc_stc * Ftemp_V
    Vmp = Vmp_stc * Ftemp_V
    Imp = Imp_stc * Ftemp_I * Fg * Fclean * Fshade

    Pmax = (
        Pmax_stc *
        Ftemp_P *
        (G_total / 1000) *
        Fg *
        Fclean *
        Fshade *
        Fmm *
        Fage
    )

    # ===============================
    # RESULTS DISPLAY
    # ===============================
    st.markdown("---")
    st.subheader("📊 Calculated Module Outputs")

    colA, colB = st.columns(2)

    with colA:
        st.success(f"**Maximum Power, Pmax** = {Pmax:.2f} W")
        st.success(f"**Voltage at MPP, Vmp** = {Vmp:.2f} V")
        st.success(f"**Open Circuit Voltage, Voc** = {Voc:.2f} V")

    with colB:
        st.success(f"**Current at MPP, Imp** = {Imp:.2f} A")
        st.success(f"**Short Circuit Current, Isc** = {Isc:.2f} A")

    # ===============================
    # CALCULATION STEPS (EXPLAINED)
    # ===============================
    st.markdown("---")
    st.markdown("### 🧮 Calculation Steps")

    st.write(
        f"**1. Rear irradiance** = BG × G_front = {BG:.2f} × {G_front:.1f} = **{G_rear:.2f} W/m²**"
    )

    st.write(
        f"**2. Total irradiance** = G_front + G_rear = "
        f"{G_front:.1f} + {G_rear:.2f} = **{G_total:.2f} W/m²**"
    )

    st.write(
        f"**3. Temperature factors**  \n"
        f"Ftemp,I = 1 + (α/100)(Tmod − 25) = **{Ftemp_I:.3f}**  \n"
        f"Ftemp,V = 1 + (β/100)(Tmod − 25) = **{Ftemp_V:.3f}**  \n"
        f"Ftemp,P = 1 + (γ/100)(Tmod − 25) = **{Ftemp_P:.3f}**"
    )

    st.write(
        f"**4. Short-circuit current**  \n"
        f"Isc = Isc_STC × Ftemp,I × Fg × Fclean × Funshade  \n"
        f"Isc = {Isc_stc:.3f} × {Ftemp_I:.3f} × {Fg:.3f} × {Fclean:.3f} × {Fshade:.3f}"
    )

    st.write(
        f"**5. Open-circuit voltage**  \n"
        f"Voc = Voc_STC × Ftemp,V = {Voc_stc:.3f} × {Ftemp_V:.3f}"
    )

    st.write(
        f"**6. Voltage at maximum power**  \n"
        f"Vmp = Vmp_STC × Ftemp,V = {Vmp_stc:.3f} × {Ftemp_V:.3f}"
    )

    st.write(
        f"**7. Current at maximum power**  \n"
        f"Imp = Imp_STC × Ftemp,I × Fg × Fclean × Funshade  \n"
        f"Imp = {Imp_stc:.3f} × {Ftemp_I:.3f} × {Fg:.3f} × {Fclean:.3f} × {Fshade:.3f}"
    )

    st.write(
        f"**8. Maximum output power**  \n"
        f"Pmax = Pmax_STC × Ftemp,P × (G_total/1000) × Fg × Fclean × Funshade × Fmm × Fage"
    )
