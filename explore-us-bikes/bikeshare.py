"""
This file is the Python application of the Explore Bike US project
"""

import datetime as dt
import time
from typing import Dict, Tuple

import pandas as pd

DATASETS_FOLDER: str = "datasets"
CITY_DATA: Dict[str, str] = {
    "chicago": "chicago.csv",
    "new york city": "new_york_city.csv",
    "washington": "washington.csv",
}
VALID_MONTHS: Dict[str, int] = {
    "all": 0,
    "january": 1,
    "february": 2,
    "march": 3,
    "april": 4,
    "may": 5,
    "june": 6,
}
VALID_DAYS: Dict[str, int] = {
    "all": -1,
    "monday": 0,
    "tuesday": 1,
    "wednesday": 2,
    "thursday": 3,
    "friday": 4,
    "saturday": 5,
    "sunday": 6,
}


def get_filters() -> Tuple[str]:
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print("Hello! Let's explore some US bike share data!")
    # Get user input for city (chicago, new york city, washington).
    # HINT: Use a while loop to handle invalid inputs
    city = input(
        f"\nWhich City would you like to analyze?\n\
            Possible choices are {[city.capitalize() for city in CITY_DATA]}.\n"
    )
    while city.lower() not in CITY_DATA:
        print(f"{city} is not a valid choice.")
        city = input(
            f"\nWhich City would you like to analyze?\n\
                Possible choices are {[city.capitalize() for city in CITY_DATA]}.\n"
        )
    # Get user input for month (all, january, february, ... , june)
    month = input(
        f"\nWhich Month would you like to analyze?\n\
            Possible choices are {[month.capitalize() for month in VALID_MONTHS]}.\n"
    )
    while month.lower() not in VALID_MONTHS:
        print(f"{month} is not a valid choice.")
        month = input(
            f"\nWhich Month would you like to analyze?\n\
            Possible choices are {[month.capitalize() for month in VALID_MONTHS]}.\n"
        )

    # Get user input for day of week (all, monday, tuesday, ... sunday)
    day = input(
        f"\nWhich Day of the week would you like to analyze?\n\
            Possible choices are {[day.capitalize() for day in VALID_DAYS]}.\n"
    )
    while day.lower() not in VALID_DAYS:
        print(f"{day} is not a valid choice.")
        day = input(
            f"\nWhich Day of the week would you like to analyze?\n\
            Possible choices are {[day.capitalize() for day in VALID_DAYS]}.\n"
        )

    print("-" * 40)
    return city.lower(), month.lower(), day.lower()


def load_data(city: str, month: str, day: str) -> pd.DataFrame:
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    print("\nLoading the chosen data frame with the chosen filters...\n")
    start_time = time.time()

    # Load the csv file associated with city inside a Pandas DataFrame
    df: pd.DataFrame = pd.read_csv(
        f"{DATASETS_FOLDER}/{CITY_DATA[city]}", index_col=0
    )

    # Cast Birth Year from float to int
    if "Birth Year" in df:
        df["Birth Year"] = df["Birth Year"].astype("Int64")

    # Convert the Start Time column to datetime
    df["Start Time"] = pd.to_datetime(df["Start Time"])

    # Extract month and day of week from Start Time to create new columns
    df["month"] = df["Start Time"].dt.month
    df["day_of_week"] = df["Start Time"].dt.dayofweek
    df["hour"] = df["Start Time"].dt.hour

    # Filter by month if applicable
    if month != "all" and month in VALID_MONTHS:
        # Filter the data frame by month to create the new data frame
        df = df[df.month == VALID_MONTHS[month]]

    # Filter by day of week if applicable
    if day != "all" and day in VALID_DAYS:
        # Filter by day of week to create the new data frame
        df = df[df.day_of_week == VALID_DAYS[day]]

    print(f"The loaded data frame contains {len(df)} records.")
    print(f"\nThis took {time.time() - start_time} seconds.")
    print("-" * 40)
    return df


def time_stats(df: pd.DataFrame) -> None:
    """Displays statistics on the most frequent times of travel."""

    print("\nCalculating The Most Frequent Times of Travel...\n")
    start_time = time.time()

    # Retrieve and display the most common month
    month: int = df.month.mode()[0]
    month_str: str = list(VALID_MONTHS.keys())[
        list(VALID_MONTHS.values()).index(month)
    ].capitalize()
    print(f"The most common month is {month_str}")

    # Retrieve and display the most common day of week
    day: int = df.day_of_week.mode()[0]
    day_str: str = list(VALID_DAYS.keys())[
        list(VALID_DAYS.values()).index(day)
    ].capitalize()
    print(f"The most common day of the week is {day_str}")

    # Retrieve and display the most common start hour
    print(f"The most common start hour is {df.hour.mode()[0]}")

    print(f"\nThis took {time.time() - start_time} seconds.")
    print("-" * 40)


