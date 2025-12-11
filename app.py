# app.py
import os
import streamlit as st
import pickle
import pandas as pd
import requests


try:
    import gdown
except Exception:
    gdown = None

st.set_page_config(page_title="Movie Recommender", layout="wide")


MOVIE_DICT_FILE = "movie_dict.pkl"
SIMILARITY_FILE = "similarity.pkl"


MOVIE_DICT_DRIVE_ID = st.secrets.get("MOVIE_DICT_DRIVE_ID", None)
SIMILARITY_DRIVE_ID = st.secrets.get("SIMILARITY_DRIVE_ID", None)

def drive_url_from_id(file_id: str) -> str:
    return f"https://drive.google.com/uc?export=download&id={file_id}"


def ensure_file(local_path: str, drive_id: str = None) -> bool:
    """
    Ensure local_path exists. If missing and drive_id provided and gdown available,
    attempt to download. Returns True if file exists after function completes.
    """
    if os.path.exists(local_path):
        return True

    if drive_id:
        url = drive_url_from_id(drive_id)
        if gdown:
            st.info(f"Downloading {local_path} from Google Drive...")
            try:
                gdown.download(url, local_path, quiet=False)
                return os.path.exists(local_path)
            except Exception as e:
                st.error(f"Download failed for {local_path}: {e}")
                return False
        else:
            st.warning("gdown is not available in the environment. Add 'gdown' to requirements.txt and redeploy.")
            return False
    return False

# ----------------- TMDB poster fetch -----------------
def fetch_poster(movie_id: int) -> str:
    api_key = st.secrets.get("TMDB_API_KEY", None)
    if not api_key:
        return "https://via.placeholder.com/500x750?text=No+Poster"

    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    params = {"api_key": api_key, "language": "en-US"}

    try:
        res = requests.get(url, params=params, timeout=6)
        if res.status_code != 200:
            return "https://via.placeholder.com/500x750?text=No+Poster"
        data = res.json()
        poster_path = data.get("poster_path")
        if not poster_path:
            return "https://via.placeholder.com/500x750?text=No+Poster"
        return "https://image.tmdb.org/t/p/w500" + poster_path
    except Exception:
        return "https://via.placeholder.com/500x750?text=No+Poster"


st.title("Movie Recommender System")



ok_movie = ensure_file(MOVIE_DICT_FILE, MOVIE_DICT_DRIVE_ID)
ok_sim = ensure_file(SIMILARITY_FILE, SIMILARITY_DRIVE_ID)

if not ok_movie:
    st.error(
        f"Required file `{MOVIE_DICT_FILE}` not found. "
        "Either upload it to your GitHub repo (same folder as app.py) or add its Drive file id to Streamlit Secrets as MOVIE_DICT_DRIVE_ID."
    )
    st.stop()

if not ok_sim:
    st.error(
        f"Required file `{SIMILARITY_FILE}` not found. "
        "Either upload it to your GitHub repo (same folder as app.py) or add its Drive file id to Streamlit Secrets as SIMILARITY_DRIVE_ID."
    )
    st.stop()


try:
    with open(MOVIE_DICT_FILE, "rb") as f:
        movies_dict = pickle.load(f)
    movies = pd.DataFrame(movies_dict)
except Exception as e:
    st.error(f"Failed to load {MOVIE_DICT_FILE}: {e}")
    st.stop()


try:
    with open(SIMILARITY_FILE, "rb") as f:
        similarity = pickle.load(f)
except Exception as e:
    st.error(f"Failed to load {SIMILARITY_FILE}: {e}")
    st.stop()


def recommend(movie: str):
    if movie not in list(movies['title'].values):
        st.warning("Selected movie not found in dataset.")
        return [], []

    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movies_list:
        idx = i[0]
        movie_id = int(movies.iloc[idx].movie_id)
        recommended_movies.append(movies.iloc[idx].title)
        recommended_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_posters


selected_movie_name = st.selectbox("How would you like to be entertained?", movies['title'].values)

if st.button("Recommend"):
    names, posters = recommend(selected_movie_name)
    if names:
        st.subheader("Here are 5 movies for you:")
        cols = st.columns(5)
        for i in range(len(names)):
            with cols[i]:
                st.image(posters[i], use_column_width=True)
                st.caption(names[i])
    else:
        st.info("No recommendations available.")
