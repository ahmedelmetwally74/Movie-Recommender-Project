# import dash_bootstrap_components as dbc
# from dash import html, Input, Output, dcc, State
# import pandas as pd
# import numpy as np
# import pathlib
# from tensorflow.keras.models import load_model
# from app import app
#
# PATH = pathlib.Path(__file__).parent
# DATA_PATH = PATH.joinpath("../data").resolve()
#
# movies = pd.read_csv(DATA_PATH.joinpath("movies.csv"))
# ratings = pd.read_csv(DATA_PATH.joinpath("ratings.csv"))
#
# # Load your item-based recommendation model
# model_path = DATA_PATH.joinpath("movie_recommender.h5")
# model = load_model(model_path)
#
# # Create mappings
# user_ids = ratings['userId'].unique().tolist()
# movie_ids = ratings['movieId'].unique().tolist()
#
# user_user_encoded = {x: i for i, x in enumerate(user_ids)}
# movie_movie_encoded = {x: i for i, x in enumerate(movie_ids)}
#
# user_encoded_user = {i: x for x, i in user_user_encoded.items()}
# movie_encoded_movie = {i: x for x, i in movie_movie_encoded.items()}
#
# # Encode genres
# all_genres = set()
# for genres in movies['genres'].str.split('|'):
#     all_genres.update(genres)
# all_genres = sorted(all_genres)
#
# genre_genre_encoded = {x: i for i, x in enumerate(all_genres)}
# genre_encoded_genre = {i: x for x, i in genre_genre_encoded.items()}
#
# def encode_genres(genres):
#     encoded = np.zeros(len(all_genres))
#     for genre in genres.split('|'):
#         if genre in genre_genre_encoded:
#             encoded[genre_genre_encoded[genre]] = 1
#     return encoded
#
# movies['genre_encoded'] = movies['genres'].apply(encode_genres)
#
# # Merge ratings with movies to get genre information
# ratings = ratings.merge(movies[['movieId', 'genre_encoded']], on='movieId', how='left')
#
# num_users = len(user_user_encoded)
# num_movies = len(movie_movie_encoded)
# num_genres = len(all_genres)
#
# # Function to preprocess movie data
# def preprocess_movie_data(movie_data):
#     encoded_genres = encode_genres(movie_data['genres'])
#     return np.array(encoded_genres).reshape(1, -1)
#
# # Function to predict similar items
# def predict_similar_items(features, num_recommendations=10):
#     # Dummy implementation: Replace with actual logic using your model
#     predictions = model.predict(features)
#     predictions = predictions.flatten()
#
#     # Get indices of top predictions
#     top_indices = predictions.argsort()[-num_recommendations:][::-1]
#
#     # Retrieve corresponding movie IDs
#     top_movie_ids = [movie_encoded_movie[i] for i in top_indices]
#
#     return top_movie_ids
#
# # Example layout and callback for your Dash app
# layout = dbc.Container(
#     [
#         html.H2("Movie Recommendation Based on Item Similarity"),
#         dcc.Input(id='movie-title-input', placeholder='Enter a Movie Title', type='text'),
#         html.Button("Generate Recommendations", id='generate-button'),
#         html.Div(id='recommended-movies-content'),
#     ],
#     fluid=True,
# )
#
# @app.callback(
#     Output('recommended-movies-content', 'children'),
#     [Input('generate-button', 'n_clicks')],
#     [State('movie-title-input', 'value')]
# )
# def update_recommended_movies(n_clicks, movie_title):
#     if n_clicks and movie_title:
#         try:
#             movie_data = movies[movies['title'] == movie_title].iloc[0]
#
#             # Preprocess movie data
#             features = preprocess_movie_data(movie_data)
#
#             # Predict similar items
#             recommended_movie_ids = predict_similar_items(features)
#
#             # Create movie cards for recommended movies
#             recommended_movie_cards = []
#             for movie_id in recommended_movie_ids:
#                 recommended_movie = movies[movies['movieId'] == movie_id].iloc[0]
#                 recommended_movie_cards.append(create_movie_card(recommended_movie))
#
#             return recommended_movie_cards
#         except Exception as e:
#             return html.P(f"Error: {e}")
#
#     return []
#
# def create_movie_card(movie_data):
#     poster = movie_data.get('Poster', '/assets/default_poster.jpg')
#     if poster == "N/A" or poster == "":
#         poster = '/assets/default_poster.jpg'
#
#     movie_title = movie_data.get('title', 'Unknown Title')
#     if movie_title == 'Unknown Title':
#         return None
#
#     return dbc.Card(
#         dbc.CardImg(src=poster, top=True, style={"height": "300px", "object-fit": "cover"}),
#         dbc.CardBody(
#             [
#                 html.H5(movie_title, className="card-title"),
#                 html.P(f"Genres: {movie_data.get('genres', 'Unknown')}", className="card-text"),
#             ]
#         ),
#         style={"width": "14rem", "margin": "10px"}
#     )
#
