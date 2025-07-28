import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title("🎬 Netflix Movie & TV Show Insights")
st.markdown("Explore trends in genres, ratings, and actor collaborations on Netflix over the years.")

df = pd.read_csv("data/netflix_titles.csv")

st.metric("Total Titles", df.shape[0])
st.metric("Total Unique Actors", df['cast'].dropna().str.split(', ').explode().nunique())

df['genres'] = df['listed_in'].str.split(', ')
genre_df = df.explode('genres')
selected_genre = st.selectbox("Choose a Genre", sorted(genre_df['genres'].unique()))
genre_year_df = genre_df[genre_df['genres'] == selected_genre]
trend = genre_year_df.groupby('release_year').size()

st.line_chart(trend)

st.subheader("🔞 Content Rating Trends Over Years")
rating_trend = df.groupby(['release_year', 'rating']).size().unstack().fillna(0)

fig, ax = plt.subplots(figsize=(15, 6))
rating_trend.plot.area(ax=ax, cmap="tab20c")
plt.title("Rating Distribution Over Time")
st.pyplot(fig)

year = st.slider("Release Year", int(df['release_year'].min()), int(df['release_year'].max()), 2020)
genre = st.text_input("Search by Genre Keyword", "Drama")

filtered_df = df[(df['release_year'] == year) & (df['listed_in'].str.contains(genre, case=False))]
st.write(f"Found {filtered_df.shape[0]} titles")
st.dataframe(filtered_df[['title', 'type', 'rating', 'date_added']])