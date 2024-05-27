from g4f.client import AsyncClient as AsyncOpenAI


class AsyncGPT:
    text_model = 'gpt-3.5-turbo'
    image_model = 'dall-e-3'

    @staticmethod
    async def generateText(messages, temperature):
        client = AsyncOpenAI()

        completion = await client.chat.completions.create(
            model=AsyncGPT.text_model,
            messages=messages,
            temperature=temperature,
        )

        return completion.choices[0].message.content

    @staticmethod
    async def generateImage(prompt):
        client = AsyncOpenAI()

        completion = await client.images.generate(
            model=AsyncGPT.image_model,
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )

        return completion.data[0].url