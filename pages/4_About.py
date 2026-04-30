import streamlit as st

st.set_page_config(page_title="Project Info", layout="centered")

st.markdown("""
<style>
/* Match the dark theme */
.stApp {
    background-color: #0f1117;
    color: #e6edf3;
}

.badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: #1c2a1c;
    color: #56d364;
    font-size: 11px;
    padding: 4px 12px;
    border-radius: 20px;
    border: 1px solid #238636;
    margin-bottom: 1.2rem;
}

.section-label {
    font-size: 0.7rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #8b949e;
    margin-bottom: 0.75rem;
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
    color: #c9d1d9;
    font-size: 0.9rem;
    line-height: 1.7;
}

.goal-box strong {
    color: #c9d645;
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

/* Streamlit default text color fix for dark bg */
p, li, label {
    color: #c9d1d9 !important;
}

h1, h2, h3 {
    color: #e6edf3 !important;
}
</style>
""", unsafe_allow_html=True)

# Badge
st.markdown('<div class="badge">🟢 Research Project</div>', unsafe_allow_html=True)

# Title
st.title("📘 Output Power Optimization of Bifacial Photovoltaic Module")
st.markdown('<p style="color:#8b949e; font-size:0.9rem;">Using Artificial Bee Colony (ABC) Algorithm</p>', unsafe_allow_html=True)
st.divider()

# About
st.markdown('<div class="section-label">About this project</div>', unsafe_allow_html=True)
st.markdown("""
<p style="color:#c9d1d9; font-size:0.95rem; line-height:1.8;">
This project integrates bifacial PV output modeling, environmental correction factors, and AI-based
optimization using the ABC algorithm. It features real-time results visualization built on a
multi-page Streamlit architecture.
</p>
""", unsafe_allow_html=True)

# Chips
st.markdown('<div class="section-label">Core components</div>', unsafe_allow_html=True)
st.markdown("""
<div class="chip-row">
    <div class="chip">☀️ Bifacial PV Modeling</div>
    <div class="chip">🌍 Environmental Correction</div>
    <div class="chip">🧠 ABC Optimization</div>
    <div class="chip">📊 Real-time Visualization</div>
    <div class="chip">📄 Multi-page Architecture</div>
</div>
""", unsafe_allow_html=True)

# Goal box — styled like the warning box in the screenshot
st.markdown("""
<div class="goal-box">
    <div class="section-label" style="color:#a8b820; margin-bottom:0.5rem;">🎯 Objective</div>
    Reduce the error between <strong>calculated output</strong> and <strong>measured field data</strong>,
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
