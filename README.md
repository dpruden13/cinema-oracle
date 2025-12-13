# Cinema Oracle

This project uses the [MovieLens dataset (small version: ~100k ratings, ~9k movies)](https://grouplens.org/datasets/movielens/) and the [TMDB 5000 Movie Dataset](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata). The files from these datasets can be found in the `datasets` directory. 

### Files:
- `requirements.txt` lists the Python libraries used. Note that this project uses Python 3.13.
- `database.py` shows the script that was used to wrangle the data from 5 CSV files (3 from MovieLens, 2 from TMDB) into a SQLite database. Now that the SQLite database has been created, this script does not need to be run again. 
- `sqlite:///database.db` is the SQLite database, which has 3 tables: movies, genres, and ratings
