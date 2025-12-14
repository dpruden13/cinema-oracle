from json import loads

from llm import call_llm, medium


def detect_intent(user_prompt: str) -> str:
    # Can result in JSONDecodeError
    return loads(call_llm(
        prompt=(
            f'Which topic does the following user prompt relate to? {user_prompt} '
            'Respond ONLY with a JSON object with a KEY and VALUE. '
            'The KEY should be "genres" or "ratings" or "title" or "year" or "cast" or "director" or "plot" or "other". '
            'The VALUE should be the specific data for that KEY. '
            'Example: {"genres": "adventure"} '
            'Another example: {"year": "1997"} '
            'Another example: {"cast": "Kate Winslet"} '
            'Another example: {"director": "James Cameron"} '
            'Another example: {"plot": "ship sinks"} '
            'Another example: {"other": "highest budget movie"}'
            ),
        model_type=medium,
        retry=False,  # the 'basic' model ignores formatting instructions
        ).strip().removeprefix('```json').removesuffix('```').strip())  # remove unnecessary text
