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

from writing import game_logging
from writing.decorators import log
from writing.write import Write
from game_user import GameUser
from ai import AI


class GameBot:
    user_file = 'data/users_data.pkl'
    users: Dict[int, GameUser] = {}

    all_time = 0
    all_moves = 0

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
        info_template = State()

        admin_mode = State()

    def __init__(self):
        self.bot = Bot(token=os.environ.get('BOT_TOKEN'))
        self.dp = Dispatcher()

        Write.send_feedback = self.send_feedback
        Write.send_history = self.send_history

        atexit.register(self.save_users)
        self.register_handlers()

        self.users = {}
        self.load_users()

    def load_users(self):
        try:
            with open(GameBot.user_file, 'rb') as file:
                self.users = dill.load(file)

        except Exception as e:
            logging.error(e)

    def save_users(self):
        with open(GameBot.user_file, 'wb') as file:
            dill.dump(self.users, file)

    def get_user(self, message: Message):
        self.users[message.from_user.id] = self.users.get(message.from_user.id,
                                                          GameUser(message.from_user.id, message.from_user.full_name))
        return self.users[message.from_user.id]

    def get_language(self, message: Message):
        return self.get_user(message).get_language()

    async def send_long_message(self, message: Message, answer: str) -> None:
        for i in range(0, len(answer), self.MAX_MESSAGE_LENGTH):
            await message.answer(answer[i:i + self.MAX_MESSAGE_LENGTH])

    async def return_to_state(self, message, state):
        if self.users.get(message.from_user.id, GameUser(message.from_user.id, message.from_user.full_name)).admin:
            await state.set_state(GameBot.States.admin_mode)
        else:
            await state.clear()

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
            await self.return_to_state(message, state)
            await message.answer(self.get_language(message).cancel(),
                                 reply_markup=ReplyKeyboardRemove(),
                                 parse_mode='Markdown')

        # Start
        @self.dp.message(Command("start"))
        @log(game_logging.start_log)
        async def handler(message: Message, state: FSMContext):
            await message.answer(self.get_language(message).start(),
                                 parse_mode='Markdown')

        # Settings
        def get_settings_menu():
            return ReplyKeyboardMarkup(
                keyboard=[
                    [
                        KeyboardButton(text="/story_settings")
                    ],
                    [
                        KeyboardButton(text="/random_settings"),
                        KeyboardButton(text="/prompts_settings"),
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

        # Random settings
        @self.dp.message(Command("random_settings"))
        @log(game_logging.set_basic_log)
        async def handler(message: Message, state: FSMContext):
            await self.get_user(message).get_game().set_random_settings()
            await message.answer(self.get_language(message).story_settings_finish(),
                                 reply_markup=ReplyKeyboardRemove(),
                                 parse_mode='Markdown')

        # Basic Settings
        @self.dp.message(Command("story_settings"))
        async def handler(message: Message, state: FSMContext):
            await state.set_state(GameBot.States.settings)
            await message.answer(self.get_language(message).story_settings(),
                                 reply_markup=ReplyKeyboardRemove(),
                                 parse_mode='Markdown')

        # Advanced settings
        def get_advanced_settings_menu():
            return ReplyKeyboardMarkup(
                keyboard=[
                    [
                        KeyboardButton(text="/start_prompt"),
                        KeyboardButton(text="/move_prompt"),
                    ],
                    [
                        KeyboardButton(text="/future_prompt"),
                        KeyboardButton(text="/past_prompt"),
                    ],
                    [
                        KeyboardButton(text="/create_info_prompt"),
                        KeyboardButton(text="/update_info_prompt"),
                    ],
                    [
                        KeyboardButton(text="/info_template"),
                        KeyboardButton(text="/finish"),
                    ],
                ],
                resize_keyboard=True,
                one_time_keyboard=True
            )

        @self.dp.message(Command("prompts_settings"))
        async def handler(message: Message, state: FSMContext):
            await message.answer(self.get_language(message).prompts_settings(),
                                 reply_markup=get_advanced_settings_menu(),
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

        @self.dp.message(Command("info_template"))
        async def handler(message: Message, state: FSMContext):
            await state.set_state(GameBot.States.info_template)
            await message.answer(self.get_language(message).info_template(),
                                 parse_mode='Markdown')

        @self.dp.message(Command("finish"))
        async def handler(message: Message, state: FSMContext):
            await message.answer(self.get_language(message).prompts_settings_finish(),
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

        # Censorship
        def get_censorship_menu():
            return ReplyKeyboardMarkup(
                keyboard=[
                    [
                        KeyboardButton(text="/enable_censorship"),
                        KeyboardButton(text="/disable_censorship")
                    ],
                ],
                resize_keyboard=True,
                one_time_keyboard=True
            )

        @self.dp.message(GameBot.States.admin_mode, Command("censorship"))
        async def handler(message: Message, state: FSMContext):
            await message.answer(self.get_language(message).censorship(),
                                 reply_markup=get_censorship_menu(),
                                 parse_mode='Markdown')

        @self.dp.message(GameBot.States.admin_mode, Command("enable_censorship"))
        @log(game_logging.enable_censorship_log)
        async def handler(message: Message, state: FSMContext):
            self.get_user(message).get_game().set_parental_control(True)
            await message.answer(self.get_language(message).enable_censorship(),
                                 reply_markup=ReplyKeyboardRemove(),
                                 parse_mode='Markdown')

        @self.dp.message(GameBot.States.admin_mode, Command("disable_censorship"))
        @log(game_logging.disable_censorship_log)
        async def handler(message: Message, state: FSMContext):
            self.get_user(message).get_game().set_parental_control(False)
            await message.answer(self.get_language(message).disable_censorship(),
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
                await state.set_state(GameBot.States.admin_mode)
                await message.answer(self.get_language(message).admin_success(),
                                     parse_mode='Markdown')
            else:
                logging.info(f'{message.from_user.id} ({message.from_user.full_name}): tried to activate the test mode')
                await message.answer(self.get_language(message).admin_fail(),
                                     parse_mode='Markdown')

        @self.dp.message(GameBot.States.admin_mode, Command("noadmin"))
        async def handler(message: Message, state: FSMContext) -> None:
            self.get_user(message).admin = False
            await message.answer(self.get_language(message).admin_bye(),
                                 parse_mode='Markdown')

        @self.dp.message(GameBot.States.admin_mode, Command("get_time"))
        @log(game_logging.time_log)
        async def handler(message: Message, state: FSMContext):
            if self.all_moves:
                average_time = self.all_time // self.all_moves
                await message.answer(f'_Average waiting time: {average_time // 60}:{(average_time % 60):02}_',
                                     parse_mode='Markdown')
            else:
                await message.answer('_There have been no requests yet_',
                                     parse_mode='Markdown')

        @self.dp.message(GameBot.States.admin_mode, Command("get_settings"))
        async def handler(message: Message, state: FSMContext):
            game = self.get_user(message).get_game()
            if game:
                await self.send_long_message(message, game.settings)

        @self.dp.message(GameBot.States.admin_mode, Command("set_openai"))
        @log(game_logging.openai_log)
        async def handler(message: Message, state: FSMContext):
            AI.current_API = 'openai'
            await message.answer(self.get_language(message).openai(),
                                 parse_mode='Markdown')

        @self.dp.message(GameBot.States.admin_mode, Command("set_groq"))
        @log(game_logging.groq_log)
        async def handler(message: Message, state: FSMContext):
            AI.current_API = 'groq'
            await message.answer(self.get_language(message).groq(),
                                 parse_mode='Markdown')

        @self.dp.message(GameBot.States.admin_mode, Command("set_ollama"))
        @log(game_logging.ollama_log)
        async def handler(message: Message, state: FSMContext):
            AI.current_API = 'ollama'
            await message.answer(self.get_language(message).ollama(),
                                 parse_mode='Markdown')

        @self.dp.message(GameBot.States.admin_mode, Command("help"))
        async def handler(message: Message, state: FSMContext):
            await message.answer(self.get_language(message).help_admin(),
                                 parse_mode='Markdown')

        # Help
        @self.dp.message(Command("help"))
        async def handler(message: Message, state: FSMContext):
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

        # States
        # Story Settings
        @self.dp.message(GameBot.States.settings)
        @log(game_logging.set_basic_log)
        async def handler(message: Message, state: FSMContext):
            await self.return_to_state(message, state)
            await self.get_user(message).get_game().set_basic_settings(message.text)
            await message.answer(self.get_language(message).story_settings_finish(),
                                 parse_mode='Markdown')

        # Prompts settings
        @self.dp.message(GameBot.States.start_prompt)
        async def handler(message: Message, state: FSMContext):
            await self.return_to_state(message, state)
            await self.get_user(message).get_game().set_start_prompt(message.text)
            await message.answer(self.get_language(message).edit_prompt(),
                                 parse_mode='Markdown')

        @self.dp.message(GameBot.States.move_prompt)
        async def handler(message: Message, state: FSMContext):
            await self.return_to_state(message, state)
            await self.get_user(message).get_game().set_move_prompt(message.text)
            await message.answer(self.get_language(message).edit_prompt(),
                                 parse_mode='Markdown')

        @self.dp.message(GameBot.States.future_prompt)
        async def handler(message: Message, state: FSMContext):
            await self.return_to_state(message, state)
            await self.get_user(message).get_game().set_future_prompt(message.text)
            await message.answer(self.get_language(message).edit_prompt(),
                                 parse_mode='Markdown')

        @self.dp.message(GameBot.States.past_prompt)
        async def handler(message: Message, state: FSMContext):
            await self.return_to_state(message, state)
            await self.get_user(message).get_game().set_past_prompt(message.text)
            await message.answer(self.get_language(message).edit_prompt(),
                                 parse_mode='Markdown')

        @self.dp.message(GameBot.States.info_template)
        async def handler(message: Message, state: FSMContext):
            await self.return_to_state(message, state)
            await self.get_user(message).get_game().set_info_template(message.text)
            await message.answer(self.get_language(message).edit_prompt(),
                                 parse_mode='Markdown')

        @self.dp.message(GameBot.States.create_info_prompt)
        async def handler(message: Message, state: FSMContext):
            await self.return_to_state(message, state)
            await self.get_user(message).get_game().set_create_info_prompt(message.text)
            await message.answer(self.get_language(message).edit_prompt(),
                                 parse_mode='Markdown')

        @self.dp.message(GameBot.States.update_info_prompt)
        async def handler(message: Message, state: FSMContext):
            await self.return_to_state(message, state)
            await self.get_user(message).get_game().set_update_info_prompt(message.text)
            await message.answer(self.get_language(message).edit_prompt(),
                                 parse_mode='Markdown')

        # Feedback
        @self.dp.message(GameBot.States.feedback)
        @log(game_logging.feedback, level='WARNING')
        async def handler(message: Message, state: FSMContext):
            await self.return_to_state(message, state)
            await self.get_user(message).get_game().write.feedback(message.text)
            await message.answer(self.get_language(message).feedback_thanks(),
                                 parse_mode='Markdown')

        # Report
        @self.dp.message(GameBot.States.report)
        @log(game_logging.complain, level='WARNING')
        async def handler(message: Message, state: FSMContext):
            await self.return_to_state(message, state)
            await self.get_user(message).get_game().write.report(message.text)
            await message.answer(self.get_language(message).bug_report_thanks(),
                                 parse_mode='Markdown')

        # Other
        # Move
        @self.dp.message()
        async def handler(message: Message, state: FSMContext):
            start_time = time.time()
            game = self.get_user(message).game

            if game.count:
                if game.wait:
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
                        await message.answer(self.get_language(message).error(),
                                             parse_mode='Markdown')

                    await temporary_message.delete()

            else:
                await message.answer(self.get_language(message).nogame(),
                                     parse_mode='Markdown')

    async def run(self):
        await self.dp.start_polling(self.bot)
