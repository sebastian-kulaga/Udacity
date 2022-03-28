"""
Script created for Udacity Data Scientist Foundations for Credit Suisse course.
It loads bikeshare data from city provided by user (Chicago, New York, Washington),
filters it and calculates various stats.
Three CSV files provided by Udacity course are needed to run this script without any issues.
"""

import time
import pandas as pd

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}
MONTH_LIST = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
DAY_LIST = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    print('Please provide from which city you would like to get data.')
    month = 'all'
    day = 'all'
    city_list = list(CITY_DATA.keys())
    filter_list = ['yes', 'no']
    city = check_and_return_if_in_list(city_list, 'city')

    print('Do you want to filter data by month, day or both?')
    user_input = check_and_return_if_in_list(filter_list, 'filter')
    if user_input == 'no':
        return city, month, day

    print('Please provide for which month you like to get data.')
    month = check_and_return_if_in_list(MONTH_LIST, 'month')

    print('Please provide for which day you like to get data.')
    day = check_and_return_if_in_list(DAY_LIST, 'day')
    print('-' * 40)
    return city, month, day


def check_and_return_if_in_list(checking_list, input_flag):
    """
    Checks if user input is present in list.
    Args:
        (list[(str)]) checking_list - list of months or days
        (str) input_flag - string that marks what to pick in input_dictionary
    Returns:
        (str) output - city, filter option, day or month picked by user if present in list, 
                       or None if not
    """
    input_dictionary = {'city': 'Type Chicago, New York or Washington: ', 'filter': 'Type yes or no: ',
                        'month': 'Type All, January, February, March, April, May, June. '
                                 'You can use lowercase and short names for months: ',
                        'day': 'Type all, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or Sunday. '
                               'You can use lowercase and short names for days: '}

    while True:
        user_input = input(input_dictionary[input_flag]).lower()
        if input_flag == 'city':
            if user_input == 'new york':
                user_input = 'new york city'
        output_list = [d for d in checking_list if d.startswith(user_input)]
        if output_list:
            output = output_list[0]
            split_output = output.split(' ')
            output = output.capitalize()
            if len(split_output) > 1:
                capitalized_words = [w.capitalize() for w in split_output]
                output = " ".join(capitalized_words)
            print('You have picked {}'.format(output))
            break
    return output.lower()


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - pandas DataFrame containing city data filtered by month and day
    """

    start_time = time.time()
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['Month'] = df['Start Time'].dt.month_name()
    df['Day'] = df['Start Time'].dt.day_name()
    # add hour column
    df['Hour'] = df['Start Time'].dt.hour
    # filter by month if applicable
    if month != 'all':
        # filter by month to create the new dataframe
        df = df[df['Month'] == month.title()]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['Day'] == day.title()]

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)
    return df


def time_stats(df):
    """
    Displays statistics on the most frequent times of travel.

    Args:
        (DataFrame) df - input DataFrame with bike data, that is used for all calculations
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    get_most_common(df, 'Month')
    get_most_common(df, 'Day')
    get_most_common(df, 'Hour')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def get_most_common(df, input_string):
    """
    Calculates and prints most common month/day/hour of travel.

    Args:
        (DataFrame) df - input DataFrame with bike data, that is used for all calculations
        (str) input_string - string with provided input to select correct column for calculation
    """
    most_common = df[input_string].value_counts()
    most_common_value = most_common.idxmax()
    most_common_count = most_common.max()
    print(f'Most Common {input_string}: {most_common_value}, Count: {most_common_count}')


def station_stats(df):
    """
    Displays statistics on the most popular stations and trip.
    
    Args:
        (DataFrame) df - input DataFrame with bike data, that is used for all calculations
    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    get_most_common(df, 'Start Station')

    get_most_common(df, 'End Station')

    station_tuple = df.groupby(['Start Station', 'End Station']).size().idxmax()
    station_count = df.groupby(['Start Station', 'End Station']).size().max()
    output_string = f'Most frequent combination of start and end station is: {station_tuple[0]}, ' \
                    f'and: {station_tuple[1]}'
    print(output_string)
    print(f'This trip was done {station_count} times')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """
    Displays statistics on the total and average trip duration.

    Args:
        (DataFrame) df - input DataFrame with bike data, that is used for all calculations
    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    print('Displaying total travel time')
    sum_of_travels = df['Trip Duration'].sum()
    get_calculated_time(sum_of_travels, 'Total')

    print('Displaying average travel time')
    mean_travel_time = df['Trip Duration'].mean()
    get_calculated_time(mean_travel_time, 'Average')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def get_calculated_time(input_time, flag):
    """
    Calculates and prints most common month/day/hour of travel.
    
    Args:
        (int) time - int that contains seconds
        (str) flag - string to print correct calculation - sum or avg of travels
    """
    input_seconds = input_time
    day = input_time // (24 * 3600)
    input_time = input_time % (24 * 3600)
    hour = input_time // 3600
    input_time %= 3600
    minutes = input_time // 60
    input_time %= 60
    seconds = input_time
    print(f'{flag} time is {input_seconds} seconds')
    print(f'That is {day} days, {hour} hours, {minutes} minutes and {seconds} seconds')


def user_stats(df):
    """
    Displays statistics on bikeshare users.

    Args:
        (DataFrame) df - input DataFrame with bike data, that is used for all calculations
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    print('Displaying user types:')
    user_types_dict = df['User Type'].value_counts().to_dict()
    print(f'There is {len(user_types_dict.keys())} user types')
    for k, v in user_types_dict.items():
        print(f'{k} user type with total count of {v}')

    print('Displaying gender data')
    if 'Gender' in df.columns:
        gender_value_counts = df['Gender'].value_counts()
        gender_index = gender_value_counts.index
        gender_values = gender_value_counts.values
        for i, element in enumerate(gender_index):
            print(f'{gender_index[i]}, total count: {gender_values[i]}')
    else:
        print('There is no gender data to display.')

    print('Displaying birth date values')
    if 'Birth Year' in df.columns:
        most_recent_birth_date = df['Birth Year'].max()
        earliest_birth_date = df['Birth Year'].min()
        print(f'{int(earliest_birth_date)} is earliest birth date.')
        print(f'{int(most_recent_birth_date)} is most recent birth date.')
        get_most_common(df, 'Birth Year')
    else:
        print('There is no birth data to display.')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def display_dataframe(df):
    """
    Displays five rows of data, waits for user input and potentially displays another.
    Works in loop.

    Args:
        (DataFrame) df - input DataFrame with bike data, that is used for all calculations
    """
    filter_list = ['yes', 'no']
    starting_row = 0
    print('Do you want to see 5 rows of data?')
    while True:
        user_input = check_and_return_if_in_list(filter_list, 'filter')
        if user_input == 'no':
            return
        else:
            print("Displaying 5 rows of data:")
            # Use pandas option to set max displayed rows and columns (5 rows and all cols)
            with pd.option_context('display.max_rows', 5, 'display.max_columns', None):
                print(df.loc[starting_row:starting_row + 4])
            starting_row = starting_row + 5
            print('-' * 40)
            print('Do you want to see another 5?')


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_dataframe(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
