import streamlit as st
import pickle
import pandas as pd
import requests
import os
from dotenv import load_dotenv

load_dotenv()


@st.cache_data
def fetch_poster(movie_id):

    url = f"https://api.themoviedb.org/3/movie/{movie_id}"

    headers = {
        "Authorization": f"Bearer {os.environ['TMDB_API_TOKEN']}"
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        poster_path = data.get("poster_path")

        if poster_path:
            return "https://image.tmdb.org/t/p/w500" + poster_path

        return None

    except requests.exceptions.RequestException as e:
        

        return None



def recommend(movie):

    movie = movie.lower()

    matches = movies[movies['title'].str.lower() == movie]

    if matches.empty:
        return [], []

    movie_index = matches.index[0]

    distances = similarity[movie_index]

    movie_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    recommended_movies_poster = []

    for i in movie_list:

        movie_id = movies.iloc[i[0]].movie_id

        movie_title = movies.iloc[i[0]].title

        recommended_movies.append(movie_title)

        # Fetch poster from TMDB
        poster = fetch_poster(movie_id)

        recommended_movies_poster.append(poster)

    return recommended_movies, recommended_movies_poster


movies_dict = pickle.load(
    open('movie_dict.pkl', 'rb')
)

movies = pd.DataFrame(movies_dict)



similarity = pickle.load(
    open('similarity.pkl', 'rb')
)



st.title("Movie Recommender System")


selected_movie_name = st.selectbox(
    'Select a Movie',
    movies['title'].values
)



if st.button('Recommend'):

    names, posters = recommend(selected_movie_name)

    if not names:
        st.error("Movie not found.")
    else:

        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.text(names[0])
            if posters[0]:
                st.image(posters[0])

        with col2:
            st.text(names[1])
            if posters[1]:
                st.image(posters[1])

        with col3:
            st.text(names[2])
            if posters[2]:
                st.image(posters[2])

        with col4:
            st.text(names[3])
            if posters[3]:
                st.image(posters[3])

        with col5:
            st.text(names[4])
            if posters[4]:
                st.image(posters[4])

st.markdown("---")
st.markdown(
    "<p style='text-align: center;'>Made by <b>Aayush Vardhan 🧠</b></p>",
    unsafe_allow_html=True
)