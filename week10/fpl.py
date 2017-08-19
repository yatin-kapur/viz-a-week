# data from https://fantasy.premierleague.com/drf/bootstrap-static

import pandas as pd
import matplotlib.pyplot as plt
import json
import urllib.request

# extracting data from site
fpl_data = urllib.request.urlopen('https://fantasy.premierleague.com/drf/bootstrap-static').read()
fpl_data = json.loads(fpl_data)

# columns for the data frame (positions)
columns = []
for i in range(4):
    columns.append(fpl_data['element_types'][i]['plural_name'])

# list of elements
players = fpl_data['elements']

# making teams list
teams = []
for i in range(1, 21):
    temp_list = []
    for player in players:
        if player['team'] == i:
            temp_list.append(player)
    teams.append(temp_list)
num_of_players = [len(x) for x in teams]

# cumulative prices
prices = []
for team in teams:
    price = 0
    for player in team:
        price += player['now_cost'] - player['cost_change_start']
    prices.append(float(price / 10))

team_names = [x['name'] for x in fpl_data['teams']]

# data frame
data = pd.DataFrame()
data['Team'] = team_names
data['Players'] = num_of_players
data['Total Cost'] = prices
data['Average Cost'] = data['Total Cost'] / data['Players']

# plotting
plt.style.use('seaborn-white')
fig, ax = plt.subplots()
plt.plot(data['Average Cost'], '-o', color='black')
plt.xticks(list(range(20)), team_names, rotation=90)
plt.xlabel('Club')
plt.ylabel('Average Fantasy Price')
plt.title('Average Fantasy Premier League Price for Each Club', fontsize=30)

fig.set_size_inches(10, 12)
plt.savefig('figure_1.png', format='png', dpi=1200)
