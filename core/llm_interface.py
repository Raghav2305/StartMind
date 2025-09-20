# core/llm_interface.py

import os
from openai import OpenAI

class LLM:
    def __init__(self, model="gpt-3.5-turbo"):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = model

    def complete(self, prompt: str, system_prompt: str = "You are a helpful startup co-founder.") -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.0 # Set to 0 for more deterministic agent selection
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Error during LLM call: {e}"