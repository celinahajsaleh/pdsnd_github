# BikeShare Data Explorer 🚲

## Overview
This project is an interactive tool for analyzing bike share data from three US cities: Chicago, New York City, and Washington. It allows users to explore bike usage patterns by analyzing data by city, month, and day.

## Data Sources
The data used in this project comes from the following bike share systems:
- Chicago: Divvy Bike Share
- New York City: Citi Bike
- Washington: Capital Bikeshare

## Features
- Time pattern analysis (most popular months, days, and hours)
- Station statistics (most used stations and common routes)
- Trip duration analysis (total and average trip time)
- User statistics (user types, gender, birth year)
- Raw data display in a readable format

## Requirements
- Python 3.x
- pandas
- numpy

## How to Use
1. Ensure the following data files are in the same directory:
   - chicago.csv
   - new_york_city.csv
   - washington.csv

2. Run the program:
   ```bash
   python bikeshare.py
   ```

3. Follow the on-screen instructions:
   - Select a city
   - Select a month (or "all" for all months)
   - Select a day (or "all" for all days)

## Main Functions
- `get_user_preferences()`: Collects user preferences
- `process_data()`: Loads and filters data
- `analyze_time_patterns()`: Analyzes time patterns
- `analyze_stations()`: Analyzes station statistics
- `analyze_trip_duration()`: Analyzes trip durations
- `analyze_users()`: Analyzes user data
- `show_raw_data()`: Displays raw data

## Available Data
- **Chicago**: Complete data (including gender and birth year)
- **New York City**: Complete data (including gender and birth year)
- **Washington**: Limited data (no gender or birth year information)

## Notes
- Data is available for months January through June
- Raw data can be viewed 5 rows at a time
- Analysis can be restarted at any time

## Contributing
Contributions are welcome! Please send pull requests with a clear description of the proposed changes. 