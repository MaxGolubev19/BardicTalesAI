from languages.english import patterns as english_patterns
from languages.russian import patterns as russian_patterns
from game import Game


class User:
    def __init__(self, user_id: int, user_name: str):
        self.id = user_id
        self.name = user_name
        self.language = 'english'
        self.admin = False

        self.game = Game(self.id, self.name, self.language)

    def get_game(self) -> Game:
        if self.game:
            return self.game

        self.game = Game(self.id, self.name, self.language)
        return self.game

    def get_language(self):
        match self.language:
            case 'english':
                return english_patterns
            case 'russian':
                return russian_patterns
            case _:
                return english_patterns

    def set_language(self, language: str) -> None:
        self.language = language
        self.get_game().set_language(language)

    def reset(self):
        return User(self.id, self.name)
