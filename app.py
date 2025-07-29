import streamlit as st
import random
import matplotlib.pyplot as plt
import numpy as np

# Sensor simulation
def get_soil_moisture():
    return random.uniform(0, 100)

def get_temperature():
    return random.uniform(10, 35)

def get_vibration():
    return random.uniform(0, 5)

def get_sound():
    return random.uniform(20, 100)

def get_nitrate_level():
    return random.uniform(0, 50)

# Analysis
def analyze_groundwater(moisture, temp, vibration, sound):
    return moisture > 60 and 10 < temp < 30 and vibration < 3 and sound < 80

def contamination_risk(nitrate):
    # Assume anything >10 ppm increases risk
    return min(100, (nitrate / 50) * 100)  # Scale from 0–100%

def estimate_depth(moisture, vibration):
    if moisture > 70 and vibration < 1:
        return 2
    elif moisture > 50:
        return 5
    elif moisture > 30:
        return 10
    else:
        return None

# UI Starts Here
st.title("💧 Hydround Groundwater Detection Prototype")

num_sensors = st.slider("Select number of sensors", 1, 16, 4)
scan_now = st.button("Run Scan")

if scan_now:
    st.subheader("🔎 Sensor Scan Results")
    cols = int(np.sqrt(num_sensors))
    rows = int(np.ceil(num_sensors / cols))

    fig, ax = plt.subplots()
    groundwater_map = np.zeros((rows, cols))
    contamination_map = np.zeros((rows, cols))

    scan_data = []

    for i in range(num_sensors):
        row = i // cols
        col = i % cols

        # Simulate
        moisture = get_soil_moisture()
        temp = get_temperature()
        vibration = get_vibration()
        sound = get_sound()
        nitrate = get_nitrate_level()

        # Analyze
        has_water = analyze_groundwater(moisture, temp, vibration, sound)
        contamination_pct = contamination_risk(nitrate)
        depth = estimate_depth(moisture, vibration)

        groundwater_map[row][col] = 1 if has_water else 0
        contamination_map[row][col] = contamination_pct

        scan_data.append({
            "Sensor": f"S{i+1}",
            "Groundwater": "Yes" if has_water else "No",
            "Contamination Risk (%)": round(contamination_pct, 1),
            "Estimated Depth (m)": depth if depth else "Not detected"
        })

    # Display Table
    st.table(scan_data)

    # Visualize field
    st.subheader("🗺️ Groundwater Map (Green = Water, Red = Dry)")
    colors = np.where(groundwater_map == 1, 'green', 'red')

    for i in range(rows):
        for j in range(cols):
            ax.add_patch(plt.Rectangle((j, -i), 1, 1, color=colors[i][j]))
            label = f"{int(contamination_map[i][j])}%"
            ax.text(j + 0.5, -i + 0.5, label, ha='center', va='center', color='white')

    ax.set_xlim(0, cols)
    ax.set_ylim(-rows, 0)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_aspect('equal')
    st.pyplot(fig)

    st.success("Scan completed.")
