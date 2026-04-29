import streamlit as st

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Bifacial PV Computation Tool",
    page_icon="⚡",
    layout="wide",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&display=swap');

/* ── Root palette ── */
:root {
    --bg:        #0b0f1a;
    --surface:   #111827;
    --card:      #161d2e;
    --border:    #1e2d47;
    --accent:    #f5a623;
    --accent2:   #3b82f6;
    --success:   #10b981;
    --text:      #e8edf5;
    --muted:     #6b7fa3;
    --font-head: 'Syne', sans-serif;
    --font-mono: 'DM Mono', monospace;
}

/* ── Base ── */
html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: var(--font-mono) !important;
}

[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stSidebar"] { background: var(--surface) !important; }

/* ── Hide default Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }

/* ── Hero banner ── */
.hero {
    background: linear-gradient(135deg, #0f1c35 0%, #0b0f1a 60%, #1a0f2e 100%);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 2.5rem 3rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 260px; height: 260px;
    background: radial-gradient(circle, rgba(245,166,35,0.12) 0%, transparent 70%);
    border-radius: 50%;
}
.hero::after {
    content: '';
    position: absolute;
    bottom: -40px; left: 20%;
    width: 180px; height: 180px;
    background: radial-gradient(circle, rgba(59,130,246,0.10) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-title {
    font-family: var(--font-head);
    font-size: 2.4rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    color: var(--text);
    margin: 0 0 0.4rem 0;
    line-height: 1.1;
}
.hero-title span { color: var(--accent); }
.hero-sub {
    font-family: var(--font-mono);
    font-size: 0.82rem;
    color: var(--muted);
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

/* ── Section headers ── */
.section-label {
    font-family: var(--font-head);
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--accent);
    margin: 1.8rem 0 0.8rem 0;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.section-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border);
}

/* ── Input cards ── */
[data-testid="stNumberInput"] > div,
[data-testid="stTextInput"] > div {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    transition: border-color 0.2s;
}
[data-testid="stNumberInput"] > div:focus-within,
[data-testid="stTextInput"] > div:focus-within {
    border-color: var(--accent2) !important;
    box-shadow: 0 0 0 3px rgba(59,130,246,0.12) !important;
}
[data-testid="stNumberInput"] input,
[data-testid="stTextInput"] input {
    background: transparent !important;
    color: var(--text) !important;
    font-family: var(--font-mono) !important;
    font-size: 0.9rem !important;
}
label, .stNumberInput label, [data-testid="stWidgetLabel"] {
    color: var(--muted) !important;
    font-family: var(--font-mono) !important;
    font-size: 0.78rem !important;
    letter-spacing: 0.04em !important;
}

/* ── Calculate button ── */
[data-testid="stButton"] > button {
    background: linear-gradient(135deg, var(--accent) 0%, #e8920f 100%) !important;
    color: #0b0f1a !important;
    font-family: var(--font-head) !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    letter-spacing: 0.04em !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.75rem 3rem !important;
    width: 100% !important;
    transition: opacity 0.2s, transform 0.15s !important;
    box-shadow: 0 4px 24px rgba(245,166,35,0.25) !important;
}
[data-testid="stButton"] > button:hover {
    opacity: 0.9 !important;
    transform: translateY(-1px) !important;
}

/* ── Result cards ── */
.result-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 1rem;
    margin: 1.5rem 0;
}
.result-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.2rem 1rem;
    text-align: center;
    position: relative;
    overflow: hidden;
}
.result-card.primary {
    border-color: var(--accent);
    background: linear-gradient(160deg, #1f1608 0%, var(--card) 60%);
}
.result-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: var(--border);
}
.result-card.primary::before { background: var(--accent); }
.result-label {
    font-family: var(--font-mono);
    font-size: 0.68rem;
    color: var(--muted);
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}
.result-value {
    font-family: var(--font-head);
    font-size: 1.6rem;
    font-weight: 800;
    color: var(--text);
    line-height: 1;
}
.result-card.primary .result-value { color: var(--accent); }
.result-unit {
    font-family: var(--font-mono);
    font-size: 0.72rem;
    color: var(--muted);
    margin-top: 0.3rem;
}

/* ── Steps ── */
.steps-box {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.5rem 1.8rem;
    margin-top: 1rem;
}
.step-row {
    display: flex;
    gap: 1rem;
    align-items: flex-start;
    padding: 0.6rem 0;
    border-bottom: 1px solid var(--border);
}
.step-row:last-child { border-bottom: none; }
.step-num {
    font-family: var(--font-head);
    font-size: 0.7rem;
    font-weight: 700;
    color: var(--accent);
    background: rgba(245,166,35,0.1);
    border-radius: 4px;
    padding: 2px 7px;
    white-space: nowrap;
    margin-top: 2px;
}
.step-text {
    font-family: var(--font-mono);
    font-size: 0.82rem;
    color: var(--muted);
    line-height: 1.7;
}
.step-text strong { color: var(--text); }

/* ── Info bar ── */
.info-bar {
    background: rgba(59,130,246,0.08);
    border: 1px solid rgba(59,130,246,0.25);
    border-radius: 8px;
    padding: 0.7rem 1.2rem;
    font-family: var(--font-mono);
    font-size: 0.78rem;
    color: #93c5fd;
    margin-top: 1rem;
}

/* ── Divider ── */
hr { border-color: var(--border) !important; margin: 1.5rem 0 !important; }

/* ── Column gap ── */
[data-testid="stHorizontalBlock"] { gap: 2rem !important; }

/* ── Streamlit success/info override (hide default) ── */
[data-testid="stAlert"] { display: none !important; }
</style>
""", unsafe_allow_html=True)

# ── Hero ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-title">⚡ Bifacial PV <span>Computation</span> Tool</div>
    <div class="hero-sub">Compute Pmax · Vmp · Imp · Voc · Isc — datasheet-based formulas</div>
</div>
""", unsafe_allow_html=True)

# ── INPUT LAYOUT ───────────────────────────────────────────────────────────────
col1, col2 = st.columns(2)

# ---------- LEFT ----------
with col1:
    st.markdown('<div class="section-label">🔆 Environmental Inputs</div>', unsafe_allow_html=True)
    G_front = st.number_input("Front Irradiance (W/m²)", value=800.0)
    BG      = st.number_input("Bifacial Gain (BG)", value=0.15)
    Tcell   = st.number_input("Cell Temperature (°C)", value=30.0)

    st.markdown('<div class="section-label">📦 Module Electrical Data at STC</div>', unsafe_allow_html=True)
    Pmax_stc = st.number_input("Pmax at STC (W)", value=450.0)
    Vmp_stc  = st.number_input("Vmp at STC (V)", value=41.0)
    Imp_stc  = st.number_input("Imp at STC (A)", value=10.98)
    Voc_stc  = st.number_input("Voc at STC (V)", value=49.5)
    Isc_stc  = st.number_input("Isc at STC (A)", value=11.5)

# ---------- RIGHT ----------
with col2:
    st.markdown('<div class="section-label">🌡 Temperature Coefficients</div>', unsafe_allow_html=True)
    alphasc = st.number_input("α (Isc coeff, %/°C)", value=0.040, format="%.3f")
    betaoc  = st.number_input("β (Voc coeff, %/°C)", value=-0.280, format="%.3f")
    alphamp = st.number_input("α (Imp coeff, %/°C)", value=0.040, format="%.3f")
    betamp  = st.number_input("β (Vmp coeff, %/°C)", value=-0.280, format="%.3f")
    gamma   = st.number_input("γ (Pmax coeff, %/°C)", value=-0.350, format="%.3f")

    st.markdown('<div class="section-label">⚙ Loss & Correction Factors</div>', unsafe_allow_html=True)
    dirt   = st.number_input("Dirt Level (%) [Range: 0 – 20%]", min_value=0.0, max_value=20.0, value=5.0)
    years  = st.number_input("Module Age (years) [Range: 0 – 25 years]", min_value=0, max_value=25, value=10, step=1)
    Fmm    = st.number_input("Mismatch Factor (Fmm) [Range: 0.95 – 1.0]", min_value=0.95, max_value=1.0, value=0.98)
    Fshade = st.number_input("Shading Factor (Fshade) [Range: 0.7 – 1.0]", min_value=0.7, max_value=1.0, value=0.95)

st.markdown("<br>", unsafe_allow_html=True)

# ── CALCULATE BUTTON ───────────────────────────────────────────────────────────
calc = st.button("⚡ Calculate Outputs")

if calc:

    # ── Rear & total irradiance ──
    G_rear  = BG * G_front
    G_total = G_front + G_rear

    # ── Irradiance factor ──
    Fg = G_front / 1000

    # ── Cleaning factor ──
    Fclean = (100 - dirt) / 100

    # ── Fage logic ──
    if years <= 0:
        Fage = 1.0
    else:
        Fage = 1 - 0.015 - 0.005 * (years - 1)

    # ── Temperature factors (fallback rules) ──
    if alphamp == 0:
        alphamp = alphasc
    if betamp == 0:
        betamp = gamma

    Ftemp_Isc = 1 + (alphasc / 100) * (Tcell - 25)
    Ftemp_Imp = 1 + (alphamp / 100) * (Tcell - 25)
    Ftemp_Voc = 1 + (betaoc  / 100) * (Tcell - 25)
    Ftemp_Vmp = 1 + (betamp  / 100) * (Tcell - 25)
    Ftemp_Pmp = 1 + (gamma   / 100) * (Tcell - 25)

    # ── Electrical outputs ──
    Isc  = Isc_stc  * Ftemp_Isc * Fg * Fclean * Fshade
    Imp  = Imp_stc  * Ftemp_Imp * Fg * Fclean * Fshade
    Voc  = Voc_stc  * Ftemp_Voc
    Vmp  = Vmp_stc  * Ftemp_Vmp
    Pmax = Pmax_stc * Ftemp_Pmp * Fg * Fclean * Fshade * Fmm * Fage

    # ── Save for ABC ──
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

    # ── OUTPUT ─────────────────────────────────────────────────────────────────
    st.markdown('<div class="section-label">📊 Calculated Electrical Outputs — Module Level</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="result-grid">
        <div class="result-card primary">
            <div class="result-label">Maximum Power Output</div>
            <div class="result-value">{Pmax:.2f}</div>
            <div class="result-unit">Pmax · W</div>
        </div>
        <div class="result-card">
            <div class="result-label">Voltage at Max Power</div>
            <div class="result-value">{Vmp:.2f}</div>
            <div class="result-unit">Vmp · V</div>
        </div>
        <div class="result-card">
            <div class="result-label">Current at Max Power</div>
            <div class="result-value">{Imp:.2f}</div>
            <div class="result-unit">Imp · A</div>
        </div>
        <div class="result-card">
            <div class="result-label">Open Circuit Voltage</div>
            <div class="result-value">{Voc:.2f}</div>
            <div class="result-unit">Voc · V</div>
        </div>
        <div class="result-card">
            <div class="result-label">Short Circuit Current</div>
            <div class="result-value">{Isc:.2f}</div>
            <div class="result-unit">Isc · A</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Calculation Steps ───────────────────────────────────────────────────────
    st.markdown('<div class="section-label">🧮 Calculation Steps</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="steps-box">

        <div class="step-row">
            <span class="step-num">01</span>
            <div class="step-text">
                Rear irradiance = BG × G_front = {BG} × {G_front} = <strong>{G_rear:.2f} W/m²</strong>
            </div>
        </div>

        <div class="step-row">
            <span class="step-num">02</span>
            <div class="step-text">
                Total irradiance = G_front + G_rear = <strong>{G_total:.2f} W/m²</strong>
            </div>
        </div>

        <div class="step-row">
            <span class="step-num">03</span>
            <div class="step-text">
                Irradiance factor Fg = G_front / 1000 = {G_front} / 1000 = <strong>{Fg:.3f}</strong>
            </div>
        </div>

        <div class="step-row">
            <span class="step-num">04</span>
            <div class="step-text">
                Temperature factors:<br>
                · Ftemp,Isc = 1 + (α_Isc/100)(T−25) = <strong>{Ftemp_Isc:.3f}</strong><br>
                · Ftemp,Imp = 1 + (α_Imp/100)(T−25) = <strong>{Ftemp_Imp:.3f}</strong><br>
                · Ftemp,Voc = 1 + (β_Voc/100)(T−25) = <strong>{Ftemp_Voc:.3f}</strong><br>
                · Ftemp,Vmp = 1 + (β_Vmp/100)(T−25) = <strong>{Ftemp_Vmp:.3f}</strong><br>
                · Ftemp,Pmp = 1 + (γ/100)(T−25) = <strong>{Ftemp_Pmp:.3f}</strong>
            </div>
        </div>

        <div class="step-row">
            <span class="step-num">05</span>
            <div class="step-text">
                Cleaning factor Fclean = (100 − dirt)/100 = (100 − {dirt})/100 = <strong>{Fclean:.3f}</strong>
            </div>
        </div>

        <div class="step-row">
            <span class="step-num">06</span>
            <div class="step-text">
                Aging factor Fage — Year 1 degradation = 1.5%, subsequent years = 0.5%/year → <strong>Fage = {Fage:.3f}</strong>
            </div>
        </div>

        <div class="step-row">
            <span class="step-num">07</span>
            <div class="step-text">
                Isc = {Isc_stc:.3f} × {Ftemp_Isc:.3f} × {Fg:.3f} × {Fclean:.3f} × {Fshade:.3f} = <strong>{Isc:.2f} A</strong><br>
                Voc = {Voc_stc:.3f} × {Ftemp_Voc:.3f} = <strong>{Voc:.2f} V</strong><br>
                Vmp = {Vmp_stc:.3f} × {Ftemp_Vmp:.3f} = <strong>{Vmp:.2f} V</strong><br>
                Imp = {Imp_stc:.3f} × {Ftemp_Imp:.3f} × {Fg:.3f} × {Fclean:.3f} × {Fshade:.3f} = <strong>{Imp:.2f} A</strong><br>
                Pmax = {Pmax_stc:.1f} × {Ftemp_Pmp:.3f} × {Fg:.3f} × {Fclean:.3f} × {Fshade:.3f} × {Fmm:.3f} × {Fage:.3f} = <strong>{Pmax:.2f} W</strong>
            </div>
        </div>

    </div>

    <div class="info-bar">
        ℹ All calculations follow the datasheet-based PV computation formula at module level.
        Results saved to session — proceed to the ABC Optimizer page.
    </div>
    """, unsafe_allow_html=True)
