from languages import get_prompts
from prompt import Prompt


class PromptEditor:
    def __init__(self, language: str):
        self.language = language

        self.start_prompt = Prompt(get_prompts.startPrompt, self.language)
        self.move_prompt = Prompt(get_prompts.movePrompt, self.language)
        self.future_prompt = Prompt(get_prompts.futurePrompt, self.language)
        self.past_prompt = Prompt(get_prompts.pastPrompt, self.language)
        self.create_info_prompt = Prompt(get_prompts.createInfoPrompt, self.language)
        self.update_info_prompt = Prompt(get_prompts.updateInfoPrompt, self.language)

        self.start_template = Prompt(get_prompts.startTemplate, self.language)
        self.move_template = Prompt(get_prompts.moveTemplate, self.language)
        self.future_template = Prompt(get_prompts.futureTemplate, self.language)
        self.past_template = Prompt(get_prompts.pastTemplate, self.language)
        self.info_template = Prompt(get_prompts.infoTemplate, self.language)

        self.settings = Prompt(get_prompts.settingsPrompt, self.language)

    def set_language(self, language: str):
        self.language = language

        self.start_prompt.edit_language(self.language)
        self.move_prompt.edit_language(self.language)
        self.future_prompt.edit_language(self.language)
        self.past_prompt.edit_language(self.language)
        self.create_info_prompt.edit_language(self.language)
        self.update_info_prompt.edit_language(self.language)

        self.start_template.edit_language(self.language)
        self.move_template.edit_language(self.language)
        self.future_template.edit_language(self.language)
        self.past_template.edit_language(self.language)
        self.info_template.edit_language(self.language)

        self.settings.edit_language(self.language)

    def get_start_prompt(self): return f'{self.start_prompt}\n{self.start_template}'
    def get_move_prompt(self): return f'{self.move_prompt}\n{self.move_template}'
    def get_future_prompt(self): return f'{self.future_prompt}\n{self.future_template}'
    def get_past_prompt(self): return f'{self.past_prompt}\n{self.past_template}'
    def get_create_info_prompt(self): return f'{self.create_info_prompt}\n{self.info_template}'
    def get_update_info_prompt(self): return f'{self.update_info_prompt}\n{self.info_template}'
    def get_settings(self): return self.settings.text

    def get_new_settings(self):
        if not self.settings.edited:
            self.settings.reset(self.language)
        return self.settings.text
