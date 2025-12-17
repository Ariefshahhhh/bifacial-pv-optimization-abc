import streamlit as st

st.title("⚡ Bifacial PV Output Computation Tool")
st.markdown("Module-level calculation of electrical outputs with temperature correction and loss factors.")
st.markdown("---")

# ===============================
# INPUT SECTION
# ===============================
col1, col2 = st.columns(2)

# -------- LEFT COLUMN --------
with col1:
    st.subheader("🔆 Environmental Inputs")
    G_front = st.number_input("Front Irradiance, G_front (W/m²)", value=800.0)
    BG = st.number_input("Bifacial Gain, BG (rear/front ratio)", value=0.20, format="%.2f")
    Tmod = st.number_input("Module Temperature, Tmod (°C)", value=30.0)

    st.subheader("📦 Module Electrical Data at STC")
    Pmax_stc = st.number_input("Pmax,STC (W)", value=450.0)
    Vmp_stc = st.number_input("Vmp,STC (V)", value=41.0)
    Imp_stc = st.number_input("Imp,STC (A)", value=10.98)
    Voc_stc = st.number_input("Voc,STC (V)", value=49.5)
    Isc_stc = st.number_input("Isc,STC (A)", value=11.5)

# -------- RIGHT COLUMN --------
with col2:
    st.subheader("🌡 Temperature Coefficients")
    alpha = st.number_input("α (Isc coeff, %/°C)", value=0.040, format="%.3f")
    beta  = st.number_input("β (Voc coeff, %/°C)", value=-0.280, format="%.3f")
    gamma = st.number_input("γ (Pmax coeff, %/°C)", value=-0.350, format="%.3f")

    st.subheader("⚙ Loss & Correction Factors")
    Fg = st.number_input("Glass Factor, Fg", value=0.97, min_value=0.80, max_value=1.00)
    Fclean = st.number_input("Cleaning Factor, Fclean", value=0.98, min_value=0.80, max_value=1.00)
    Funshade = st.number_input("Unshaded Factor, Funshade", value=0.95, min_value=0.80, max_value=1.00)
    Fmm = st.number_input("Mismatch Factor, Fmm", value=0.98, min_value=0.80, max_value=1.00)
    Fage = st.number_input("Aging Factor, Fage", value=0.95, min_value=0.80, max_value=1.00)

# ===============================
# CALCULATION
# ===============================
if st.button("Calculate Electrical Outputs"):

    # ---- Bifacial irradiance ----
    G_rear = BG * G_front
    G_total = G_front + G_rear

    # ---- Temperature factors (from your formula PDF) ----
    Ftemp_I = 1 + (alpha / 100) * (Tmod - 25)
    Ftemp_V = 1 + (beta  / 100) * (Tmod - 25)
    Ftemp_P = 1 + (gamma / 100) * (Tmod - 25)

    # ---- Electrical outputs ----
    Isc = Isc_stc * Ftemp_I * Fg * Fclean * Funshade
    Voc = Voc_stc * Ftemp_V
    Vmp = Vmp_stc * Ftemp_V
    Imp = Imp_stc * Ftemp_I * Fg * Fclean * Funshade

    Pmax = (
        Pmax_stc
        * Ftemp_P
        * Fg
        * Fclean
        * Funshade
        * Fmm
        * Fage
        * (G_total / 1000)
    )

    # ===============================
    # RESULTS
    # ===============================
    st.markdown("---")
    st.subheader("📊 Calculated Module-Level Outputs")

    colA, colB = st.columns(2)
    with colA:
        st.success(f"Maximum Power Output, **Pmax** = {Pmax:.2f} W")
        st.success(f"Voltage at Max Power, **Vmp** = {Vmp:.2f} V")
        st.success(f"Open Circuit Voltage, **Voc** = {Voc:.2f} V")

    with colB:
        st.success(f"Current at Max Power, **Imp** = {Imp:.2f} A")
        st.success(f"Short Circuit Current, **Isc** = {Isc:.2f} A")

    # ===============================
    # STEP-BY-STEP CALCULATION DISPLAY
    # ===============================
    st.markdown("---")
    st.markdown("### 🧮 Calculation Steps")

    st.write(
        f"1️⃣ Rear irradiance = BG × G_front = {BG:.2f} × {G_front:.1f} = **{G_rear:.2f} W/m²**"
    )

    st.write(
        f"2️⃣ Total irradiance = G_front + G_rear = {G_front:.1f} + {G_rear:.2f} = **{G_total:.2f} W/m²**"
    )

    st.write(
        f"3️⃣ Temperature factors:"
        f"  \n• Ftemp,I = 1 + (α/100)(T−25) = **{Ftemp_I:.3f}**"
        f"  \n• Ftemp,V = 1 + (β/100)(T−25) = **{Ftemp_V:.3f}**"
        f"  \n• Ftemp,P = 1 + (γ/100)(T−25) = **{Ftemp_P:.3f}**"
    )

    st.write(
        f"4️⃣ Isc = Isc,STC × Ftemp,I × Fg × Fclean × Funshade"
        f"  \n= {Isc_stc:.2f} × {Ftemp_I:.3f} × {Fg:.3f} × {Fclean:.3f} × {Funshade:.3f}"
        f"  \n= **{Isc:.2f} A**"
    )

    st.write(
        f"5️⃣ Voc = Voc,STC × Ftemp,V"
        f"  \n= {Voc_stc:.2f} × {Ftemp_V:.3f}"
        f"  \n= **{Voc:.2f} V**"
    )

    st.write(
        f"6️⃣ Vmp = Vmp,STC × Ftemp,V"
        f"  \n= {Vmp_stc:.2f} × {Ftemp_V:.3f}"
        f"  \n= **{Vmp:.2f} V**"
    )

    st.write(
        f"7️⃣ Imp = Imp,STC × Ftemp,I × Fg × Fclean × Funshade"
        f"  \n= {Imp_stc:.2f} × {Ftemp_I:.3f} × {Fg:.3f} × {Fclean:.3f} × {Funshade:.3f}"
        f"  \n= **{Imp:.2f} A**"
    )

    st.write(
        f"8️⃣ Pmax = Pmax,STC × Ftemp,P × Fg × Fclean × Funshade × Fmm × Fage × (G_total/1000)"
        f"  \n= **{Pmax:.2f} W**"
    )
