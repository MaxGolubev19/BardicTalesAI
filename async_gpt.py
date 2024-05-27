import os
from groq import AsyncGroq
from openai import AsyncOpenAI


class AsyncGPT:
    text_openai_model = 'gpt-4o'
    text_groq_model = 'llama3-70b-8192'
    image_model = 'dall-e-3'

    # @staticmethod
    # async def generateText(messages):
    #     client = AsyncOpenAI(
    #         api_key=os.environ.get("OPENAI_API_KEY"),
    #     )
    #
    #     completion = await client.chat.completions.create(
    #         model=AsyncGPT.text_openai_model,
    #         messages=messages,
    #     )
    #     return completion.choices[0].message.content

    @staticmethod
    async def generateText(messages):
        client = AsyncGroq(
            api_key=os.environ.get("GROQ_API_KEY"),
        )

        completion = await client.chat.completions.create(
            model=AsyncGPT.text_groq_model,
            messages=messages,
        )
        print(completion.choices[0].message.content)
        return completion.choices[0].message.content

    @staticmethod
    async def generateImage(prompt):
        # client = AsyncOpenAI(
        #     api_key=os.environ.get("OPENAI_API_KEY"),
        # )
        #
        # completion = await client.images.generate(
        #     model=AsyncGPT.image_model,
        #     prompt=prompt,
        #     size="1024x1024",
        #     quality="standard",
        #     n=1,
        # )
        #
        # return completion.data[0].url
        return 'картинка'
