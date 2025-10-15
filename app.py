import gradio as gr
import pickle
import pandas as pd
import requests

# ---- Load Data ----
movies = pickle.load(open('movies_dict.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
df = pd.DataFrame(movies)

# ---- Function to Fetch Movie Poster ----
def fetch_poster(movie_name):
    api_key = "YOUR_TMDB_API_KEY"  # 🔑 Replace with your TMDB API key
    url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={movie_name}"
    response = requests.get(url).json()

    if response.get('results'):
        poster_path = response['results'][0].get('poster_path')
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500/{poster_path}"
    return "https://via.placeholder.com/500x750?text=No+Poster+Found"

# ---- Function to Recommend Movies ----
def recommend(movie):
    try:
        index = df[df['title'] == movie].index[0]
    except IndexError:
        return {"Error": "Movie not found in database. Please try another."}

    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movies = []
    recommended_posters = []

    for i in distances[1:6]:
        movie_name = df.iloc[i[0]].title
        recommended_movies.append(movie_name)
        recommended_posters.append(fetch_poster(movie_name))

    # Return as dictionary {movie: poster}
    return {recommended_movies[i]: recommended_posters[i] for i in range(len(recommended_movies))}

# ---- Gradio Interface ----
demo = gr.Interface(
    fn=recommend,
    inputs=gr.Textbox(label="🎬 Enter a Movie Name"),
    outputs=gr.Gallery(label="Recommended Movies").style(grid=[2], height="auto"),
    title="Movie Recommender System 🍿",
    description="Enter your favorite movie and get 5 similar movies with posters!"
)

# ---- Launch App ----
demo.launch()
