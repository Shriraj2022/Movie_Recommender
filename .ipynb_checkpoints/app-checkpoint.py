import streamlit as st
import pickle
import pandas as pd 
import requests

movie_dict = pickle.load(open('movies_dict.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))
movies = pd.DataFrame(movie_dict)
st.set_page_config(layout="wide")

st.title('Movie Recommender')
selected_movie_name = st.selectbox(
    'Enter movie name', movies['title'])

st.write('You selected:', selected_movie_name)


def fetch_poster(movie_id):
    data = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=4855bf0312b7baf811fba304214dfbc8'.format(movie_id)).json()['poster_path']
    return "https://image.tmdb.org/t/p/w500/" + data

def recommend_similar_movies(name):

    movie_index = movies[movies['title'] == name].index[0]
    x = pd.DataFrame(enumerate(similarity[movie_index]))
    sorted_x = x.sort_values(by=1, ascending = False)
    top_movies_indexes = sorted_x.iloc[1:6,0]
    top_movies_list = top_movies_indexes.tolist()
    movie_names = movies.iloc [top_movies_list,1].to_list()  
    return movie_names , top_movies_list


if st.button('Recommend'):
    x = recommend_similar_movies(selected_movie_name)[0]
    y = recommend_similar_movies(selected_movie_name)[1]
    names = []
    index_for_movie = y
    for i in x:
        names.append(i)
    
    col1,col2, col3, col4, col5 = st.columns(5)
    for i in range(5):
        with col1 if i == 0 else col2 if i == 1 else col3 if i == 2 else col4 if i == 3 else col5:
            if len(names[i]) > 20: 
                st.header(names[i])
                st.image(fetch_poster(movies.iloc[y[i],0]),width = 350)
            else:
                st.header(names[i])
                st.write("")
                st.write("")
                st.write("")
                st.image(fetch_poster(movies.iloc[y[i],0]),width = 350)