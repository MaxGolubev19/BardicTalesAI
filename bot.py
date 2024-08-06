import logging
import os
import time
import dill
import atexit
from typing import Dict

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

from writing import game_logging
from writing.decorators import log
from ai import AI
from game_user import GameUser


class GameBot:
    user_file = 'info/users_data.pkl'
    users: Dict[int, GameUser] = {}

    all_time = 0
    all_moves = 0

    MAX_MESSAGE_LENGTH = 4096

    class States(StatesGroup):
        settings = State()
        feedback = State()
        bug_report = State()
        language = State()

        settings_pro_start = State()
        settings_pro_move = State()
        settings_pro_rule = State()

        admin_mode = State()

    def __init__(self):
        self.bot = Bot(token=os.environ.get('BOT_TOKEN'))
        self.dp = Dispatcher()
        self.register_handlers()
        atexit.register(self.save_users)

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

    def register_handlers(self) -> None:
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
                        KeyboardButton(text="/basic_settings"),
                        # KeyboardButton(text="/advanced_settings")
                    ],
                    [
                        KeyboardButton(text="/random_settings"),
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

        # Random genre
        @self.dp.message(Command("random_settings"))
        @log(game_logging.set_basic_log)
        async def handler(message: Message, state: FSMContext):
            self.get_user(message).get_game().set_genre()
            await message.answer(self.get_language(message).basic_finish(),
                                 reply_markup=ReplyKeyboardRemove(),
                                 parse_mode='Markdown')

        # Basic Settings
        @self.dp.message(Command("basic_settings"))
        async def handler(message: Message, state: FSMContext):
            await state.set_state(GameBot.States.settings)
            await message.answer(self.get_language(message).basic_start(),
                                 reply_markup=ReplyKeyboardRemove(),
                                 parse_mode='Markdown')

        @self.dp.message(GameBot.States.settings)
        @self.dp.message(GameBot.States.settings)
        @log(game_logging.set_basic_log)
        async def handler(message: Message, state: FSMContext):
            await self.return_to_state(message, state)
            self.get_user(message).get_game().set_settings(message.text)
            await message.answer(self.get_language(message).basic_finish(),
                                 parse_mode='Markdown')

        # # Advanced settings
        # def get_advanced_settings_menu():
        #     return ReplyKeyboardMarkup(
        #         keyboard=[
        #             [
        #                 KeyboardButton(text="/set_role"),
        #                 KeyboardButton(text="/set_start"),
        #                 KeyboardButton(text="/set_move"),
        #                 KeyboardButton(text="/set_rule"),
        #                 KeyboardButton(text="/set_past"),
        #                 KeyboardButton(text="/set_info_template"),
        #                 KeyboardButton(text="/set_info"),
        #             ],
        #         ],
        #         resize_keyboard=True,
        #         one_time_keyboard=True
        #     )
        #
        # @self.dp.message(Command("advanced_settings"))
        # async def handler(message: Message, state: FSMContext):
        #     await message.answer(self.get_language(message).start_prompt(),
        #                          reply_markup=get_advanced_settings_menu(),
        #                          parse_mode='Markdown')
        #
        # @self.dp.message(GameBot.States.settings_pro_start)
        # async def handler(message: Message, state: FSMContext):
        #     await state.set_state(GameBot.States.settings_pro_move)
        #     self.get_user(message).get_game().set_start_prompt(message.text)
        #     await message.answer(self.get_language(message).move_prompt(),
        #                          parse_mode='Markdown')
        #
        # @self.dp.message(GameBot.States.settings_pro_move)
        # async def handler(message: Message, state: FSMContext):
        #     await state.set_state(GameBot.States.settings_pro_rule)
        #     self.get_user(message).get_game().set_move_prompt(message.text)
        #     await message.answer(self.get_language(message).rule_prompt(),
        #                          parse_mode='Markdown')
        #
        # @self.dp.message(GameBot.States.settings_pro_rule)
        # @log(game_logging.set_advanced_log)
        # async def handler(message: Message, state: FSMContext):
        #     await self.return_to_state(message, state)
        #     self.get_user(message).get_game().set_rule_prompt(message.text)
        #     await message.answer(self.get_language(message).prompts_finish(),
        #                          parse_mode='Markdown')

        # Feedback
        @self.dp.message(Command("feedback"))
        async def handler(message: Message, state: FSMContext):
            await state.set_state(GameBot.States.feedback)
            await message.answer(self.get_language(message).feedback(),
                                 parse_mode='Markdown')

        @self.dp.message(GameBot.States.feedback)
        @log(game_logging.feedback, level='WARNING')
        async def handler(message: Message, state: FSMContext):
            await self.return_to_state(message, state)
            self.get_user(message).get_game().history.feedback(message.text)
            await message.answer(self.get_language(message).feedback_thanks(),
                                 parse_mode='Markdown')

        # Complaint
        @self.dp.message(Command("report"))
        async def handler(message: Message, state: FSMContext):
            await state.set_state(GameBot.States.bug_report)
            await message.answer(self.get_language(message).bug_report(),
                                 parse_mode='Markdown')

        @self.dp.message(GameBot.States.bug_report)
        @log(game_logging.complain, level='WARNING')
        async def handler(message: Message, state: FSMContext):
            await self.return_to_state(message, state)
            self.get_user(message).get_game().history.bug_report(message.text)
            await message.answer(self.get_language(message).bug_report_thanks(),
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
            self.get_user(message).set_language('English')
            await message.answer(self.get_language(message).new_language(),
                                 reply_markup=ReplyKeyboardRemove(),
                                 parse_mode='Markdown')

        @self.dp.message(Command("russian"))
        @log(game_logging.russian_log)
        async def handler(message: Message, state: FSMContext):
            self.get_user(message).set_language('Russian')
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
                await self.send_long_message(message, game.settings_prompt)

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
                await self.send_long_message(message, await self.get_user(message).get_game().start())
                self.log_waiting_time(message, start_time)
                await self.users[message.from_user.id].game.other()

            except Exception as e:
                logging.error(e)
                await message.answer(self.get_language(message).error(),
                                     parse_mode='Markdown')

            await temporary_message.delete()

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
                        await self.send_long_message(message,
                                                     await self.users[message.from_user.id].game.move(message.text))
                        self.log_waiting_time(message, start_time)
                        await self.users[message.from_user.id].game.other()

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
