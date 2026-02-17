
# STREAMLIT APP: TANZANIA TOURISM EXPENDITURE PREDICTION
# To run this: streamlit run tourism.py

import streamlit as st
import pandas as pd
import pickle
import numpy as np

# Set page configuration
st.set_page_config(
    page_title="Tourism Expenditure Prediction",
    layout="centered")

# --- ADVANCED MODERN STYLING ---
st.markdown("""
    <style>
    .stApp {
        background-color: #FFF5E1; /* Light cream background */

    }
    
    /* Main Card */
    .main-card {
        background: black;
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0px 5px 20px rgba(0,0,0,0.08);
    }

    /* Main Title */
   h-1 {
    text-align: center;
    font-weight: 798;
    background-color: #FF6C00; /* Dark Orange */
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
/* Sidebar */
section[data-testid="stSidebar"] {
   background-color: grey;
    padding: 15px;
}
/* Sidebar custom title */
.sidebar-title {
    font-size: 22px;
    font-weight: bold;
    margin-bottom: 10px;
    color: black;
}


/* Sidebar text */
.sidebar-text {
    font-size: 15px;
    line-height: 1.6;
    margin-bottom: 20px;
    color: black;
}


.sidebar-section-title {
    font-size: 16px;
    font-weight: bold;
    margin-top: 20px;
    margin-bottom: 8px;
    color: black;
}

    .stButton > button {
        background-color: #FF8C00; /* Dark Orange */

        color: black;
        font-weight: bold;
        border-radius: 5px;
        transition: 0.2s ease-in-out;
        width: 100%;
    }
         
    .stButton > button:hover {
        background-color: red;
        transform: scale(1.05); /* Slight pop effect */
        color: black;
        
    }
    </style>
    """, unsafe_allow_html=True)

# --- NAVIGATION MENU (OPTIONS) ---
with st.sidebar:
    st.title("Main Menu")
    # This creates the navigation options
    selection = st.radio("Go to:", ["Predict Expenditure", "Summary", "About Project"])
    
    st.markdown("---")


    # A checkbox option in the sidebar
    enable_tips = st.checkbox("Show Help Tips", value=True)
    
    if enable_tips:
        st.caption("💡 Tips: Higher hotel classes significantly increase predicted expenditure.")
     
    show_group= st.checkbox("Show Project Contributors", value=False)
    if show_group:
      
     st.info("This Project Prepared by Group work Team ")

# --- 📂 Load Model and Columns ---
try:
    with open("tourism_model.pkl", "rb") as f:
        model = pickle.load(f)
    
except FileNotFoundError:
    st.error("Error: 'tourism_model.pkl' or 'tourism_training_columns.pkl' not found.")
    st.stop()

# --- OPTION 1: PREDICTION PAGE ---
if selection == "Predict Expenditure":
    st.title("Tanzania Tourism Expenditure")

    st.markdown("Predict the total expenditure of a tourist based on their visit details.")

    with st.container():
        st.subheader("📋 Enter Visit Details")
        col1, col2 = st.columns(2)
       
        with col1:
             purpose = st.radio(
                "Purpose of Visit",
                options=["Conference", "VFR", "Leisure", "Business"],
                help="Select the primary reason for your trip. 'VFR' stands for Visiting Friends and Relatives."
             )
             stay_days = st.number_input("Length of Stay (Days)", min_value=0.5, max_value=60.0, value=7.0, step=0.1, format="%.1f")

             daily_spending = st.number_input("Daily Spending (USD)", min_value=1.0, value=150.0)
             
        with col2:
             hotel_class = st.radio(
                "Hotel Class",
                options=["Luxury", "Standard","Budget"],
                help="Choose the star rating or category of your accommodation."
             )

    # Prediction Logic
    if st.button("💰 Predict Total Expenditure"):
        # 1. Create initial DataFrame from inputs
        input_data = pd.DataFrame({
            "Length_of_Stay_Days": [stay_days],
            "Daily_Spending_USD": 

[daily_spending],
            "Purpose_of_Visit": [purpose],
            "Hotel_Class": [hotel_class]
        })

        # 2. One-Hot Encoding
        input_encoded = pd.get_dummies(input_data, columns=["Purpose_of_Visit", "Hotel_Class"])

        # 3. Align with training columns
        final_input = input_encoded.reindex(columns=model_columns, fill_value=0)

        # 4. Perform Prediction
        prediction = model.predict(final_input)

        # 5. Display Result

        st.success(f" Predicted Total Expenditure: ${prediction[0]:,.2f}")
        st.balloons()

        # --- THE st.info SUMMARY ---
        # This gives an immediate recap on the prediction page
        st.info(f"📋 **Summary:** A {stay_days:.1f} days stay for **{purpose}** at a **{hotel_class}** hotel.")

        # Save results to session state so the Summary page can see them
        st.session_state.last_prediction = True
        st.session_state.last_pred = prediction[0]
        st.session_state.last_purpose = purpose
        st.session_state.last_hotel = hotel_class
        st.session_state.last_stay = stay_days
        st.session_state.last_daily = daily_spending

# --- OPTION 2: SUMMARY PAGE ---
elif selection == "Summary":
    st.title( "📊  Detailed Summary")
    
    if 'last_prediction' in st.session_state:
        # Using st.info for a professional breakdown
        st.info(f"""
            ### Final Estimate: ${st.session_state.last_pred:,.2f}
            ---
            **Trip Details Recap:**
            - **Primary Purpose:** {st.session_state.last_purpose}
            - **Accommodation:** {st.session_state.last_hotel} Class
            - **Total Stay:** {st.session_state.last_stay:.1f} Days
            - **Daily Expenditure Rate:** ${st.session_state.last_daily}
            
            *Note: This estimate is based on the current machine learning model parameters.*
        """)
        
        if st.button("Clear Summary"):
            del st.session_state.last_prediction
            st.rerun()
    else:
        st.warning("⚠️ No prediction data found. Please go to 'Predict Expenditure' and click the predict button first.")

# --- OPTION 3: ABOUT PAGE ---
elif selection == "About Project":
    st.title("About the Model")
    st.write("This application uses Machine Learning to estimate tourism revenue for Tanzania.")
    st.write("It was developed to help analyze the impact of different stay factors on total tourist spending.")
    st.markdown("""
    **Developer Info:**
    - **Entity:** Eastern Africa Statistical Training Centre (EASTC)
    - **Variables:** Length of Stay, Purpose, Daily Spending, Hotel Class.
    """)
