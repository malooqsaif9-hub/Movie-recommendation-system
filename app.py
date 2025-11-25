import streamlit as st
import pickle
import pandas as pd

def recommend(movie):
    # Check if movie exists
    if movie not in movies['title'].values:
        return []
    
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    recommended_movies = []
    for i in movies_list:
        recommended_movies.append(movies.iloc[i[0]].title)

    return recommended_movies


st.title('Movie Recommender System')

# Load data
movies_dict = pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl','rb'))

selected_movie_name = st.selectbox(
    'How would you like to be entertained?',
    movies['title'].values
)

if st.button('Recommend'):
    names = recommend(selected_movie_name)
    
    st.header("Here are 5 movies for you:")
    for name in names:
        st.write(name)
