import os
import logging

from openai import AsyncClient as OpenaiClient
from groq import AsyncGroq as GroqClient


class AI:
    gpt_model = 'gpt-4o-mini'
    llama_model = 'llama3-70b-8192'
    gemini_model = 'gemma2-9b-it'

    current_model = gpt_model

    @staticmethod
    def get():
        match AI.current_model:
            case AI.gpt_model:
                return OpenaiClient, AI.gpt_model, os.environ.get("OPENAI_API_KEY")
            case AI.llama_model:
                return GroqClient, AI.llama_model, os.environ.get("GROQ_API_KEY")
            case AI.gemini_model:
                return GroqClient, AI.gemini_model, os.environ.get("GROQ_API_KEY")

    @staticmethod
    async def generateText(messages: list, logInfo: str) -> str:
        client, model, api_key = AI.get()
        logging.info(f'{logInfo} [START] <{model}>')

        completion = await client(api_key=api_key).chat.completions.create(
            model=model,
            messages=messages,
        )

        logging.info(f'{logInfo} [DONE] <{model}>')
        return completion.choices[0].message.content

    @staticmethod
    def format(content: str, role: str) -> dict:
        return {
            'role': role,
            'content': content,
        }
