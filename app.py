import streamlit as st
import pickle
import joblib
st.set_page_config(layout="wide")
st.title("Movie Recommender")
st.write("This is a movie recommender app")

# Load data
with open("movies.pkl", "rb") as f:
    movies = pickle.load(f)

similarity = joblib.load("similarity.joblib")

# List of movie titles for dropdown
movie_titles = movies['title'].values


def recommend(selected_movie):
    # Step 1: Find index of selected movie
    movie_index = movies[movies['title'] == selected_movie].index[0]

    # Step 2: Get similarity scores
    distances = similarity[movie_index]

    # Step 3: Pair index with similarity score
    movie_distance_list = list(enumerate(distances))

    # Step 4: Sort by similarity
    sorted_movies = sorted(movie_distance_list, reverse=True, key=lambda x: x[1])

    # Step 5: Get top 5 similar movies (excluding itself)
    recommended_movies = sorted_movies[1:6]

    # Step 6: Return movie names
    recommended_titles = []
    for i in recommended_movies:
        recommended_titles.append(movies.iloc[i[0]].title)

    return recommended_titles


# UI
selected_movie = st.selectbox("Select a movie", movie_titles)

if st.button("Recommend"):
    st.write("Recommended movies are:")
    
    recommendations = recommend(selected_movie)
    
    for movie in recommendations:
        st.write(movie)