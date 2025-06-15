import time
import pandas as pd
import numpy as np
from datetime import datetime
import logging
from colorama import init, Fore, Style
from tqdm import tqdm
import sys

# Initialize colorama
init()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bikeshare.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

# Dictionary mapping cities to their data files
CITY_FILES = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}

def print_separator():
    """Print a separator line for better readability."""
    print('\n' + '=' * 50 + '\n')

def print_colored(text, color=Fore.WHITE):
    """Print colored text to console."""
    print(f"{color}{text}{Style.RESET_ALL}")

def get_user_preferences():
    """
    Collects user preferences for city, month, and day analysis.

    Returns:
        tuple: (city, month, day) - User selected filters
    """
    print_separator()
    print('🚲 Welcome to the BikeShare Data Explorer! 🚲')
    print_separator()

    # Get city selection
    while True:
        print("\n📌 Available cities:")
        for city in CITY_FILES.keys():
            print(f"  • {city.title()}")
        city = input("\n👉 Select a city to analyze: ").lower()
        if city in CITY_FILES:
            break
        print("\n❌ Invalid city! Please select from the available options.")

    # Get month selection
    valid_months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    while True:
        print("\n📅 Available months:")
        for month in valid_months[:-1]:
            print(f"  • {month.title()}")
        print("  • all (for no month filter)")
        month = input(f"\n👉 Select month for {city.title()} analysis: ").lower()
        if month in valid_months:
            break
        print("\n❌ Invalid month! Please select from the available options.")

    # Get day selection
    valid_days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
    while True:
        print("\n📆 Available days:")
        for day in valid_days[:-1]:
            print(f"  • {day.title()}")
        print("  • all (for no day filter)")
        day = input(f"\n👉 Select day for {city.title()} analysis: ").lower()
        if day in valid_days:
            break
        print("\n❌ Invalid day! Please select from the available options.")

    print_separator()
    return city, month, day

def process_data(city, month, day):
    """
    Loads and filters data based on user preferences.

    Args:
        city (str): Selected city
        month (str): Selected month
        day (str): Selected day

    Returns:
        DataFrame: Filtered data
    """
    try:
        logging.info(f"Loading data for {city}")
        print_colored("\nLoading data...", Fore.YELLOW)
        
        # Load city data with progress bar
        df = pd.read_csv(CITY_FILES[city])
        
        print_colored("Processing data...", Fore.YELLOW)
        # Convert and extract datetime components
        df['Start Time'] = pd.to_datetime(df['Start Time'])
        df['month'] = df['Start Time'].dt.month
        df['day'] = df['Start Time'].dt.day_name()

        # Apply filters
        if month != 'all':
            months = ['january', 'february', 'march', 'april', 'may', 'june']
            month_idx = months.index(month) + 1
            df = df[df['month'] == month_idx]

        if day != 'all':
            df = df[df['day'] == day.title()]

        logging.info("Data processing completed successfully")
        return df
        
    except FileNotFoundError:
        logging.error(f"Data file not found for {city}")
        print_colored(f"\nError: Could not find data file for {city}", Fore.RED)
        sys.exit(1)
    except Exception as e:
        logging.error(f"Error processing data: {str(e)}")
        print_colored(f"\nError: An unexpected error occurred: {str(e)}", Fore.RED)
        sys.exit(1)


def analyze_time_patterns(df, month, day):
    """Analyzes and displays time-based patterns in the data."""

    print('\n=== Time Analysis ===\n')
    start_time = time.time()

    months = ['january', 'february', 'march', 'april', 'may', 'june']

    if month == 'all':
        popular_month = df['month'].mode()[0]
        print(f"Most popular month: {months[popular_month - 1].title()}")

    if day == 'all':
        popular_day = df['day'].mode()[0]
        print(f"Most popular day: {popular_day}")

    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print(f"Most popular hour: {popular_hour}:00")

    print(f"\nAnalysis completed in {time.time() - start_time:.2f} seconds")
    print('-' * 40)


