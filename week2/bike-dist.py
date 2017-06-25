# data from http://www.bayareabikeshare.com/open-data

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# aesthetics
plt.style.use("bmh")

# reading the data
babs = pd.read_csv("201608_trip_data.csv")
weather = pd.read_csv("201608_weather_data.csv")

# keeping columns that are needed
babs = babs[['Start Date', 'Duration']]
babs['Start Date'] = [x.split()[0] for x in babs.loc[:, 'Start Date']]

weather['Temperature (C)'] = (weather['Mean TemperatureF'] - 32) * (5/9)
weather = weather[['PDT', 'Temperature (C)']]
weather = weather.rename(columns={'PDT': 'Start Date'})

# adding weather columns
bike_data = pd.merge(babs, weather, how='right')

# averaging the duration for the temperatures
bike_data = bike_data.groupby('Temperature (C)').mean()
bike_data = bike_data.reset_index()

# graph
sns.regplot(data = bike_data, x = 'Temperature (C)', y = 'Duration', fit_reg = False, marker='h', color='black')
plt.xlim(-2,)
plt.ylabel('Duration (s)')

plt.show()
