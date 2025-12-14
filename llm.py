from transformers import pipeline


def call_deepseek(prompt: str) -> str:
    # https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B
    pipe = pipeline("text-generation", model="deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B")
    messages = [{"role": "user", "content": prompt}]
    response = pipe(messages)
    return [r for r in response[0]['generated_text'] if r['role'] == 'assistant'][0]['content']
