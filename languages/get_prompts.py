import random


def read(language, directory, prompt_name: str) -> str:
    return open(f'languages/{language}/{directory}/{prompt_name}.txt', 'r', encoding='utf-8').read()


# Prompts
def startPrompt(language): return read(language, 'prompts', 'startPrompt')
def movePrompt(language): return read(language, 'prompts', 'movePrompt')
def futurePrompt(language): return read(language, 'prompts', 'futurePrompt')
def pastPrompt(language): return read(language, 'prompts', 'pastPrompt')
def createInfoPrompt(language): return read(language, 'prompts', 'createInfoPrompt')
def updateInfoPrompt(language): return read(language, 'prompts', 'updateInfoPrompt')


# Templates
def startTemplate(language): return read(language, 'templates', 'startTemplate')
def moveTemplate(language): return read(language, 'templates', 'moveTemplate')
def futureTemplate(language): return read(language, 'templates', 'futureTemplate')
def pastTemplate(language): return read(language, 'templates', 'pastTemplate')
def infoTemplate(language): return read(language, 'templates', 'infoTemplate')


# Settings
def settingsPrompt(language): return read(language, 'genres', randomSettings())


def randomSettings() -> str:
    return random.choices([genre[0] for genre in genres],
                          weights=[genre[1] for genre in genres],
                          k=1)[0]


genres = [
    ('dark_fantasy', 30),
    ('cyberpunk', 15),
    ('fantasy', 15),
    ('post_apocalyptic', 10),
    ('steampunk', 5),
    ('retrofuturism', 5),
    ('urban_fantasy', 5),
    ('detective', 5),
    ('space_opera', 5),
    ('dystopia', 5),
]
