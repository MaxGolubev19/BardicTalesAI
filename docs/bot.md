# bot.py

Класс `GameBot` управляет Telegram-ботом, обрабатывает команды и управляет взаимодействием с пользователем.

## Класс `GameBot`

### Атрибуты  
- `MAX_MESSAGE_LENGTH (int)`: Максимальная длина отправляемого сообщения.  
- `bot (Bot)`: Экземпляр Telegram-бота.  
- `dp (Dispatcher)`: Диспетчер событий для обработки сообщений.  
- `users (Dict[int, User])`: Словарь пользователей.  
- `user_file (str)`: Путь к файлу с сохранёнными пользователями.  
- `all_time (int)`: Общее время ожидания обработки сообщений.  
- `all_moves (int)`: Количество обработанных ходов.  

### Вложенный класс `States`
Состояния пользователя в боте:
- `settings` – Настройка описания истории.  
- `feedback` – Отправка обратной связи.  
- `report` – Сообщение о проблеме.  
- `language` – Выбор языка.  
- `start_prompt`, `move_prompt`, `future_prompt`, `past_prompt`, `create_info_prompt`, `update_info_prompt` – Настройка соответствующего промта.  
- `start_template`, `move_template`, `future_template`, `past_template`, `info_template` – Настройка соответствующего шаблона.  

### Методы  

#### `__init__(self, token: str)`  
Инициализирует бота, загружает пользователей, регистрирует обработчики команд.  

---

#### `load_users(self) -> None`  
Загружает сохранённых пользователей из файла.  

---

#### `save_users(self) -> None`  
Сохраняет пользователей в файл перед завершением работы.  

---

#### `get_user(self, message: Message) -> User`  
Возвращает объект `User` для заданного пользователя.  

---

#### `get_language(self, message: Message) -> Module`  
Определяет язык текущего пользователя.  

---

#### `async send_long_message(self, message: Message, answer: str) -> None`  
Отправляет сообщение от имени бота. Сообщения допустимого размера пытается парсить, длинные сообщения разбивает на части.  

---

#### `log_waiting_time(self, message, start_time) -> None`  
Логирует время ожидания ответа.  

---

#### `async send_history(self, message: str) -> None`  
Отправляет сообщение в канал истории игр.  

---

#### `async send_feedback(self, message: str) -> None`  
Отправляет сообщение в канал обратной связи.  

---

#### `register_handlers(self) -> None`  
Регистрирует обработчики команд.  

#### **Обработчики команд**
- `/start` – Начало использования бота, отображает меню жанров.
- `/cancel` – Отмена текущего действия.
- `/settings` – Открывает меню настроек.
- `/story_settings`, `/random_settings` – Редактирование описания истории.
- `/prompts_settings`, `/templates_settings` – Редактирование промтов и шаблонов.
- `/feedback`, `/report` – Отправка отзывов и жалоб.
- `/info`, `/future` – Получение информации об игре.
- `/gpt`, `/llama`, `/gemini` – Выбор модели AI.
- `/language`, `/english`, `/russian` – Изменение языка.
- `/history`, `/open_history`, `/hide_history` – Включение и отключение режима инкогнито.
- `/reset` – Сброс настроек пользователя.
- `/admin`, `/noadmin` – Вход и выход из режима администратора.
- `/get_time`, `/get_settings`, `/get_future` – Команды для администраторов (получение среднего времени ответа бота, команды для тестирования).
- `/set_gpt`, `/set_llama`, `/set_gemini` – Установка AI-модели.
- `/help` – Получение инструкции по использованию бота.
- `/newgame` – Начало новой игры.

---

#### `async run(self) -> None`  
Запускает бота, начиная обработку сообщений.
