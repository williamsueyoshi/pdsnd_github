import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def valid_input(display_message, valid_inputs):
    """
    Keeps asking user for input until a valid one is received.
    Input is case insensitive.

    Args:
        (str) display_message - message to be displayed for the user when
                                asking for input
        (list) valid_inputs - list containing the valid options for input

    Returns:
        (str) user_input - message inserted by the user
    """

    # makes every item in the "valid_inputs" list lower case
    valid_inputs = [list_item.lower() for list_item in valid_inputs]

    while True: #keeps asking the user for a valid input
        try:
            user_input = input('\n' + display_message)
        except:
            print('\nInvalid Input')
        else:
            if user_input.lower() in valid_inputs:
                break
            print('\nInvalid Input')

    return user_input.lower()


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no
                      month filter
        (str) day - name of the day of week to filter by, or "all" to apply no
                    day filter
    """

    print('\nHello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington)
    display_message = 'Enter city name (chicago, new york city, washington): '
    valid_inputs = ['chicago', 'new york city', 'washington']
    city = valid_input(display_message, valid_inputs)

    # get user input for month (all, january, february, ... , june)
    display_message = 'Enter month (all, january, february, ... , june): '
    valid_inputs = ['all', 'january', 'february', 'march', 'april', 'may',
                    'june']
    month = valid_input(display_message, valid_inputs)

    # get user input for day of week (all, monday, tuesday, ... sunday)
    display_message = 'Enter day of week (all, monday, ... , sunday): '
    valid_inputs = ['all', 'monday', 'tuesday', 'wednesday', 'thursday',
                    'friday', 'saturday', 'sunday']
    day = valid_input(display_message, valid_inputs)

    print('\n' + '-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if
    applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no
                      month filter
        (str) day - name of the day of week to filter by, or "all" to apply no
                    day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[(df['month'] == month)]

    # filter by day of week if applicable
    if day != 'all':
        # use the index of the days_of_week list to get the corresponding int
        days_of_week = ['monday', 'tuesday', 'wednesday', 'thursday',
                        'friday', 'saturday', 'sunday']
        day = days_of_week.index(day)

        # filter by day of week to create the new dataframe
        df = df[(df['day_of_week'] == day)]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    popular_month = int(df['month'].mode())
    print('Most Common Month: ', months[popular_month - 1].title())

    # display the most common day of week
    days_of_week = ['monday', 'tuesday', 'wednesday', 'thursday',
                    'friday', 'saturday', 'sunday']
    popular_day = int(df['day_of_week'].mode())
    print('\nMost Common Day of Week: ', days_of_week[popular_day].title())

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = int(df['hour'].mode())
    print('\nMost Common Start Hour: ', popular_hour)

    print("\nThis took %s seconds.\n" % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('Most Common Start Station: ', df['Start Station'].mode()[0])

    # display most commonly used end station
    print('\nMost Common End Station: ', df['End Station'].mode()[0])

    # creates a dataframe with the combination of start/end stations and
    #   counts the occurrence of each one
    combination = df.groupby(['Start Station', 'End Station']).count()

    # selects the first column of the dataframe to transform it into a series
    combination = combination.iloc[:,0]

    # display most frequent combination of start station and end station trip
    print('')
    print('Most Common Start/End Station Combination: ', combination.idxmax())

    print("\nThis took %s seconds.\n" % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    total_travel_time_hours = total_travel_time//3600
    total_travel_time_minutes = (total_travel_time%3600)//60
    total_travel_time_seconds = (total_travel_time%3600)%60
    print('Total Travel Time: {} Hours, {} Minutes, {} Seconds'
            .format(total_travel_time_hours, total_travel_time_minutes,
                    total_travel_time_seconds))
    print('or\nTotal Travel Time: {} Seconds'.format(total_travel_time))

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    mean_travel_time_minutes = int(mean_travel_time//60)
    mean_travel_time_seconds = int(mean_travel_time%60)
    print('\nMean Travel Time: {} Minutes, {} Seconds'
            .format(mean_travel_time_minutes, mean_travel_time_seconds))
    print('or\nMean Travel Time: {} Seconds'.format(mean_travel_time))

    print("\nThis took %s seconds.\n" % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # creates a dataframe with the counts of user types
    #   .iloc transforms the dataframe into a series
    user_types_count = df.groupby(['User Type']).count().iloc[:,0]

    # Display counts of user types
    #   .to_string makes only the user types and counts be shown
    print('User Types Count:\n')
    print(user_types_count.to_string(header=False))

    # Display counts of gender
    # "if clause" to treat Washington case, with no values for Gender
    if 'Gender' not in df:
        print('\nGenders Count: No Information')
    else:
        # creates a dataframe with the counts of genders
        #   .iloc transforms the dataframe into a series
        genders_count = df.groupby(['Gender']).count().iloc[:,0]

        #   .to_string makes only the genders and counts be shown
        print('\nGenders Count:\n')
        print(genders_count.to_string(header=False))

    # Display earliest, most recent, and most common year of birth
    # "if clause" to treat Washington case, with no values for Birth Year
    if 'Birth Year' not in df:
        print('\nEarliest Year of Birth: No Information')
        print('\nMost Recent Year of Birth: No Information')
        print('Most Common Year of Birth: No Information')
    else:
        print('\nEarliest Year of Birth: ', int(df['Birth Year'].min()))
        print('\nMost Recent Year of Birth: ', int(df['Birth Year'].max()))
        print('')
        print('Most Common Year of Birth: ', int(df['Birth Year'].mode()[0]))

    print("\nThis took %s seconds.\n" % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        print('\nWould you like to see the raw data? Enter yes or no.\n')
        display_raw_data = input()
        current_row = 0     #row that will be displayed
        while display_raw_data.lower() == 'yes':
            print('')
            print(df.iloc[current_row:current_row + 5,:])
            print('\nWould you like to see 5 more rows? Enter yes or no.\n')
            display_raw_data = input()
            current_row += 5

        print('\nWould you like to restart? Enter yes or no.\n')
        restart = input()
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
