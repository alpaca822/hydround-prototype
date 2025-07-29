import streamlit as st
import random
import time

# --- Sensor Reading Simulations ---
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

# --- Analyze Sensor Data ---
def analyze_groundwater(moisture, temp, vibration, sound, nitrate):
    groundwater = moisture > 60 and 10 < temp < 30 and vibration < 3 and sound < 80
    contamination_risk = nitrate > 10

    if groundwater and not contamination_risk:
        conclusion = "✅ Groundwater detected and safe for use."
    elif groundwater and contamination_risk:
        conclusion = "⚠️ Groundwater detected but contamination risk present!"
    elif not groundwater and contamination_risk:
        conclusion = "❌ No groundwater detected and contamination risk present."
    else:
        conclusion = "❌ No groundwater detected."

    return groundwater, contamination_risk, conclusion

# --- Estimate groundwater depth ---
def estimate_depth(moisture, vibration):
    if moisture > 70 and vibration < 1:
        return 2
    elif moisture > 50:
        return 5
    elif moisture > 30:
        return 10
    else:
        return None

# --- Display results for one scan ---
def display_results(i, moisture, temp, vibration, sound, nitrate, groundwater, contamination, conclusion, depth):
    st.markdown(f"### 🔎 Hydround Scan #{i}")
    st.write(f"- **Soil Moisture:** {moisture:.2f}%")
    st.write(f"- **Temperature:** {temp:.2f} °C")
    st.write(f"- **Vibration Level:** {vibration:.2f}")
    st.write(f"- **Ambient Sound:** {sound:.2f} dB")
    st.write(f"- **Nitrate Level:** {nitrate:.2f} ppm")
    if depth:
        st.write(f"- **Estimated Groundwater Depth:** {depth} meters")
    else:
        st.write(f"- **Estimated Groundwater Depth:** Not detected")
    st.write(f"- **Groundwater Present:** {'Yes' if groundwater else 'No'}")
    st.write(f"- **Contamination Risk:** {'Yes' if contamination else 'No'}")
    st.markdown(f"**📝 Conclusion:** {conclusion}")
    st.markdown("---")

# --- Streamlit App ---
def main():
    st.title("🌊 Hydround Groundwater Detection Prototype")

    st.write("""
    This app simulates Hydround’s groundwater sensor readings and AI-powered analysis.
    Use the button below to run simulated scans and get real-time groundwater status.
    """)

    num_scans = st.slider("Number of scans to run", min_value=1, max_value=10, value=3)

    if st.button("Run Hydround Scan"):
        for i in range(1, num_scans + 1):
            moisture = get_soil_moisture()
            temp = get_temperature()
            vibration = get_vibration()
            sound = get_sound()
            nitrate = get_nitrate_level()

            groundwater, contamination, conclusion = analyze_groundwater(moisture, temp, vibration, sound, nitrate)
            depth = estimate_depth(moisture, vibration)

            display_results(i, moisture, temp, vibration, sound, nitrate, groundwater, contamination, conclusion, depth)
            
            if i != num_scans:
                time.sleep(1)  # pause 1 sec between scans for effect

if __name__ == "__main__":
    main()
