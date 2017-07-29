# data from http://www.tdcj.state.tx.us/death_row/dr_executed_offenders.html

import matplotlib.pyplot as plt
import pandas as pd
import bs4 as bs
import urllib.request

# race, thanks, sorry dictionary
races = {'Black': 0, 'White': 0, 'Hispanic': 0, 'Other': 0}
thanks = {'Black': 0, 'White': 0, 'Hispanic': 0, 'Other': 0}
sorry = {'Black': 0, 'White': 0, 'Hispanic': 0, 'Other': 0}

def count(race, url_ext):
    """
    takes the parameters for the inmate and produces data, updating respective dictionaries
    """
    try:
        url = 'http://www.tdcj.state.tx.us/death_row/{}'.format(url_ext)
        page = urllib.request.urlopen(url)
        soup = bs.BeautifulSoup(page, 'lxml')
    except urllib.error.HTTPError:
        return

    # getting last sentence
    try:
        data = soup.find_all('div', {'id': 'body'})
        last = list(data[0])[21]
        last = last.get_text()
        last = last.split(' ')
    except:
        return

    # counting sorry
    for word in last:
        if word.lower() == 'sorry':
            sorry[race] += 1

    # counting thanks
    for word in last:
        if word.lower() == 'thanks' or word.lower() == 'thank':
            thanks[race] += 1

    # races
    races[race] += 1

# getting the table from the
url = 'http://www.tdcj.state.tx.us/death_row/dr_executed_offenders.html'
page = urllib.request.urlopen(url)
soup = bs.BeautifulSoup(page, 'lxml')

# table entries for inmates
table = soup.table
rows = table.find_all('tr')
rows = rows[1:]

for row in rows:
    url_ext = row.find_all('a')[1]['href']
    race = list(row)[17].text
    race = race.replace(' ', '')

    count(race, url_ext)

# making the data frame with the entries
data = pd.DataFrame({'Sorry': sorry, 'Thanks': thanks, 'Entries': races})
data['Sorry/Entry'] = data.Sorry/data.Entries
data['Thanks/Entry'] = data.Thanks/data.Entries
data = data.drop('Other')

fig = plt.figure()

plt.style.use('dark_background')

ax = fig.add_subplot(111)

width = 0.1

data['Sorry/Entry'].plot(kind='bar', color='#61E71A',
                         width=width, position=1, label='Sorry/Statement')
data['Thanks/Entry'].plot(kind='bar', color='#35E4E7',
                          width=width, position=0, label='Thanks/Statement')

ax.legend()
plt.xticks(rotation=0)

plt.title('Last Statements Before Death Penalty')

plt.savefig('figure_1.png', format='png', dpi=1200)
