import streamlit as st

st.title("⚡ Bifacial PV Output Computation Tool")
st.markdown("Compute Pmax, Vmp, Imp, Voc, and Isc using datasheet-based formulas.")
st.markdown("---")

# ------------------ INPUT LAYOUT ------------------
col1, col2 = st.columns(2)

# ---------- LEFT ----------
with col1:
    st.subheader("🔆 Environmental Inputs")

    G_front = st.number_input("Front Irradiance (W/m²)", value=800.0)
    BG = st.number_input("Bifacial Gain (BG)", value=0.15)
    Tcell = st.number_input("Cell Temperature (°C)", value=30.0)

    st.subheader("📦 Module Electrical Data at STC")
    Pmax_stc = st.number_input("Pmax at STC (W)", value=450.0)
    Vmp_stc = st.number_input("Vmp at STC (V)", value=41.0)
    Imp_stc = st.number_input("Imp at STC (A)", value=10.98)
    Voc_stc = st.number_input("Voc at STC (V)", value=49.5)
    Isc_stc = st.number_input("Isc at STC (A)", value=11.5)

# ---------- RIGHT ----------
with col2:
    st.subheader("🌡 Temperature Coefficients")
    alphasc = st.number_input("α (Isc coeff, %/°C)", value=0.040, format="%.3f")
    betaoc  = st.number_input("β (Voc coeff, %/°C)", value=-0.280, format="%.3f")
    alphamp = st.number_input("α (Imp coeff, %/°C)", value=0.040, format="%.3f")
    betamp  = st.number_input("β (Vmp coeff, %/°C)", value=-0.280, format="%.3f")
    gamma = st.number_input("γ (Pmax coeff, %/°C)", value=-0.350, format="%.3f")



    st.subheader("⚙ Loss & Correction Factors")

    st.write("Dirt Level (%) [Range: 0 – 20%]")
    dirt = st.number_input("Dirt Level (%)", min_value=0.0, max_value=20.0, value=5.0)
    
    st.write("Module Age (years) [Range: 0 – 25 years]")
    years = st.number_input("Module Age (years)", min_value=0, max_value=25, value=10, step=1)
    
    st.write("Mismatch Factor (Fmm) [Range: 0.95 – 1.0]")
    Fmm = st.number_input("Mismatch Factor (Fmm)", min_value=0.95, max_value=1.0, value=0.98)

    st.write("Shading Factor (Fshade) [Range: 0.7 – 1.0]")
    Fshade = st.number_input("Shading Factor (Fshade)", min_value=0.7, max_value=1.0, value=0.95)

