import os
from openai import OpenAI

# Initialize the OpenAI client with the API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Define system prompts for each agent persona
SYSTEM_PROMPTS = {
    "CTOAgent": (
        "You are a highly experienced startup CTO. "
        "Advise on technology choices, system architecture, and engineering best practices. "
        "Keep answers concise but thorough."
    ),
    "PMAgent": (
        "You are a skilled product manager for startups. "
        "Guide the user on product features, roadmap planning, user stories, and MVP scope."
    ),
    "InvestorAgent": (
        "You are a seasoned startup investor. "
        "Provide insights on funding strategies, investor pitch, valuation, and business growth."
    )
}

class Agent:
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.system_prompt = SYSTEM_PROMPTS.get(
            agent_name,
            "You are a helpful AI assistant."
        )

    def generate_prompt(self, context: str, user_input: str) -> str:
        """
        Combine system prompt, context, and user input into one final prompt for the LLM.

        Args:
            context (str): Relevant context retrieved from memory and RAG retriever.
            user_input (str): The current user question or instruction.

        Returns:
            str: The full prompt string sent to the LLM.
        """
        prompt = (
            f"{self.system_prompt}\n\n"
            f"Context:\n{context}\n\n"
            f"User: {user_input}\n"
            f"Answer:"
        )
        return prompt

    def call_llm(self, prompt: str) -> str:
        """
        Send prompt to OpenAI Chat Completions API and get response.

        Args:
            prompt (str): The prompt string.

        Returns:
            str: The generated text response from the LLM.
        """
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.7,
                n=1
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Error during LLM call: {e}"