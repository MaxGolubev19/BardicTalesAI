class Write:
    send_history = None
    send_feedback = None

    MAX_MESSAGE_LENGTH = 4096

    def __init__(self, user_id: int, user_name: str):
        self.user_id = user_id
        self.user_name = user_name
        self.incognito = False

    async def write_message(self, role: str, content: str) -> None:
        head = f'#{role}\n#{self.user_id} {self.user_name}:\n'
        if not self.incognito:
            for i in range(0, len(content), self.MAX_MESSAGE_LENGTH - len(head)):
                await Write.send_history(f'{head}{content[i:i + self.MAX_MESSAGE_LENGTH - len(head)]}')

    async def write_feedback(self, role: str, content: str) -> None:
        head = f'#{role}\n#{self.user_id} {self.user_name}:\n'
        for i in range(0, len(content), self.MAX_MESSAGE_LENGTH - len(head)):
            await Write.send_feedback(f'{head}{content[i:i + self.MAX_MESSAGE_LENGTH - len(head)]}')

    async def set_settings(self, settings: str) -> None:
        await self.write_message('Settings', settings)

    async def set_start_prompt(self, prompt: str) -> None:
        await self.write_message('StartPrompt', prompt)

    async def set_move_prompt(self, prompt: str) -> None:
        await self.write_message('MovePrompt', prompt)

    async def set_future_prompt(self, prompt: str) -> None:
        await self.write_message('FuturePrompt', prompt)

    async def set_past_prompt(self, prompt: str) -> None:
        await self.write_message('PastPrompt', prompt)

    async def set_create_info_prompt(self, prompt: str) -> None:
        await self.write_message('CreateInfoPrompt', prompt)

    async def set_update_info_prompt(self, prompt: str) -> None:
        await self.write_message('UpdateInfoPrompt', prompt)

    async def set_start_template(self, prompt: str) -> None:
        await self.write_message('StartTemplate', prompt)

    async def set_move_template(self, prompt: str) -> None:
        await self.write_message('MoveTemplate', prompt)

    async def set_future_template(self, prompt: str) -> None:
        await self.write_message('FutureTemplate', prompt)

    async def set_past_template(self, prompt: str) -> None:
        await self.write_message('PastTemplate', prompt)

    async def set_info_template(self, prompt: str) -> None:
        await self.write_message('InfoTemplate', prompt)

    async def move(self, role: str, content: str) -> None:
        await self.write_message(role, content)

    async def feedback(self, content: str) -> None:
        await self.write_feedback('Feedback', content)

    async def report(self, content: str) -> None:
        await self.write_feedback('Report', content)

    def set_incognito(self, incognito: bool) -> None:
        self.incognito = incognito