# ------------------ CALCULATION ------------------
if st.button("Calculate Outputs"):

    # Rear & total irradiance
    G_rear = BG * G_front
    G_total = G_front + G_rear

    # Irradiance factor
    Fg = G_front / 1000

    # Cleaning factor
    Fclean = (100 - dirt) / 100

    # ---------- FIXED Fage LOGIC ----------
    if years <= 0:
        Fage = 1.0
    else:
        Fage = 1 - 0.015 - 0.005 * (years - 1)

    # -------- Temperature factors --------
    # Fallback rules:
    # - If alphamp not given → use alphasc
    # - If betamp not given → use gamma
    
    if alphamp == 0:
        alphamp = alphasc
    
    if betamp == 0:
        betamp = gamma
    
    Ftemp_Isc = 1 + (alphasc / 100) * (Tcell - 25)
    Ftemp_Imp = 1 + (alphamp / 100) * (Tcell - 25)
    Ftemp_Voc = 1 + (betaoc  / 100) * (Tcell - 25)
    Ftemp_Vmp = 1 + (betamp  / 100) * (Tcell - 25)
    Ftemp_Pmp = 1 + (gamma   / 100) * (Tcell - 25)
    
    # -------- Electrical outputs --------
    Isc  = Isc_stc  * Ftemp_Isc * Fg * Fclean * Fshade
    Imp  = Imp_stc  * Ftemp_Imp * Fg * Fclean * Fshade
    Voc  = Voc_stc  * Ftemp_Voc
    Vmp  = Vmp_stc  * Ftemp_Vmp
    Pmax = Pmax_stc * Ftemp_Pmp * Fg * Fclean * Fshade * Fmm * Fage

    # --- SAVE FOR ABC (THIS IS THE KEY PART) ---
    # --- SAVE FOR ABC (THIS IS THE KEY PART) ---
    st.session_state["Pmax_calculated"] = Pmax
    st.session_state["Pmax_STC"] = Pmax_stc
    st.session_state["Ftemp_P"] = Ftemp_Pmp
    st.session_state["Fg"] = Fg
    st.session_state["Fclean"] = Fclean
    st.session_state["Fshade"] = Fshade
    st.session_state["Fmm"] = Fmm
    st.session_state["Fage"] = Fage


    # ------------------ OUTPUT ------------------
    st.markdown("---")
    st.subheader("📊 Calculated Electrical Outputs (Module Level)")

    st.success(f"Maximum Power Output, **Pmax** = {Pmax:.2f} W")
    st.success(f"Voltage at Maximum Power, **Vmp** = {Vmp:.2f} V")
    st.success(f"Current at Maximum Power, **Imp** = {Imp:.2f} A")
    st.success(f"Open Circuit Voltage, **Voc** = {Voc:.2f} V")
    st.success(f"Short Circuit Current, **Isc** = {Isc:.2f} A")

    st.markdown("### 🧮 Calculation Steps")
    st.write(f"1️⃣ Rear irradiance = BG × G_front = {BG} × {G_front} = **{G_rear:.2f} W/m²**")
    st.write(f"2️⃣ Total irradiance = G_front + G_rear = **{G_total:.2f} W/m²**")

    st.write(f"3️⃣ Irradiance factor Fg = G_front / 1000 = {G_front} / 1000 = **{Fg:.3f}**")


    
    st.write(
        f"4️⃣ Temperature factors:\n"
        f"- Ftemp,Isc = 1 + (α_Isc/100)(T−25) = **{Ftemp_Isc:.3f}**\n"
        f"- Ftemp,Imp = 1 + (α_Imp/100)(T−25) = **{Ftemp_Imp:.3f}**\n"
        f"- Ftemp,Voc = 1 + (β_Voc/100)(T−25) = **{Ftemp_Voc:.3f}**\n"
        f"- Ftemp,Vmp = 1 + (β_Vmp/100)(T−25) = **{Ftemp_Vmp:.3f}**\n"
        f"- Ftemp,Pmp = 1 + (γ/100)(T−25) = **{Ftemp_Pmp:.3f}**"
    )

    st.write(
        f"5️⃣ Cleaning factor Fclean = (100 − dirt)/100 = "
        f"(100 − {dirt})/100 = **{Fclean:.3f}**"
    )
    
    st.write(
        f"6️⃣ Aging factor Fage:\n"
        f"- Year 1 degradation = 1.5%\n"
        f"- Subsequent years = 0.5%/year\n"
        f"- Total Fage = **{Fage:.3f}**"
    )
    
    st.write(
        f"7️⃣ Electrical calculations:\n"
        f"- Isc = {Isc_stc:.3f} × {Ftemp_Isc:.3f} × {Fg:.3f} × "
        f"{Fclean:.3f} × {Fshade:.3f} = **{Isc:.2f} A**\n"
        f"- Voc = {Voc_stc:.3f} × {Ftemp_Voc:.3f} = **{Voc:.2f} V**\n"
        f"- Vmp = {Vmp_stc:.3f} × {Ftemp_Vmp:.3f} = **{Vmp:.2f} V**\n"
        f"- Imp = {Imp_stc:.3f} × {Ftemp_Imp:.3f} × {Fg:.3f} × "
        f"{Fclean:.3f} × {Fshade:.3f} = **{Imp:.2f} A**\n"
        f"- Pmax = {Pmax_stc:.1f} × {Ftemp_Pmp:.3f} × {Fg:.3f} × "
        f"{Fclean:.3f} × {Fshade:.3f} × {Fmm:.3f} × {Fage:.3f} "
        f"= **{Pmax:.2f} W**"
    )
    
    st.info("All calculations follow the datasheet-based PV computation formula at module level.")














