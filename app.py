import streamlit as st
import pickle
import joblib
import requests

st.set_page_config(page_title="🎬 Movie Recommender", layout="wide")

# ---------------- UI Styling ----------------
st.markdown("""
<style>
img {
    border-radius: 12px;
}
h1 {
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

st.title("🎬 Movie Recommender System")
st.markdown("Search and discover similar movies 🍿")

api_key = "28813756eda3cfd4efbad1c2f28e7763"

# ---------------- Load Data ----------------
with open("movies.pkl", "rb") as f:
    movies = pickle.load(f)

similarity = joblib.load("similarity.joblib")

# ---------------- Poster + Rating ----------------
@st.cache_data
def fetch_movie_details(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
    data = requests.get(url).json()

    poster = data.get('poster_path')
    rating = data.get('vote_average')

    poster_url = "https://image.tmdb.org/t/p/w500/" + poster if poster else None

    return poster_url, rating

# ---------------- Recommendation ----------------
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]

    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    names, posters, ratings = [], [], []

    for i in movie_list:
        idx = i[0]

        title = movies.iloc[idx].title
        movie_id = movies.iloc[idx].id

        poster, rating = fetch_movie_details(movie_id)

        names.append(title)
        posters.append(poster)
        ratings.append(rating)

    return names, posters, ratings

# ---------------- Search Feature ----------------
search_input = st.text_input("🔍 Search for a movie")

if search_input:
    matches = movies[movies['title'].str.contains(search_input.lower())]

    if len(matches) > 0:
        selected_movie = matches.iloc[0].title

        if st.button("Recommend"):
            names, posters, ratings = recommend(selected_movie)

            st.markdown("## 🎬 Recommended Movies")
            st.write("---")

            cols = st.columns(5)

            for i in range(5):
                with cols[i]:
                    st.caption(f"**{names[i]}**")
                    st.image(posters[i])
                    st.caption(f"⭐ {ratings[i]}")
    else:
        st.warning("No matching movie found")