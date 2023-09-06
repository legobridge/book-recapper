from typing import List

import backoff
import google.generativeai as palm
from backoff import expo
from google.generativeai.types import (
    SafetySettingDict,
    HarmBlockThreshold,
    HarmCategory,
)


class PalmHelper:
    def __init__(self, api_key) -> None:
        palm.configure(api_key=api_key)

        models = [
            m
            for m in palm.list_models()
            if "embedText" in m.supported_generation_methods
        ]
        self.embedding_model = models[0]

        models = [
            m
            for m in palm.list_models()
            if "generateText" in m.supported_generation_methods
        ]
        self.generation_model = models[0]

        self.SAFETY_SETTINGS = [
            SafetySettingDict(category=hc, threshold=HarmBlockThreshold.BLOCK_NONE)
            for hc in HarmCategory
        ]

    @backoff.on_exception(wait_gen=expo, exception=BaseException, max_tries=10)
    def generate_embedding(self, text: str) -> List[float]:
        return palm.generate_embeddings(model=self.embedding_model.name, text=text)[
            "embedding"
        ]

    @backoff.on_exception(wait_gen=expo, exception=BaseException, max_tries=10)
    def complete_prompt(self, prompt: str, temperature: float = 0.0) -> str:
        return palm.generate_text(
            model=self.generation_model.name,
            prompt=prompt,
            temperature=temperature,
            safety_settings=self.SAFETY_SETTINGS,
        ).result
