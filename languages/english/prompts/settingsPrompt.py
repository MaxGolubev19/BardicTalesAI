import random


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


def randomSetting(setting): return f'A story in the setting of "{setting}"'
def randomGenre(genre): return f'A story in the genre of "{genre}"'


def settingsPrompt(user_settings: str = None):
    return (
        'User\'s preferences:\n'
        f'{user_settings if user_settings else randomSettings()}'
    )
