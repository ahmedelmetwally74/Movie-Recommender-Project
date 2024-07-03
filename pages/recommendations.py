import pathlib
import dash_bootstrap_components as dbc
from dash import html, Input, Output
import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
import requests
from app import app

# File paths
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../movielens Dataset").resolve()
MODELS_PATH = PATH.joinpath("../Models").resolve()

# Load data
movies = pd.read_csv(DATA_PATH.joinpath("movies.csv"))
ratings = pd.read_csv(DATA_PATH.joinpath("ratings.csv"))

# Model paths
cf_model_path = MODELS_PATH.joinpath("cf_model_final.keras")
item_model_path = MODELS_PATH.joinpath("movie_recommender.h5")

# Debugging lines to check the paths
print("cf_model_path exists:", cf_model_path.exists())
print("item_model_path exists:", item_model_path.exists())

# Get the maximum user and movie IDs
max_userid = ratings['userId'].drop_duplicates().max()
max_movieid = ratings['movieId'].drop_duplicates().max()
num_users = max_userid + 1
num_items = max_movieid + 1

user_ids = ratings['userId'].unique().tolist()
movie_ids = ratings['movieId'].unique().tolist()

# Create mappings
user_user_encoded = {x: i for i, x in enumerate(user_ids)}
movie_movie_encoded = {x: i for i, x in enumerate(movie_ids)}

user_encoded_user = {i: x for x, i in user_user_encoded.items()}
movie_encoded_movie = {i: x for x, i in movie_movie_encoded.items()}

# Process genres
all_genres = set()
for genres in movies['genres'].str.split('|'):
    all_genres.update(genres)
all_genres = sorted(all_genres)

# Create genre mappings
genre_genre_encoded = {x: i for i, x in enumerate(all_genres)}
genre_encoded_genre = {i: x for x, i in genre_genre_encoded.items()}

# Encode genres
def encode_genres(genres):
    encoded = np.zeros(len(all_genres))
    for genre in genres.split('|'):
        if genre in genre_genre_encoded:
            encoded[genre_genre_encoded[genre]] = 1
    return encoded

movies['genre_encoded'] = movies['genres'].apply(encode_genres)

# Merge ratings with movies to get genre information
ratings = ratings.merge(movies[['movieId', 'genre_encoded']], on='movieId', how='left')

# Function to fetch movie data from OMDb API
def fetch_movie_data(movie_title):
    api_key = '249559df'  # Replace with your actual OMDb API key
    url = f'http://www.omdbapi.com/?t={movie_title}&apikey={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Function to create movie card with poster
def create_movie_card(movie_data):
    poster = movie_data.get('Poster', '/assets/default_poster.jpg')
    if poster == "N/A" or poster == "":
        poster = '/assets/default_poster.jpg'

    movie_title = movie_data.get('Title', 'Unknown Title')
    if movie_title == 'Unknown Title':
        return None  # Skip creating card for unknown titles

    return dbc.Col(
        dbc.Card(
            [
                dbc.CardImg(src=poster, top=True, style={"height": "300px", "object-fit": "cover"}),
                dbc.CardBody(
                    [
                        html.A(
                            html.H5(movie_title, className="card-title"),
                            href=f"https://www.imdb.com/title/{movie_data.get('imdbID')}/",
                            target="_blank"
                        ),
                        html.P(f"Genres: {movie_data.get('Genre', 'Unknown')}", className="card-text"),
                    ],
                    style={"text-align": "center", "min-height": "130px"}
                ),
            ],
            style={"width": "14rem", "margin": "10px"}  # Adjusted card width
        ),
        width=3  # Each column width for 4 cards per row
    )

# Function to get user-based recommendations
def get_user_based_recommendations(user_id, num_recommendations=42):
    cf_model = load_model(cf_model_path)
    all_movie_ids = np.array([movie_id for movie_id in range(1, max_movieid + 1)])
    predicted_ratings = cf_model.predict([np.array([user_id] * len(all_movie_ids)), all_movie_ids])
    top_indices = np.argsort(predicted_ratings.flatten())[::-1][:num_recommendations]
    recommended_movie_ids = all_movie_ids[top_indices]
    recommended_movies = movies[movies['movieId'].isin(recommended_movie_ids)]

    recommended_movie_cards = []
    for _, movie in recommended_movies.iterrows():
        movie_data = fetch_movie_data(movie['title'])
        if movie_data:
            recommended_movie_cards.append(create_movie_card(movie_data))

    return recommended_movie_cards

