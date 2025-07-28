import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from itertools import combinations
from collections import Counter

df = pd.read_csv("data/netflix_titles.csv")
print(df.head())

df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
df.dropna(subset=['date_added', 'listed_in', 'rating', 'cast'], inplace=True)

df_genres = df.copy()
df_genres['genres'] = df_genres['listed_in'].str.split(', ')
df_genres = df_genres.explode('genres')

genre_counts = df_genres.groupby(['release_year', 'genres']).size().unstack().fillna(0)

import matplotlib.pyplot as plt
genre_counts.rolling(3).mean().plot(figsize=(15, 6))
plt.title("Genre Popularity Over Time")
plt.xlabel("Year")
plt.ylabel("Number of Titles")
plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
plt.tight_layout()
plt.show()

cast_df = df[df['cast'].notnull()].copy()
cast_df['actors'] = cast_df['cast'].str.split(', ')

pair_counter = Counter()
for actors in cast_df['actors']:
    for pair in combinations(sorted(actors), 2):
        pair_counter[pair] += 1

co_df = pd.DataFrame(pair_counter.items(), columns=['pair', 'count'])
top_pairs = co_df.sort_values(by='count', ascending=False).head(100)

actors = list(set([a for pair in top_pairs['pair'] for a in pair]))
matrix = pd.DataFrame(0, index=actors, columns=actors)

for (a1, a2), count in zip(top_pairs['pair'], top_pairs['count']):
    matrix.loc[a1, a2] = count
    matrix.loc[a2, a1] = count

plt.figure(figsize=(12, 10))
sns.heatmap(matrix, cmap="Reds")
plt.title("Actor Co-occurrence Heatmap (Top Pairs)")
plt.show()

rating_trend = df.groupby(['release_year', 'rating']).size().unstack().fillna(0)

rating_trend.plot(kind='area', stacked=True, figsize=(14, 6), cmap='tab20c')
plt.title("Netflix Content Ratings Over Time")
plt.xlabel("Release Year")
plt.ylabel("Number of Titles")
plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
plt.tight_layout()
plt.show()