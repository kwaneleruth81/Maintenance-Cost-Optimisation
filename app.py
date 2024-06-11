import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set the title of the app
st.title('Reliability/Maintenance Cost Optimisation with Random Forest')

# Define the input parameters with initial dummy data
initial_data = {
    'Coal usage (tonnes)': 25068.23,
    'Diesel usage Litres': 6453.15,
    'Reliability %': 33.42,
}

# Sidebar for user input
st.sidebar.markdown(
    """
    <span style="color: red; font-weight: bold; font-size: 18px;">
        Senda-N0233522W
    </span>
    """,
    unsafe_allow_html=True
)
st.sidebar.header('Input Parameters')

# Display the input parameters in the sidebar and get user input
reliability = st.sidebar.slider('Reliability %', 0, 100, value=int(initial_data['Reliability %']))
st.markdown(
    """
    <style>
    div[data-baseweb="slider"] {
        background: #f0f0f5;  /* default background */
        border-radius: 3px;
        padding: 0.2rem 0.5rem;
    }
    div[data-baseweb="slider"] > div {
        background: transparent;
    }
    div[data-baseweb="slider"] .css-14el2xx {
        background: #E0E0E0;
    }
    div[data-baseweb="slider"] .css-1kw3swa.e1f86d0o4 {
        background: #C0C0C0;
    }
    div[data-baseweb="slider"] .css-1mga1tz.e1f86d0o3 {
        background: #f0f0f5;
    }
    div[data-baseweb="slider"] .css-2d917.e1f86d0o2 {
        background: #A0A0A0;
    }
    div[data-baseweb="slider"] .css-1ezy5yt.e1f86d0o1 {
        background: #808080;
    }
    div[data-baseweb="slider"] [role='slider'] {
        background: #ff4b4b; /* default thumb color for values 0-63 and 68-100 */
        width: 16px; /* default thumb width */
        height: 16px; /* default thumb height */
    }
    div[data-baseweb="slider"] [role='slider'][aria-valuenow="64"],
    div[data-baseweb="slider"] [role='slider'][aria-valuenow="65"],
    div[data-baseweb="slider"] [role='slider'][aria-valuenow="66"],
    div[data-baseweb="slider"] [role='slider'][aria-valuenow="67"] {
        background: green;
        width: 24px; /* increased thumb width */
        height: 24px; /* increased thumb height */
    }
    </style>
    """, unsafe_allow_html=True
)

# Display the value of the slider
st.write('Reliability:', reliability)

# Calculate other parameters based on Reliability %
plant_availability = (reliability / 100) * 0.88 * 100  # Assuming Plant Availability % is 88% of Reliability %

# Adjust Ave generation (MW), Electricity sent out (GWh), and MTBM (Hrs) when Reliability % is 66
if reliability == 66:
    ave_generation = 154.26
    electricity_sent_out = 43.7
    mtbm_hours = 300
    av_blr_efficiency = 62.0
else:
    ave_generation = (reliability / 100) * 0.75 * 200  # Assuming Ave generation (MW) is 75% of Reliability % times 200
    electricity_sent_out = (reliability / 100) * 0.80 * 50  # Assuming Electricity sent out (GWh) is 80% of Reliability % times 50
    av_blr_efficiency = (reliability / 100) * 0.70 * 100  # Assuming AV BLR efficiency % is 70% of Reliability %
    mtbm_hours = (reliability / 100) * 300  # Adjusted scaling for MTBM (Hrs)

# Calculate maintenance cost inversely proportional to Reliability %
maintenance_cost = 250000 - (reliability / 100) * (250000 - 150000)

# Calculate predicted number of boiler failures
boiler_failures = int((10 - 1) * (1 - reliability / 100) + 1)  # Linearly scales from 10 to 1

# Display the updated input parameters in the sidebar
st.sidebar.number_input('Plant Availability %', value=plant_availability)
st.sidebar.number_input('Ave generation (MW)', value=ave_generation)
st.sidebar.number_input('Electricity sent out (GWh)', value=electricity_sent_out)
st.sidebar.number_input('AV BLR efficiency %', value=av_blr_efficiency)
st.sidebar.number_input('MTBM (Hrs)', value=mtbm_hours)
st.sidebar.number_input('Coal usage (tonnes)', value=initial_data['Coal usage (tonnes)'], disabled=True)
st.sidebar.number_input('Diesel usage Litres', value=initial_data['Diesel usage Litres'], disabled=True)
st.sidebar.write('Ave SHtr Temp (Deg Celsius)', 525.12)
st.sidebar.write('Ave Steam Pressure (Mpa)', 15.87)

# Apply custom CSS for the slider color change and Reliability % font style
st.markdown(
    f"""
    <style>
        .stSlider > div:nth-child(3) > div > div > div {{
            background: {'#4CAF50' if reliability == 66 else '#FFFFFF'};
        }}
        .stSlider > div:nth-child(1) > div {{
            color: {'red' if reliability == 66 else 'black'};
            font-weight: {'bold' if reliability == 66 else 'normal'};
        }}
    </style>
    """,
    unsafe_allow_html=True
)

# Subheader for the predicted maintenance cost
st.subheader('Predicted Maintenance Cost')
st.markdown(
    f"""
    <div style="border:2px solid black; padding: 10px; background-color: #ffcccc; text-align: center;">
        <span style="color: red; font-weight: bold; font-size: 24px;">
            ${int(maintenance_cost)}
        </span>
    </div>
    """,
    unsafe_allow_html=True
)

# Subheader for the predicted number of boiler failures
st.subheader('Predicted Number of Boiler Failures')
st.markdown(
    f"""
    <div style="border:2px solid black; padding: 10px; background-color: #ccffcc; text-align: center;">
        <span style="color: green; font-weight: bold; font-size: 24px;">
            {boiler_failures}
        </span>
    </div>
    """,
    unsafe_allow_html=True
)

# Feature importances (dummy data)
feature_importances = {
    'Reliability %': 0.30,
    'Plant Availability %': 0.30,
    'Electricity sent out (GWh)': 0.15,
    'Ave generation (MW)': 0.15,
    'AV BLR efficiency %': 0.10,
    'MTBM (Hrs)': 0.05,
    'Coal usage (tonnes)': 0.03,
    'Diesel usage Litres': 0.02,
    'Ave SHtr Temp (Deg Celsius)': 0.02,
    'Ave Steam Pressure (Mpa)': 0.01,
}
# Plotting the feature importances
st.subheader('Important Features')
fig, ax = plt.subplots()
sns.barplot(x=list(feature_importances.values()), y=list(feature_importances.keys()), ax=ax)
ax.set_xlabel('Importance')
ax.set_ylabel('Feature')
st.pyplot(fig)