def station_stats(df: pd.DataFrame) -> None:
    """Displays statistics on the most popular stations and trip."""

    print("\nCalculating The Most Popular Stations and Trip...\n")
    start_time = time.time()

    # Retrieve and display most commonly used start station
    print(f"The most common start station is {df['Start Station'].mode()[0]}")

    # Retrieve and display most commonly used end station
    print(f"The most common end station is {df['End Station'].mode()[0]}")

    # Retrieve and display most frequent combination of start station and end station trip
    df_start_end_station = (
        df.groupby(["Start Station", "End Station"])
        .size()
        .sort_values(ascending=False)
    )
    most_common_trip: Tuple[str] = df_start_end_station.index[0]
    print(
        f"The most common trip is {most_common_trip[0]} -> {most_common_trip[1]}"
    )

    print(f"\nThis took {time.time() - start_time} seconds.")
    print("-" * 40)


def trip_duration_stats(df: pd.DataFrame) -> None:
    """Displays statistics on the total and average trip duration."""

    print("\nCalculating Trip Duration...\n")
    start_time = time.time()

    # Retrieve and display total travel time
    total_travel_time_seconds: int = int(df["Trip Duration"].sum())
    total_travel_time_delta = dt.timedelta(seconds=total_travel_time_seconds)
    total_years: int = total_travel_time_delta.days // 365
    total_days: int = total_travel_time_delta.days % 365
    total_hours: int = total_travel_time_delta.seconds // 3600
    total_minutes: int = total_travel_time_delta.seconds // 60 % 60
    total_seconds: int = total_travel_time_delta.seconds % 60
    print(
        f"The total travel time is\n\
        {total_years} years,\n\
        {total_days} days,\n\
        {total_hours} hours,\n\
        {total_minutes} minutes and\n\
        {total_seconds} seconds\n\
        (or a total of {total_travel_time_seconds} seconds)."
    )

    # Retrieve and display mean travel time
    print(
        f"The average travel time is {df['Trip Duration'].mean():.1f} seconds"
    )

    print(f"\nThis took {time.time() - start_time} seconds.")
    print("-" * 40)


def user_stats(df: pd.DataFrame) -> None:
    """Displays statistics on bike share users."""

    print("\nCalculating User Stats...\n")
    start_time = time.time()

    # Retrieve and display counts of user types
    df_user_type_count = df["User Type"].value_counts()
    print("Here are the different user types and their count.")
    for user_type, count in df_user_type_count.items():
        print(f"\t{user_type}:\t{count}")

    # Retrieve and display counts of gender
    if "Gender" in df:
        df_gender_count = df["Gender"].value_counts()
        print("Here are the different genders and their count.")
        for gender, count in df_gender_count.items():
            print(f"\t{gender}:\t{count}")
    else:
        print(
            "The data frame does not contain any information about the gender."
        )

    # Display earliest, most recent, and most common year of birth
    if "Birth Year" in df:
        print(f"The earliest birth date is {df['Birth Year'].min()}.")
        print(f"The most recent birth date is {df['Birth Year'].max()}.")
        print(f"The most common birth date is {df['Birth Year'].mode()[0]}.")
    else:
        print(
            "The data frame does not contain any information about the birth year."
        )

    print(f"\nThis took {time.time() - start_time} seconds.")
    print("-" * 40)


def display_records(df: pd.DataFrame) -> None:
    """Displays the data frame (df) records by batch of 5 if required by the user."""
    display: str = input(
        "\nWould you like to display the 5 fist records? Enter yes or no.\n"
    )
    step: int = 5
    current_record_idx: int = 0
    while display == "yes":
        for _ in range(step):
            if current_record_idx >= len(df):
                print("We are at the end of the data frame. Aborting.")
                break
            print(f"\nRecord at index {current_record_idx}:\n")
            print(df.iloc[current_record_idx])
            current_record_idx += 1
        display: str = input(
            "\nWould you like to display the 5 next records? Enter yes or no.\n"
        )


def main() -> None:
    """Main function"""
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_records(df)

        restart = input("\nWould you like to restart? Enter yes or no.\n")
        if restart.lower() != "yes":
            break


if __name__ == "__main__":
    main()
