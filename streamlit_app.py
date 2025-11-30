import streamlit as st
import pandas as pd
import os # Needed to talk to the file system

st.title("Patient Intake System")

with st.form("intake_form"):
    st.subheader("New Patient Entry")
    
    # 1. Demographics
    name = st.text_input("Patient Name")
    age = st.number_input("Age", min_value=0, max_value=120)
    weight = st.number_input("Enter your Weight in Kg")
    height = st.number_input("Enter Your height in Cm")
    height = height / 100  
    bms = st.form_submit_button("Get BMI")
    if height <= 0:
        st.error("Height must be greater than zero.")
    else:
        bmi = weight / (height ** 2)
        bmi = int(bmi)
        obesity = False
        bms = bmi 
        if bms > 30:
            st.warning("Patient is in obesity range")
        else:
            st.success("Patient is not suffered from Obesity")
            obesity = True
    
    
    # 2. Clinical Data
    blood_type = st.selectbox("Blood Type", ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
    is_smoker = st.checkbox("History of Smoking?")
    
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    # 3. The Submit Button
    submitted = st.form_submit_button("Save to Database")

if submitted:
    # Create a dictionary of the new data
    new_data = {
        "Name": name,
        "Age": age,
        "Blood Type": blood_type,
        "Smoker": is_smoker,
        "Obesity": obesity
    }
    
    # Convert to a Pandas DataFrame (A single row table)
    df = pd.DataFrame([new_data])
    
    # Save to CSV
    # If file doesn't exist, create it. If it does, append without header.
    file_path = "patient_database.csv"
    
    if not os.path.exists(file_path):
        df.to_csv(file_path, index=False)
    else:
        df.to_csv(file_path, mode='a', header=False, index=False)
        
    st.success(f"Patient {name} added successfully!")

st.divider() # Adds a visual line
st.subheader("Upload Lab Results")

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # 1. Create a folder called 'lab_results' if it doesn't exist
    save_folder = "lab_results"
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)
        
    # 2. Save the file to that folder
    save_path = os.path.join(save_folder, uploaded_file.name)
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
        
    st.success(f"File saved successfully to: {save_path}")

    # 3. Display Preview
    lab_data = pd.read_csv(save_path)
    st.dataframe(lab_data)


import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.title("Clinical Analytics Dashboard")

file_path = "patient_database.csv"

if os.path.exists(file_path):
    df = pd.read_csv(file_path)
    
    # TABS: Clean way to organize dashboards
    tab1, tab2 = st.tabs(["Population Stats", "Raw Data"])
    
    with tab1:
        st.subheader("Patient Demographics")
        
        # BAR CHART: Blood Types
        fig_blood = px.bar(df, x="Blood Type", title="Distribution of Blood Types", color="Blood Type")
        st.plotly_chart(fig_blood)
        
        # SCATTER PLOT: Age Analysis
        # We are creating a jitter plot to see age distribution
        fig_age = px.histogram(df, x="Age", nbins=10, title="Patient Age Distribution")
        st.plotly_chart(fig_age)

    with tab2:
        st.dataframe(df)
        
else:
    st.warning("No patient data found. Please go to the Intake Form and add patients!")


st.divider()
st.header("Global Health Research Data")

# Load data directly from a public URL
url = "https://raw.githubusercontent.com/plotly/datasets/master/diabetes.csv"
public_data = pd.read_csv(url)

st.write("Connected to Public Diabetes Database via Cloud URL")

# Interactive Toggle
show_correlations = st.toggle("Show Correlation Heatmap")

if show_correlations:
    # Simple Scatter Matrix to show relationships
    fig = px.scatter_matrix(
        public_data, 
        dimensions=["Glucose", "BloodPressure", "BMI", "Age"],
        color="Outcome",
        title="Diabetes Risk Factors"
    )
    st.plotly_chart(fig)

        