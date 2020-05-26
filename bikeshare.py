import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    print('Which city would you like to see data?/Pour quelle ville souhaitez-vous voir les donnees?')
    city = input("Please enter the name of the city to analyze/Veuillez entrer le nom de la ville a analyser: ").lower()

    while city not in CITY_DATA:
        city = input('Invalid entry. Please enter one of the following cities, chicago, new york city, washington: ').lower()

    # TO DO: get user input for month (all, january, february, ... , june)
    print('Which month?/Quel mois?')
    month = input('Please enter month name/Veuillez entrer le mois: ').lower()

    while month not in ['january','february','march','april','may','june']:
        month = input('Invalid entry. Please enter one of the following months, january, february, march, april, may, june/Veuillez entrer un mois: ').lower()

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    print('Which day?/Quel jour?')
    day = input('Please enter day name/Veuillez entrer un jour: ').lower()

    while day not in ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']:
        day = input('Invalid entry. Please enter one of the following days, monday, tuesday, wednesday, thursday, friday, saturday, sunday: ').lower()

    print('-'*40)
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
    #load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    #convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    #extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    #filter by month if applicable
    if month != 'all':
        #use the index of the months list to get the corresponding int
        months = ['january','february','march','april','may','june']
        month = months.index(month) + 1

        #filter by month to create the new dataframe
        df = df[df['month'] == month]

    #filter by day of week if applicable
    if day != 'all':
        #filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    popular_month = df['month'].mode()[0]
    print('The most popular month is: {}'.format(popular_month))

    # TO DO: display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('The most popular day of week is: {}'.format(popular_day))

    # TO DO: display the most common start hour
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('The most popular start hour is: {}'.format(popular_hour))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('The most popular start station is: {}'.format(popular_start_station))


    # TO DO: display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('The most popular end station is: {}'.format(popular_end_station))

    # TO DO: display most frequent combination of start station and end station trip
    df['popular trip'] = df['Start Station'] + " - " + df['End Station']
    most_popular_trip = df['popular trip'].mode()[0]
    print('The most frequent combination start-end station trip is: {}'.format(most_popular_trip))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    df['trip_duration'] = df['End Time'] - df['Start Time']

    # display total travel time
    print("The total travel time is: {}".format(df['trip_duration'].sum()))

    # display mean travel time
    print("The mean travel time is: {}".format(df['trip_duration'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print('The counts of user types is: ', df['User Type'].value_counts())

    # TO DO: Display counts of gender
    if city != 'washington':
        print('The counts of gender is: {}'.format(df['Gender'].value_counts()))

    # TO DO: Display earliest, most recent, and most common year of birth
    if city != 'washington':
        print('The earliest year of birth is: {}'.format(int(df['Birth Year'].min())))
        print('The most recent year of birth is: {}'.format(int(df['Birth Year'].max())))
        print('The most common year of birth is: {}'.format(int(df['Birth Year'].mode()[0])))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    """Displays 5 rows of raw data upon request to the user."""

    index=0
    user_input='y'

    while user_input in ['yes','y','yep','yea','yeah'] and index+5 < df.shape[0]:
        user_input = input('would you like to display 5 rows of raw data? ').lower()
        print(df.iloc[index:index+5])
        index += 5

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
