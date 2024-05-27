from gpt import GPT
from game_context import startContext, userPrompt, codePrompt, systemPrompt, imagePrompt


class Game:
    def __init__(self, settings):
        self.counter = 0

        self.gpt = GPT()
        self.settings = settings

        self.logFile = 'log.txt'
        open(self.logFile, 'w')

    async def start(self):
        await self.gpt.addMessage(startContext)

        if self.settings:
            await self.gpt.addMessage(f'Параметры истории:\n{self.settings}', role='system')

        await self.gpt.addMessage(userPrompt, role='system')
        return await self.userResponse()

    async def move(self, message):
        self.counter += 1
        await self.gpt.addMessage(message)

        if self.counter == 10:
            await self.gpt.addMessage('Закончи историю', role='system')
        result = await self.userResponse()
        return result

    async def userResponse(self):
        await self.gpt.addMessage(codePrompt, role='system')
        answer = await self.gpt.generate()
        self.gpt.deleteMessage()

        result = {
            'code': answer[0],
            'text': answer[1:],
        }

        match result['code']:
            case '1':
                await self.gpt.addMessage(result['text'], role='assistant')
                try:
                    result['image'] = await self.createImage(result['text'])
                except Exception:
                    pass
                await self.systemResponse(systemPrompt)

            case '2':
                await self.gpt.addMessage(result['text'], role='assistant')
                try:
                    result['image'] = await self.createImage(result['text'])
                except Exception:
                    pass

            case '3':
                await self.gpt.addMessage(result['text'], role='assistant')

            case '0':
                self.gpt.deleteMessage()

            case _:
                pass

        return result

    async def systemResponse(self, message):
        await self.gpt.addMessage(message, role='system')
        result = await self.gpt.generate()
        self.gpt.deleteMessage()
        await self.gpt.addMessage(result, role='assistant')

    async def createImage(self, text):
        return await self.gpt.generateImage(f'{imagePrompt}{text}')

    def get_context(self):
        return self.gpt.context
