import streamlit as st

st.set_page_config(
    page_title="Bifacial PV Optimization System",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🔆 Bifacial PV Output Optimization System")
st.markdown("---")

st.markdown("""
Welcome to the **Bifacial Photovoltaic Output Optimization System**.  
Navigate using the sidebar to access different system modules:

### 📌 System Modules:
- **PV Output Calculator**  
  Compute power output using irradiance, temperature, and bifacial correction factors.

- **ABC Optimization**  
  Apply Artificial Bee Colony (ABC) algorithm to reduce calculation error and match measured power.

- **Results & Graphs**  
  Compare measured vs calculated vs optimized results, including error graphs.

- **About / Documentation**  
  Learn about the algorithm, formulas, methodology, and project summary.

---

This system is developed for academic research related to:
- Bifacial PV performance modeling  
- AI-based parameter tuning  
- PV output error minimization  

Use the sidebar to begin.
""")





