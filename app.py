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
st.markdown("Enter your trip details below, and we'll estimate the fare.")

# Sample Data
df = pd.DataFrame({
    "pickup_datetime": [pd.Timestamp("2013-07-06 17:18:00", tz='UTC')],
    "pickup_longitude": [-73.950655],
    "pickup_latitude": [40.783282],
    "dropoff_longitude": [-73.984365],
    "dropoff_latitude": [40.769802],
    "passenger_count": [1],
})

# User Editable Data
st.subheader("📍 Trip Details")
edited_df = st.data_editor(df, num_rows="dynamic")

# API Call
if st.button("Estimate Fare"):
    try:
        response = requests.get(url=url, params=edited_df.iloc[0].to_dict())
        response.raise_for_status()  # Check for HTTP errors
        fare = response.json().get("fare", "N/A")
        st.success(f"💰 Estimated Fare: **${fare}**")
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching fare: {e}")
