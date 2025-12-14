from transformers import pipeline
from ollama import chat, ChatResponse
from openai import OpenAI


MODEL_TYPES = [
    basic := 'basic',
    medium := 'medium',
    best := 'best',
    ]


def call_deepseek(prompt: str) -> str:
    # https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B
    pipe = pipeline("text-generation", model="deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B")
    messages = [{"role": "user", "content": prompt}]
    response = pipe(messages)
    return [r for r in response[0]['generated_text'] if r['role'] == 'assistant'][0]['content']


def call_gemma(prompt: str) -> str:
    # https://github.com/ollama/ollama-python
    response: ChatResponse = chat(model='gemma3:12b', messages=[{'role': 'user', 'content': prompt}])
    return response.message.content


def call_openai(prompt: str) -> str:
    # https://platform.openai.com/docs/quickstart?api-mode=responses&language=python
    client = OpenAI()
    response = client.responses.create(model="gpt-4.1-nano", input=prompt)
    return response.output_text


def call_llm(prompt: str, model_type: str = best, retry: bool = True) -> str:
    try:
        if model_type == basic:
            return call_deepseek(prompt)
        elif model_type == medium:
            return call_gemma(prompt)
        elif model_type == best:
            return call_openai(prompt)
        else:
            raise Exception(f'Unrecognized model_type "{model_type}", should be one of {MODEL_TYPES}')
    except Exception:
        if retry:
            model_type_index = MODEL_TYPES.index(model_type)
            if model_type_index == 0:
                raise
            return call_llm(prompt=prompt, model_type=MODEL_TYPES[model_type_index - 1], retry=retry)
        else:
            raise
