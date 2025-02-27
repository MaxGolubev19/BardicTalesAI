import asyncio

from ai import AI
from writing.write import Write
from prompt_editor import PromptEditor

from languages.english import patterns as english_patterns
from languages.russian import patterns as russian_patterns


class Game:
    HISTORY_SIZE = 5

    def __init__(self, user_id: int, user_name: str, language: str):
        self.write = Write(user_id, user_name)
        self.user_id = user_id
        self.user_name = user_name
        self.language = language
        self.prompt_editor = PromptEditor(self.language)

        self.future = None
        self.past = [None for _ in range(Game.HISTORY_SIZE * 2 + 1)]
        self.info = None

        self.past_relevant = True
        self.info_relevant = True

        self.count = 0
        self.wait = False
        self.current_task = None

    def set_language(self, language: str):
        self.language = language
        self.prompt_editor.set_language(self.language)
        return self

    async def set_settings(self, settings: str):
        self.prompt_editor.settings.edit(settings)
        await self.write.set_settings(settings)
        return self

    async def set_random_settings(self):
        self.prompt_editor.settings.reset(self.language)
        await self.write.set_settings(self.prompt_editor.get_settings())
        return self

    async def set_start_prompt(self, prompt: str):
        self.prompt_editor.start_prompt.edit(prompt)
        await self.write.set_start_prompt(prompt)
        return self

    async def set_move_prompt(self, prompt: str):
        self.prompt_editor.move_prompt.edit(prompt)
        await self.write.set_move_prompt(prompt)
        return self

    async def set_future_prompt(self, prompt: str):
        self.prompt_editor.future_prompt.edit(prompt)
        await self.write.set_future_prompt(prompt)
        return self

    async def set_past_prompt(self, prompt: str):
        self.prompt_editor.past_prompt.edit(prompt)
        await self.write.set_past_prompt(prompt)
        return self

    async def set_create_info_prompt(self, prompt: str):
        self.prompt_editor.create_info_prompt.edit(prompt)
        await self.write.set_create_info_prompt(prompt)
        return self

    async def set_update_info_prompt(self, prompt: str):
        self.prompt_editor.update_info_prompt.edit(prompt)
        await self.write.set_update_info_prompt(prompt)
        return self

    async def set_start_template(self, prompt: str):
        self.prompt_editor.start_template.edit(prompt)
        await self.write.set_start_template(prompt)
        return self

    async def set_move_template(self, prompt: str):
        self.prompt_editor.move_template.edit(prompt)
        await self.write.set_move_template(prompt)
        return self

    async def set_future_template(self, prompt: str):
        self.prompt_editor.future_template.edit(prompt)
        await self.write.set_future_template(prompt)
        return self

    async def set_past_template(self, prompt: str):
        self.prompt_editor.past_template.edit(prompt)
        await self.write.set_past_template(prompt)
        return self

    async def set_info_template(self, prompt: str):
        self.prompt_editor.info_template.edit(prompt)
        await self.write.set_info_template(prompt)
        return self

    def set_incognito(self, incognito: bool):
        self.write.set_incognito(incognito)
        return self

    def reset(self):
        return Game(self.user_id, self.user_name, self.language)

    async def start(self) -> str:
        if self.current_task is not None:
            self.current_task.cancel()

        self.wait = True
        self.count = 1
        self.past_relevant = False
        self.info_relevant = False

        self.future = None
        self.past = [None for _ in range(Game.HISTORY_SIZE * 2 + 1)]
        self.info = None

        now = await self.createTaskAI([
            AI.format(self.prompt_editor.get_start_prompt(), 'system'),
            AI.format(self.prompt_editor.get_new_settings(), 'user'),
        ], 'now', 'Bot')

        self.wait = False
        return now

    async def move(self, answer: str) -> str:
        while not (self.past_relevant and self.info_relevant):
            await asyncio.sleep(0.1)

        self.wait = True
        self.count += 1
        self.past_relevant = False
        self.info_relevant = False

        self.past[0] = AI.format(answer, 'user')
        await self.write.move('User', answer)

        now = await self.createTaskAI([
            AI.format(self.prompt_editor.get_move_prompt(), 'system'),
            AI.format(self.prompt_editor.get_settings(), 'user'),
            AI.format(self.info, 'user'),
            AI.format(self.future, 'user'),
            *self.past[:(self.count - 1) * 2][::-1],
        ], 'now', 'Bot')

        self.wait = False
        return now

    async def other(self, now: str):
        if self.count == 1:
            await self.generate_future(now)
        await self.generate_past(now)
        await self.generate_info(now)

    async def generate_future(self, now: str):
        self.future = await self.createTaskAI([
            AI.format(self.prompt_editor.get_future_prompt(), 'system'),
            AI.format(self.prompt_editor.get_settings(), 'user'),
            AI.format(now, 'user'),
        ], 'future', 'Future')

    async def generate_past(self, now):
        if self.count == Game.HISTORY_SIZE + 1:
            self.past[-1] = AI.format(self.past[-2]['content'], 'user')
 
        elif self.count > Game.HISTORY_SIZE + 1:
            self.past[-1] = AI.format(await self.createTaskAI([
                AI.format(self.prompt_editor.get_past_prompt(), 'system'),
                self.past[-1],
                AI.format(self.past[-2]['content'], 'user'),
            ], 'past', 'Past'), 'user')

        for i in range(Game.HISTORY_SIZE - 1, 0, -1):
            self.past[i * 2] = self.past[i * 2 - 2]
            self.past[i * 2 + 1] = self.past[i * 2 - 1]

        self.past[1] = AI.format(now, 'assistant')
        self.past_relevant = True

    async def generate_info(self, now):
        if self.info is None:
            self.info = await self.createTaskAI([
                AI.format(self.prompt_editor.get_create_info_prompt(), 'system'),
                AI.format(now, 'user'),
            ], 'info', 'Info')

        else:
            self.info = await self.createTaskAI([
                AI.format(self.prompt_editor.get_update_info_prompt(), 'system'),
                AI.format(self.info, 'user'),
                AI.format(now, 'user'),
            ], 'info', 'Info')

        self.info_relevant = True

    async def createTaskAI(self, messages: list, typeRequest: str, role: str) -> str:
        self.current_task = asyncio.create_task(
            AI.generateText(
                messages,
                f'{self.user_id} ({self.user_name}): (move {self.count}) generating {typeRequest}'
            )
        )

        result = await self.current_task
        self.current_task = None
        await self.write.move(role, result)
        return result

    def get_patterns(self):
        match self.language:
            case 'english':
                return english_patterns
            case 'russian':
                return russian_patterns
            case _:
                return english_patterns

    def get_info(self):
        if self.info is None:
            return self.get_patterns().not_generate()
        elif self.info_relevant:
            return self.info
        else:
            return f'{self.get_patterns().old_information()}\n\n{self.info}'

    def get_future(self):
        if self.future is None:
            return self.get_patterns().not_generate()
        else:
            return self.future

    def __getstate__(self):
        state = self.__dict__.copy()
        state['current_task'] = None
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self.current_task = None
