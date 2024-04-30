#!/usr/bin/env python
# coding: utf-8

# In[8]:


import streamlit as st
import pandas as pd

# Load the dataset
def load_data():
    return pd.read_csv('new_dataset.csv')

movies_df = load_data()

# Convert 'release_date' column to datetime format
movies_df['release_date'] = pd.to_datetime(movies_df['release_date'])

# Sidebar filters
st.sidebar.title('Movie Filters')

# Budget range
budget_range = st.sidebar.slider('Select Budget Range', min_value=0, max_value=movies_df['budget'].max(), step=1000000)

#genre
genres = movies_df['genres'].str.split(', ').explode().unique()
selected_genre = st.sidebar.selectbox('Select Genre', genres)

# Keywords
keywords = st.sidebar.text_input('Enter Keywords')

# Original Language
original_language = st.sidebar.selectbox('Select Original Language', movies_df['original_language'].unique())

# Popularity range
popularity_min = st.sidebar.slider('Select Minimum Popularity', min_value=movies_df['popularity'].min(), max_value=movies_df['popularity'].max(), step=0.1)
popularity_max = st.sidebar.slider('Select Maximum Popularity', min_value=movies_df['popularity'].min(), max_value=movies_df['popularity'].max(), step=0.1)
popularity_range = (popularity_min, popularity_max)  # Ensure it's a tuple

# Release Date
st.sidebar.subheader("Select Release Date:")
release_date_year = st.sidebar.number_input("Year", min_value=int(movies_df['release_date'].dt.year.min()), max_value=int(movies_df['release_date'].dt.year.max()))
release_date_month = st.sidebar.number_input("Month", min_value=1, max_value=12)
release_date_day = st.sidebar.number_input("Day", min_value=1, max_value=31)
release_date = f"{release_date_year}-{release_date_month:02d}-{release_date_day:02d}"

# Vote Average range
vote_average_min = st.sidebar.slider('Select Minimum Vote Average', min_value=movies_df['vote_average'].min(), max_value=movies_df['vote_average'].max(), step=0.1)
vote_average_max = st.sidebar.slider('Select Maximum Vote Average', min_value=movies_df['vote_average'].min(), max_value=movies_df['vote_average'].max(), step=0.1)
vote_average_range = (vote_average_min, vote_average_max)  # Ensure it's a tuple

# Filter movies based on selected criteria
filtered_movies = movies_df[
    (movies_df['budget'] >= budget_range) &
    (movies_df['genres'].str.contains(selected_genre, na=False)) &
    (movies_df['keywords'].str.contains(keywords, na=False)) &
    (movies_df['original_language'] == original_language) &
    (movies_df['popularity'] > popularity_range[0]) &  
    (movies_df['popularity'] < popularity_range[1]) & 
    (movies_df['release_date'].dt.strftime('%Y-%m-%d') == release_date) &  # Compare formatted release_date
    (movies_df['vote_average'] > vote_average_range[0]) &
    (movies_df['vote_average'] < vote_average_range[1])
]

# Display movie recommendations
st.title('Movie Recommendations')
if len(filtered_movies) == 0:
    st.write('No movies found with the selected criteria.')
else:
    st.write('Top Recommendations:')
    for index, movie in filtered_movies.head(5).iterrows():
        st.write(f"Title: {movie['title']}")
        st.write(f"Overview: {movie['overview']}")

