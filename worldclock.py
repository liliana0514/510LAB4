import streamlit as st
import datetime
import pytz
import time

# Use Streamlit's new page feature to create separate pages
PAGES = {
    "World Clock": "world_clock",
    "UNIX Timestamp Converter": "unix_converter"
}
st.sidebar.title('Navigation')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))

# Function to get current time for a timezone and UNIX timestamp
def get_time(zone):
    tz = pytz.timezone(zone)
    now = datetime.datetime.now(tz)
    return now.strftime('%Y-%m-%d %H:%M:%S'), int(now.timestamp())

if selection == "World Clock":
    st.title("World Clock")

    # List of timezones (you can expand this list)
    timezones = ['UTC', 'US/Eastern', 'US/Pacific', 'Europe/London', 'Asia/Tokyo', 'Australia/Sydney']

    # Streamlit widget for selecting time zones, allowing up to 4 locations
    selected_timezones = st.multiselect('Select up to 4 locations', timezones, default=['UTC'])

    # Container to hold our dynamic content
    container = st.container()
    
    def update_time():
        with container:
            st.write("---")  # Separator
            for zone in selected_timezones:
                time_str, unix_ts = get_time(zone)
                st.write(f"Time in {zone}: {time_str} (UNIX Timestamp: {unix_ts})")
                
    while True:
        update_time()
        time.sleep(1)  # Update the time every second

elif selection == "UNIX Timestamp Converter":
    st.title("UNIX Timestamp Converter")

    unix_timestamp_input = st.number_input("Enter UNIX Timestamp", min_value=0, value=int(time.time()), step=1, format="%d")
    
    # Convert and display the human-readable format
    if unix_timestamp_input:
        human_time = datetime.datetime.utcfromtimestamp(unix_timestamp_input).strftime('%Y-%m-%d %H:%M:%S')
        st.write("Human-readable time:", human_time)

