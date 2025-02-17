import os
import streamlit as st
import pickle
import pandas as pd
import requests
import urllib.request

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'.format(movie_id))
    data = response.json()
    return "http://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):
    try:
        movie_index = movies[movies['title'] == movie].index[0]
        distances = similarity[movie_index]  # Now similarity should be loaded
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

        recommended_movies = []
        recommended_movies_poster = []
        for i in movies_list:
            movie_id = movies.iloc[i[0]].movie_id
            recommended_movies.append(movies.iloc[i[0]].title)
            recommended_movies_poster.append(fetch_poster(movie_id))
        return recommended_movies, recommended_movies_poster
    except Exception as e:
        print(f"Error in recommendation function: {e}")
        return [], []

# Load movie data
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

# Check if similarity.pkl exists or download it
if not os.path.exists("similarity.pkl"):
    url = "https://raw.githubusercontent.com/nihal4429/Movie_Recommendation_System/main/pythonProject/similarity.pkl"
    destination_path = "similarity.pkl"
    try:
        urllib.request.urlretrieve(url, destination_path)
        print("Download successful")
    except Exception as e:
        print(f"Error downloading file: {e}")
else:
    print("similarity.pkl already exists")

# Load the similarity matrix
try:
    with open("similarity.pkl", "rb") as f:
        similarity = pickle.load(f)
    print("Similarity matrix loaded successfully")
except Exception as e:
    print(f"Error loading similarity.pkl: {e}")

# Streamlit app
st.title('Movie Recommendation System')

selected_movie_name = st.selectbox('Select a movie:', movies['title'].values)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    if not names:
        st.error("An error occurred while fetching recommendations.")
    else:
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.text(names[0])
            st.image(posters[0])
        with col2:
            st.text(names[1])
            st.image(posters[1])
        with col3:
            st.text(names[2])
            st.image(posters[2])
        with col4:
            st.text(names[3])
            st.image(posters[3])
        with col5:
            st.text(names[4])
            st.image(posters[4])
