def startPrompt(language): return read(language, 'startPrompt')
def futurePrompt(language): return read(language, 'futurePrompt')
def movePrompt(language): return read(language, 'movePrompt')
def pastPrompt(language): return read(language, 'pastPrompt')
def infoTemplate(language): return read(language, 'infoTemplate')
def createInfoPrompt(language): return read(language, 'createInfoPrompt')
def updateInfoPrompt(language): return read(language, 'updateInfoPrompt')


def read(language, prompt_name):
    return open(f'languages/{language}/prompts/{prompt_name}.txt', 'r', encoding='utf-8').read()


def settingsPrompt(language):
    match language:
        case 'english':
            from languages.english.prompts import settingsPrompt as languageModule
        case 'russian':
            from languages.russian.prompts import settingsPrompt as languageModule
        case _:
            from languages.english.prompts import settingsPrompt as languageModule

    return languageModule.settingsPrompt()
