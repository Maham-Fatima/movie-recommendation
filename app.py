import streamlit as st
import requests
import pickle
import pandas as pd


movies = pickle.load(open('movie.pkl', 'rb'))
movies = pd.DataFrame(movies)
similarity = pickle.load(open('similarity.pkl', 'rb'))


api_key = 'b5652d45'


def fetch_poster(movie_title):
    response = requests.get(f"https://www.omdbapi.com/?t={movie_title}&apikey={api_key}")
    data = response.json()
    if data.get('Response') == 'True':
        return data.get('Poster')
    else:
        return None


def recommend(movie):
    if movie not in movies['title'].values:
        return []  
    index = movies[movies['title'] == movie].index[0]
    distances = similarity[index]
    movie_indices = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:7]

    recommended_movies = []
    for i in movie_indices:
        movie_title = movies.iloc[i[0]].title
        poster_url = fetch_poster(movie_title)
        recommended_movies.append((movie_title, poster_url))
    return recommended_movies


st.header("🎬 Movie Recommendation System by Maham")


movie_options = movies['title'].values
selected_movie = st.selectbox("Or choose a movie from the list:", movie_options)
user_input = st.text_input("Or enter a movie name manually:")


if st.button("🔍 Search Recommendations"):
    search_movie = user_input if user_input else selected_movie
    with st.spinner('🔎 Fetching recommendations...'):
        movies_list = recommend(search_movie)
    st.success('✅ Done!')

    if movies_list:
        st.subheader(f"Movies similar to **{search_movie}**:")
        
       
        cols = st.columns(3)
        for idx, (movie_title, poster_url) in enumerate(movies_list):
            with cols[idx % 3]:
                st.text(movie_title)
                if poster_url:
                    st.image(poster_url, use_container_width=True)
                else:
                    st.write("Poster not found")
    else:
        st.error("❌ Movie not found in our database. Please try another title.")
