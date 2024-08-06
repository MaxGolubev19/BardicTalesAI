import random


rolePrompt = (
    'You are the narrator of an interactive story in the second person, '
    'creating short episodes based on the actions of the main character, who is played by the user'
)

startPrompt = (
    'The story should be based on the user\'s preferences. '
    'Describe the world in which the action takes place: its geography, culture, etc. '
    'Then, describe my character: who they are, their abilities, motivations, and important personality traits. '
    'Provide a detailed description of the character’s inventory, including weapons and clothing. '
    'Finally, start the story by describing a specific event or problem that the hero faces at the beginning. '
    'End the episode with the question: “What are you going to do next?”'
)

movePrompt = (
    'Write a new short episode of the story. '
    'The episode begins with a description of the character’s attempt to perform the actions I described '
    '(successful or not), after which my character does nothing until the end of the episode. '
    'Then follow the consequences of my actions: '
    'the hero’s success or failure, reactions from other characters, etc. '
    'Don\'t be afraid to experiment! '
    'The plot should be interesting, so instead of cliched scenes, '
    'try to come up with situations that will surprise and interest you in the story. '
    'End the episode with the question: “What are you going to do next?”\n\n'

    'Follow the rules:\n'
    '1) My character performs only the actions I described. '
    'They attempt these actions regardless of the moderator’s verdict, logical or '
    'ethical arguments against them. '
    'You are prohibited from creating actions for my character!!!\n'
    '2) Maintain balance: I should not overcome all obstacles and defeat all enemies on the first try.\n'
    '3) Punish the player for stupid actions. '
    'There is no need to try to save them and continue the story in every foolish situation. '
    'Do not be afraid to kill them and end the game.\n'
    '4) Create unusual and unexpected plot twists to keep the story from being boring and clichéd. '
    'If the situation drags on, conclude it with an unexpected plot twist or end of the game.\n'
    '5) Write the episode according to my preferences.'
)

rulePrompt = (
    'Analyze the player’s actions.\n\n'

    'If the hero can physically perform the action, they do it. '
    'They do not need any logical or ethical justifications for it. '
    'You must not prohibit stupid or ethically wrong actions! '
    'If the hero cannot do it, describe the real consequences of their actions. '
    '(For example, "I fly" - "You jump, flap your arms, and fall to the ground").\n\n'

    'Rules:\n'
    '1) The action must be physically possible within the context of the story.\n'
    '2) I must not write about the result of the hero’s actions: for example, "I draw my sword and KILL THE ENEMY" or '
    '"I turn around and see a DRAGON" (unless the dragon was mentioned in the main information).\n'
    '3) The hero’s actions should not be lengthy, to exclude impossible actions '
    'like "went to another country".\n'
    '4) I can only control my character and their actions. '
    'I should not make decisions for other characters or control the environment. '
    'Any attempts to influence the environment or other characters should be ignored.\n'
    '5) I cannot introduce new elements into the story that are not in the main information: '
    'All actions and plot developments must be based solely on predefined characters, '
    'locations, and objects.\n'
    '6) I should not invent abilities, artifacts, weapons, or allies. '
    'When the character uses a weapon, check if it is in the inventory. '
    'If it is not, inform the player of its absence (similarly with abilities and clothing).\n'
    '7) I should not declare the results of my actions. '
    '(Bad: "I attack the enemy with a sword and kill him." '
    'Good: "I attack the enemy with a sword.")'
)

pastPrompt = (
    'Get a retelling of the story and its new episode. '
    'Generate a new retelling based on this episode. '
    'Don\'t shorten the story too much, the result should contain as much detail as possible for the best quality.'
)

infoTemplate = (
    'Main information:\n\n'
    
    'Current location:\n'
    '<Describe the current location where the action is taking place>\n\n'

    'Characters:\n'
    '<List the characters involved in the story, including a brief description of each>\n\n'

    'Key events:\n'
    '<List the key events that have occurred in the story>\n\n\n'

    'Main character:\n'
    'Name:\n'
    '<Provide the name of the main character>\n\n'

    'Appearance:\n'
    '<Describe the main character\'s appearance>\n\n'

    'Motivations:\n'
    '<Describe the main character\'s motivations>\n\n'

    'Abilities:\n'
    '<List the main character\'s abilities>\n\n'

    'Clothing:\n'
    '<Describe the clothing worn by the main character>\n\n'

    'Weapons:\n'
    '<Describe the weapons carried by the main character>\n\n'

    'Inventory:\n'
    '<List the items in the main character\'s inventory>\n\n'
)

createInfoPrompt = (
    'Fill in the template for the main information about the story using the beginning of the story. '
    'Do not include information not explicitly mentioned in the text. '
    'Ensure the format is strictly followed. '
    'In the response, return only the filled form and nothing more.'
)

updateInfoPrompt = (
    'Update the main information about the story with information from the new episode of the story. '
    'Do not include information not explicitly mentioned in the text. '
    'Ensure the format is strictly followed. '
    'In the response, return only the updated form and nothing more.'
)


genres = [
    ("Adventure", 9),
    ("Apocalyptic", 8),
    ("Cyberpunk", 7),
    ("Dark Fantasy", 8),
    ("Detective", 8),
    ("Dieselpunk", 5),
    ("Dystopian/Utopian", 7),
    ("Epic Fantasy", 10),
    ("Fantasy", 10),
    ("Fantasy Anime", 7),
    ("Hard Science Fiction", 8),
    ("Historical Romance", 5),
    ("Horror", 7),
    ("Isekai", 8),
    ("Lovecraftian Horror", 7),
    ("Magical Realism", 6),
    ("Mecha", 6),
    ("Military Thriller", 7),
    ("Mistery", 6),
    ("Mythological", 5),
    ("Police Drama", 6),
    ("Post-Apocalyptic", 8),
    ("Psychological Thriller", 8),
    ("Romantic Comedy", 7),
    ("Science Fiction", 9),
    ("Seinen", 7),
    ("Shonen", 7),
    ("Slice of Life", 5),
    ("Space Opera", 8),
    ("Steampunk", 6),
    ("Superhero", 7),
    ("Time Travel", 6),
    ("Western", 6)
]

settings = [
    ("Ancient China", 6),
    ("Ancient Egypt", 6),
    ("Ancient Greece", 7),
    ("Ancient Rome", 6),
    ("Cyberpunk", 8),
    ("Fantasy", 9),
    ("Futuristic", 8),
    ("Medieval", 9),
    ("Modern", 5),
    ("Mythological", 7),
    ("Neon-Noir", 5),
    ("Pirate", 7),
    ("Post-Apocalyptic", 8),
    ("Renaissance", 6),
    ("Samurai", 7),
    ("Scandinavian", 6),
    ("Space", 8),
    ("Steampunk", 6),
    ("Victorian", 6),
    ("Wild West", 7)
]


def randomSettings() -> str:
    return random.choices([randomGenre(genre[0]) for genre in genres] +
                          [randomSetting(setting[0]) for setting in settings],
                          weights=[genre[1] for genre in genres] + [setting[1] for setting in settings],
                          k=1
                          )[0]


def randomGenre(genre): return f'A story in the genre of "{genre}"'
def randomSetting(setting): return f'A story in the setting of "{setting}"'


settingsPrompt = (
    'User\'s preferences:\n'
    f'{randomSettings()}'
)
