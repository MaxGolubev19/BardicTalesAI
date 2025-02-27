class Prompt:
    def __init__(self, get: callable, language: str, edited: str = False):
        self.get = get
        self.language = language
        self.edited = edited
        self.text = get(self.language)

    def __str__(self):
        return self.text

    def edit(self, prompt):
        self.text = prompt
        self.edited = True

    def edit_language(self, language):
        self.language = language
        if not self.edited:
            self.text = self.get(language)

    def reset(self, language):
        self.language = language
        self.edited = False
        self.text = self.get(self.language)
