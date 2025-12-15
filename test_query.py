from llm import medium
from query import detect_intent, answer_query


def test_genre_intent():
    answer = detect_intent(user_prompt="What are some adventure movies in this dataset?")
    assert answer == {"genre": "adventure"}


def test_director_intent():
    answer = detect_intent(user_prompt="Which movies were directed by James Cameron?")
    assert answer == {"director": "James Cameron"}


def test_year_intent():
    answer = detect_intent(user_prompt="Which movies came out in 1930?")
    assert answer == {"year": "1930"}


def test_answer_query_does_not_crash():
    answer_query(user_prompt="Which movies were directed by James Cameron?", model_type=medium)
