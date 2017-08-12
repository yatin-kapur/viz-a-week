# data from http://ede.grid.unep.ch.com

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as tkr
from matplotlib.ticker import FormatStrFormatter
plt.style.use('ggplot')

# loading datasets and removing rows with NA values
arrivals = pd.read_csv('arrivals.csv')
departures = pd.read_csv('departures.csv')

del arrivals['UN Code']
del departures['UN Code']
del arrivals['Arab World']
del departures['Arab World']
# we only need one subregion column so remove from departures
del departures['GEO Region']

arrivals = arrivals.dropna(how='any')
departures = departures.dropna(how='any')

# keeping only the relevant columns
columns = [col for col in list(arrivals)
           if col.startswith('1') or
           col.startswith('2') or
           col == 'Country Name']

# merging the tables
data = pd.merge(arrivals[['GEO Region']+columns], departures[columns],
                on='Country Name', suffixes=('_a', '_d'))

# summing data by subregion
data = data.groupby('GEO Region').sum()

# generating difference of departures - arrivals
for col in columns:
    if col == 'Country Name':
        continue
    data[col] = data[col + '_a'] - data[col + '_d']
    del data[col + '_a']
    del data[col + '_d']

# transposing data so that time periods are indexed
data = data.T

fig, ax = plt.subplots()

# plotting
for label in data.columns:
    plt.plot_date(data.index, data[label], fmt='-')

ax.yaxis.set_major_formatter(FormatStrFormatter('%.0f'))
ax.yaxis.set_major_formatter(
        tkr.FuncFormatter(lambda y,  p: format(int(y), ',')))
plt.legend()
plt.ylabel('Number of People')
plt.yticks(rotation=45)
plt.xlabel('Year')
plt.title('Tourism: Arrivals - Departures, by GEO Region (1995-2013)')

fig.set_size_inches(9, 5)
plt.savefig('figure_1.png', format='png', dpi=1200)
