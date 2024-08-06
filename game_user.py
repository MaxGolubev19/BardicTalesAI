from languages.english import patterns as english_patterns
from languages.russian import patterns as russian_patterns
from game import Game


class GameUser:
    def __init__(self, user_id: int, user_name: str):
        self.id = user_id
        self.name = user_name
        self.language = 'English'
        self.admin = False

        self.game = Game(self.id, self.name, self.language)

    def get_game(self) -> Game:
        if self.game:
            return self.game

        self.game = Game(self.id, self.name, self.language)
        return self.game

    def get_language(self):
        match self.language:
            case 'English':
                return english_patterns
            case 'Russian':
                return russian_patterns

    def set_language(self, language: str) -> None:
        self.language = language
        self.get_game().set_language(language)

    def reset(self):
        return GameUser(self.id, self.name)
