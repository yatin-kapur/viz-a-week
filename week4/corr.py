import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# read data
bribes = pd.read_csv('share-of-people-paying-bribes-2013.csv')
corruption = pd.read_csv('average-rating-of-corruption-perception.csv')

bribes = bribes[['Entity', 'Share of people who have bribed']]
corruption = corruption[['Entity', 'Corruption Perception Rating']]

# merge data
data = pd.merge(bribes, corruption, on='Entity')
data = data.sort_values('Corruption Perception Rating', ascending=0)

# style set
plt.style.use('dark_background')

# plot graph
sns.regplot(data=data, x='Corruption Perception Rating',
            y='Share of people who have bribed',
            fit_reg=False, color='#22AF5D',
            scatter_kws={'alpha':0.8}, marker='x')
plt.grid(color='#8c8c8c')
plt.xticks(rotation=90)
plt.title('Corruption Perception Rating vs. Share of Bribes (2013)',
            fontsize=20)
plt.xlabel(s='Corruption Perception Rating', labelpad=10)
plt.ylabel(s='Share of People Who Have Bribed', labelpad=10)

plt.show()
