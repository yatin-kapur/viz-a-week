import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

data = pd.read_csv('https://raw.githubusercontent.com/soccermetrics/project-data/master/english-premier-league-2011-2012/Goals.csv')

data = data[['Matchday', 'Away Team', 'Home Team', 'Team']]

for x in range(len(data)):
    if data.loc[x, 'Team'] == data.loc[x, 'Away Team']:
        data.loc[x, 'G'] = 'A'
    else:
        data.loc[x, 'G'] = 'H'

sns.countplot(data.Matchday, hue=data.G)
plt.title('Home Goals vs. Away Goals Per Matchday PL 2011-12')

plt.show()
