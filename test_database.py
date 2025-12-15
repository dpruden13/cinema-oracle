from database import query_database


def test_number_of_movies_returned():
    results = query_database("SELECT * FROM movies")
    assert len(results) == 9_742


def test_number_of_ratings_returned():
    results = query_database("SELECT * FROM ratings")
    assert len(results) == 100_836
