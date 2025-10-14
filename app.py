



packages = ['plotly', 'gdown', 'pandas', 'streamlit', 'requests']
for p in packages:
    try:
        __import__(p)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", p])
import streamlit as st
import plotly.express as px
import pandas as pd
import gdown
import pickle

import sys
import subprocess

movies=pickle.load(open('movies_dict.pkl','rb'))
url = 'https://drive.google.com/uc?id=1aAh3j-gItp6RU6ODlC6G3ui1dvzf7fLM'
output = 'similarity.pkl'
gdown.download(url, output, quiet=False)


similarity = pickle.load(open('similarity.pkl', 'rb'))
df=pd.DataFrame(movies)

import requests

def fetch_poster(movie_name):
    api_key = '965cc9eceaef8a74325bfa6502bddbb1'
    try:
        url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={movie_name}"
        data = requests.get(url).json()
        if data.get('results'):
            poster_path = data['results'][0].get('poster_path')
            if poster_path:
                return f"https://image.tmdb.org/t/p/w500{poster_path}"
        return "https://via.placeholder.com/500x750?text=No+Image"
    except Exception as e:
        print("Error fetching poster:", e)
        return "https://via.placeholder.com/500x750?text=Error"



def recommend(movie):
    # get the integer index instead of Index object
    index = df[df['title'] == movie].index[0]  # Remember to put [0] after index

    # enumerate similarity scores
    distances = list(enumerate(similarity[index]))

    # sort by similarity (highest first) and skip the first (itself)
    movies_list = sorted(distances, reverse=True, key=lambda x: x[1])[1:6]
    recommandation,posters=[],[]
    for i in movies_list:
        recommandation.append(df.iloc[i[0]].title)
        posters.append(fetch_poster(df.iloc[i[0]].title))
    return recommandation,posters



st.title('🎥 Movie Recommender System')

selected_name = st.selectbox('Select a movie from the dropdown', df['title'].values)

if st.button("Recommend"):
    names, posters = recommend(selected_name)

    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])





