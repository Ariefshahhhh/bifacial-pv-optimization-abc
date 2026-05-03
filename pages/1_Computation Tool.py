import streamlit as st

st.title("⚡ Bifacial PV Output Computation Tool")
st.markdown("Compute Pmax, Vmp, Imp, Voc, and Isc using datasheet-based formulas.")
st.markdown("---")

# ------------------ INPUT LAYOUT ------------------
col1, col2 = st.columns(2)

# ---------- LEFT ----------
with col1:
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
    gamma   = st.number_input("γ (Pmax coeff, %/°C)", value=-0.350, format="%.3f")

    st.subheader("⚙ Loss & Correction Factors")
    dirt   = st.number_input("Dirt Level (%) [Range: 0 – 20%]", min_value=0.0, max_value=20.0, value=5.0)
    years  = st.number_input("Module Age (years) [Range: 0 – 25 years]", min_value=0, max_value=25, value=10, step=1)
    Fmm    = st.number_input("Mismatch Factor (Fmm) [Range: 0.95 – 1.0]", min_value=0.95, max_value=1.0, value=0.98)
    Fshade = st.number_input("Shading Factor (Fshade) [Range: 0.7 – 1.0]", min_value=0.7, max_value=1.0, value=0.95)

# ------------------ 5 SETS OF ENVIRONMENTAL INPUTS ------------------
st.markdown("---")
st.subheader("🔆 Environmental Inputs (5 Sets)")

input_sets = []
cols = st.columns(5)
for i, col in enumerate(cols):
    with col:
        st.markdown(f"**Set {i+1}**")
        g  = col.number_input(f"G_front (W/m²)", value=800.0, key=f"G_front_{i}")
        bg = col.number_input(f"BG", value=0.15, key=f"BG_{i}")
        t  = col.number_input(f"Tcell (°C)", value=30.0, key=f"Tcell_{i}")
        input_sets.append((g, bg, t))

# ------------------ CALCULATION ------------------
if st.button("Calculate Outputs"):

    # ---------- FIXED Fage LOGIC ----------
    if years <= 0:
        Fage = 1.0
    else:
        Fage = 1 - 0.015 - 0.005 * (years - 1)

    # Cleaning factor
    Fclean = (100 - dirt) / 100

    # Fallback rules
    _alphamp = alphamp if alphamp != 0 else alphasc
    _betamp  = betamp  if betamp  != 0 else gamma

    # ------------------ OUTPUT ------------------
    st.markdown("---")
    st.subheader("📊 Calculated Pmax Output (Module Level)")

    result_cols = st.columns(5)
    pmax_results = []

    for i, (G_front, BG, Tcell) in enumerate(input_sets):
        G_rear   = BG * G_front
        G_total  = G_front + G_rear
        Fg       = G_front / 1000

        Ftemp_Pmp = 1 + (gamma / 100) * (Tcell - 25)

        Pmax = Pmax_stc * Ftemp_Pmp * Fg * Fclean * Fshade * Fmm * Fage
        pmax_results.append(Pmax)

        with result_cols[i]:
            st.success(f"**Set {i+1}**\nPmax = {Pmax:.2f} W")

    # Save first set for other pages (same as before)
    G_front0, BG0, Tcell0 = input_sets[0]
    Fg0 = G_front0 / 1000
    Ftemp_Pmp0 = 1 + (gamma / 100) * (Tcell0 - 25)
    Pmax0 = Pmax_stc * Ftemp_Pmp0 * Fg0 * Fclean * Fshade * Fmm * Fage

    st.session_state["Pmax_calculated"] = pmax_results
    st.session_state["Pmax_STC"]        = Pmax_stc
    st.session_state["Ftemp_P"]         = 1 + (gamma / 100) * (input_sets[0][2] - 25)
    st.session_state["Fg"]              = Fg0
    st.session_state["Fclean"]          = Fclean
    st.session_state["Fshade"]          = Fshade
    st.session_state["Fmm"]             = Fmm
    st.session_state["Fage"]            = Fage

    st.info("All calculations follow the datasheet-based PV computation formula at module level.")
