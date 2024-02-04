# TECHIN 510 Lab 4 

Real-time streamlit

## Overview
Hi! This is the repository for my personal To-Do list for TECHIN 510.  
------This code outlines a Streamlit web application for managing tasks, showcasing the use of SQLite for storage, Pydantic for data validation, and Streamlit for the web interface.  
------It demonstrates key concepts like database operations, form handling, and dynamic content update in a web app.
------datetime.ipynb: This notebook contains the code for the datetime exercise.
------regex.ipynb: This notebook contains the code for the regex exercise.
------app.py: Example world clock app.

## How to Run

Create a gitignore as your first step! Put the following In your gitignore file! Do NOT commit the sqlite files!
```
venv
```

Put the following in your requirements.txt file
```
streamlit
yfinance
pandas
pytz
psycopg2-binary
```

Open the terminal and run the following commands:
```    
pip install -r requirements.txt 
pip install streamlit
pip install yfinance 
pip install psycopg2-binary

```

Run the app using the command in the terminal
```bash
streamlit run app.py
```
## Detailed Comment for Every Part
- Define the database connection parameters for connecting to a PostgreSQL database.
- Set up a sidebar in the Streamlit app for page navigation.
- Function to get current time and UNIX timestamp for a timezone
- Fetch financial data using yfinance
- Inject fetched data into PostgreSQL database

## Lessons Learned
- Learning to fetch financial data using the `yfinance` library .
- Gaining insights into handling timezones with the `pytz` library and displaying current times in different time zones, which is crucial for applications dealing with global data.
- The process of connecting to a PostgreSQL database using `psycopg2`, executing SQL statements, and handling transactions.
- Balancing between dynamic content that updates periodically (like a world clock) and static content that changes based on user input (like converting UNIX timestamps or displaying financial data).

## Questions / Uncertainties
- Understanding the performance implications of fetching data from external APIs (like Yahoo Finance) and inserting data into databases directly from a Streamlit app, especially when these operations are triggered frequently.


## Contact

- Liliana Hsu
# TECHIN510







