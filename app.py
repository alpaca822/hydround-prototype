import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import random

st.set_page_config(page_title="Hydround Groundwater Detection Prototype")

st.title("Hydround Groundwater Detection Prototype")
st.write(
    "Select the number of Hydround chips used on your farmland, then click **Submit** to run the scan and check groundwater presence and contamination risk."
)

# -- Sensor simulation functions --

def simulate_sensors():
    moisture = random.uniform(0, 100)
    temp = random.uniform(10, 35)
    vibration = random.uniform(0, 5)
    sound = random.uniform(20, 100)
    nitrate = random.uniform(0, 50)
    return moisture, temp, vibration, sound, nitrate

def analyze_groundwater(moisture, temp, vibration, sound, nitrate):
    groundwater_present = moisture > 60 and 10 < temp < 30 and vibration < 3 and sound < 80
    contamination_risk_percent = min(max((nitrate / 50) * 100, 0), 100)
    if not groundwater_present:
        contamination_risk_percent = 0
    return groundwater_present, contamination_risk_percent

# -- Form to select number of Hydround chips --

with st.form(key="chips_form"):
    num_chips = st.slider("Number of Hydround chips:", min_value=1, max_value=20, value=4)
    submit_button = st.form_submit_button(label="Submit")

if submit_button:
    # Simulate and analyze each chip
    chip_results = []
    for _ in range(num_chips):
        sensors = simulate_sensors()
        groundwater, contamination = analyze_groundwater(*sensors)
        chip_results.append({
            "groundwater": groundwater,
            "contamination": contamination,
            "sensors": sensors,
        })

    # Calculate overall results
    overall_groundwater = any(chip["groundwater"] for chip in chip_results)
    if overall_groundwater:
        contamination_values = [
            chip["contamination"] for chip in chip_results if chip["groundwater"]
        ]
        overall_contamination = sum(contamination_values) / len(contamination_values)
    else:
        overall_contamination = 0.0

    st.markdown(f"### Overall Groundwater Present: {'✅ Yes' if overall_groundwater else '❌ No'}")
    st.markdown(f"### Overall Contamination Risk: {overall_contamination:.2f}%")

    # Display individual Hydround chip results
    st.write("### Individual Hydround Chip Sensor Results:")
    for idx, chip in enumerate(chip_results, start=1):
        soil_moisture, temp, vibration, sound, nitrate = chip["sensors"]
        st.markdown(f"**Hydround Chip #{idx}:**")
        st.write(
            f"- Soil Moisture: {soil_moisture:.1f} %\n"
            f"- Temperature: {temp:.1f} °C\n"
            f"- Vibration Level: {vibration:.2f}\n"
            f"- Ambient Sound: {sound:.1f} dB\n"
            f"- Nitrate Level: {nitrate:.1f} ppm\n"
            f"- Groundwater Present: {'Yes' if chip['groundwater'] else 'No'}\n"
            f"- Contamination Risk: {chip['contamination']:.2f}%\n"
        )

    # Visual groundwater presence map with black grid lines
    rows = 2
    cols = (num_chips + 1) // 2

    fig, ax = plt.subplots(figsize=(cols * 1.5, rows))
    for i, chip in enumerate(chip_results):
        row = i // cols
        col = i % cols
        color = "blue" if chip["groundwater"] else "saddlebrown"
        rect = plt.Rectangle(
            (col, rows - row - 1),
            1,
            1,
            facecolor=color,
            edgecolor="black",  # <-- Add grid line border
            linewidth=1
        )
        ax.add_patch(rect)

        if chip["groundwater"]:
            contamination_pct = chip["contamination"]
            ax.text(
                col + 0.5,
                rows - row - 0.5,
                f"{contamination_pct:.1f}%",
                color="white",
                ha="center",
                va="center",
                fontsize=12,
                weight='bold',
            )

    ax.set_xlim(0, cols)
    ax.set_ylim(0, rows)
    ax.set_aspect('equal')
    ax.axis("off")
    st.pyplot(fig)

else:
    st.info("Waiting for you to select the number of Hydround chips and submit.")


