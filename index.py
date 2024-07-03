from dash import dcc, html, Input, Output, State, callback_context
from dash_iconify import DashIconify
import pathlib
import dash_bootstrap_components as dbc
import pandas as pd
from app import app
from pages import homepage, user, movie, popular, user_recommendations

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("./data").resolve()

movies = pd.read_csv(DATA_PATH.joinpath("movies.csv"))
ratings = pd.read_csv(DATA_PATH.joinpath("ratings.csv"))
# Get the maximum user and movie IDs
max_userid = ratings['userId'].drop_duplicates().max()
max_movieid = ratings['movieId'].drop_duplicates().max()
num_users = max_userid + 1
num_items = max_movieid + 1

OMDB_API_KEY = '249559df'  # Replace with your actual OMDb API key
OMDB_API_URL = f'http://www.omdbapi.com/?apikey={OMDB_API_KEY}'

# Define layout structure
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dbc.Row([
        dbc.Col(
            dbc.Nav(
                [
                    html.Div(
                        html.Img(src=app.get_asset_url('moviematch.png'),
                                 style={'height': '60px', 'margin-bottom': '20px'}),
                        style={"text-align": "center", "margin-top": "10px", "margin-bottom": "60px",
                               "padding-top": "20px"}
                    ),
                    html.Div("M E N U",
                             style={"margin-top": "8px", "margin-bottom": "10px", "padding-left": "20px",
                                    "font-family": "Roboto Condensed', sans-serif", "color": "#525050"}
                             ),
                    dbc.NavLink(
                        [
                            html.Span(id='home-icon', children=DashIconify(icon="fa:home", style={'margin-right': 11,
                                                                                                  'font-size': 28})),
                            html.Span("Home", id='home-text',
                                      style={"font-family": "Roboto Condensed', sans-serif", 'color': '#fff'})
                        ],
                        id='nav-home',
                        href="/pages/homepage",
                        style={"padding-left": "30px", "padding-bottom": "5px"},
                        active="exact"
                    ),
                    dbc.NavLink(
                        [
                            html.Span(id='user-icon', children=DashIconify(icon="fa-solid:user-friends",
                                                                           style={'margin-right': 12,
                                                                                  'font-size': 28})),
                            html.Span("Personalized Picks", id='user-text',
                                      style={"font-family": "Roboto Condensed', sans-serif", 'color': '#fff'})
                        ],
                        id='nav-user',
                        href="/pages/user",
                        style={"padding-left": "30px", "padding-bottom": "5px"},
                        active="exact"
                    ),
                    dbc.NavLink(
                        [
                            html.Span(id='movie-icon', children=DashIconify(icon="fa:film",
                                                                            style={'margin-right': 12,
                                                                                   'font-size': 28})),
                            html.Span("Movie Matchmaker", id='movie-text',
                                      style={"font-family": "Roboto Condensed', sans-serif", 'color': '#fff'})
                        ],
                        id='nav-movie',
                        href="/pages/movie",
                        style={"padding-left": "30px", "padding-bottom": "5px"},
                        active="exact"
                    ),
                    dbc.NavLink(
                        [
                            html.Span(id='star-icon', children=DashIconify(icon="uim:star",
                                                                           style={'margin-right': 12,
                                                                                  'font-size': 32})),
                            html.Span("Top Rated", id='star-text',
                                      style={"font-family": "Roboto Condensed', sans-serif", 'color': '#fff'})
                        ],
                        id='nav-top-rated',
                        href="/pages/popular",
                        style={"padding-left": "30px", "padding-bottom": "5px"},
                        active="exact"
                    )
                ],
                vertical=True,
                style={"height": "100%", "background-color": "#141313"}
            ),
            style={"position": "fixed", "width": "320px", "height": "100%"},
            width=3
        ),
        dbc.Col(
            html.Div(id='page-content', style={"margin-left": "270px", "padding": "20px"})  # Adjusted margin-left
        )
    ])
])


@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/pages/homepage':
        return homepage.layout
    elif pathname == '/pages/user':
        return user.layout
    elif pathname == '/pages/movie':
        return movie.layout
    elif pathname == '/pages/popular':
        return popular.layout
    elif pathname.startswith('/pages/recommendations'):
        return user_recommendations.layout

    else:
        return homepage.layout


@app.callback(
    [
        Output('home-icon', 'style'),
        Output('home-text', 'style'),
        Output('user-icon', 'style'),
        Output('user-text', 'style'),
        Output('movie-icon', 'style'),
        Output('movie-text', 'style'),
        Output('star-icon', 'style'),
        Output('star-text', 'style')
    ],
    [Input('url', 'pathname')]
)
def update_navlink_styles(pathname):
    active_color = '#f72f6a'
    default_color = '#fff'

    home_icon_style = {'color': active_color if pathname == '/pages/homepage' else default_color, 'margin-right': 11,
                       'font-size': 28}
    home_text_style = {'color': active_color if pathname == '/pages/homepage' else default_color,
                       "font-family": "Roboto Condensed', sans-serif"}

    user_icon_style = {'color': active_color if pathname == '/pages/user' or pathname.startswith(
        '/pages/user/recommendations?user_id=') else default_color, 'margin-right': 12,
                       'font-size': 28}
    user_text_style = {'color': active_color if pathname == '/pages/user' or pathname.startswith(
        '/pages/user/recommendations?user_id=') else default_color,
                       "font-family": "Roboto Condensed', sans-serif"}

    movie_icon_style = {'color': active_color if pathname == '/pages/movie' else default_color, 'margin-right': 12,
                        'font-size': 28}
    movie_text_style = {'color': active_color if pathname == '/pages/movie' else default_color,
                        "font-family": "Roboto Condensed', sans-serif"}

    star_icon_style = {'color': active_color if pathname == '/pages/popular' else default_color, 'margin-right': 12,
                       'font-size': 28}
    star_text_style = {'color': active_color if pathname == '/pages/popular' else default_color,
                       "font-family": "Roboto Condensed', sans-serif"}

    return home_icon_style, home_text_style, user_icon_style, user_text_style, movie_icon_style, movie_text_style, star_icon_style, star_text_style,


# Combined callback for both user and movie recommendations
@app.callback(
    Output('url', 'pathname'),
    [Input('user-submit-button', 'n_clicks'),
     Input('movie-submit-button', 'n_clicks')],
    [State('user-id-dropdown', 'value'),
     State('movie-dropdown', 'value')]
)
def update_output(n_clicks_user, n_clicks_movie, user_id, movie_id):
    print(n_clicks_user, n_clicks_movie)
    ctx = callback_context
    if not ctx.triggered:
        return '/pages/homepage'
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id == 'user-submit-button' and n_clicks_user and user_id is not None:
        return f'/pages/recommendations?user_id={user_id}'
    elif button_id == 'movie-submit-button' and n_clicks_movie and movie_id is not None:
        return f'/pages/recommendations?movie_id={movie_id}'

    return '/pages/homepage'


if __name__ == '__main__':
    app.run_server(port='8051', debug=False)
