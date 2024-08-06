import asyncio

from ai import AI
from writing.write import Write
from languages.english import patterns as english_patterns, prompts as english_prompts
from languages.russian import patterns as russian_patterns, prompts as russian_prompts


class Game:
    HISTORY_SIZE = 5

    def __init__(self, user_id: int, user_name: str, language: str):
        self.write = Write(user_id, user_name)
        self.user_id = user_id
        self.user_name = user_name
        self.language = language

        self.settings = self.get_prompts().settingsPrompt
        self.role_prompt = self.get_prompts().rolePrompt
        self.start_prompt = self.get_prompts().startPrompt
        self.move_prompt = self.get_prompts().movePrompt
        self.rule_prompt = self.get_prompts().rulePrompt
        self.past_prompt = self.get_prompts().pastPrompt
        self.info_template = self.get_prompts().infoTemplate
        self.create_info_prompt = self.get_prompts().createInfoPrompt
        self.update_info_prompt = self.get_prompts().updateInfoPrompt

        self.edit_settings = False
        self.edit_role_prompt = False
        self.edit_start_prompt = False
        self.edit_move_prompt = False
        self.edit_rule_prompt = False
        self.edit_past_prompt = False
        self.edit_info_template = False
        self.edit_create_info_prompt = False
        self.edit_update_info_prompt = False

        self.parental_control = True

        self.now = None
        self.past = None
        self.info = None
        self.lasts = [None for _ in range(Game.HISTORY_SIZE)]
        self.answers = [None for _ in range(Game.HISTORY_SIZE)]

        self.past_relevant = True
        self.info_relevant = True

        self.count = 0
        self.wait = 0
        self.current_task = None

    def set_language(self, language: str):
        self.language = language

        if not self.edit_settings:
            self.settings = self.get_prompts().settingsPrompt

        if not self.edit_role_prompt:
            self.role_prompt = self.get_prompts().rolePrompt

        if not self.edit_start_prompt:
            self.start_prompt = self.get_prompts().startPrompt

        if not self.edit_move_prompt:
            self.move_prompt = self.get_prompts().movePrompt

        if not self.edit_rule_prompt:
            self.rule_prompt = self.get_prompts().rulePrompt

        if not self.edit_past_prompt:
            self.past_prompt = self.get_prompts().pastPrompt

        if not self.edit_info_template:
            self.info_template = self.get_prompts().infoTemplate

        if not self.edit_create_info_prompt:
            self.create_info_prompt = self.get_prompts().createInfoPrompt

        if not self.edit_update_info_prompt:
            self.update_info_prompt = self.get_prompts().updateInfoPrompt

        return self

    async def set_basic_settings(self, settings: str):
        self.settings = settings
        self.edit_settings = True
        await self.write.set_settings(settings)
        return self

    async def set_random_settings(self):
        self.settings = self.get_prompts().settingsPrompt
        self.edit_settings = False
        await self.write.set_settings(self.settings)
        return self

    async def set_role_prompt(self, role_prompt: str):
        self.role_prompt = role_prompt
        self.edit_role_prompt = True
        await self.write.set_role_prompt(role_prompt)
        return self

    async def set_start_prompt(self, start_prompt: str):
        self.start_prompt = start_prompt
        self.edit_start_prompt = True
        await self.write.set_start_prompt(start_prompt)
        return self

    async def set_move_prompt(self, move_prompt: str):
        self.move_prompt = move_prompt
        self.edit_move_prompt = True
        await self.write.set_move_prompt(move_prompt)
        return self

    async def set_rule_prompt(self, rule_prompt: str):
        self.rule_prompt = rule_prompt
        self.edit_rule_prompt = True
        await self.write.set_rule_prompt(rule_prompt)
        return self

    async def set_past_prompt(self, past_prompt: str):
        self.past_prompt = past_prompt
        self.edit_past_prompt = True
        await self.write.set_past_prompt(past_prompt)
        return self

    async def set_info_template(self, info_template: str):
        self.info_template = info_template
        self.edit_info_template = True
        await self.write.set_info_template(info_template)
        return self

    async def set_create_info_prompt(self, create_info_prompt: str):
        self.create_info_prompt = create_info_prompt
        self.edit_create_info_prompt = True
        await self.write.set_create_info_prompt(create_info_prompt)
        return self

    async def set_update_info_prompt(self, update_info_prompt: str):
        self.update_info_prompt = update_info_prompt
        self.edit_update_info_prompt = True
        await self.write.set_update_info_prompt(update_info_prompt)
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

        if not self.edit_settings:
            self.settings = self.get_prompts().settingsPrompt

        self.past_relevant = True
        self.info_relevant = True

        self.now = None
        self.past = None
        self.info = None
        self.lasts = [None for _ in range(5)]
        self.answers = [None for _ in range(5)]

        self.count = 0
        self.wait = 1

        await self.generate_now()

        self.wait = 0
        return self.now

    async def move(self, answer: str) -> str:
        while self.current_task is not None:
            await asyncio.sleep(0.1)

        for i in range(Game.HISTORY_SIZE - 2, -1, -1):
            self.answers[i + 1] = self.answers[i]

        self.answers[0] = answer

        await self.write.move('User', answer)
        self.wait = 1

        await self.generate_now(answer)

        self.wait = 0
        return self.now

    async def generate_now(self, answer: str = None) -> None:
        self.past_relevant = False
        self.info_relevant = False

        if self.count == 0:
            messages = [
                AI.format(self.get_prompts().rolePrompt, 'system'),
                AI.format(self.start_prompt, 'user'),
                AI.format('Send me the user\'s preferences.', 'assistant'),
                AI.format(self.settings, 'user'),
            ]

        elif self.count == 1:
            messages = [
                AI.format(self.get_prompts().rolePrompt, 'system'),
                AI.format(self.move_prompt, 'user'),
                # AI.format('Send me the rules.', 'assistant'),
                AI.format(self.rule_prompt, 'user'),
                # AI.format('Send me the user\'s preferences.', 'assistant'),
                AI.format(self.settings, 'user'),
                # AI.format('Send me the main information.', 'assistant'),
                AI.format(self.info, 'user'),
                AI.format(self.now, 'assistant'),
                AI.format(answer, 'user'),
            ]

        elif 2 <= self.count <= Game.HISTORY_SIZE + 1:
            messages = [
                AI.format(self.get_prompts().rolePrompt, 'system'),
                AI.format(self.move_prompt, 'user'),
                # AI.format('Send me the rules.', 'assistant'),
                AI.format(self.rule_prompt, 'user'),
                # AI.format('Send me the user\'s preferences.', 'assistant'),
                AI.format(self.settings, 'user'),
                # AI.format('Send me the main information.', 'assistant'),
                AI.format(self.info, 'user'),
                *[i for j in [
                    (AI.format(self.lasts[i], 'assistant'),
                     AI.format(self.answers[i], 'user'))
                    for i in range(self.count - 2, -1, -1)
                ] for i in j],
                AI.format(self.now, 'assistant'),
                AI.format(answer, 'user'),
            ]

        else:
            messages = [
                AI.format(self.get_prompts().rolePrompt, 'system'),
                AI.format(self.move_prompt, 'user'),
                # AI.format('Send me the rules.', 'assistant'),
                AI.format(self.rule_prompt, 'user'),
                # AI.format('Send me the user\'s preferences.', 'assistant'),
                AI.format(self.settings, 'user'),
                # AI.format('Send me the main information.', 'assistant'),
                AI.format(self.info, 'user'),
                # AI.format('Send me the brief summary of past events.', 'assistant'),
                AI.format(self.past, 'user'),
                *[i for j in [
                    (AI.format(self.lasts[i], 'assistant'),
                     AI.format(self.answers[i], 'user'))
                    for i in range(Game.HISTORY_SIZE - 1, -1, -1)
                ] for i in j],
                AI.format(self.now, 'assistant'),
                AI.format(answer, 'user'),
            ]

        self.now = await self.createTaskAI(messages, 'now', 'Bot')

        if self.now[-8:].lower() == 'the end!' or self.now[-6:].lower() == 'конец!':
            self.count = -1

    async def other(self):
        await self.generate_past()

        for i in range(Game.HISTORY_SIZE - 2, -1, -1):
            if self.lasts[i] is not None:
                self.lasts[i + 1] = self.lasts[i]

        self.lasts[0] = self.now

        await self.generate_info()
        self.count += 1

    async def generate_past(self):
        if self.count < Game.HISTORY_SIZE:
            self.past = None
        elif self.count == Game.HISTORY_SIZE:
            self.past = self.lasts[Game.HISTORY_SIZE - 1]
        else:
            self.past = await self.createTaskAI([
                AI.format(self.get_prompts().pastPrompt, 'user'),
                # AI.format('Send me the previous part of the story.', 'assistant'),
                AI.format(self.past, 'user'),
                # AI.format('Send me the latest episode', 'assistant'),
                AI.format(self.lasts[Game.HISTORY_SIZE - 1], 'user'),
            ], 'past', 'Past')

        self.past_relevant = True

    async def generate_info(self):
        match self.count:
            case 0:
                messages = [
                    AI.format(self.get_prompts().createInfoPrompt, 'user'),
                    # AI.format('Send me the template for the main information.', 'assistant'),
                    AI.format(self.get_prompts().infoTemplate, 'user'),
                    # AI.format('Send me the beginning of the story.', 'assistant'),
                    AI.format(self.now, 'user'),
                ]

            case _:
                messages = [
                    AI.format(self.get_prompts().updateInfoPrompt, 'user'),
                    # AI.format('Send me the main information.', 'assistant'),
                    AI.format(self.info, 'user'),
                    # AI.format('Send me the new episode of the story.', 'assistant'),
                    AI.format(self.now, 'user'),
                ]

        self.info = await self.createTaskAI(messages, 'info', 'Info')
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

    def get_prompts(self):
        match self.language:
            case 'English':
                return english_prompts
            case 'Russian':
                return russian_prompts

    def get_past(self):
        if self.past is None:
            return self.get_patterns().not_generate()
        elif self.info_relevant:
            return self.past
        else:
            return f'{self.get_patterns().old_information()}\n\n{self.past}'

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
