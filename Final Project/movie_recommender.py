import streamlit as st
import pandas as pd

# Load the dataset
@st.cache
def load_data():
    return pd.read_csv('/Users/camellia/Documents/GitHub/BIO174-2024/AC-homework/Final Project/tmdb_5000_movies.csv')

movies_df = load_data()

# Sidebar filters
st.sidebar.title('Movie Filters')

# Budget range
budget_range = st.sidebar.slider('Select Budget Range', min_value=0, max_value=movies_df['budget'].max(), step=1000000)

# Original Language
original_language = st.sidebar.selectbox('Select Original Language', movies_df['original_language'].unique())

# Production Country
production_country = st.sidebar.selectbox('Select Production Country', movies_df['production_countries'].unique())

# Rating range
rating_range = st.sidebar.slider('Select Rating Range', min_value=movies_df['vote_average'].min(), max_value=movies_df['vote_average'].max(), step=0.1)

# Popularity range
popularity_range = st.sidebar.slider('Select Popularity Range', min_value=movies_df['popularity'].min(), max_value=movies_df['popularity'].max(), step=0.1)

# Filter movies based on selected criteria
filtered_movies = movies_df[
    (movies_df['budget'] >= budget_range) &
    (movies_df['original_language'] == original_language) &
    (movies_df['production_countries'] == production_country) &
    (movies_df['vote_average'] >= rating_range[0]) &
    (movies_df['vote_average'] <= rating_range[1]) &
    (movies_df['popularity'] >= popularity_range[0]) &
    (movies_df['popularity'] <= popularity_range[1])
]

# Display movie recommendations
st.title('Movie Recommendations')
if len(filtered_movies) == 0:
    st.write('No movies found with the selected criteria.')
else:
    st.write('Top Recommendations:')
    for index, movie in filtered_movies.head(5).iterrows():
        st.write(movie['title'])