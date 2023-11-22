import os
from typing import List

import backoff
from backoff import expo
from openai import OpenAI


class OpenAIHelper:
    def __init__(self):
        self.api_key = os.environ["OPENAI_API_KEY"]
        self.client = OpenAI()

    @backoff.on_exception(wait_gen=expo, exception=BaseException, max_tries=10)
    def generate_embedding(self, text: str) -> List[float]:
        response = self.client.embeddings.create(
            model="text-embedding-ada-002", input=text
        )
        return response.data[0].embedding

    @backoff.on_exception(wait_gen=expo, exception=BaseException, max_tries=10)
    def complete_prompt(self, prompt: str, temperature: float = 0.0) -> str:
        response = self.client.chat.completions.create(
            model="gpt-4-1106-preview",
            # model="gpt-3.5-turbo-1106",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
            temperature=temperature,
        )
        return response.choices[0].message.content