def analyze_stations(df):
    """Analyzes and displays station-related statistics."""

    print('\n=== Station Analysis ===\n')
    start_time = time.time()

    popular_start = df["Start Station"].mode()[0]
    popular_end = df["End Station"].mode()[0]

    print(f"Most popular starting station: {popular_start}")
    print(f"Most popular ending station: {popular_end}")

    df["Route"] = df["Start Station"] + " → " + df["End Station"]
    popular_route = df["Route"].mode()[0]
    print(f"Most popular route: {popular_route}")

    print(f"\nAnalysis completed in {time.time() - start_time:.2f} seconds")
    print('-' * 40)


def analyze_trip_duration(df):
    """Analyzes and displays trip duration statistics."""

    print('\n=== Trip Duration Analysis ===\n')
    start_time = time.time()

    total_duration = df["Trip Duration"].sum()
    avg_duration = df["Trip Duration"].mean()

    # Convert to more readable format
    total_hours = total_duration // 3600
    total_minutes = (total_duration % 3600) // 60
    avg_minutes = avg_duration // 60

    print(f"Total travel time: {total_hours} hours and {total_minutes} minutes")
    print(f"Average trip duration: {avg_minutes:.1f} minutes")

    print(f"\nAnalysis completed in {time.time() - start_time:.2f} seconds")
    print('-' * 40)


def analyze_users(df):
    """Analyzes and displays user-related statistics."""

    print('\n=== User Analysis ===\n')
    start_time = time.time()

    # User type analysis
    user_types = df["User Type"].value_counts()
    print("User type distribution:")
    for user_type, count in user_types.items():
        print(f"- {user_type}: {count:,} users")

    # Gender analysis (if available)
    if 'Gender' in df.columns:
        gender_stats = df['Gender'].value_counts()
        print("\nGender distribution:")
        for gender, count in gender_stats.items():
            print(f"- {gender}: {count:,} users")
    else:
        print("\nGender data not available for this city")

    # Birth year analysis (if available)
    if 'Birth Year' in df.columns:
        earliest = int(df['Birth Year'].min())
        latest = int(df['Birth Year'].max())
        common = int(df['Birth Year'].mode()[0])

        print("\nBirth year statistics:")
        print(f"- Earliest birth year: {earliest}")
        print(f"- Most recent birth year: {latest}")
        print(f"- Most common birth year: {common}")
    else:
        print("\nBirth year data not available for this city")

    print(f"\nAnalysis completed in {time.time() - start_time:.2f} seconds")
    print('-' * 40)


def show_raw_data(city):
    """Displays raw data in chunks based on user request."""

    print_separator()
    print('📊 Raw Data Viewer')
    print_separator()

    while True:
        view_data = input("👀 Would you like to view 5 rows of raw data? (yes/no): ").lower()
        if view_data != 'yes':
            break

        for chunk in pd.read_csv(CITY_FILES[city], chunksize=5):
            print("\n📋 Sample data:")
            print(chunk)

            if input("\n👀 View more data? (yes/no): ").lower() != 'yes':
                return

    print("\n🙏 Thank you for using the data viewer!")


def main():
    try:
        while True:
            # Get user preferences
            city, month, day = get_user_preferences()

            # Process data
            print("\n⏳ Loading and processing data...")
            df = process_data(city, month, day)

            # Display analyses
            analyze_time_patterns(df, month, day)
            analyze_stations(df)
            analyze_trip_duration(df)
            analyze_users(df)
            show_raw_data(city)

            # Ask to restart
            if input('\n🔄 Would you like to analyze another dataset? (yes/no): ').lower() != 'yes':
                print('\n👋 Thank you for using the BikeShare Data Explorer!')
                break
                
    except KeyboardInterrupt:
        print_colored('\n\nProgram terminated by user.', Fore.YELLOW)
        sys.exit(0)
    except Exception as e:
        logging.error(f"Unexpected error in main: {str(e)}")
        print_colored(f"\nAn unexpected error occurred: {str(e)}", Fore.RED)
        sys.exit(1)


if __name__ == "__main__":
    main()