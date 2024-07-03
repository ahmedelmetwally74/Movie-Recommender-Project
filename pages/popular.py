# popular.py
import pathlib
import dash_bootstrap_components as dbc
from dash import html
import pandas as pd
import requests


# File paths
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../movielens Dataset").resolve()

top_movies = pd.read_csv(DATA_PATH.joinpath("top_movies.csv"))


def fetch_movie_data(movie_title):
    api_key = '8884cb9'  # Replace with your actual OMDb API key
    url = f'http://www.omdbapi.com/?t={movie_title}&apikey={api_key}'

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data.get('Response') == 'True':
            print(f"Fetched data for {movie_title}: {data}")
            return data
        else:
            print(f"OMDb API error for {movie_title}: {data.get('Error')}")
            return None
    else:
        print(f"Failed to fetch data for {movie_title}, status code: {response.status_code}")
        return None

def create_movie_card(movie_data):
    poster = movie_data.get('Poster', '/assets/default_poster.jpg')
    if poster == "N/A" or poster == "":
        poster = '/assets/default_poster.jpg'

    movie_title = movie_data.get('Title', 'Unknown Title')
    if movie_title == 'Unknown Title':
        return None  # Skip creating card for unknown titles

    imdb_link = f"https://www.imdb.com/title/{movie_data.get('imdbID')}/"

    return dbc.Col(
        dbc.Card(
            [
                html.A(
                    dbc.CardImg(src=poster, top=True, style={"height": "300px"}),
                    href=imdb_link,
                    target="_blank"
                ),
                dbc.CardBody(
                    html.A(
                        html.H5(movie_title, className="card-title"),
                        href=imdb_link,
                        target="_blank"
                    ),
                    style={"text-align":"center", "min-height": "110px"}  # Adjust height for card body
                ),
            ],
            style={"width": "200px", "margin": "10px"}
        ),
        width=3  # Each column width for 4 cards per row
    )

movie_cards = []

for title in top_movies['title']:
    movie_data = fetch_movie_data(title)
    if movie_data:
        movie_card = create_movie_card(movie_data)
        if movie_card:
            movie_cards.append(movie_card)

layout = dbc.Container(
    [
        dbc.Row([dbc.Col(html.H3("Most Popular Movies"), width={"size": 6})]),
        dbc.Row([dbc.Col(html.Hr())]),
        dbc.Row(
            [
                dbc.Col(movie_card, width=2)
                for movie_card in movie_cards
            ],
            justify="start",
            className="g-2"
        )
    ],
    fluid=True,
    style={"margin-top": "40px", 'margin-left':'10px'}
)
