# data from https://ourworldindata.org

import pandas as pd
import numpy as np
import matplotlib as plt
import seaborn as sns

# reading data into life expetancy dataframe
life_expectancy = pd.read_csv("life-expectancy.csv")

# deleting unneeded columns
del life_expectancy['Indicator Name']
del life_expectancy['Indicator Code']
del life_expectancy['Country Code']
del life_expectancy['2016']
life_expectancy = life_expectancy.iloc[:, :-1]
life_expectancy.index = life_expectancy['Country Name']
del life_expectancy['Country Name']

# removing countries without entries
life_expectancy = life_expectancy.dropna()

# unstacking the years, turning it into a dataframe from series and resetting indices to prepare for merge
life_expectancy = life_expectancy.stack()
life_expectancy = pd.DataFrame(life_expectancy)
life_expectancy = life_expectancy.reset_index()
life_expectancy = life_expectancy.rename(columns = {'level_1':'Year', 0:'Life Expectancy'})
life_expectancy['Year'] = life_expectancy['Year'].apply(np.int64) # making year values integers

# reading data for spending on healthcare
health_spending = pd.read_csv("hc-exp.csv")

# deleting unneeded columns
del health_spending['Country code']
health_spending = health_spending.rename(columns = {'Entity': 'Country Name'})

# defining years to merge on
years = np.arange(2002, 2014, 1)

# removing elements that are not in the years range
for i in range(len(health_spending.loc[:, 'Year'])):
    if health_spending.loc[i, 'Year'] not in years:
        health_spending.loc[i, 'Year'] = np.nan

health_spending = health_spending.dropna()
health_spending['Year'] = health_spending['Year'].apply(np.int64)

for i in range(len(life_expectancy.loc[:, 'Year'])):
    if life_expectancy.loc[i, 'Year'] not in years:
        life_expectancy.loc[i, 'Year'] = np.nan

life_expectancy = life_expectancy.dropna()
life_expectancy['Year'] = life_expectancy['Year'].apply(np.int64)

# merge
final_df = pd.merge(health_spending, life_expectancy, on=['Country Name', 'Year'])

print(final_df.head())
