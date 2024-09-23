def start(): return (
    '*Welcome to BardicTalesAI!*\n\n'

    'In this bot, you are the protagonist in an interactive storytelling experience. '
    'You can choose your actions and shape the story as it unfolds.\n\n'

    'To begin, use /newgame. '
    'Customize your experience with /settings and get assistance with /help. '
    'Enjoy crafting your unique story!'
)


def help(): return (
    '*Game*\n'
    '/newgame - start a new game\n'
    '/settings - customize the story\n'
    '/info - get main information about the story\n'
    '/reset - reset to default settings\n\n'

    '*Bot*\n'
    '/feedback - leave feedback or suggestions\n'
    '/report - report a found bug\n'
    '/language - choose the language\n'
    '/history - show/hide message history\n'
    '/cancel - cancel the current action'
)


def help_admin(): return (
    '*Game*\n'
    '/newgame - start a new game\n'
    '/settings - customize the story\n'
    '/info - get main information about the story\n'
    '/censorship - set censorship level\n'
    '/reset - reset to default settings\n\n'

    '*Bot*\n'
    '/feedback - leave feedback or suggestions\n'
    '/report - report a found bug\n'
    '/language - choose the language\n'
    '/history - show/hide message history\n'
    '/cancel - cancel the current action\n\n'

    '*Admin mode*\n'
    '/get\_settings - get current settings\n'
    '/get\_time - get the average user wait time\n'
)


def settings(): return (
    'Here you can configure the game\n\n'

    '*Story Settings*\n'
    'Describe the kind of story you\'d like to be the hero of.\n\n'

    '*Random Settings*\n'
    'Sets random story settings\n\n'
    
    '*Prompt Settings*\n'
    'Configure the prompts used in story generation\n\n'
)


def story_settings(): return (
    '_What kind of story would you like to be the hero of? '
    'The more detailed your description, the better the game will match your preferences_'
)


def story_settings_finish(): return '_The story is set!_'


def prompts_settings(): return (
    '_Here you can configure the bot by changing the prompts it uses_'
)


def start_prompt(): return (
    '_Enter the initial prompt. '
    'It will be used to generate the beginning of the story_'
)


def move_prompt(): return (
    '_Enter the prompt for generating a new episode. '
    'It will be used to create episodes based on the player\'s actions (except for the first one)_'
)


def future_prompt(): return (
    '_Enter a prompt for developing the further plot._'
)


def past_prompt(): return (
    '_Enter the prompt for summarizing past events. '
    'The bot fully remembers only the last 5 episodes_'
)


def create_info_prompt(): return (
    '_Enter the prompt for filling in key information about the story_'
)


def update_info_prompt(): return (
    '_Enter the prompt for updating key information about the story_'
)


def info_template(): return (
    '_Enter the template for storing key information about the story_'
)


def edit_prompt(): return '_Prompt has been changed_'
def prompts_settings_finish(): return '_Prompts have been configured_'


def feedback(): return '_Please share your thoughts or suggestions so we can improve our service_'


def feedback_thanks(): return (
    '_Thank you for your feedback! '
    'We will consider your suggestions and strive to improve our service_'
)


def bug_report(): return '_Please describe the bug you encountered_'


def bug_report_thanks(): return (
    '_Thank you for reporting the bug! '
    'We will work on fixing it as soon as possible_'
)


def language(): return (
    '_Here you can set the game language. '
    'Please note that the bot works best in English!_'
)


def new_language(): return '_Language set to English_'


def censorship(): return (
    '_Here you can switch between the censored model (default) and the uncensored model. '
    'The uncensored model takes longer to respond and is less accurate than the main model!_'
)


def enable_censorship(): return '_Censorship: on_'


def disable_censorship(): return '_Censorship: off_'


def history(): return (
    '_Here you can open (default) or hide the chat history with the bot. '
    'Leaving the history open helps us improve the bot!_'
)


def open_history(): return '_Incognito mode: off_'


def hide_history(): return '_Incognito mode: on_'


def reset(): return '_Settings have been reset_'


def cancel(): return '_Action canceled_'


def nogame(): return '_You need to start the game!_'


def admin_success(): return '_Admin mode: on_'


def admin_fail(): return '_ACCESS IS DENIED_'


def admin_bye(): return '_Admin mode: off_'


def not_generate(): return 'Not generated yet'


def old_information(): return 'INFORMATION IS NOT RELEVANT'


def openai(): return '_API changed to openai_'


def groq(): return '_API changed to groq_'


def ollama(): return '_API changed to ollama_'


def wait(): return (
    '_Please wait while the AI generates a response. '
    'This may take some time_'
)


def wait_strong(): return (
    '_Please wait while the AI generates a response. '
    'This may take some time!_'
)


def error(): return (
    f'_An error occurred! Please try again!_'
)
