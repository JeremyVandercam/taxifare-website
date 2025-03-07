import datetime
import streamlit as st
import pandas as pd
import requests

'''
# TaxiFareModel front
'''

st.markdown('''
Remember that there are several ways to output content into your web page...

Either as with the title by just creating a string (or an f-string). Or as with this paragraph using the `st.` functions
''')

'''
## Here we would like to add some controllers in order to ask the user to select the parameters of the ride

1. Let's ask for:
- date and time
- pickup longitude
- pickup latitude
- dropoff longitude
- dropoff latitude
- passenger count
'''

'''
## Once we have these, let's call our API in order to retrieve a prediction

See ? No need to load a `model.joblib` file in this app, we do not even need to know anything about Data Science in order to retrieve a prediction...

🤔 How could we call our API ? Off course... The `requests` package 💡
'''

url = 'https://taxifare-872733186184.europe-west1.run.app/predict'

if url == 'https://taxifare.lewagon.ai/predict':

    st.markdown('Maybe you want to use your own API for the prediction, not the one provided by Le Wagon...')

'''

2. Let's build a dictionary containing the parameters for our API...

3. Let's call our API using the `requests` package...

4. Let's retrieve the prediction from the **JSON** returned by the API...

## Finally, we can display the prediction to the user
'''
st.title("🚖 NYC Taxi Fare Estimator")
st.markdown("Enter your trip details below, and we'll estimate the fare.")

# User Input Form
with st.form("fare_form"):
    pickup_lat = st.number_input("📍 Pickup Latitude", value=40.783282, format="%.6f")
    dropoff_lat = st.number_input("🎯 Drop-off Latitude", value=40.769802, format="%.6f")
    passenger_count = st.number_input("👥 Passenger Count", min_value=1, max_value=6, value=1)
    pickup_long = st.number_input("📍 Pickup Longitude", value=-73.950655, format="%.6f")
    dropoff_long = st.number_input("🎯 Drop-off Longitude", value=-73.984365, format="%.6f")
    pickup_time = st.date_input("⏰ Pickup Time", value=datetime.datetime(2013, 7, 6, 17, 18, tzinfo=datetime.timezone.utc))
    submitted = st.form_submit_button("Estimate Fare")

# Process User Input
if submitted:
    params = {
        "pickup_datetime": pickup_time.isoformat(),
        "pickup_longitude": pickup_long,
        "pickup_latitude": pickup_lat,
        "dropoff_longitude": dropoff_long,
        "dropoff_latitude": dropoff_lat,
        "passenger_count": passenger_count,
    }

    url = "https://taxifare-872733186184.europe-west1.run.app/predict"

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        fare = response.json()["fare"]
        st.success(f"💰 Estimated Fare: **${fare}**")
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching fare: {e}")

# Optional: Map Visualization
st.subheader("🗺️ Trip Map")
st.map(pd.DataFrame({"lat": [pickup_lat, dropoff_lat], "lon": [pickup_long, dropoff_long]}))