# Function to get item-based recommendations
def get_item_based_recommendations(user_id, num_recommendations=42):
    item_model = load_model(item_model_path)

    user_encoded = user_user_encoded[user_id]
    movie_ids = movies['movieId'].values

    # Filter out movie_ids that are not in movie2movie_encoded
    valid_movie_ids = [movie_id for movie_id in movie_ids if movie_id in movie_movie_encoded]
    valid_movie_encoded = [movie_movie_encoded[movie_id] for movie_id in valid_movie_ids]
    genre_encoded = np.stack(movies[movies['movieId'].isin(valid_movie_ids)]['genre_encoded'].values)

    user_array = np.array([user_encoded] * len(valid_movie_encoded))

    predictions = item_model.predict([user_array, np.array(valid_movie_encoded), genre_encoded])
    predictions = predictions.flatten()

    # Sort predictions to get the highest-rated movies
    top_n_indices = predictions.argsort()[-num_recommendations:][::-1]
    top_n_movie_ids = [movie_encoded_movie[valid_movie_encoded[i]] for i in top_n_indices]
    top_n_predictions = predictions[top_n_indices]

    # Fetch detailed data for the top-rated movies
    recommended_movies = movies[movies['movieId'].isin(top_n_movie_ids)]

    # Create movie cards for display
    recommended_movie_cards = []
    for _, movie in recommended_movies.iterrows():
        movie_data = fetch_movie_data(movie['title'])
        if movie_data:
            recommended_movie_cards.append(create_movie_card(movie_data))

    return recommended_movie_cards

# Layout definition for recommendations page
layout = dbc.Container(
    [
        dbc.Row(id='recommended-movies-heading'),
        html.Div(
            [
                dbc.Spinner(html.Div(id="loading-output"), color="danger", spinner_style={"margin-top": "250px"}),
            ]
        ),
        # Placeholder for recommended movies
        dbc.Row(id='recommended-movies-content')
    ],
    fluid=True,
)

# Callback to update recommended movies list and progress bar
@app.callback(
    [Output('recommended-movies-heading', 'children'),
     Output('recommended-movies-content', 'children'),
     Output("loading-output", "children")],
    [Input('url', 'pathname')]
)
def update_recommended_movies(pathname):
    if pathname and pathname.startswith('/pages/recommendations?user_id='):
        try:
            user_id = int(pathname.split('=')[1])

            # Get user-based recommendations
            recommended_movie_cards = get_user_based_recommendations(user_id)

            # Display "Suggested for you" heading after recommendations are ready
            heading = dbc.Row([
                dbc.Row(dbc.Col(html.H3("Suggested for you"), width={"size": 6}, style={"margin-top": "40px", 'margin-left': '10px'})),
                dbc.Row(dbc.Col(html.Hr()))
            ])

            return heading, dbc.Row(recommended_movie_cards, id='recommended-movies-content'), {"display": "none"}

        except Exception as e:
            return html.P(f"Error: {e}"), [], {"margin": "20px", "display": "block"}

    elif pathname and pathname.startswith('/pages/recommendations?movie_id='):
        try:
            movie_id = int(pathname.split('=')[1])
            # Get item-based recommendations
            recommended_movie_cards = get_item_based_recommendations(movie_id)

            # Display "Recommended for movie" heading after recommendations are ready
            heading = dbc.Row([
                dbc.Row(dbc.Col(html.H3("Similar to this Movie"), width={"size": 6}, style={"margin-top": "40px", 'margin-left': '10px'})),
                dbc.Row(dbc.Col(html.Hr()))
            ])

            return heading, dbc.Row(recommended_movie_cards, id='recommended-movies-content'), {"display": "none"}

        except Exception as e:
            return html.P(f"Error: {e}"), [], {"margin": "20px", "display": "block"}

    return [], [], {"margin": "20px", "display": "block"}
