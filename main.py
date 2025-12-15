from llm import best
from query import answer_query

from fastapi import FastAPI

api = FastAPI()


@api.get("/")
async def read_item(user_prompt: str, model_type: str = best, retry: bool = True):
    return answer_query(user_prompt=user_prompt, model_type=model_type, retry=retry)
