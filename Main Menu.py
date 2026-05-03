import streamlit as st

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="Bifacial PV Optimization System",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------ CUSTOM STYLE ------------------
st.markdown("""
<style>
.main {
    background-color: #0e1117;
}

h1, h2, h3 {
    color: #00d4ff;
}

.section-card {
    background-color: #161b22;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.3);
    margin-bottom: 15px;
}

.small-text {
    color: #9aa4b2;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)

# ------------------ HEADER ------------------
st.markdown("<h1 style='text-align: center;'>🔆 Bifacial PV Output Optimization System</h1>", unsafe_allow_html=True)
st.markdown("<p class='small-text' style='text-align: center;'>AI-Based Solar Performance Modeling & Optimization</p>", unsafe_allow_html=True)

st.markdown("---")

# ------------------ INTRO ------------------
st.markdown("""
<div class='section-card'>
This system is designed to analyze and optimize bifacial photovoltaic (PV) module performance  
using both physical modeling and AI-based optimization (Artificial Bee Colony algorithm).
</div>
""", unsafe_allow_html=True)

# ------------------ MODULES ------------------
st.subheader("📌 System Modules")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class='section-card'>
    <h3>🔋 Computational Tool</h3>
    <p class='small-text'>
    Compute electrical outputs (Pmax, Vmp, Imp, Voc, Isc) based on irradiance,
    temperature, and bifacial gain factors.
    </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='section-card'>
    <h3>🐝 ABC Optimization</h3>
    <p class='small-text'>
    Apply Artificial Bee Colony (ABC) algorithm to optimize parameters and reduce
    error between calculated and measured PV output.
    </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class='section-card'>
    <h3>📊 Results & Graphs</h3>
    <p class='small-text'>
    Visual comparison of calculated, measured, and optimized results including
    error convergence plots.
    </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='section-card'>
    <h3>📘 Documentation</h3>
    <p class='small-text'>
    Detailed explanation of formulas, methodology, and system architecture
    for academic and research purposes.
    </p>
    </div>
    """, unsafe_allow_html=True)

# ------------------ FOOTER ------------------
st.markdown("---")

st.markdown("""
<div style='text-align: center;' class='small-text'>
Developed for Final Year Project (FYP) • Electrical Engineering  
Focus: PV Modeling • Optimization • AI Integration
</div>
""", unsafe_allow_html=True)





