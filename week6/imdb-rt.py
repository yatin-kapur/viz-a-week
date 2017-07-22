# imdb data from http://www.imdb.com/chart/top?sort=ir,desc&mode=simple&page=1

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import bs4 as bs
import urllib.request
import re

imdb_wp = urllib.request.urlopen('http://www.imdb.com/chart/top?sort=ir,desc&mode=simple&page=1')
soup = bs.BeautifulSoup(imdb_wp, 'lxml')

table_data = soup.table

# putting data of first 100 into a list
movies = []
sent = 0
for movie in table_data.find_all('td', {'class': 'titleColumn'}):
    movies.append(movie.text)
    movies[sent] = movies[sent].lstrip('(\n| |.)')[:-8]
    movies[sent] = movies[sent].lstrip('(\n|0|1|2|3|4|5|6|7|8|9|.)')[6:]
    # handling case for special bollywood movie
    if movies[sent] == 'Drishyam':
        movies[sent] = 'Drishyam_2015'
    sent += 1

# putting imdb ratings in a list
imdb_ratings = []
sent = 0
for movie in table_data.find_all('td', {'class': 'imdbRating'}):
    imdb_ratings.append(movie.text)
    imdb_ratings[sent] = float(imdb_ratings[sent][1:4])
    sent += 1

    # getting the rotten tomatoes ratings in a list
rt_ratings = list(range(250))
sent = 0
for movie in movies:
    try:
        temp = re.sub(r' ', '_', movie).lower()
        temp = re.sub(r':', '', temp)
        temp = re.sub(r'^(the_)','', temp)
        url = 'https://www.rottentomatoes.com/m/' + temp
        rt_wp = urllib.request.urlopen(url)
        rt_soup = bs.BeautifulSoup(rt_wp, 'lxml')
        if rt_soup.find_all('span', {'class':'meter-value superPageFontColor'}):
            rt_ratings[sent] = (rt_soup.find_all('span', {'class':'meter-value superPageFontColor'})[0].text)
            sent += 1
        else:
            sent += 1
    except urllib.error.HTTPError:
        sent += 1
    except UnicodeEncodeError:
        sent += 1

# make dataframe of the ratings and drop the values that were not found in rotten tomatoes
for i in list(range(250)):
    if type(rt_ratings[i]) is str:
        rt_ratings[i] = float(rt_ratings[i][:-1])

data = pd.DataFrame({'Movie': movies, 'IMDB Rating': imdb_ratings, 'Tomatometer %': rt_ratings})
for i in list(range(250)):
    if type(rt_ratings[i]) is int:
        data.loc[i, 'Tomatometer %'] = False

data = data[data['Tomatometer %'] != False]

sns.stripplot(data=data, x='IMDB Rating', y='Tomatometer %')
plt.title('Top 250 IMDB Rated Movies and Their Tomatometer %')

plt.savefig('figure_1.png', format='png', dpi=1200)
