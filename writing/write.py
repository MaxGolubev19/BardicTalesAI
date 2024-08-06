import os
from datetime import datetime


class Write:
    history_file = 'info/history.txt'
    feedback_file = 'info/feedback.txt'

    def __init__(self, user_id: int, user_name: str):
        self.user_id = user_id
        self.user_name = user_name
        self.incognito = False

    def write_message(self, role: str, content: str) -> None:
        if not self.incognito:
            with open(Write.history_file, 'a', encoding='utf-8') as file:
                file.write((
                    f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {self.user_id} [{self.user_name}] - {role}:\n\n"
                    f"{content}\n"
                    f"{'-' * 400}\n"
                ))

    def write_feedback(self, role: str, content: str) -> None:
        with open(Write.feedback_file, 'a', encoding='utf-8') as file:
            file.write((
                f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - "
                f"{self.user_id} [{self.user_name}] - {role}:\n\n"
                f"{content}\n"
                f"{'-' * 400}\n"
            ))

    def set_settings(self, settings: str) -> None:
        self.write_message('Settings', settings)

    def set_start_prompt(self, start_prompt: str) -> None:
        self.write_message('Start prompt', start_prompt)

    def set_move_prompt(self, move_prompt: str) -> None:
        self.write_message('Move prompt', move_prompt)

    def set_rule_prompt(self, rule_prompt: str) -> None:
        self.write_message('Rule prompt', rule_prompt)

    def move(self, role: str, content: str) -> None:
        self.write_message(role, content)

    def feedback(self, content: str) -> None:
        self.write_feedback('Feedback', content)

    def bug_report(self, content: str) -> None:
        self.write_feedback('Bug report', content)

    def set_incognito(self, incognito: bool) -> None:
        self.incognito = incognito
