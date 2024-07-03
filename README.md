# Movie Recommendation System

This project is a user-based movie recommendation system developed using the MovieLens dataset. The system employs a deep learning model to provide personalized movie recommendations for users based on their past ratings.

## About the Project

The goal of this project is to build a recommendation system that suggests movies to users based on their preferences. We used collaborative filtering techniques and deep learning to create a model that predicts the ratings users would give to movies they have not yet rated. The model was developed using TensorFlow and Keras, leveraging embeddings and dense layers to capture the latent features of users and movies.

### Key Features
- **User Embeddings**: Represent users in a latent space based on their interactions with movies.
- **Movie Embeddings**: Represent movies in a latent space based on user interactions.
- **Dense Layers**: Combine user and movie embeddings to predict ratings.
- **Dropout Layers**: Regularize the model to prevent overfitting.
- **Early Stopping**: Stop training when the model performance stops improving on the validation set.

### Dataset

We used the [MovieLens](https://www.kaggle.com/datasets/hanahelaly/movielens-small) dataset for training and evaluating our recommendation system. The dataset includes:

- **Ratings**: Contains user ratings for different movies.
- **Movies**: Contains metadata about the movies, including titles and genres.

#### Dataset Files
- `ratings.csv`: User ratings for movies.
- `movies.csv`: Metadata about the movies.
- `links.csv`: Identifiers that can be used to link to other sources of movie data.
- `tags.csv`: User-generated tags for movies.

### Project Structure

- **movielens Dataset**: Contains the dataset files.
- **models**: Contains the saved model architecture and weights.
- **Project Repositories**: Jupyter notebooks used for model training and evaluation.
- **README.md**: Project documentation.

## Video Demonstration

![Video Demonstration](https://github.com/ahmedelmetwally74/Movie-Recommender-Project/blob/main/Movie%20Match.gif)

## Team Members
- Ahmed El-Metwally
- Nawal Abdelmoniem
- Hana Helaly
- Nada Ibrahim
