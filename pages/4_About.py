import streamlit as st

st.set_page_config(page_title="Project Info", layout="centered")

st.markdown("""
<style>
.stApp {
    background-color: #0f1117;
}

.chip-row {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-bottom: 1.5rem;
}

.chip {
    background: #1c2128;
    border: 1px solid #30363d;
    border-radius: 6px;
    padding: 6px 14px;
    font-size: 0.8rem;
    color: #79c0ff;
}

.goal-box {
    background: #1a1f16;
    border: 1px solid #3d4a1e;
    border-radius: 10px;
    padding: 1.2rem 1.5rem;
    margin: 1.5rem 0;
    line-height: 1.7;
}

.footer-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 2rem;
    padding-top: 1.2rem;
    border-top: 1px solid #21262d;
    color: #8b949e;
    font-size: 0.82rem;
}

.tag {
    font-size: 0.7rem;
    color: #388bfd;
    background: #112240;
    border: 1px solid #1f6feb;
    padding: 3px 10px;
    border-radius: 4px;
}
</style>
""", unsafe_allow_html=True)

# Title — uses Streamlit's native st.title so font/size is identical to your ABC page
st.title("📘 Output Power Optimization of Bifacial Photovoltaic Module")
st.markdown("Using Artificial Bee Colony (ABC) Algorithm")
st.divider()

# About
st.subheader("About this project")
st.markdown(
    "This project integrates bifacial PV output modeling, environmental correction factors, "
    "and AI-based optimization using the ABC algorithm. It features real-time results "
    "visualization built on a multi-page Streamlit architecture."
)

# Chips
st.subheader("Core components")
st.markdown("""
<div class="chip-row">
    <div class="chip">☀️ Bifacial PV Modeling</div>
    <div class="chip">🌍 Environmental Correction</div>
    <div class="chip">🧠 ABC Optimization</div>
    <div class="chip">📊 Real-time Visualization</div>
    <div class="chip">📄 Multi-page Architecture</div>
</div>
""", unsafe_allow_html=True)

# Objective box
st.subheader("Objective")
st.markdown("""
<div class="goal-box">
    🎯 Reduce the error between <strong>calculated output</strong> and <strong>measured field data</strong>,
    improving prediction accuracy of bifacial PV systems using intelligent optimization.
</div>
""", unsafe_allow_html=True)

st.divider()

# Footer
st.markdown("""
<div class="footer-row">
    <span>Developed by <strong style="color:#e6edf3;">Arief Shah</strong></span>
    <span class="tag">FYP / Research</span>
</div>
""", unsafe_allow_html=True)
