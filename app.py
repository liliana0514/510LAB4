import streamlit as st
import datetime
import pytz
import time

# List of timezones (you can expand this list)
timezones = ['UTC', 'US/Eastern', 'US/Pacific', 'Europe/London', 'Asia/Tokyo']

# Streamlit widget for selecting time zones
selected_timezones = st.multiselect('Select up to 4 locations', timezones, default=['UTC'])

# Function to get current time for a timezone
def get_time(zone):
    tz = pytz.timezone(zone)
    return datetime.datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')

# Create a placeholder for each timezone
placeholders = [st.empty() for _ in selected_timezones]

while True:
    for i, zone in enumerate(selected_timezones):
        with placeholders[i]:
            st.write(f"Time in {zone}: {get_time(zone)}")
    time.sleep(1)

