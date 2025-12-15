from json import loads

from llm import call_llm, best
from database import query_database


def detect_intent(user_prompt: str) -> str:
    # Can result in JSONDecodeError
    return loads(
        call_llm(
            prompt=(
                f'Which topic does the following user prompt relate to? {user_prompt} '
                'Respond ONLY with a JSON object with a KEY and VALUE. '
                'The KEY should be "genres" or "ratings" or "title" or "year" or "director" or "plot" or "other". '
                'The VALUE should be the specific data for that KEY. '
                'Example: {"genres": "adventure"} '
                'Another example: {"year": "1997"} '
                'Another example: {"cast": "Kate Winslet"} '
                'Another example: {"director": "James Cameron"} '
                'Another example: {"plot": "ship sinks"} '
                'Another example: {"other": "highest budget movie"}'
                ).strip().removeprefix('```json').removesuffix('```').strip()))  # remove unnecessary text


def answer_query(user_prompt: str, model_type: str = best, retry: bool = True) -> str:
    intent = detect_intent(user_prompt)
    topic, data = list(intent.items())[0]
    if topic == 'genres':
        statement = f"SELECT * FROM genres JOIN movies ON genres.movieId=movies.movieId WHERE genres LIKE '%{data}%'"
    elif topic == 'ratings':
        statement = f"SELECT * FROM ratings JOIN movies ON ratings.movieId=movies.movieId WHERE rating = '{data}' LIMIT 1000"
    elif topic == 'title':
        statement = f"SELECT * FROM movies WHERE title LIKE '%{data}%'"
    elif topic == 'year':
        statement = f"SELECT * FROM movies WHERE year = '{data}'"
    elif topic == 'director':
        statement = f"SELECT * FROM movies WHERE director LIKE '%{data}%'"
    elif topic == 'plot':
        statement = f"SELECT * FROM movies WHERE overview LIKE '%{data}%'"
    else:
        raise Exception(f'Could not ascertain user intent: {topic} -> {data}')
    movies = query_database(statement)
    prompt = f'Given these movies: {movies} answer this question: {user_prompt}'
    return call_llm(prompt=prompt, model_type=model_type, retry=retry)
