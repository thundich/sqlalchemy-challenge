# sqlalchemy-challenge
Module 10 Challenge

Tamara Hundich

11/28/2023

  Michigan State University edX Data Analytics Bootcamp 

  SQLAlchemy Challenge 10: Using SQL Alchemy to connect to SQLite database and Designing Climate App

  Analysis Question: Which station id has the greatest number of observations?  USC00519281

## Requirements
  - Part 1: Analyze and Explore the Climate Data
        - Note that you’ll use the provided files (climate_starter.ipynb and hawaii.sqlite) to complete your climate analysis and data exploration.
        - Use the SQLAlchemy create_engine() function to connect to your SQLite database.
        - Use the SQLAlchemy automap_base() function to reflect your tables into classes, and then save references to the classes named station and measurement.
        - Link Python to the database by creating a SQLAlchemy session.
        - Perform a precipitation analysis and then a station analysis by completing the steps in the following two subsections.
        - Preciptation Analysis
            - Find the most recent date in the dataset.
            - Using that date, get the previous 12 months of precipitation data by querying the previous 12 months of data.
            - Select only the "date" and "prcp" values.
            - Load the query results into a Pandas DataFrame. Explicitly set the column names. 
            - Sort the DataFrame values by "date".
            - Plot the results by using the DataFrame plot method
            - Use Pandas to print the summary statistics for the precipitation data.
       - Station Analysis
            - Design a query to calculate the total number of stations in the dataset.
            - Design a query to find the most-active stations (that is, the stations that have the most rows). To do so, complete the following steps:
                - List the stations and observation counts in descending order.
                - Answer the following question: which station id has the greatest number of observations?
            - Design a query that calculates the lowest, highest, and average temperatures that filters on the most-active station id found in the previous query.
            - Design a query to get the previous 12 months of temperature observation (TOBS) data. To do so, complete the following steps
                - Filter by the station that has the greatest number of observations
                - Query the previous 12 months of TOBS data for that station
                - Plot the results as a histogram with bins=12
                - Close your session.
- Part 2: Design Your Climate App
    - Now that you’ve completed your initial analysis, you’ll design a Flask API based on the queries that you just developed. To do so, use Flask to create your routes as follows:
        - /
            - Start at the homepage.
            - List all the available routes.
        - /api/v1.0/precipitation
            - Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data) to a dictionary using date as the key and prcp as the value
            - Return the JSON representation of your dictionary.
        - /api/v1.0/stations
            - Return a JSON list of stations from the dataset
        - /api/v1.0/<start> and /api/v1.0/<start>/<end>
            - Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.
            - For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.
            - For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive. 

## Installation and Configuration 
- Python, SQLAlchemy, SQLite, Flask 
	
- Files included with repository include the Resources codes provided, README, app.py, and climate.starter.ipynb

- While reviewing the data analysis on the precipitation analysis, there were multiple dates with the same numbers. In order to obtain an accurate number for the total tobs count, a sum of the dates had to occur in order to find the correct values. These numbers were added together due to a dictionary cannot have more than 1 unique key. 

- Also while running the server, there was found to be exceptions that were needed. Added exceptions to the coding in order to obtain a more accurate feedback or user experience. 
