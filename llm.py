from transformers import pipeline
from ollama import chat, ChatResponse


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

answer = call_gemma('What is the biggest city in the world?')
print(answer)
