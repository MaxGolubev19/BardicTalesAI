from async_gpt import AsyncGPT
import aiofiles
import datetime


class GPT:
    def __init__(self):
        self.context = []
        self.logFile = 'log.txt'
        open(self.logFile, 'w')

    async def addContext(self, context):
        for message in context:
            self.context.append(message)

        async with aiofiles.open(self.logFile, mode='a', encoding='utf-8') as logFile:
            for message in context:
                await logFile.write(f'({datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}) {message["role"]}:\n'
                                    f'{message["content"]}\n\n')

    async def addMessage(self, message, role='user'):
        self.context.append({
            'role': role,
            'content': message,
        })

        async with aiofiles.open(self.logFile, mode='a', encoding='utf-8') as logFile:
            await logFile.write(f'({datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}) {role}:\n'
                                f'{message}\n\n')

    def deleteMessage(self):
        self.context.pop(-1)

    async def generate(self):
        return await AsyncGPT.generateText(self.context)

    async def generatePlus(self, message, role='user'):
        await self.addMessage(message, role)
        return await self.generate()

    @staticmethod
    async def generateOne(prompt, role='user'):
        context = [{
            'role': role,
            'content': prompt,
        }]

        return await AsyncGPT.generateText(context)

    async def generateImage(self, prompt):
        async with aiofiles.open(self.logFile, mode='a', encoding='utf-8') as logFile:
            await logFile.write(f'({datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}) '
                                f'assistant: *рисует картинку*\n\n')

        return await AsyncGPT.generateImage(prompt)
