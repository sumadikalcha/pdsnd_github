import pandas as pd
import numpy as nd
import time

#Define the Global Valid Lists:

#City data showing the CSV files for each city to be loaded
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

#Create the required lists for proper validation of the input
cities = ['chicago', 'washington', 'new york city']
months = ['january', 'february', 'march', 'april', 'may', 'june']
days = ['sunday','monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')


    while True:
        # get user input for city (chicago, new york city, washington).
        city = input("Please choose the city : Chicago, Washington, New York City\n")
        city = city.lower()
        if city.lower() in cities:
            break
        else:
            print("Can you please check if you have given the right input. \nInputs are case sensitive, Please give Give another try")

    while True:
        # get user input for month (all, january, february, ... , june)
        month = input("Please select a month from January, February, March, April, May, June or All only\n")
        month = month.lower()
        #making sure all is accepted
        if month == 'all':
            break
        #check for the valid months as an input
        elif month.lower() in months:
            break
        else:
            print("Can you please check if you have given the right input. \nInputs are case sensitive, Please give Give another try")

    while True:
        # get user input for day of week (all, monday, tuesday, ... sunday)
        day = input("Please select a day from Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or All only\n")
        day = day.lower()
        # Handle all and make it as an acceptable input
        if day == 'all':
            break
        # Check for the validity of the inputs in days list
        elif day.lower() in days:
            break
        else:
            print("Can you please check if you have given the right input. \nInputs are case sensitive, Please give Give another try")
    #Separate the various methods by a good line with 40 dashes
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

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # extract month and day of week from Start Time to create new column, Month and the day of the week.
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month_index = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month_index]

        # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df, city, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    print ("Your Choice : \nCity = {} \nMonth = {} \nDay Of the Week : {} \n".format(city.title(), month.title(), day.title()))
    # display the most common month
    popular_month = df['month'].mode()[0]
    #Get the required name for the corrensponding month number
    popular_month_name = int(popular_month)-1
    print ("The Most Popular month is : ", months[popular_month_name].title())
    print()
    # display the most common day of week
    popular_dow = df['day_of_week'].mode()[0]
    print ("The Most Popular day of the week is : ", popular_dow)
    print()
    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print ("The Most Popular Hour is : ", popular_hour)
    print()

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_StartStation = df['Start Station'].mode()[0]
    print ("The Most Popular Start Station is : ", popular_StartStation)
    #Add additional information as to why this was the popular station by retrieving the number of trips starts at this station
    print ("And, the number of trips starting in that station are : ", df[df['Start Station'] == popular_StartStation]['Start Station'].count())
    print()

    # display most commonly used end station
    popular_EndStation = df['End Station'].mode()[0]
    print ("The Most Popular End Station is : ", popular_EndStation)
    #Add additional information as to why this was the popular station by retrieving the number of trips ending at this station
    print ("And, the number of trips ending in that station are : ", df[df['End Station'] == popular_EndStation]['End Station'].count())
    print()

    # display most frequent combination of start station and end station trip.. Achieve this by adding the Start and End Station
    df['trip'] = df['Start Station'] + " to " + df['End Station']
    popular_trip = df['trip'].mode()[0]
    print ("The Most Popular trip is : ", popular_trip)
    #Display the number of times this trip is taken
    print ("And, the Number of times this trip is taken : ", df[df['trip'] == popular_trip]['trip'].count())
    print()

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    trip_duration = df['Trip Duration'].sum()
    trip_mean = df['Trip Duration'].mean()

    # display total travel time
    print ("The Total trip duration is : ", trip_duration)
    # display mean travel time
    print ("\nThe mean travel time is : ", trip_mean)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print ("The counts by User types are :\n")
    print (df.groupby(['User Type'])['User Type'].count())

    # Display counts of gender
    try:
        print ()
        print ("The counts by Gender are:\n", df.groupby(['Gender'])['Gender'].count())
    except KeyError:
        print ("Gender data is not represented for this city")


    # Display earliest, most recent, and most common year of birth
    try:
        print ("\nThe oldest user is born in the year:\n", int(df['Birth Year'].min()))
        print ("\nThe yougest user is born in the year:\n", int(df['Birth Year'].max()))
        print ()
        common_year_of_birth = df['Birth Year'].mode()
        print ("The most common year of birth is: {}".format(int(common_year_of_birth)))
    except KeyError:
        print ("Birth Year data is not represented for this city")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def displayData (df, row_num, city):
    """Used to display data row wise in a user readable format """
    i=0
    #Iteration as 5 is fixed.
    while i<5:
        print("[\nStart Time : {} ,".format(df.iloc[row_num]['Start Time']))
        print("End Time : {} ,".format(df.iloc[row_num]['End Time']))
        print("Trip Duration : {} ,".format(df.iloc[row_num]['Trip Duration']))
        print("Start Station : {} ,".format(df.iloc[row_num]['Start Station']))
        print("End Station : {} ,".format(df.iloc[row_num]['End Station']))
        print("User Type : {} ,".format(df.iloc[row_num]['User Type']))
        #Handling Washington city where the values are not given
        if city not in ('washington'):
            print("Gender : {} ,".format(df.iloc[row_num]['Gender']))
            print("Birth Year : {}".format(df.iloc[row_num]['Birth Year']))
        else:
            #printing None for the data where not present
            print("Gender : None ,")
            print("Birth Year : None")
        print("]\n")
        row_num += 1
        i+=1
    return row_num

def main():
    """ Retrieves the BikeShare data metrics by calling various functions"""
    while True:
        #Take inputs for the city, month, day from the below function
        city, month, day = get_filters()
        #Load the data into a Pandas Data Frame
        df = load_data(city, month, day)
        #Perform the Time statistics like, popular hour etc.
        time_stats(df, city, month, day)
        #Perform the Station Statistics
        station_stats(df)
        #Perform the Trip Duration Statistics
        trip_duration_stats(df)
        #Perform the statitics by the user types and other demographics
        user_stats(df)

        row_num = 0
        #Checking if the data needs to be displayed by taking input from user.
        while True:
            show_data = input("\nWould you still like to see the actual data? Enter yes or no.\n")
            if show_data not in ('yes', 'no'):
                print("\nPlease enter yes or no only. you entered:", show_data)
            #if yes, show only the first 5 rows and keep looping.
            elif show_data == 'yes':
                print("\n Showing only 5 rows")
                row_num = displayData(df, row_num, city)
            #Break when NO.
            else:
                break
        #Check if other city or any dimension of the data needs to be relooked upon.
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
