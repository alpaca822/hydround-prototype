import streamlit as st
import random

st.set_page_config(page_title="Hydround Groundwater Detection Prototype", layout="wide")

st.title("🌊 Hydround Groundwater Detection Prototype 🌊")
st.write(
    "Select the number of Hydround chips used in your agriculture. "
    "We will run scans to check groundwater presence and contamination risk for each chip."
)

# User input: number of chips
num_chips = st.number_input("Number of Hydround chips:", min_value=1, max_value=20, value=4, step=1)

st.write("---")

# Function to simulate sensor readings for a single chip
def simulate_chip_readings():
    moisture = random.uniform(0, 100)      # Soil moisture %
    temp = random.uniform(10, 35)          # Temperature °C
    vibration = random.uniform(0, 5)       # Vibration level
    sound = random.uniform(20, 100)        # Ambient sound dB
    nitrate = random.uniform(0, 50)        # Nitrate ppm

    # Groundwater presence logic
    groundwater = moisture > 60 and 10 < temp < 30 and vibration < 3 and sound < 80

    # Contamination risk as percentage (scaled nitrate level, max 100%)
    contamination_risk_pct = min(100, nitrate * 2)

    return {
        "moisture": moisture,
        "temp": temp,
        "vibration": vibration,
        "sound": sound,
        "nitrate": nitrate,
        "groundwater": groundwater,
        "contamination_risk_pct": contamination_risk_pct,
    }

# Simulate readings for all chips
chip_results = [simulate_chip_readings() for _ in range(num_chips)]

# Display results for each chip
st.subheader("Per-Chip Sensor Readings and Analysis")
for idx, chip in enumerate(chip_results, start=1):
    st.markdown(f"### Chip {idx}")
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"- **Soil Moisture:** {chip['moisture']:.1f}%")
        st.write(f"- **Temperature:** {chip['temp']:.1f} °C")
        st.write(f"- **Vibration Level:** {chip['vibration']:.1f}")
    with col2:
        st.write(f"- **Ambient Sound:** {chip['sound']:.1f} dB")
        st.write(f"- **Nitrate Level:** {chip['nitrate']:.1f} ppm")
        st.write(f"- **Groundwater Present:** {'✅ Yes' if chip['groundwater'] else '❌ No'}")
        st.write(f"- **Contamination Risk:** {chip['contamination_risk_pct']:.0f}%")
    st.markdown("---")

# Calculate overall summary
overall_groundwater = any(chip['groundwater'] for chip in chip_results)
average_contamination = sum(chip['contamination_risk_pct'] for chip in chip_results) / num_chips

st.subheader("Overall Farmland Summary")
st.write(f"**Groundwater Present Across Farmland:** {'✅ Yes' if overall_groundwater else '❌ No'}")
st.write(f"**Average Contamination Risk:** {average_contamination:.0f}%")

st.write("---")

# Visualization grid for groundwater presence & contamination risk per chip
st.subheader("Groundwater Presence Map")

cols = st.columns(num_chips)

for i, chip in enumerate(chip_results):
    color = "#1E90FF" if chip['groundwater'] else "#A0522D"  # DodgerBlue or Sienna (brown)
    cols[i].markdown(
        f"""
        <div style="
            background-color: {color};
            padding: 20px 0;
            border-radius: 8px;
            text-align: center;
            font-weight: bold;
            color: white;
            user-select: none;
            ">
            Chip {i+1}<br>
            {chip['contamination_risk_pct']:.0f}% contamination
        </div>
        """,
        unsafe_allow_html=True,
    )

st.write("___")
st.write("This prototype simulates Hydround chip sensor data and visualizes groundwater and contamination risk across your field.")

