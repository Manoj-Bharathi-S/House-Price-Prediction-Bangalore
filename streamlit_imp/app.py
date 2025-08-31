import streamlit as st
import pickle
import json
import numpy as np
import os

# Hide Streamlit UI elements
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    [data-testid="stDeployButton"] {display:none;}
    /* Hide the copy link button */
    .stApp [data-testid="stToolbar"] {display:none;}
    /* Adjust spacing */
    #root > div:nth-child(1) > div > div > div > div > section > div {padding-top: 0rem;}
    </style>
""", unsafe_allow_html=True)

# Set page config
st.set_page_config(
    page_title="Bangalore House Price Predictor",
    page_icon="🏠",
    layout="centered"
)

# Copy of utility functions from util.py
__locations = None
__data_columns = None
__model = None

def load_saved_artifacts():
    print("Loading saved artifacts...start")
    global __data_columns
    global __locations
    global __model

    # Path to artifacts (relative to the script location)
    base_path = os.path.dirname(os.path.abspath(__file__))
    columns_path = os.path.join(base_path, 'artifacts', 'columns.json')
    model_path = os.path.join(base_path, 'artifacts', 'banglore_home_prices_model.pickle')

    with open(columns_path, "r") as f:
        __data_columns = json.load(f)['data_columns']
        __locations = __data_columns[3:]  # first 3 columns are sqft, bath, bhk

    if __model is None:
        with open(model_path, 'rb') as f:
            __model = pickle.load(f)
    print("Loading saved artifacts...done")

def get_estimated_price(location, sqft, bhk, bath):
    try:
        loc_index = __data_columns.index(location.lower())
    except:
        loc_index = -1

    x = np.zeros(len(__data_columns))
    x[0] = sqft
    x[1] = bath
    x[2] = bhk
    if loc_index >= 0:
        x[loc_index] = 1

    return round(__model.predict([x])[0], 2)

def get_location_names():
    return __locations

# Load artifacts when the app starts
load_saved_artifacts()

# App UI
st.title('🏠 Bangalore House Price Predictor')
st.write('Predict the price of your dream home in Bangalore')

# Input form
with st.form("prediction_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        sqft = st.number_input('Total Square Feet', min_value=300, max_value=10000, value=1000, step=50)
        bhk = st.selectbox('BHK', [1, 2, 3, 4, 5, 6])
    
    with col2:
        bath = st.selectbox('Number of Bathrooms', [1, 2, 3, 4, 5])
        location = st.selectbox('Location', get_location_names())
    
    # Center the submit button with adjusted spacing
    _, center_col, _ = st.columns([1.5, 1, 1.5])
    with center_col:
        submitted = st.form_submit_button("Predict Price")

# Make prediction when form is submitted
if submitted:
    with st.spinner('Predicting...'):
        price = get_estimated_price(location, sqft, bhk, bath)
        st.success(f'### Estimated Price: ₹{price:,.2f} Lakhs')
        
        # Show some context
        st.write(f"For a {bhk} BHK apartment of {sqft} sq.ft. in {location.title()}")

# Add some additional information
st.markdown("---")
st.markdown("""
### About
This app predicts house prices in Bangalore using a machine learning model trained on historical data.

### How to use
1. Enter the property details
2. Click 'Predict Price' to get an estimate

*Note: This is an estimate based on available data and may not reflect current market conditions.*
""")
