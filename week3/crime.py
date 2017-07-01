# data from: https://github.com/emorisse/FBI-Hate-Crime-Statistics

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Polygon

# reading crime data
crime = pd.read_csv("crime-data.csv")
crime = crime.dropna()

# converting floats to ints
crime.loc[:, '1st quarter'] = np.int64(crime.loc[:, '1st quarter'])
crime.loc[:, '2nd quarter'] = np.int64(crime.loc[:, '2nd quarter'])
crime.loc[:, '3rd quarter'] = np.int64(crime.loc[:, '3rd quarter'])
crime.loc[:, '4th quarter'] = np.int64(crime.loc[:, '4th quarter'])

# adding modifying columns
crime['Total Crime'] = crime['1st quarter'] + crime['2nd quarter'] \
                        + crime['3rd quarter'] + crime['4th quarter']
crime = crime[['State', 'Agency type', 'Agency name', 'Population', 'Total Crime']]

# removing states without universities or colleges
list_of_uc = crime[crime['Agency type'] == 'Universities and Colleges']
list_of_uc = list_of_uc['State']
list_of_uc = list(set(list(list_of_uc)))

for state in crime['State']:
    if state not in list_of_uc:
        crime = crime[crime['State'] != state]

# making data with totals by state
crime_total = crime.groupby('State').sum()
crime_uc = crime[crime['Agency type'] == 'Universities and Colleges']
crime_uc = crime_uc.groupby('State').sum()

crime_total = crime_total.reset_index()
crime_uc = crime_uc.reset_index()

crime = pd.merge(crime_total, crime_uc, on='State',
                 suffixes=[' in State', ' in Schools'])

# code list of states
state_dict = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY',
}

# creating list of state codes for plotly
crime['Code'] = crime['State'].map(state_dict)

# adding percentage
crime['Percentage in Schools'] =  100 * crime['Total Crime in Schools'] / crime['Total Crime in State']

# removing underscores from names
for i in range(len(crime.loc[:, 'State'])):
    if '_' in crime.loc[i, 'State']:
        crime.loc[i, 'State'] = crime.loc[i, 'State'].replace("_", " ")

# creating map
m = Basemap(projection='mill',llcrnrlat=20,urcrnrlat=50,
            llcrnrlon=-130,urcrnrlon=-60,resolution='f')

# drawing lines and making them all white
m.drawcoastlines(color='#FFFFFF')
m.drawstates(color='#FFFFFF')
m.fillcontinents(color='#FFFFFF', lake_color='#FFFFFF')
m.drawmapboundary(fill_color='#FFFFFF', color='#FFFFFF')

# making states for the usa bordered so that they are visible
m.readshapefile('st99_d00', name='states', drawbounds=True, color='#FFFFFF')

# list of state names
state_names = []
for shape_dict in m.states_info:
    state_names.append(shape_dict['NAME'])

# list of states in table
list_of_states = crime['State']

# create axis to plot on
ax = plt.gca()

# looping through states and plotting according to school crime ratio
sent = 0
for state in list_of_states:
    seg = m.states[state_names.index(state)]
    fill = Polygon(seg, facecolor='#e60000', edgecolor='#FFFFFF',
                   alpha=crime.loc[sent, 'Percentage in Schools'] * 0.05)
    sent += 1
    ax.add_patch(fill)

# states with an undefined percentage
not_in_crime = [state for state in state_names if state not in list(list_of_states)]
not_in_crime = list(set(list(not_in_crime)))
not_in_crime

# looping through states and making them grey bc of no crime
sent = 0
for state in not_in_crime:
    seg = m.states[state_names.index(state)]
    fill = Polygon(seg, facecolor='#e6e6e6', edgecolor='#FFFFFF')
    sent += 1
    ax.add_patch(fill)

plt.title('Percentage of Crime in Universities & Colleges for States (2013)')
plt.annotate('redder: higher portion of state crime in commited in schools',
             xy=(0.1,0), xycoords='axes fraction')
plt.annotate('grey: no recorded crimes in schools', xy=(0.1, -0.05),
             xycoords='axes fraction')

plt.show()
