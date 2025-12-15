from json import loads

import pandas as pd
from sqlmodel import SQLModel, create_engine

DATASETS_DIRECTORY = 'datasets'
MOVIE_LENS_SUBDIRECTORY = 'ml-latest-small'
TMDB_SUBDIRECTORY = 'tmdb'

def _load_dataframe(subdirectory: str, filename: str) -> pd.DataFrame:
    return pd.read_csv(f'{DATASETS_DIRECTORY}/{subdirectory}/{filename}')

# MOVIE LENS DATASET
# movies.csv columns: ['movieId', 'title', 'genres']
# ratings.csv columns: ['userId', 'movieId', 'rating', 'timestamp']
# links.csv columns: ['movieId', 'imdbId', 'tmdbId']
# tags.csv columns: ['userId', 'movieId', 'tag', 'timestamp'] -> not relevant here
ml_movies = _load_dataframe(MOVIE_LENS_SUBDIRECTORY, 'movies.csv').astype({'movieId': 'Int64'})
ml_ratings = _load_dataframe(MOVIE_LENS_SUBDIRECTORY, 'ratings.csv')
ml_links = _load_dataframe(MOVIE_LENS_SUBDIRECTORY, 'links.csv').dropna().astype('Int64')
merged_ml = ml_movies.merge(ml_links, left_on='movieId', right_on='movieId', how='left')

# Both the "genres" and "ratings" tables are easily derived from the MovieLens dataset
ml_movies['genre'] = ml_movies['genres'].rename('genre')
genres = ml_movies[['movieId', 'genre']]
ratings = ml_ratings[['movieId', 'rating']]
# The full "movies" table is mainly based on the MovieLens dataset but is supplemented by the TMDB dataset as available

# TMDB DATASET
# tmdb_5000_movies.csv columns: ['budget', 'genres', 'homepage', 'id', 'keywords', 'original_language',
#                       'original_title', 'overview', 'popularity', 'production_companies',
#                       'production_countries', 'release_date', 'revenue', 'runtime',
#                       'spoken_languages', 'status', 'tagline', 'title', 'vote_average', 'vote_count']
# tmdb_5000_credits.csv columns: ['movie_id', 'title', 'cast', 'crew']
tmdb_movies = _load_dataframe(TMDB_SUBDIRECTORY, 'tmdb_5000_movies.csv').astype({'id': 'Int64'})
tmdb_credits = _load_dataframe(TMDB_SUBDIRECTORY, 'tmdb_5000_credits.csv').astype({'movie_id': 'Int64'})
merged_tmdb = tmdb_movies.merge(tmdb_credits, left_on='id', right_on='movie_id')

merged_ml_and_tmdb = merged_ml.merge(merged_tmdb, left_on='tmdbId', right_on='id', how='left')

# All relevant fields for the consolidated "movies" table:
# id: uses the MovieLens id is the primary key (tmdbId from MovieLens' links.csv is essentially a foreign key)
movie_id = merged_ml_and_tmdb['movieId']
# - title: more convenient in MovieLens (longer list of movies)
title = merged_ml_and_tmdb['title'].apply(lambda text: text.strip()[:-6].strip())
# - year: more convenient in MovieLens (appended to "title")
year = merged_ml_and_tmdb['title'].apply(lambda text: text.strip()[-5:-1].strip()).rename('year')
# - overview/plot: TMDB
overview = merged_ml_and_tmdb['overview']
# - cast: TMDB
merged_ml_and_tmdb['cast'] = merged_ml_and_tmdb['cast'].fillna('').apply(lambda c: loads(c) if c else [])
cast = merged_ml_and_tmdb['cast'].apply(lambda cm: ', '.join([c['name'] for c in cm]))
# - director: TMDB
def _get_director(crew: str) -> str:
    if not crew:
        return ''

    try:
        for d in loads(crew):
            if d.get('job', '').lower() == 'director':
                return d.get('name')
    except TypeError:
        return ''

    return ''

director = merged_ml_and_tmdb['crew'].apply(lambda crew: _get_director(crew)).rename('director')

movies = pd.concat([movie_id, title, year, overview, cast, director], axis=1, join='outer').fillna('')

TOTAL_MOVIES = len(ml_movies)
num_movies, num_genres = len(movies), len(genres)
message = f"Number of movies ({num_movies}) and genres ({num_genres}) don't both equal {TOTAL_MOVIES}!"
assert num_movies == num_genres == TOTAL_MOVIES, message

# SQLite Database with 3 tables: movies, genres, and ratings
engine = create_engine("sqlite:///database.db")
SQLModel.metadata.create_all(engine)

movies.to_sql(name='movies', con=engine)
genres.to_sql(name='genres', con=engine)
ratings.to_sql(name='ratings', con=engine)
