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

# reading data for spending on healthcare
health_spending = pd.read_csv("hc-exp.csv")

# deleting unneeded columns
del health_spending['Country code']
health_spending.index = health_spending['Entity']
del health_spending['Entity']

print(health_spending.head())
