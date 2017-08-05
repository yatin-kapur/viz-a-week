# data from http://uwflow.com

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
plt.style.use('dark_background')

# tax gdp data
tax = pd.read_csv('tax-rev-gdp.csv')
tax = tax[tax['Year'] == 2013]
tax = tax[['Entity', 'Year', 'Total Taxes']]

# education spend data
edu = pd.read_csv('spending-edu.csv')
edu = edu[edu['Year'] == 2013]
edu = edu[['Entity', 'Total Government Expenditure on Education']]

# merging table into one data set
data = pd.merge(tax, edu, on='Entity')

sns.lmplot(data=data, x='Total Taxes', y='Total Government Expenditure on Education')
plt.xlabel('Total Taxes as % of GDP')
plt.ylabel('Total Expenditure on Education as % of GDP')
plt.title('Expenditure on Education vs. Total Taxes Collected (2013)')
plt.xticks(rotation=90)

plt.savefig('figure_1.png', figsize=(15,20), format='png', dpi=1200)
