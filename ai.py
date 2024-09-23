import os
import logging

from openai import AsyncClient as OpenaiClient
from ollama import AsyncClient as OllamaClient
from groq import AsyncGroq


class AI:
    openai_model = 'gpt-4o-mini'
    groq_model = 'llama-3.1-70b-versatile'
    llama_model = 'llama3'
    uncensored_llama_model = 'dolphin-llama3'

    current_API = 'openai'

    @staticmethod
    def model(parental_control) -> str:
        if parental_control:
            return AI.llama_model
        return AI.uncensored_llama_model

    @staticmethod
    async def generateText(messages: list, parental_control: bool, forLogging: str = None) -> str:
        if not parental_control:
            return await AI.generateOllama(messages, parental_control, forLogging)

        match AI.current_API:
            case 'openai':
                return await AI.generateGPT(messages, forLogging)
            case 'groq':
                return await AI.generateGroq(messages, forLogging)
            case 'ollama':
                return await AI.generateOllama(messages, parental_control, forLogging)

    @staticmethod
    async def generateGPT(messages: list, forLogging: str = None) -> str:
        # TestLog
        if forLogging:
            logging.info(f'{forLogging} [START] <GPT>')

        # Generate AI's answer
        client = OpenaiClient(
            api_key=os.environ.get("OPENAI_API_KEY"),
        )

        completion = await client.chat.completions.create(
            model=AI.openai_model,
            messages=messages,
        )

        # TestLog
        if forLogging:
            logging.info(f'{forLogging} [DONE] <GPT>')

        # Return AI's answer
        return completion.choices[0].message.content

    @staticmethod
    async def generateGroq(messages: list, forLogging: str = None) -> str:
        # TestLog
        if forLogging:
            logging.info(f'{forLogging} [START] <Groq>')

        # Generate AI's answer
        client = AsyncGroq(
            api_key=os.environ.get("GROQ_API_KEY"),
        )

        completion = await client.chat.completions.create(
            model=AI.groq_model,
            messages=messages,
        )

        # TestLog
        if forLogging:
            logging.info(f'{forLogging} [DONE] <Groq>')

        # Return AI's answer
        return completion.choices[0].message.content

    @staticmethod
    async def generateOllama(messages: list, parental_control: bool, forLogging: str = None) -> str:
        # TestLog
        if forLogging:
            logging.info(f'{forLogging} [START] <ollama>')

        # Generate AI's answer
        response = await OllamaClient().chat(
            model=AI.model(parental_control),
            messages=messages
        )

        # TestLog
        if forLogging:
            logging.info(f'{forLogging} [DONE] <ollama>')

        # Return AI's answer
        return response['message']['content']

    @staticmethod
    def format(content: str, role: str) -> dict:
        return {
            'role': role,
            'content': content,
        }
