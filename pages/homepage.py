import dash_bootstrap_components as dbc
from dash import html
import requests

# Example movie titles
movie_titles = ['fight+club', 'deadpool', 'inside+out', 'bad+boys', 'top+gun+maverick']

# Function to fetch movie data from OMDb API
def fetch_movie_data(movie_title):
    api_key = '249559df'  # Replace with your actual OMDb API key
    url = f'http://www.omdbapi.com/?t={movie_title}&apikey={api_key}'

    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Function to update carousel items based on fetched data
def update_carousel_items(movie_titles):
    carousel_items = []
    for title in movie_titles:
        movie_data = fetch_movie_data(title)
        if movie_data and movie_data.get('Poster'):
            carousel_items.append({
                "key": title,
                "src": movie_data['Poster'],
                "alt": movie_data.get('Title', 'Unknown Title'),
                "href": f"https://www.imdb.com/title/{movie_data.get('imdbID')}/"  # IMDb link
            })
        else:
            carousel_items.append({
                "key": title,
                "src": '/assets/default_poster.jpg',  # Default image if no poster available
                "alt": title,
                "href": "#"  # Placeholder link
            })
    return carousel_items



# Define layout for homepage
layout = dbc.Container(
    [
        # Title Row
        dbc.Row(
            dbc.Col(
                html.Div(
                    [
                        html.H1(
                            [
                                "MOVIE RECOMMENDATION ENGINE"
                            ],
                            className="display-4",
                            style={
                                'text-align': 'center', 'margin-top': '40px', 'margin-bottom': '50px',
                                'text-shadow': '0 0 7px rgba(247,232,232,.5), 0 0 10px rgba(216,170,210,.5)'
                            }
                        )
                    ]
                )
            )
        ),

        # Main Content Row
        dbc.Row(
            [
                # Text Content Column
                dbc.Col(
                    html.Div(
                        [

                            html.P("Finding the perfect movie has never been easier!",
                                   className="lead",
                                   style={'margin-top': '10px', 'margin-bottom': '10px', "font-family": "Roboto Condensed, sans-serif"}),
                            html.P(
                                "Struggling to choose a movie from countless options? Let our advanced recommendation engine do the work for you! By analyzing your viewing history and favorite films, we’ll suggest the perfect movie for your next night in. Discover your next favorite film effortlessly!",
                                style={'margin-top': '20px', 'margin-bottom': '30px', "font-family": "Roboto Condensed, sans-serif"}),

                            html.A(
                                dbc.Button("Get Started", color='dark', className="me-1", href="/pages/user"),
                                style={'text-align': 'center', 'margin-bottom': '20px', 'display': 'block',
                                       'color': '#f72f6a'}
                            ),
                            html.H4("Why Choose Us?", style={'margin-top': '60px', 'margin-bottom': '20px','color':'#b7aeae'}),
                            html.Ul(
                                [
                                    html.Li("Personalized Recommendations"),
                                    html.Li("Wide Range of Movies"),
                                    html.Li("Easy to Use Interface"),
                                    html.Li("Regular Updates"),
                                ],
                                style={"font-family": "Roboto Condensed, sans-serif"}
                            )
                        ],
                        style={'padding': '15px'}
                    ),
                    width=7  # Adjust width for text content column
                ),

                # Carousel Column
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            dbc.Carousel(
                                items=update_carousel_items(movie_titles),
                                id='carousel',  # Assign an id for callbacks
                                controls=True,
                                indicators=True,
                                interval=1900,
                                ride="carousel"
                            )
                        ),
                        style={"width": "84%", "margin": "auto"}
                    ),
                    width=5  # Adjust width for carousel column
                ),
            ],
            style={"padding-top": "18px", "padding-left": "120px", "padding-right": "120px"},  # Adjust padding
        ),
        dbc.Row(
            dbc.Col(
                html.Div(
                    [
                        html.H2("Statistics", style={'margin-top': '40px', 'margin-bottom': '20px','color':'#ef174d'}),
                        html.P("Over 9,000 movies recommended!", style={"font-family": "Roboto Condensed, sans-serif"}),
                        html.P("Updated weekly with new movies", style={"font-family": "Roboto Condensed, sans-serif"}),
                    ],
                    style={'text-align': 'center', 'padding': '20px'}
                )
            )
        )
    ],
    fluid=True,
)


