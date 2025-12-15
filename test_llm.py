from llm import call_llm, medium, basic


def test_best_model_does_not_crash():
    call_llm(prompt="What are some adventure movies in this dataset?")


def test_medium_model_does_not_crash():
    call_llm(prompt="Which movies were directed by James Cameron?", model_type=medium)


def test_basic_model_does_not_crash():
    call_llm(prompt="Which movies came out in 1930?", model_type=basic, retry=False)
