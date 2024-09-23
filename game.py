import asyncio

from ai import AI
from writing.write import Write

from languages import get_prompts
from languages.english import patterns as english_patterns
from languages.russian import patterns as russian_patterns


class Game:
    HISTORY_SIZE = 5

    def __init__(self, user_id: int, user_name: str, language: str):
        self.write = Write(user_id, user_name)
        self.user_id = user_id
        self.user_name = user_name
        self.language = language

        self.settings = get_prompts.settingsPrompt(self.language)
        self.start_prompt = get_prompts.startPrompt(self.language)
        self.future_prompt = get_prompts.futurePrompt(self.language)
        self.move_prompt = get_prompts.movePrompt(self.language)
        self.past_prompt = get_prompts.pastPrompt(self.language)
        self.create_info_prompt = get_prompts.createInfoPrompt(self.language)
        self.update_info_prompt = get_prompts.updateInfoPrompt(self.language)
        self.info_template = get_prompts.infoTemplate(self.language)

        self.edit_settings = False
        self.edit_start_prompt = False
        self.edit_move_prompt = False
        self.edit_future_prompt = False
        self.edit_past_prompt = False
        self.edit_create_info_prompt = False
        self.edit_update_info_prompt = False
        self.edit_info_template = False

        self.parental_control = True

        self.future = None
        self.past = [None for _ in range(Game.HISTORY_SIZE * 2 + 1)]
        self.info = None

        self.past_relevant = True
        self.info_relevant = True

        self.count = 0
        self.wait = 0
        self.current_task = None

    def set_language(self, language: str):
        self.language = language

        if not self.edit_settings:
            self.settings = get_prompts.settingsPrompt(self.language)

        if not self.edit_start_prompt:
            self.start_prompt = get_prompts.startPrompt(self.language)

        if not self.edit_move_prompt:
            self.move_prompt = get_prompts.movePrompt(self.language)

        if not self.edit_future_prompt:
            self.future_prompt = get_prompts.futurePrompt(self.language)

        if not self.edit_past_prompt:
            self.past_prompt = get_prompts.pastPrompt(self.language)

        if not self.edit_create_info_prompt:
            self.create_info_prompt = get_prompts.createInfoPrompt(self.language)

        if not self.edit_update_info_prompt:
            self.update_info_prompt = get_prompts.updateInfoPrompt(self.language)

        if not self.edit_info_template:
            self.info_template = get_prompts.infoTemplate(self.language)

        return self

    async def set_basic_settings(self, settings: str):
        self.settings = settings
        self.edit_settings = True
        await self.write.set_settings(settings)
        return self

    async def set_random_settings(self):
        self.settings = get_prompts.settingsPrompt(self.language)
        self.edit_settings = False
        await self.write.set_settings(self.settings)
        return self

    async def set_start_prompt(self, start_prompt: str):
        self.start_prompt = start_prompt
        self.edit_start_prompt = True
        await self.write.set_start_prompt(start_prompt)
        return self

    async def set_move_prompt(self, prompt: str):
        self.move_prompt = prompt
        self.edit_move_prompt = True
        await self.write.set_move_prompt(prompt)
        return self

    async def set_future_prompt(self, prompt: str):
        self.future_prompt = prompt
        self.edit_future_prompt = True
        await self.write.set_future_prompt(prompt)
        return self

    async def set_past_prompt(self, prompt: str):
        self.past_prompt = prompt
        self.edit_past_prompt = True
        await self.write.set_past_prompt(prompt)
        return self

    async def set_create_info_prompt(self, prompt: str):
        self.create_info_prompt = prompt
        self.edit_create_info_prompt = True
        await self.write.set_create_info_prompt(prompt)
        return self

    async def set_update_info_prompt(self, prompt: str):
        self.update_info_prompt = prompt
        self.edit_update_info_prompt = True
        await self.write.set_update_info_prompt(prompt)
        return self

    async def set_info_template(self, prompt: str):
        self.info_template = prompt
        self.edit_info_template = True
        await self.write.set_info_template(prompt)
        return self

    def set_parental_control(self, parental_control: bool):
        self.parental_control = parental_control
        return self

    def set_incognito(self, incognito: bool):
        self.write.set_incognito(incognito)
        return self

    def reset(self):
        return Game(self.user_id, self.user_name, self.language)

    async def start(self) -> str:
        if self.current_task is not None:
            self.current_task.cancel()

        self.wait = 1
        self.count = 1
        self.past_relevant = False
        self.info_relevant = False

        self.future = None
        self.past = [None for _ in range(Game.HISTORY_SIZE * 2 + 1)]
        self.info = None

        if not self.edit_settings:
            self.settings = get_prompts.settingsPrompt(self.language)

        now = await self.createTaskAI([
            AI.format(self.start_prompt, 'system'),
            AI.format(self.settings, 'user'),
        ], 'now', 'Bot')

        self.wait = 0
        return now

    async def move(self, answer: str) -> str:
        while self.current_task is not None:
            await asyncio.sleep(0.1)

        self.wait = 1
        self.past_relevant = False
        self.info_relevant = False

        self.past[0] = AI.format(answer, 'user')
        await self.write.move('User', answer)

        now = await self.createTaskAI([
            AI.format(self.move_prompt, 'system'),
            AI.format(self.settings, 'user'),
            AI.format(self.info, 'user'),
            AI.format(self.future, 'user'),
            *self.past[:(self.count - 1) * 2][::-1],
        ], 'now', 'Bot')

        # TODO
        if now[-8:].lower() == 'the end!' or now[-6:].lower() == 'конец!':
            self.count = 0

        self.wait = 0
        return now

    async def other(self, now: str):
        if self.count == 1:
            await self.generate_future(now)

        await self.generate_past(now)
        await self.generate_info(now)
        self.count += 1

    async def generate_future(self, now: str):
        self.future = await self.createTaskAI([
            AI.format(self.future_prompt, 'system'),
            AI.format(self.settings, 'user'),
            AI.format(now, 'user'),
        ], 'future', 'Future')

    async def generate_past(self, now):
        if self.count == Game.HISTORY_SIZE + 1:
            self.past[-1] = self.past[-3]

        elif self.count > Game.HISTORY_SIZE + 1:
            self.past[-1] = await self.createTaskAI([
                AI.format(self.past_prompt, 'system'),
                AI.format(self.past[-1], 'user'),
                AI.format(self.past[-2], 'user'),
            ], 'past', 'Past')

        for i in range(Game.HISTORY_SIZE - 1, 0, -1):
            self.past[i * 2] = self.past[i * 2 - 2]
            self.past[i * 2 + 1] = self.past[i * 2 - 1]

        self.past[1] = AI.format(now, 'assistant')
        self.past_relevant = True

    async def generate_info(self, now):
        self.info = await self.createTaskAI([
            AI.format(self.create_info_prompt if self.count == 1 else self.update_info_prompt, 'system'),
            AI.format(self.info_template, 'user'),
            AI.format(now, 'user'),
        ], 'info', 'Info')

        self.info_relevant = True

    async def createTaskAI(self, messages: list, typeRequest: str, role: str) -> str:
        self.current_task = asyncio.create_task(
            AI.generateText(
                messages,
                self.parental_control,
                f'{self.user_id} ({self.user_name}): (move {self.count}) generating {typeRequest}'
            )
        )

        result = await self.current_task
        self.current_task = None
        await self.write.move(role, result)
        return result

    def get_patterns(self):
        match self.language:
            case 'English':
                return english_patterns
            case 'Russian':
                return russian_patterns

    def get_info(self):
        if self.info is None:
            return self.get_patterns().not_generate()
        elif self.info_relevant:
            return self.info
        else:
            return f'{self.get_patterns().old_information()}\n\n{self.info}'

    def __getstate__(self):
        state = self.__dict__.copy()
        state['current_task'] = None
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self.current_task = None
