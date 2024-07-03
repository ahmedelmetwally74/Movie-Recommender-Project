import pathlib
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, State
import pandas as pd

# File paths
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../movielens Dataset").resolve()

# Load movies data
movies = pd.read_csv(DATA_PATH.joinpath("movies.csv"))


layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                html.H2("🚀 Get Movie Recommendations Now!",
                        style={
                            'text-align': 'center', 'margin-top': '40px', 'margin-bottom': '50px',
                            'text-shadow': '0 0 7px rgba(231,72,182,.5), 0 0 10px rgba(216,170,210,.5)'
                        })
            )
        ),
        dbc.Row(
            dbc.Col(
                html.Div("Select a Movie Title", style={'margin-bottom': '10px'}),
                width=6,
                style={'margin': 'auto'}
            )
        ),
        dbc.Row(
            dbc.Col(
                dcc.Dropdown(
                    id='movie-dropdown',
                    options=[{'label': title, 'value': movie_id} for movie_id, title in zip(movies['movieId'], movies['title'])],
                    placeholder="Select a Movie Title",
                    style={'margin-bottom': '20px', 'color': '#161414'}
                ),
                width=6,
                style={'margin': 'auto'}
            )
        ),
        dbc.Row(
            dbc.Col(
                dbc.Button("Generate", id='movie-submit-button', color='dark', style={'margin-top': '20px'}),
                width='auto',
                style={'margin': 'auto'}
            )
        ),
        # Store to hold button state
        dcc.Store(id='movie-button-state', storage_type='session', data={'button_clicked': False})
    ],
    fluid=True,
)
