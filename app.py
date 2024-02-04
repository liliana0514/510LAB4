import streamlit as st
import datetime
import pytz
import yfinance as yf
import psycopg2
from psycopg2.extras import execute_batch
import time

# Part A: Initialize a session state for history
# Initialize session state for history if not already done
if 'history' not in st.session_state:
    st.session_state.history = []

# Part B: Database connection parameters
# Define the database connection parameters for connecting to a PostgreSQL database.
db_config = {
    'dbname': 'postgres',
    'user': 'liliana',  # Use your Azure username
    'password': '#May05140414',  # Use your actual password
    'host': 'techin510lab4liliana.postgres.database.azure.com',
    'sslmode': 'require'  # Force SSL
}

# Part C: Sidebar for navigation
# Set up a sidebar in the Streamlit app for page navigation.
PAGES = {
    "World Clock": "world_clock",
    "UNIX Timestamp Converter": "unix_converter",
    "Real-time Financial Data Viewer & Database Injector": "financial_data_viewer"
}
st.sidebar.title('Navigation')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))

# Part D: Function to get current time and UNIX timestamp for a timezone
# This function takes a timezone as input and returns the current time and UNIX timestamp.
def get_time(zone):
    tz = pytz.timezone(zone)
    now = datetime.datetime.now(tz)
    return now.strftime('%Y-%m-%d %H:%M:%S'), int(now.timestamp())

# Part E: Fetch financial data using yfinance
# Fetches the latest financial data for a given stock symbol from Yahoo Finance.
def fetch_finance_data(ticker_symbol):
    """Fetches the latest financial data for the given stock symbol using yfinance."""
    ticker = yf.Ticker(ticker_symbol)
    data = ticker.history(period="1d")
    return data

# Part F: Inject fetched data into PostgreSQL database
# This function takes financial data and a stock symbol, then inserts the data into a PostgreSQL database.
def ingest_data_into_db(data, ticker_symbol):
    """Injects the fetched financial data into the PostgreSQL database."""
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        
        # Prepare the SQL insert statement
        insert_sql = """
        INSERT INTO finance_data (ticker, date, open, high, low, close, volume) 
        VALUES (%s, %s, %s, %s, %s, %s, %s);
        """
        
        # Iterate over the data rows and prepare data for insertion
        data_for_insert = []
        for index, row in data.iterrows():
            # Format the date as a string
            date = index.strftime('%Y-%m-%d')
            data_row = (ticker_symbol, date, row['Open'], row['High'], row['Low'], row['Close'], row['Volume'])
            data_for_insert.append(data_row)
        
        # Execute the insert statement for each row
        for record in data_for_insert:
            cursor.execute(insert_sql, record)
        
        conn.commit()  # Commit the transaction
        cursor.close()
        conn.close()
        st.success('Data successfully injected into the database.')
    except Exception as e:
        st.error(f'Error injecting data into the database: {e}')

# Part G: Display financial data
# Display financial data for a given stock symbol on the Streamlit app.
def display_finance_data(ticker_symbol):
    """Displays financial data for the given stock symbol."""
    data = fetch_finance_data(ticker_symbol)
    if not data.empty:
        st.write(f"Stock Symbol: {ticker_symbol}")
        st.dataframe(data)
        # Optionally, log the view in session state history
        st.session_state.history.append((ticker_symbol, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    else:
        st.write("No data found for the stock symbol.")

# Part H: World Clock Page
# Display the current time in selected timezones.
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

# Part I: UNIX Timestamp Converter Page
# Convert a given UNIX timestamp to human-readable time format.
elif selection == "UNIX Timestamp Converter":
    st.title("UNIX Timestamp Converter")
    unix_timestamp_input = st.number_input("Enter UNIX Timestamp", min_value=0, value=int(time.time()), step=1, format="%d")
    human_time = datetime.datetime.utcfromtimestamp(unix_timestamp_input).strftime('%Y-%m-%d %H:%M:%S')
    st.write("Human-readable time:", human_time)


# Part J: Real-time Financial Data Viewer & Database Injector Page
# This part handles the selection of stock symbols, fetching their financial data, displaying it, and allowing the user to inject this data into a database.
elif selection == "Real-time Financial Data Viewer & Database Injector":
    st.title('Real-time Financial Data Viewer & Database Injector')
    options = st.multiselect('Select stock symbols (up to 4)', ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA', 'META'], [])
    
    for ticker_symbol in options[:4]:  # Limit to showing up to 4 stocks
        if ticker_symbol:
            data = fetch_finance_data(ticker_symbol)
            if not data.empty:
                display_finance_data(ticker_symbol)
                # Inject data into database when the button is pressed
                if st.button(f'Inject {ticker_symbol} Data into Database'):
                    ingest_data_into_db(data, ticker_symbol)

    # Display view history
    st.write("View History:")
    for item in st.session_state.history:
        st.write(f"Stock Symbol: {item[0]}, View Time: {item[1]}")
