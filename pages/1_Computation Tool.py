import streamlit as st

st.set_page_config(page_title="Bifacial PV Computation Tool", layout="wide")

st.markdown("""
<style>
    html, body, [class*="css"] { font-family: 'Segoe UI', sans-serif; }

    .page-title {
        font-size: 1.75rem; font-weight: 700; color: #1e293b; margin-bottom: 0.15rem;
    }
    .page-sub { font-size: 0.85rem; color: #64748b; margin-bottom: 0.5rem; }

    .section-header {
        font-size: 0.68rem; font-weight: 700; letter-spacing: 0.13em;
        text-transform: uppercase; color: #2563eb;
        border-bottom: 2px solid #2563eb;
        padding-bottom: 4px; margin: 1.4rem 0 0.75rem 0;
    }

    label, [data-testid="stWidgetLabel"] p {
        font-size: 0.8rem !important; color: #374151 !important; font-weight: 500 !important;
    }

    hr { border: none; border-top: 1px solid #e5e7eb; margin: 1.2rem 0; }

    .result-row {
        display: grid; grid-template-columns: repeat(5, 1fr);
        gap: 0.75rem; margin: 1rem 0 1.5rem 0;
    }
    .result-card {
        background: #f8fafc; border: 1px solid #e2e8f0;
        border-top: 3px solid #2563eb; border-radius: 8px;
        padding: 0.9rem 1rem; text-align: center;
    }
    .result-card.highlight { background: #eff6ff; border-top-color: #1d4ed8; }
    .rc-label {
        font-size: 0.68rem; font-weight: 700; letter-spacing: 0.1em;
        text-transform: uppercase; color: #6b7280; margin-bottom: 0.3rem;
    }
    .rc-value { font-size: 1.5rem; font-weight: 700; color: #1e293b; line-height: 1.1; }
    .result-card.highlight .rc-value { color: #1d4ed8; }
    .rc-unit { font-size: 0.7rem; color: #94a3b8; margin-top: 0.25rem; }

    .steps-wrap {
        background: #f8fafc; border: 1px solid #e2e8f0;
        border-radius: 8px; overflow: hidden; margin-top: 0.5rem;
    }
    .step-row {
        display: flex; align-items: flex-start; gap: 0.9rem;
        padding: 0.65rem 1.1rem; border-bottom: 1px solid #e2e8f0;
        font-size: 0.82rem; color: #374151; line-height: 1.65;
    }
    .step-row:last-child { border-bottom: none; }
    .step-row:nth-child(even) { background: #ffffff; }
    .step-n {
        min-width: 22px; height: 22px; background: #2563eb; color: #fff;
        border-radius: 50%; font-size: 0.65rem; font-weight: 700;
        display: flex; align-items: center; justify-content: center;
        margin-top: 2px; flex-shrink: 0;
    }
    .step-row b { color: #1e293b; }

    .info-note {
        font-size: 0.78rem; color: #1d4ed8; background: #eff6ff;
        border: 1px solid #bfdbfe; border-radius: 6px;
        padding: 0.6rem 1rem; margin-top: 1rem;
    }

    [data-testid="stButton"] > button {
        background-color: #2563eb !important; color: #ffffff !important;
        font-weight: 600 !important; font-size: 0.88rem !important;
        border: none !important; border-radius: 6px !important;
        padding: 0.55rem 2.5rem !important;
    }
    [data-testid="stButton"] > button:hover { background-color: #1d4ed8 !important; }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown('<div class="page-title">⚡ Bifacial PV Output Computation Tool</div>', unsafe_allow_html=True)
st.markdown('<div class="page-sub">Compute Pmax, Vmp, Imp, Voc, and Isc using datasheet-based formulas.</div>', unsafe_allow_html=True)
st.markdown('<hr>', unsafe_allow_html=True)

# ── Inputs ────────────────────────────────────────────────────────────────────
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown('<div class="section-header">🔆 Environmental Inputs</div>', unsafe_allow_html=True)
    G_front  = st.number_input("Front Irradiance (W/m²)", value=800.0)
    BG       = st.number_input("Bifacial Gain (BG)", value=0.15)
    Tcell    = st.number_input("Cell Temperature (°C)", value=30.0)

    st.markdown('<div class="section-header">📦 Module Electrical Data at STC</div>', unsafe_allow_html=True)
    Pmax_stc = st.number_input("Pmax at STC (W)", value=450.0)
    Vmp_stc  = st.number_input("Vmp at STC (V)", value=41.0)
    Imp_stc  = st.number_input("Imp at STC (A)", value=10.98)
    Voc_stc  = st.number_input("Voc at STC (V)", value=49.5)
    Isc_stc  = st.number_input("Isc at STC (A)", value=11.5)

with col2:
    st.markdown('<div class="section-header">🌡 Temperature Coefficients</div>', unsafe_allow_html=True)
    alphasc = st.number_input("α (Isc coeff, %/°C)", value=0.040, format="%.3f")
    betaoc  = st.number_input("β (Voc coeff, %/°C)", value=-0.280, format="%.3f")
    alphamp = st.number_input("α (Imp coeff, %/°C)", value=0.040, format="%.3f")
    betamp  = st.number_input("β (Vmp coeff, %/°C)", value=-0.280, format="%.3f")
    gamma   = st.number_input("γ (Pmax coeff, %/°C)", value=-0.350, format="%.3f")

    st.markdown('<div class="section-header">⚙ Loss & Correction Factors</div>', unsafe_allow_html=True)
    dirt   = st.number_input("Dirt Level (%) [Range: 0 – 20%]", min_value=0.0, max_value=20.0, value=5.0)
    years  = st.number_input("Module Age (years) [Range: 0 – 25 years]", min_value=0, max_value=25, value=10, step=1)
    Fmm    = st.number_input("Mismatch Factor (Fmm) [Range: 0.95 – 1.0]", min_value=0.95, max_value=1.0, value=0.98)
    Fshade = st.number_input("Shading Factor (Fshade) [Range: 0.7 – 1.0]", min_value=0.7, max_value=1.0, value=0.95)

st.markdown('<hr>', unsafe_allow_html=True)

# ── Calculate ─────────────────────────────────────────────────────────────────
if st.button("Calculate Outputs"):

    # Irradiance
    G_rear  = BG * G_front
    G_total = G_front + G_rear
    Fg      = G_front / 1000
    Fclean  = (100 - dirt) / 100

    # Fage
    Fage = 1.0 if years <= 0 else 1 - 0.015 - 0.005 * (years - 1)

    # Temperature factors (with fallback)
    if alphamp == 0: alphamp = alphasc
    if betamp  == 0: betamp  = gamma

    Ftemp_Isc = 1 + (alphasc / 100) * (Tcell - 25)
    Ftemp_Imp = 1 + (alphamp / 100) * (Tcell - 25)
    Ftemp_Voc = 1 + (betaoc  / 100) * (Tcell - 25)
    Ftemp_Vmp = 1 + (betamp  / 100) * (Tcell - 25)
    Ftemp_Pmp = 1 + (gamma   / 100) * (Tcell - 25)

    # Electrical outputs
    Isc  = Isc_stc  * Ftemp_Isc * Fg * Fclean * Fshade
    Imp  = Imp_stc  * Ftemp_Imp * Fg * Fclean * Fshade
    Voc  = Voc_stc  * Ftemp_Voc
    Vmp  = Vmp_stc  * Ftemp_Vmp
    Pmax = Pmax_stc * Ftemp_Pmp * Fg * Fclean * Fshade * Fmm * Fage

    # Save for ABC page
    st.session_state["Pmax_calculated"] = Pmax
    st.session_state["Pmax_STC"]        = Pmax_stc
    st.session_state["Ftemp_P"]         = Ftemp_Pmp
    st.session_state["Fg"]              = Fg
    st.session_state["Fclean"]          = Fclean
    st.session_state["Fshade"]          = Fshade
    st.session_state["Fmm"]             = Fmm
    st.session_state["Fage"]            = Fage
    st.session_state["Ftemp_Isc"]       = Ftemp_Isc
    st.session_state["Ftemp_Imp"]       = Ftemp_Imp
    st.session_state["Ftemp_Voc"]       = Ftemp_Voc
    st.session_state["Ftemp_Vmp"]       = Ftemp_Vmp
    st.session_state["Isc_stc"]         = Isc_stc
    st.session_state["Imp_stc"]         = Imp_stc
    st.session_state["Voc_stc"]         = Voc_stc
    st.session_state["Vmp_stc"]         = Vmp_stc

    # ── Results ──────────────────────────────────────────────────────────────
    st.markdown('<hr>', unsafe_allow_html=True)
    st.markdown('<div class="section-header">📊 Calculated Electrical Outputs — Module Level</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="result-row">
        <div class="result-card highlight">
            <div class="rc-label">Pmax</div>
            <div class="rc-value">{Pmax:.2f}</div>
            <div class="rc-unit">W · Maximum Power Output</div>
        </div>
        <div class="result-card">
            <div class="rc-label">Vmp</div>
            <div class="rc-value">{Vmp:.2f}</div>
            <div class="rc-unit">V · Voltage at Max Power</div>
        </div>
        <div class="result-card">
            <div class="rc-label">Imp</div>
            <div class="rc-value">{Imp:.2f}</div>
            <div class="rc-unit">A · Current at Max Power</div>
        </div>
        <div class="result-card">
            <div class="rc-label">Voc</div>
            <div class="rc-value">{Voc:.2f}</div>
            <div class="rc-unit">V · Open Circuit Voltage</div>
        </div>
        <div class="result-card">
            <div class="rc-label">Isc</div>
            <div class="rc-value">{Isc:.2f}</div>
            <div class="rc-unit">A · Short Circuit Current</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Steps ─────────────────────────────────────────────────────────────────
    st.markdown('<div class="section-header">🧮 Calculation Steps</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="steps-wrap">
        <div class="step-row">
            <div class="step-n">1</div>
            <div>Rear irradiance = BG × G_front = {BG} × {G_front} = <b>{G_rear:.2f} W/m²</b></div>
        </div>
        <div class="step-row">
            <div class="step-n">2</div>
            <div>Total irradiance = G_front + G_rear = {G_front} + {G_rear:.2f} = <b>{G_total:.2f} W/m²</b></div>
        </div>
        <div class="step-row">
            <div class="step-n">3</div>
            <div>Irradiance factor Fg = G_front / 1000 = {G_front} / 1000 = <b>{Fg:.3f}</b></div>
        </div>
        <div class="step-row">
            <div class="step-n">4</div>
            <div>
                Temperature factors:<br>
                &nbsp;&nbsp;· Ftemp,Isc = 1 + (α_Isc / 100)(T − 25) = <b>{Ftemp_Isc:.3f}</b><br>
                &nbsp;&nbsp;· Ftemp,Imp = 1 + (α_Imp / 100)(T − 25) = <b>{Ftemp_Imp:.3f}</b><br>
                &nbsp;&nbsp;· Ftemp,Voc = 1 + (β_Voc / 100)(T − 25) = <b>{Ftemp_Voc:.3f}</b><br>
                &nbsp;&nbsp;· Ftemp,Vmp = 1 + (β_Vmp / 100)(T − 25) = <b>{Ftemp_Vmp:.3f}</b><br>
                &nbsp;&nbsp;· Ftemp,Pmp = 1 + (γ / 100)(T − 25) = <b>{Ftemp_Pmp:.3f}</b>
            </div>
        </div>
        <div class="step-row">
            <div class="step-n">5</div>
            <div>Cleaning factor Fclean = (100 − dirt) / 100 = (100 − {dirt}) / 100 = <b>{Fclean:.3f}</b></div>
        </div>
        <div class="step-row">
            <div class="step-n">6</div>
            <div>Aging factor Fage — Year 1 degradation = 1.5%, subsequent years = 0.5%/year → <b>Fage = {Fage:.3f}</b></div>
        </div>
        <div class="step-row">
            <div class="step-n">7</div>
            <div>
                Isc &nbsp;= {Isc_stc:.3f} × {Ftemp_Isc:.3f} × {Fg:.3f} × {Fclean:.3f} × {Fshade:.3f} = <b>{Isc:.2f} A</b><br>
                Voc = {Voc_stc:.3f} × {Ftemp_Voc:.3f} = <b>{Voc:.2f} V</b><br>
                Vmp = {Vmp_stc:.3f} × {Ftemp_Vmp:.3f} = <b>{Vmp:.2f} V</b><br>
                Imp &nbsp;= {Imp_stc:.3f} × {Ftemp_Imp:.3f} × {Fg:.3f} × {Fclean:.3f} × {Fshade:.3f} = <b>{Imp:.2f} A</b><br>
                Pmax = {Pmax_stc:.1f} × {Ftemp_Pmp:.3f} × {Fg:.3f} × {Fclean:.3f} × {Fshade:.3f} × {Fmm:.3f} × {Fage:.3f} = <b>{Pmax:.2f} W</b>
            </div>
        </div>
    </div>

    <div class="info-note">
        ℹ All calculations follow the datasheet-based PV computation formula at module level.
        Values have been saved — proceed to the ABC Optimizer page.
    </div>
    """, unsafe_allow_html=True)
