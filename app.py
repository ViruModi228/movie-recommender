import streamlit as st
import pickle
import pandas as pd
import requests

# TMDB API KEY
API_KEY = 'ac222af16cbc79455144e4bc946c4336'

# Function to get movie poster using TMDb API
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    data = requests.get(url).json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
  movie_index = movies[movies['title'] == movie].index[0]
  distances = similarity[movie_index]
  movies_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:7]
  
  recommended_movies = []
  recommended_posters = []

  for i in movies_list:
    recommended_movies.append(movies.iloc[i[0]].title)
    recommended_posters.append(fetch_poster(movies.iloc[i[0]].movie_id))
  return recommended_movies,recommended_posters

movies_dict = pickle.load(open('movies.pkl','rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl','rb'))

st.title('Movie Recommender System')
name = st.selectbox(
    'Select Your Movie',movies['title'].values)
if st.button('Recommend'):
    recommendations, posters = recommend(name)

    # Create 6 columns for displaying the recommended movies
    cols = st.columns(6)  # Create 5 columns
    for i in range(len(recommendations)):
        with cols[i]:
            st.text(recommendations[i])  # Display the movie title
            st.image(posters[i], use_column_width='auto', width=150) # Display the movie poster