import os
import time
import dill
import atexit
import logging
from typing import Dict

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

from languages import get_prompts
from writing import game_logging
from writing.decorators import log
from writing.write import Write
from game_user import GameUser
from ai import AI


class GameBot:
    MAX_MESSAGE_LENGTH = 4096

    class States(StatesGroup):
        settings = State()
        feedback = State()
        report = State()
        language = State()

        start_prompt = State()
        move_prompt = State()
        future_prompt = State()
        past_prompt = State()
        create_info_prompt = State()
        update_info_prompt = State()

        start_template = State()
        move_template = State()
        future_template = State()
        past_template = State()
        info_template = State()

    def __init__(self, token: str):
        self.bot = Bot(token=token)
        self.dp = Dispatcher()

        Write.send_feedback = self.send_feedback
        Write.send_history = self.send_history

        self.user_file = f'data/users.pkl'
        self.users: Dict[int, GameUser] = {}

        atexit.register(self.save_users)
        self.register_handlers()

        self.all_time = 0
        self.all_moves = 0

        self.load_users()

    def load_users(self):
        try:
            with open(self.user_file, 'rb') as file:
                self.users = dill.load(file)
        except Exception as e:
            logging.error(e)

    def save_users(self):
        with open(self.user_file, 'wb') as file:
            dill.dump(self.users, file)

    def get_user(self, message: Message):
        self.users[message.from_user.id] = self.users.get(message.from_user.id,
                                                          GameUser(message.from_user.id, message.from_user.full_name))
        return self.users[message.from_user.id]

    def get_language(self, message: Message):
        return self.get_user(message).get_language()

    async def send_long_message(self, message: Message, answer: str) -> None:
        try:
            await message.answer(answer, parse_mode='Markdown')
        except Exception:
            for i in range(0, len(answer), self.MAX_MESSAGE_LENGTH):
                await message.answer(answer[i:i + self.MAX_MESSAGE_LENGTH])

    def log_waiting_time(self, message, start_time):
        time_working = int(time.time() - start_time)
        logging.info(f'{message.from_user.id} ({message.from_user.full_name}): Waiting time (move) - '
                     f'{time_working // 60}:{(time_working % 60):02}')
        self.all_time += time_working
        self.all_moves += 1

    async def send_history(self, message: str):
        await self.bot.send_message(chat_id=-1002178954297, text=message)

    async def send_feedback(self, message: str):
        await self.bot.send_message(chat_id=-1002246159913, text=message)

    def register_handlers(self) -> None:
        # Commands
        # Cancel
        @self.dp.message(Command("cancel"))
        async def handler(message: Message, state: FSMContext):
            await state.clear()
            await message.answer(self.get_language(message).cancel(),
                                 reply_markup=ReplyKeyboardRemove(),
                                 parse_mode='Markdown')

        def genres_menu():
            return ReplyKeyboardMarkup(
                keyboard=[
                    [
                        KeyboardButton(text="/dark_fantasy"),
                    ],
                    [
                        KeyboardButton(text="/cyberpunk"),
                    ],
                    [
                        KeyboardButton(text="/funny_fantasy"),
                    ],
                    [
                        KeyboardButton(text="/post_apocalyptic"),
                    ],
                    [
                        KeyboardButton(text="/steampunk"),
                    ],
                    [
                        KeyboardButton(text="/retrofuturism"),
                    ],
                    [
                        KeyboardButton(text="/urban_fantasy"),
                    ],
                    [
                        KeyboardButton(text="/detective"),
                    ],
                    [
                        KeyboardButton(text="/space_opera"),
                    ],
                    [
                        KeyboardButton(text="/dystopia"),
                    ],
                ],
                resize_keyboard=True,
                one_time_keyboard=True
            )

        # Start
        @self.dp.message(Command("start"))
        @log(game_logging.start_log)
        async def handler(message: Message, state: FSMContext):
            await message.answer(self.get_language(message).start(),
                                 reply_markup=genres_menu(),
                                 parse_mode='Markdown')

        @self.dp.message(Command("dark_fantasy"))
        async def handler(message: Message, state: FSMContext):
            await state.clear()
            game = self.get_user(message).get_game()
            await game.set_settings(get_prompts.read(game.language, 'genres', 'dark_fantasy'))
            await message.answer(self.get_language(message).story_settings_finish(),
                                 reply_markup=ReplyKeyboardRemove(),
                                 parse_mode='Markdown')

        @self.dp.message(Command("cyberpunk"))
        async def handler(message: Message, state: FSMContext):
            await state.clear()
            game = self.get_user(message).get_game()
            await game.set_settings(get_prompts.read(game.language, 'genres', 'cyberpunk'))
            await message.answer(self.get_language(message).story_settings_finish(),
                                 reply_markup=ReplyKeyboardRemove(),
                                 parse_mode='Markdown')

        @self.dp.message(Command("funny_fantasy"))
        async def handler(message: Message, state: FSMContext):
            await state.clear()
            game = self.get_user(message).get_game()
            await game.set_settings(get_prompts.read(game.language, 'genres', 'fantasy'))
            await message.answer(self.get_language(message).story_settings_finish(),
                                 reply_markup=ReplyKeyboardRemove(),
                                 parse_mode='Markdown')

        @self.dp.message(Command("post_apocalyptic"))
        async def handler(message: Message, state: FSMContext):
            await state.clear()
            game = self.get_user(message).get_game()
            await game.set_settings(get_prompts.read(game.language, 'genres', 'post_apocalyptic'))
            await message.answer(self.get_language(message).story_settings_finish(),
                                 reply_markup=ReplyKeyboardRemove(),
                                 parse_mode='Markdown')

        @self.dp.message(Command("steampunk"))
        async def handler(message: Message, state: FSMContext):
            await state.clear()
            game = self.get_user(message).get_game()
            await game.set_settings(get_prompts.read(game.language, 'genres', 'steampunk'))
            await message.answer(self.get_language(message).story_settings_finish(),
                                 reply_markup=ReplyKeyboardRemove(),
                                 parse_mode='Markdown')

        @self.dp.message(Command("retrofuturism"))
        async def handler(message: Message, state: FSMContext):
            await state.clear()
            game = self.get_user(message).get_game()
            await game.set_settings(get_prompts.read(game.language, 'genres', 'retrofuturism'))
            await message.answer(self.get_language(message).story_settings_finish(),
                                 reply_markup=ReplyKeyboardRemove(),
                                 parse_mode='Markdown')

        @self.dp.message(Command("urban_fantasy"))
        async def handler(message: Message, state: FSMContext):
            await state.clear()
            game = self.get_user(message).get_game()
            await game.set_settings(get_prompts.read(game.language, 'genres', 'urban_fantasy'))
            await message.answer(self.get_language(message).story_settings_finish(),
                                 reply_markup=ReplyKeyboardRemove(),
                                 parse_mode='Markdown')

        @self.dp.message(Command("detective"))
        async def handler(message: Message, state: FSMContext):
            await state.clear()
            game = self.get_user(message).get_game()
            await game.set_settings(get_prompts.read(game.language, 'genres', 'detective'))
            await message.answer(self.get_language(message).story_settings_finish(),
                                 reply_markup=ReplyKeyboardRemove(),
                                 parse_mode='Markdown')

        @self.dp.message(Command("space_opera"))
        async def handler(message: Message, state: FSMContext):
            await state.clear()
            game = self.get_user(message).get_game()
            await game.set_settings(get_prompts.read(game.language, 'genres', 'space_opera'))
            await message.answer(self.get_language(message).story_settings_finish(),
                                 reply_markup=ReplyKeyboardRemove(),
                                 parse_mode='Markdown')

        @self.dp.message(Command("dystopia"))
        async def handler(message: Message, state: FSMContext):
            await state.clear()
            game = self.get_user(message).get_game()
            await game.set_settings(get_prompts.read(game.language, 'genres', 'dystopia'))
            await message.answer(self.get_language(message).story_settings_finish(),
                                 reply_markup=ReplyKeyboardRemove(),
                                 parse_mode='Markdown')

        # Settings
        def get_settings_menu():
            return ReplyKeyboardMarkup(
                keyboard=[
                    [
                        KeyboardButton(text="/story_settings"),
                        KeyboardButton(text="/random_settings"),
                    ],
                    [
                        KeyboardButton(text="/prompts_settings"),
                        KeyboardButton(text="/templates_settings"),
                    ],
                    [
                        KeyboardButton(text="/cancel"),
                    ],
                ],
                resize_keyboard=True,
                one_time_keyboard=True
            )

        @self.dp.message(Command("settings"))
        async def handler(message: Message, state: FSMContext):
            await message.answer(self.get_language(message).settings(),
                                 reply_markup=get_settings_menu(),
                                 parse_mode='Markdown')

        # Story Settings
        @self.dp.message(Command("story_settings"))
        async def handler(message: Message, state: FSMContext):
            await state.set_state(GameBot.States.settings)
            await message.answer(self.get_language(message).story_settings(),
                                 reply_markup=ReplyKeyboardRemove(),
                                 parse_mode='Markdown')

        # Random settings
        @self.dp.message(Command("random_settings"))
        @log(game_logging.set_basic_log)
        async def handler(message: Message, state: FSMContext):
            await self.get_user(message).get_game().set_random_settings()
            await message.answer(self.get_language(message).story_settings_finish(),
                                 reply_markup=ReplyKeyboardRemove(),
                                 parse_mode='Markdown')

        # Prompts settings
        def get_prompts_settings_menu():
            return ReplyKeyboardMarkup(
                keyboard=[
                    [
                        KeyboardButton(text="/start_prompt"),
                    ],
                    [
                        KeyboardButton(text="/move_prompt"),
                    ],
                    [
                        KeyboardButton(text="/future_prompt"),
                    ],
                    [
                        KeyboardButton(text="/past_prompt"),
                    ],
                    [
                        KeyboardButton(text="/create_info_prompt"),
                    ],
                    [
                        KeyboardButton(text="/update_info_prompt"),
                    ],
                    [
                        KeyboardButton(text="/finish"),
                    ],
                ],
                resize_keyboard=True,
                one_time_keyboard=True
            )

        @self.dp.message(Command("prompts_settings"))
        async def handler(message: Message, state: FSMContext):
            await message.answer(self.get_language(message).prompts_settings(),
                                 reply_markup=get_prompts_settings_menu(),
                                 parse_mode='Markdown')

        @self.dp.message(Command("start_prompt"))
        async def handler(message: Message, state: FSMContext):
            await state.set_state(GameBot.States.start_prompt)
            await message.answer(self.get_language(message).start_prompt(),
                                 parse_mode='Markdown')

        @self.dp.message(Command("move_prompt"))
        async def handler(message: Message, state: FSMContext):
            await state.set_state(GameBot.States.move_prompt)
            await message.answer(self.get_language(message).move_prompt(),
                                 parse_mode='Markdown')

        @self.dp.message(Command("future_prompt"))
        async def handler(message: Message, state: FSMContext):
            await state.set_state(GameBot.States.future_prompt)
            await message.answer(self.get_language(message).future_prompt(),
                                 parse_mode='Markdown')

        @self.dp.message(Command("past_prompt"))
        async def handler(message: Message, state: FSMContext):
            await state.set_state(GameBot.States.past_prompt)
            await message.answer(self.get_language(message).past_prompt(),
                                 parse_mode='Markdown')

        @self.dp.message(Command("create_info_prompt"))
        async def handler(message: Message, state: FSMContext):
            await state.set_state(GameBot.States.create_info_prompt)
            await message.answer(self.get_language(message).create_info_prompt(),
                                 parse_mode='Markdown')

        @self.dp.message(Command("update_info_prompt"))
        async def handler(message: Message, state: FSMContext):
            await state.set_state(GameBot.States.update_info_prompt)
            await message.answer(self.get_language(message).update_info_prompt(),
                                 parse_mode='Markdown')

        # Templates settings
        def get_templates_settings_menu():
            return ReplyKeyboardMarkup(
                keyboard=[
                    [
                        KeyboardButton(text="/start_template"),
                    ],
                    [
                        KeyboardButton(text="/move_template"),
                    ],
                    [
                        KeyboardButton(text="/future_template"),
                    ],
                    [
                        KeyboardButton(text="/past_template"),
                    ],
                    [
                        KeyboardButton(text="/info_template"),
                    ],
                    [
                        KeyboardButton(text="/finish"),
                    ],
                ],
                resize_keyboard=True,
                one_time_keyboard=True
            )

        @self.dp.message(Command("templates_settings"))
        async def handler(message: Message, state: FSMContext):
            await message.answer(self.get_language(message).templates_settings(),
                                 reply_markup=get_templates_settings_menu(),
                                 parse_mode='Markdown')

        @self.dp.message(Command("start_template"))
        async def handler(message: Message, state: FSMContext):
            await state.set_state(GameBot.States.start_template)
            await message.answer(self.get_language(message).start_template(),
                                 parse_mode='Markdown')

        @self.dp.message(Command("move_template"))
        async def handler(message: Message, state: FSMContext):
            await state.set_state(GameBot.States.move_template)
            await message.answer(self.get_language(message).move_template(),
                                 parse_mode='Markdown')

        @self.dp.message(Command("future_template"))
        async def handler(message: Message, state: FSMContext):
            await state.set_state(GameBot.States.future_template)
            await message.answer(self.get_language(message).future_template(),
                                 parse_mode='Markdown')

        @self.dp.message(Command("past_template"))
        async def handler(message: Message, state: FSMContext):
            await state.set_state(GameBot.States.past_template)
            await message.answer(self.get_language(message).past_template(),
                                 parse_mode='Markdown')

        @self.dp.message(Command("info_template"))
        async def handler(message: Message, state: FSMContext):
            await state.set_state(GameBot.States.info_template)
            await message.answer(self.get_language(message).info_template(),
                                 parse_mode='Markdown')

        @self.dp.message(Command("finish"))
        async def handler(message: Message, state: FSMContext):
            await message.answer(self.get_language(message).advanced_settings_finish(),
                                 reply_markup=ReplyKeyboardRemove(),
                                 parse_mode='Markdown')

        # Feedback
        @self.dp.message(Command("feedback"))
        async def handler(message: Message, state: FSMContext):
            await state.set_state(GameBot.States.feedback)
            await message.answer(self.get_language(message).feedback(),
                                 parse_mode='Markdown')

        # Report
        @self.dp.message(Command("report"))
        async def handler(message: Message, state: FSMContext):
            await state.set_state(GameBot.States.report)
            await message.answer(self.get_language(message).report(),
                                 parse_mode='Markdown')

        # Info
        @self.dp.message(Command("info"))
        @log(game_logging.info_log)
        async def handler(message: Message, state: FSMContext):
            game = self.get_user(message).get_game()
            if game:
                await self.send_long_message(message, game.get_info())
            else:
                await message.answer(self.get_language(message).unknown_command(),
                                     parse_mode='Markdown')

        @self.dp.message(Command("future"))
        @log(game_logging.info_log)
        async def handler(message: Message, state: FSMContext):
            game = self.get_user(message).get_game()
            if game and game.future:
                await self.send_long_message(message, game.future)
            else:
                await message.answer(self.get_language(message).unknown_command(),
                                     parse_mode='Markdown')

        @self.dp.message(Command("gpt"))
        @log(game_logging.gpt_log)
        async def handler(message: Message, state: FSMContext):
            AI.current_model = AI.gpt_model
            await message.answer(self.get_language(message).gpt(),
                                 parse_mode='Markdown')

        @self.dp.message(Command("llama"))
        @log(game_logging.llama_log)
        async def handler(message: Message, state: FSMContext):
            AI.current_model = AI.llama_model
            await message.answer(self.get_language(message).llama(),
                                 parse_mode='Markdown')

        @self.dp.message(Command("gemini"))
        @log(game_logging.gemini_log)
        async def handler(message: Message, state: FSMContext):
            AI.current_model = AI.gemini_model
            await message.answer(self.get_language(message).gemini(),
                                 parse_mode='Markdown')

        # Change language
        def get_language_menu():
            return ReplyKeyboardMarkup(
                keyboard=[
                    [
                        KeyboardButton(text="/english"),
                    ],
                    [
                        KeyboardButton(text="/russian"),
                    ],
                ],
                resize_keyboard=True,
                one_time_keyboard=True
            )

        @self.dp.message(Command("language"))
        async def handler(message: Message):
            await message.answer(self.get_language(message).language(),
                                 reply_markup=get_language_menu(),
                                 parse_mode='Markdown')

        @self.dp.message(Command("english"))
        @log(game_logging.english_log)
        async def handler(message: Message, state: FSMContext):
            self.get_user(message).set_language('english')
            await message.answer(self.get_language(message).new_language(),
                                 reply_markup=ReplyKeyboardRemove(),
                                 parse_mode='Markdown')

        @self.dp.message(Command("russian"))
        @log(game_logging.russian_log)
        async def handler(message: Message, state: FSMContext):
            self.get_user(message).set_language('russian')
            await message.answer(self.get_language(message).new_language(),
                                 reply_markup=ReplyKeyboardRemove(),
                                 parse_mode='Markdown')

        # Message history
        def get_history_menu():
            return ReplyKeyboardMarkup(
                keyboard=[
                    [
                        KeyboardButton(text="/open_history"),
                        KeyboardButton(text="/hide_history")
                    ],
                ],
                resize_keyboard=True,
                one_time_keyboard=True
            )

        @self.dp.message(Command("history"))
        async def handler(message: Message, state: FSMContext):
            await message.answer(self.get_language(message).history(),
                                 reply_markup=get_history_menu(),
                                 parse_mode='Markdown')

        @self.dp.message(Command("open_history"))
        @log(game_logging.open_history_log)
        async def handler(message: Message, state: FSMContext):
            self.get_user(message).get_game().set_incognito(False)
            await message.answer(self.get_language(message).open_history(),
                                 reply_markup=ReplyKeyboardRemove(),
                                 parse_mode='Markdown')

        @self.dp.message(Command("hide_history"))
        @log(game_logging.hide_history_log)
        async def handler(message: Message, state: FSMContext):
            self.get_user(message).get_game().set_incognito(True)
            await message.answer(self.get_language(message).hide_history(),
                                 reply_markup=ReplyKeyboardRemove(),
                                 parse_mode='Markdown')

        # Reset settings
        @self.dp.message(Command("reset"))
        @log(game_logging.reset_log)
        async def handler(message: Message, state: FSMContext):
            self.users[message.from_user.id] = self.get_user(message).reset()
            await message.answer(self.get_language(message).reset(),
                                 parse_mode='Markdown')

        # Admin mode
        @self.dp.message(Command("admin"))
        async def handler(message: Message, state: FSMContext) -> None:
            if str(message.from_user.id) in os.environ.get('ADMIN_ID'):
                logging.info(f'{message.from_user.id} ({message.from_user.full_name}): activated the test mode')
                self.get_user(message).admin = True
                await message.answer(self.get_language(message).admin_success(),
                                     parse_mode='Markdown')
            else:
                logging.info(f'{message.from_user.id} ({message.from_user.full_name}): tried to activate the test mode')
                await message.answer(self.get_language(message).admin_fail(),
                                     parse_mode='Markdown')

        @self.dp.message(Command("noadmin"))
        async def handler(message: Message, state: FSMContext) -> None:
            if self.get_user(message).admin:
                self.get_user(message).admin = False
                await message.answer(self.get_language(message).admin_bye(),
                                     parse_mode='Markdown')
            else:
                await message.answer(self.get_language(message).unknown_command(),
                                     parse_mode='Markdown')

        @self.dp.message(Command("get_time"))
        @log(game_logging.time_log)
        async def handler(message: Message, state: FSMContext):
            if self.get_user(message).admin:
                if self.all_moves:
                    average_time = self.all_time // self.all_moves
                    await message.answer(f'_Average waiting time: {average_time // 60}:{(average_time % 60):02}_',
                                         parse_mode='Markdown')
                else:
                    await message.answer('_There have been no requests yet_',
                                         parse_mode='Markdown')
            else:
                await message.answer(self.get_language(message).unknown_command(),
                                     parse_mode='Markdown')

        @self.dp.message(Command("get_settings"))
        async def handler(message: Message, state: FSMContext):
            if self.get_user(message).admin:
                game = self.get_user(message).get_game()
                if game:
                    await self.send_long_message(message, game.prompt_editor.get_settings())
            else:
                await message.answer(self.get_language(message).unknown_command(),
                                     parse_mode='Markdown')

        @self.dp.message(Command("get_future"))
        async def handler(message: Message, state: FSMContext):
            if self.get_user(message).admin:
                game = self.get_user(message).get_game()
                if game:
                    await self.send_long_message(message, game.get_future())
            else:
                await message.answer(self.get_language(message).unknown_command(),
                                     parse_mode='Markdown')

        @self.dp.message(Command("set_gpt"))
        @log(game_logging.gpt_log)
        async def handler(message: Message, state: FSMContext):
            if self.get_user(message).admin:
                AI.current_model = AI.gpt_model
                await message.answer(self.get_language(message).gpt(),
                                     parse_mode='Markdown')
            else:
                await message.answer(self.get_language(message).unknown_command(),
                                     parse_mode='Markdown')

        @self.dp.message(Command("set_llama"))
        @log(game_logging.llama_log)
        async def handler(message: Message, state: FSMContext):
            if self.get_user(message).admin:
                AI.current_model = AI.llama_model
                await message.answer(self.get_language(message).llama(),
                                     parse_mode='Markdown')
            else:
                await message.answer(self.get_language(message).unknown_command(),
                                     parse_mode='Markdown')

        @self.dp.message(Command("set_gemini"))
        @log(game_logging.gemini_log)
        async def handler(message: Message, state: FSMContext):
            if self.get_user(message).admin:
                AI.current_model = AI.gemini_model
                await message.answer(self.get_language(message).gemini(),
                                     parse_mode='Markdown')
            else:
                await message.answer(self.get_language(message).unknown_command(),
                                     parse_mode='Markdown')

        # Help
        @self.dp.message(Command("help"))
        async def handler(message: Message, state: FSMContext):
            if self.get_user(message).admin:
                await message.answer(self.get_language(message).help_admin(),
                                     parse_mode='Markdown')
            else:
                await message.answer(self.get_language(message).help(),
                                     parse_mode='Markdown')

        # New game
        @self.dp.message(Command("newgame"))
        @log(game_logging.newgame_log)
        async def handler(message: Message, state: FSMContext):
            start_time = time.time()

            temporary_message = await message.answer(self.get_language(message).wait(),
                                                     parse_mode='Markdown')

            try:
                now = await self.get_user(message).get_game().start()
                await self.send_long_message(message, now)
                self.log_waiting_time(message, start_time)
                await self.users[message.from_user.id].game.other(now)

            except Exception as e:
                logging.error(e)
                await message.answer(self.get_language(message).error(),
                                     parse_mode='Markdown')

            await temporary_message.delete()

        # Unknown command
        @self.dp.message(lambda message: message.text.startswith('/'))
        async def unknown_command_handler(message: Message):
            await message.answer(self.get_language(message).unknown_command(),
                                 parse_mode='Markdown')

        # States
        # Story Settings
        @self.dp.message(GameBot.States.settings)
        @log(game_logging.set_basic_log)
        async def handler(message: Message, state: FSMContext):
            await state.clear()
            await self.get_user(message).get_game().set_settings(message.text)
            await message.answer(self.get_language(message).story_settings_finish(),
                                 parse_mode='Markdown')

        # Prompts settings
        @self.dp.message(GameBot.States.start_prompt)
        async def handler(message: Message, state: FSMContext):
            await state.clear()
            await self.get_user(message).get_game().set_start_prompt(message.text)
            await message.answer(self.get_language(message).edit_prompt(),
                                 parse_mode='Markdown')

        @self.dp.message(GameBot.States.move_prompt)
        async def handler(message: Message, state: FSMContext):
            await state.clear()
            await self.get_user(message).get_game().set_move_prompt(message.text)
            await message.answer(self.get_language(message).edit_prompt(),
                                 parse_mode='Markdown')

        @self.dp.message(GameBot.States.future_prompt)
        async def handler(message: Message, state: FSMContext):
            await state.clear()
            await self.get_user(message).get_game().set_future_prompt(message.text)
            await message.answer(self.get_language(message).edit_prompt(),
                                 parse_mode='Markdown')

        @self.dp.message(GameBot.States.past_prompt)
        async def handler(message: Message, state: FSMContext):
            await state.clear()
            await self.get_user(message).get_game().set_past_prompt(message.text)
            await message.answer(self.get_language(message).edit_prompt(),
                                 parse_mode='Markdown')

        @self.dp.message(GameBot.States.create_info_prompt)
        async def handler(message: Message, state: FSMContext):
            await state.clear()
            await self.get_user(message).get_game().set_create_info_prompt(message.text)
            await message.answer(self.get_language(message).edit_prompt(),
                                 parse_mode='Markdown')

        @self.dp.message(GameBot.States.update_info_prompt)
        async def handler(message: Message, state: FSMContext):
            await state.clear()
            await self.get_user(message).get_game().set_update_info_prompt(message.text)
            await message.answer(self.get_language(message).edit_prompt(),
                                 parse_mode='Markdown')

        # Templates settings
        @self.dp.message(GameBot.States.start_template)
        async def handler(message: Message, state: FSMContext):
            await state.clear()
            await self.get_user(message).get_game().set_start_template(message.text)
            await message.answer(self.get_language(message).edit_template(),
                                 parse_mode='Markdown')

        @self.dp.message(GameBot.States.move_template)
        async def handler(message: Message, state: FSMContext):
            await state.clear()
            await self.get_user(message).get_game().set_move_template(message.text)
            await message.answer(self.get_language(message).edit_template(),
                                 parse_mode='Markdown')

        @self.dp.message(GameBot.States.future_template)
        async def handler(message: Message, state: FSMContext):
            await state.clear()
            await self.get_user(message).get_game().set_future_template(message.text)
            await message.answer(self.get_language(message).edit_template(),
                                 parse_mode='Markdown')

        @self.dp.message(GameBot.States.past_template)
        async def handler(message: Message, state: FSMContext):
            await state.clear()
            await self.get_user(message).get_game().set_past_template(message.text)
            await message.answer(self.get_language(message).edit_template(),
                                 parse_mode='Markdown')

        @self.dp.message(GameBot.States.info_template)
        async def handler(message: Message, state: FSMContext):
            await state.clear()
            await self.get_user(message).get_game().set_info_template(message.text)
            await message.answer(self.get_language(message).edit_template(),
                                 parse_mode='Markdown')

        # Feedback
        @self.dp.message(GameBot.States.feedback)
        @log(game_logging.feedback, level='WARNING')
        async def handler(message: Message, state: FSMContext):
            await state.clear()
            await self.get_user(message).get_game().write.feedback(message.text)
            await message.answer(self.get_language(message).feedback_thanks(),
                                 parse_mode='Markdown')

        # Report
        @self.dp.message(GameBot.States.report)
        @log(game_logging.complain, level='WARNING')
        async def handler(message: Message, state: FSMContext):
            await state.clear()
            await self.get_user(message).get_game().write.report(message.text)
            await message.answer(self.get_language(message).bug_report_thanks(),
                                 parse_mode='Markdown')

        # Other
        # Move
        @self.dp.message()
        async def handler(message: Message, state: FSMContext):
            start_time = time.time()
            game = self.get_user(message).game

            if not game.count:
                await message.answer(self.get_language(message).noga11me(),
                                     parse_mode='Markdown')
            elif game.wait:
                await message.answer(self.get_language(message).wait_strong(),
                                     parse_mode='Markdown')
            else:
                temporary_message = await message.answer(self.get_language(message).wait(),
                                                         parse_mode='Markdown')
                try:
                    now = await self.users[message.from_user.id].game.move(message.text)
                    await self.send_long_message(message, now)
                    self.log_waiting_time(message, start_time)
                    await self.users[message.from_user.id].game.other(now)

                except Exception as e:
                    logging.error(e)
                    self.get_user(message).get_game().wait = 0
                    self.get_user(message).get_game().past_relevant = True
                    self.get_user(message).get_game().info_relevant = True
                    await message.answer(self.get_language(message).error(),
                                         parse_mode='Markdown')

                await temporary_message.delete()

    async def run(self):
        await self.dp.start_polling(self.bot)
