import logging
from functools import wraps

from aiogram.fsm.context import FSMContext
from aiogram.types import Message


def simpleanswer(answer):
    def decorator(func):
        @wraps(func)
        async def wrapper(message: Message, state: FSMContext, *args, **kwargs):
            await func(message, state, *args, *kwargs)
            await message.answer(answer(), parse_mode='Markdown')

        return wrapper

    return decorator


def log(info, level='INFO'):
    def decorator(func):
        @wraps(func)
        async def wrapper(message: Message, *args, **kwargs):
            log_message = f'{message.from_user.id} ({message.from_user.full_name}): {info()}'

            match level:
                case 'DEBUG':
                    logging.debug(log_message)
                case 'INFO':
                    logging.info(log_message)
                case 'WARNING':
                    logging.warning(log_message)
                case 'ERROR':
                    logging.error(log_message)
                case 'CRITICAL':
                    logging.critical(log_message)

            return await func(message, *args, **kwargs)
        return wrapper
    return decorator
