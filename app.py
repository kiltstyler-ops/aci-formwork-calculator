import streamlit as st
import math

# --- App Styling ---
st.set_page_config(page_title="ACI Formwork Solver", layout="wide")
st.title("🏗️ ACI 347 Formwork Design Suite")
st.markdown("Professional-grade concrete pressure and BOM generator.")

# --- Sidebar Inputs ---
st.sidebar.header("Jobsite Conditions")
wall_h = st.sidebar.number_input("Wall Height (ft)", value=12.0)
wall_l = st.sidebar.number_input("Wall Length (ft)", value=50.0)
rate = st.sidebar.slider("Pour Rate (ft/hr)", 1.0, 15.0, 5.0)
temp = st.sidebar.slider("Concrete Temp (F)", 40, 100, 70)

st.sidebar.header("Engineering Settings")
sf = st.sidebar.selectbox("Safety Factor", [2.0, 2.5, 3.0, 4.0])
tie_type = st.sidebar.selectbox("Tie Type", ["Snap-Tie (3k)", "She-Bolt (5k)", "Taper-Tie (7.5k)"])

# --- Logic Processing ---
# ACI Pressure Calculation
p_max = min(150 * wall_h, (150 + 9000 * rate / temp))
p_max = max(p_max, 600)

# Hardware Capacity Mapping
caps = {"Snap-Tie (3k)": 4500, "She-Bolt (5k)": 9000, "Taper-Tie (7.5k)": 15000}
swl = caps[tie_type] / sf
max_tie_spacing = math.sqrt(swl / p_max) * 12

# --- Main Display ---
col1, col2 = st.columns(2)

with col1:
    st.metric("Design Pressure", f"{round(p_max, 0)} PSF")
    st.write(f"**Governing Tie Spacing:** {round(max_tie_spacing, 1)} inches O.C.")
    st.info("Calculation based on ACI 347-14 Equation 4.2/4.3")

with col2:
    st.subheader("Bill of Materials")
    plywood = math.ceil((wall_h * wall_l * 2) / 32)
    st.write(f"📦 **Plywood (4x8):** {plywood} sheets")
    st.write(f"🔗 **Ties Required:** {math.ceil((wall_l*12/max_tie_spacing)*(wall_h*12/max_tie_spacing))} pcs")

# Data Table Preview
st.divider()
st.subheader("Structural Reference Table")
st.table({"Variable": ["Pressure", "Safety Factor", "Allowable Load"], 
          "Value": [f"{p_max} psf", sf, f"{swl} lbs"]})
