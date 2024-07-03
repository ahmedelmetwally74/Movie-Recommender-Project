import pathlib
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, State
import pandas as pd
from app import app

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../data").resolve()

movies = pd.read_csv(DATA_PATH.joinpath("movies.csv"))
ratings = pd.read_csv(DATA_PATH.joinpath("ratings.csv"))
# Get the maximum user and movie IDs
max_userid = ratings['userId'].drop_duplicates().max()
max_movieid = ratings['movieId'].drop_duplicates().max()
num_users = max_userid + 1
num_items = max_movieid + 1

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
                html.Div("Select user ID", style={'margin-bottom': '10px'}),
                width=6,
                style={'margin': 'auto'}
            )
        ),
        dbc.Row(
            dbc.Col(
                dcc.Dropdown(
                    id='user-id-dropdown',
                    options=[{'label': f'User {uid}', 'value': uid} for uid in range(1, max_userid + 1)],
                    placeholder="Select a User ID",
                    style={'margin-bottom': '20px', 'color': '#161414'}
                ),
                width=6,
                style={'margin': 'auto'}
            )
        ),
        dbc.Row(
            dbc.Col(
                dbc.Button("Generate", id='user-submit-button', color='dark', style={'margin-top': '20px'}),
                width='auto',
                style={'margin': 'auto'}
            )
        )
    ],
    fluid=True,
)

@app.callback(
    Output('user-submit-button', 'href'),  # Output is the href attribute of the button
    [Input('user-submit-button', 'n_clicks')],  # Trigger on button click
    [State('user-id-dropdown', 'value')]  # Get selected value from dropdown
)
def update_button_href(n_clicks_user, user_id):
    if n_clicks_user and user_id:
        return f'/pages/recommendations?user_id={user_id}'
    else:
        return '/pages/user'  # Default to user page if no button clicked or no user ID selected
