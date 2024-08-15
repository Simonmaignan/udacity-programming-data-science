"""
This file is the Python application of the Explore Bike US project
"""

import time
from typing import Dict

import pandas as pd
import numpy as np

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


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print("Hello! Let's explore some US bikeshare data!")
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input(
        f"\nWhich City would you like to analyze?\
            Possible choices are {[city.capitalize() for city in CITY_DATA]}.\n"
    )
    while city.lower() not in CITY_DATA:
        print(f"{city} is not a valid choice.")
        city = input(
            f"\nWhich City would you like to analyze?\
                Possible choices are {[city.capitalize() for city in CITY_DATA]}.\n"
        )
    # get user input for month (all, january, february, ... , june)
    month = input(
        f"\nWhich Month would you like to analyze?\
            Possible choices are {[month.capitalize() for month in VALID_MONTHS]}.\n"
    )
    while month.lower() not in VALID_MONTHS:
        print(f"{month} is not a valid choice.")
        month = input(
            f"\nWhich Month would you like to analyze?\
            Possible choices are {[month.capitalize() for month in VALID_MONTHS]}.\n"
        )

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input(
        f"\nWhich Day of the week would you like to analyze?\
            Possible choices are {[day.capitalize() for day in VALID_DAYS]}.\n"
    )
    while day.lower() not in VALID_DAYS:
        print(f"{day} is not a valid choice.")
        day = input(
            f"\nWhich Day of the week would you like to analyze?\
            Possible choices are {[day.capitalize() for day in VALID_DAYS]}.\n"
        )

    print("-" * 40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # Load the csv file associated with city inside a Pandas DataFrame
    df = pd.read_csv(f"{DATASETS_FOLDER}/{CITY_DATA[city]}")

    # Convert the Start Time column to datetime
    df["Start Time"] = pd.to_datetime(df["Start Time"])

    # Extract month and day of week from Start Time to create new columns
    df["month"] = df["Start Time"].dt.month
    df["day_of_week"] = df["Start Time"].dt.dayofweek

    # Filter by month if applicable
    if month != "all" and month in VALID_MONTHS:
        # Filter the data frame by month to create the new data frame
        df = df[df.month == VALID_MONTHS[month]]

    # Filter by day of week if applicable
    if day != "all" and day in VALID_DAYS:
        # Filter by day of week to create the new data frame
        df = df[df.day_of_week == VALID_DAYS[day]]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print("\nCalculating The Most Frequent Times of Travel...\n")
    start_time = time.time()

    # display the most common month

    # display the most common day of week

    # display the most common start hour

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print("\nCalculating The Most Popular Stations and Trip...\n")
    start_time = time.time()

    # display most commonly used start station

    # display most commonly used end station

    # display most frequent combination of start station and end station trip

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print("\nCalculating Trip Duration...\n")
    start_time = time.time()

    # display total travel time

    # display mean travel time

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print("\nCalculating User Stats...\n")
    start_time = time.time()

    # Display counts of user types

    # Display counts of gender

    # Display earliest, most recent, and most common year of birth

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)


def main():
    while True:
        city, month, day = get_filters()
        print(city, month, day)
        df = load_data(city, month, day)
        print(df.head())

        # time_stats(df)
        # station_stats(df)
        # trip_duration_stats(df)
        # user_stats(df)

        restart = input("\nWould you like to restart? Enter yes or no.\n")
        if restart.lower() != "yes":
            break


if __name__ == "__main__":
    main()
