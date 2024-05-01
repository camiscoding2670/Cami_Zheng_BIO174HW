#!/usr/bin/env python
# coding: utf-8

# In[2]:


import streamlit as st
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

# Load the dataset
def load_data():
    return pd.read_csv('new_dataset.csv')

movies_df = load_data()
genres = movies_df['genres'].str.split(', ').explode().unique()    
production_companies = movies_df['production_companies'].str.split(', ').explode().unique()

# Define function to filter and display movies
def filter_and_display_movies():
    st.title('Welcome to Movie Recommender')
    st.subheader('BIO174 Final Project by Cami Zheng')

    # Sidebar filters
    st.sidebar.title('Movie Filters')

    # Genre
    selected_genres = st.sidebar.multiselect('Select Genre', genres)

    # Keywords
    keywords = st.text_input("I'm looking for...")
    if keywords:
        st.write("You entered: ", keywords)
    
    # Original Language
    original_language = st.sidebar.selectbox('Select Original Language', movies_df['original_language'].unique())

    # Release Year
    release_date = st.sidebar.number_input('Select release year', min_value=int(movies_df['release_date'].min()), max_value=int(movies_df['release_date'].max()))

    # Popularity range
    popularity_min = st.sidebar.slider('Select Minimum Popularity', min_value=movies_df['popularity'].min(), max_value=movies_df['popularity'].max(), step=0.1)
    popularity_max = st.sidebar.slider('Select Maximum Popularity', min_value=movies_df['popularity'].min(), max_value=movies_df['popularity'].max(), step=0.1, value=movies_df['popularity'].max())
    popularity_range = (popularity_min, popularity_max)  # Ensure it's a tuple

    # production companies
    selected_production_companies = st.sidebar.multiselect('Select production companies', production_companies)


    # Vote Average range
    vote_average_min = st.sidebar.slider('Select Minimum Vote Average', min_value=movies_df['vote_average'].min(), max_value=movies_df['vote_average'].max(), step=0.1)
    vote_average_max = st.sidebar.slider('Select Maximum Vote Average', min_value=movies_df['vote_average'].min(), max_value=movies_df['vote_average'].max(), step=0.1, value=movies_df['vote_average'].max())
    vote_average_range = (vote_average_min, vote_average_max)  # Ensure it's a tuple

    # Reset button
    if st.sidebar.button("Reset", type="primary"):
        selected_genres = []
        keywords = ""
        original_language = ""
        popularity_range = (movies_df['popularity'].min(), movies_df['popularity'].max())
        selected_production_companies = []
        release_date = None
        vote_average_range = (movies_df['vote_average'].min(), movies_df['vote_average'].max())

    # Filter movies based on selected criteria
    filtered_movies = movies_df.dropna(subset=['genres']).loc[
        (movies_df['genres'].str.contains('|'.join(selected_genres), na=False)) &
        (movies_df['keywords'].str.contains(keywords, na=False)) &
        (movies_df['original_language'] == original_language) &
        (movies_df['popularity'] > popularity_range[0]) &
        (movies_df['popularity'] < popularity_range[1]) &
        (movies_df['production_companies'].str.contains('|'.join(selected_production_companies), na=False)) &
        (movies_df['release_date'] == release_date if release_date is not None else True) &  # Compare formatted release_date
        (movies_df['vote_average'] > vote_average_range[0]) &
        (movies_df['vote_average'] < vote_average_range[1])
    ]

    # Check if any movies are found
    if not filtered_movies.empty:
        # Display movie recommendations
        st.header('Movie Recommendations')
        for index, movie in filtered_movies.head(5).iterrows():
            st.write(f"Title: {movie['title']}")
            st.write(f"Overview: {movie['overview']}")
            st.write(f"Link:{movie['homepage']}")
    else:
        # No movies found, recommend based on similar genre or rating
        st.write('No movies found with the selected criteria. Recommending similar movies...')
        # Calculate TF-IDF matrix for genres
        tfidf_vectorizer = TfidfVectorizer()
        tfidf_matrix = tfidf_vectorizer.fit_transform(movies_df['genres'].fillna(''))
        # If at least one genre is selected
        if selected_genres:
            # Calculate cosine similarity between movies based on genres
            genre_similarity = cosine_similarity(tfidf_matrix, tfidf_matrix)
            # Get movies similar to the selected genre
            similar_movies_idx = genre_similarity[movies_df.index[movies_df['genres'].str.contains(selected_genres[0])].tolist()].argsort(axis=1)[:, ::-1][:, 1]
            # Display similar movies
            for idx in similar_movies_idx[:5]:
                movie = movies_df.iloc[idx]
                st.write(f"Title: {movie['title']}")
                st.write(f"Overview: {movie['overview']}")
                st.write(f"Link:{movie['homepage']}")
        else:
            st.write('No genre selected. Recommending top-rated movies...')
            top_rated_movies = movies_df.sort_values(by='vote_average', ascending=False).head(5)
    
# Call the function to filter and display movies
filter_and_display_movies()

