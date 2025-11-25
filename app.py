import gdown
import os
import pickle
import pandas as pd
import streamlit as st

# Function to auto-download files if missing
def download_if_missing(url, filename):
    if not os.path.exists(filename):
        import gdown
        gdown.download(url, filename, quiet=False)

# Google Drive Direct Links
url_similarity = "https://drive.google.com/uc?export=download&id=11QEMRlcQuAV0ynxpaDt6IUG_nuwLDiGX"
url_movies_dict = "https://drive.google.com/uc?export=download&id=1eQ91oGsDgOV8L_jFhE8ngqUO-iUOMsN1"

# Download files if missing (required for Streamlit Cloud)
download_if_missing(url_similarity, "similarity.pkl")
download_if_missing(url_movies_dict, "movie_dict.pkl")

# Load Data
movies_dict = pickle.load(open("movie_dict.pkl", "rb"))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open("similarity.pkl", "rb"))
st.title('Movie Recommender System')

def recommend(movie):
    if movie not in movies['title'].values:
        return []
    index = movies[movies['title'] == movie].index[0]
    distances = similarity[index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    return [movies.iloc[i[0]].title for i in movies_list]

selected_movie = st.selectbox(
    'How would you like to be entertained?',
    movies['title'].values
)

if st.button('Recommend'):
    names = recommend(selected_movie)
    st.header("Here are 5 movies for you:")
    for name in names:
        st.write(name)


