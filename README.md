🎬 Movie Recommendation System

A Content-Based Movie Recommendation System built using Python and Streamlit.
The system recommends top 5 similar movies by analyzing movie metadata including genres, keywords, cast, crew, and overview using cosine similarity.

 Features

. Content-based movie recommendation

. NLP-based tag generation

. Cosine similarity for accurate matching

. Fast and smooth performance

. Clean and simple Streamlit user interface

. Preprocessed dataset stored using pickle

. Technologies Used

Python

Pandas

NumPy

Scikit-learn

Streamlit

Pickle
movie-recommendation-system/
│
├── app.py                # Main Streamlit app
├── movie_dict.pkl        # Movie data (title, movie_id, tags)
├── similarity.pkl        # Cosine similarity matrix
└── README.md             # Project documentation
▶️ How to Run the Project
1️⃣ Install the Required Libraries
pip install -r requirements.txt
pip install streamlit pandas numpy scikit-learn
streamlit run app.py
http://localhost:8501
How It Works

Reads the movie dataset

Combines metadata (keywords, genres, cast, crew, overview)

Creates a tags column

Converts tags to vectors using CountVectorizer

Computes cosine similarity between all movies

When a user selects a movie, it returns the top 5 most similar movies

