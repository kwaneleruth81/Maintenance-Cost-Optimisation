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

# Calculate other parameters based on Reliability %
plant_availability = (reliability / 100) * 0.88 * 100  # Assuming Plant Availability % is 88% of Reliability %
ave_generation = (reliability / 100) * 0.75 * 200  # Assuming Ave generation (MW) is 75% of Reliability % times 200
electricity_sent_out = (reliability / 100) * 0.80 * 50  # Assuming Electricity sent out (GWh) is 80% of Reliability % times 50

# Set AV BLR efficiency % and MTBM (Hrs) based on Reliability %
if reliability == 66:
    av_blr_efficiency = 62.0
    mtbm_hours = 200
else:
    av_blr_efficiency = (reliability / 100) * 0.70 * 100  # Assuming AV BLR efficiency % is 70% of Reliability %
    mtbm_hours = (reliability / 100) * 200  # Adjusted scaling for MTBM (Hrs)

# Calculate maintenance cost inversely proportional to Reliability %
maintenance_cost = 250000 - (reliability / 100) * (250000 - 150000)

# Calculate predicted number of boiler failures
boiler_failures = int((10 - 1) * (1 - reliability / 100) + 1)  # Linearly scales from 10 to 1

# Display the updated input parameters in the sidebar
st.sidebar.number_input('Plant Availability %', value=plant_availability, disabled=True)
st.sidebar.number_input('Ave generation (MW)', value=ave_generation, disabled=True)
st.sidebar.number_input('Electricity sent out (GWh)', value=electricity_sent_out, disabled=True)
st.sidebar.number_input('AV BLR efficiency %', value=av_blr_efficiency, disabled=True)
st.sidebar.number_input('MTBM (Hrs)', value=mtbm_hours, disabled=True)
st.sidebar.number_input('Coal usage (tonnes)', value=initial_data['Coal usage (tonnes)'])
st.sidebar.number_input('Diesel usage Litres', value=initial_data['Diesel usage Litres'])
st.sidebar.write('Ave SHtr Temp (Deg Celsius)', 525.12)
st.sidebar.write('Ave Steam Pressure (Mpa)', 15.87)

# Display the slider with color change at 66%
slider_color = '#4CAF50' if reliability == 66 else '#FFFFFF'
st.markdown(
    f"""
    <style>
        .stSlider > div:nth-child(3) > div > div > div {{
            background: {slider_color};
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
