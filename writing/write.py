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

    async def set_role_prompt(self, role_prompt: str) -> None:
        await self.write_message('RolePrompt', role_prompt)

    async def set_start_prompt(self, start_prompt: str) -> None:
        await self.write_message('StartPrompt', start_prompt)

    async def set_move_prompt(self, move_prompt: str) -> None:
        await self.write_message('MovePrompt', move_prompt)

    async def set_rule_prompt(self, rule_prompt: str) -> None:
        await self.write_message('RulePrompt', rule_prompt)

    async def set_past_prompt(self, past_prompt: str) -> None:
        await self.write_message('PastPrompt', past_prompt)

    async def set_info_template(self, info_template: str) -> None:
        await self.write_message('InfoTemplate', info_template)

    async def set_create_info_prompt(self, create_info_prompt: str) -> None:
        await self.write_message('CreateInfoPrompt', create_info_prompt)

    async def set_update_info_prompt(self, update_info_prompt: str) -> None:
        await self.write_message('UpdateInfoPrompt', update_info_prompt)

    async def move(self, role: str, content: str) -> None:
        await self.write_message(role, content)

    async def feedback(self, content: str) -> None:
        await self.write_feedback('Feedback', content)

    async def bug_report(self, content: str) -> None:
        await self.write_feedback('Report', content)

    def set_incognito(self, incognito: bool) -> None:
        self.incognito = incognito
