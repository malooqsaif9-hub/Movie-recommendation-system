import streamlit as st
import pickle
import pandas as pd
import requests

# ---------- TMDB POSTER FETCH FUNCTION ----------

def fetch_poster(movie_id: int) -> str:
    """
    Fetch poster URL from TMDB using movie_id.
    Uses API key stored in Streamlit secrets.
    """
    api_key = st.secrets.get("TMDB_API_KEY", None)

    # If no API key, return a placeholder image
    if not api_key:
        return "https://via.placeholder.com/500x750?text=No+Poster"

    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    params = {
        "api_key": api_key,
        "language": "en-US"
    }

    try:
        res = requests.get(url, params=params, timeout=5)
        if res.status_code != 200:
            return "https://via.placeholder.com/500x750?text=No+Poster"

        data = res.json()
        poster_path = data.get("poster_path")
        if not poster_path:
            return "https://via.placeholder.com/500x750?text=No+Poster"

        return "https://image.tmdb.org/t/p/w500" + poster_path

    except Exception:
        # Any error → safe fallback
        return "https://via.placeholder.com/500x750?text=No+Poster"


# ---------- RECOMMENDATION FUNCTION ----------

def recommend(movie: str):
    # Get index of selected movie
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]

    # Top 5 similar movies (skip index 0 because it's the same movie)
    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_posters


# ---------- STREAMLIT UI ----------

st.title('Movie Recommender System')

# Load data
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

selected_movie_name = st.selectbox(
    'How would you like to be entertained?',
    movies['title'].values
)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    st.subheader("Here are 5 movies for you:")

    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.image(posters[i])
            st.caption(names[i])
