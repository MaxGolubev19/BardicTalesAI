# write.py

Класс `Write` отвечает за логирование и отправку истории сообщений, отзывов и отчётов.

## Класс `Write`

### Атрибуты  
- `send_history (callable | None)`: Функция для отправки истории сообщений.  
- `send_feedback (callable | None)`: Функция для отправки обратной связи.  
- `MAX_MESSAGE_LENGTH (int)`: Максимальная длина сообщения (4096 символов).  
- `user_id (int)`: Идентификатор пользователя.  
- `user_name (str)`: Имя пользователя.  
- `incognito (bool)`: Флаг скрытия истории сообщений.  

### Методы  

#### `__init__(self, user_id: int, user_name: str)`  
Создаёт объект `Write` для указанного пользователя.  

---

#### `async write_message(self, role: str, content: str) -> None`  
Отправляет сообщение в канал истории, если инкогнито-режим отключён. Разбивает длинные сообщения.  

---

#### `async write_feedback(self, role: str, content: str) -> None`  
Отправляет сообщение в канал обратной связи. Разбивает длинные сообщения.  

---

#### `async set_settings(self, settings: str) -> None`  
Сохраняет в истории описание игры.  

---

#### `async set_start_prompt(self, prompt: str) -> None`  
Сохраняет в истории стартовый промт.  

---

#### `async set_move_prompt(self, prompt: str) -> None`  
Сохраняет в истории промт для очередного хода.  

---

#### `async set_future_prompt(self, prompt: str) -> None`  
Сохраняет в истории промт для предсказания будущего.  

---

#### `async set_past_prompt(self, prompt: str) -> None`  
Сохраняет в истории промт для краткого содержания предыдущих событий.  

---

#### `async set_create_info_prompt(self, prompt: str) -> None`  
Сохраняет в истории промт для создания информации об игре.  

---

#### `async set_update_info_prompt(self, prompt: str) -> None`  
Сохраняет в истории промт для обновления информации об игре.  

---

#### `async set_start_template(self, prompt: str) -> None`  
Сохраняет в истории шаблон первого эпизода игры.  

---

#### `async set_move_template(self, prompt: str) -> None`  
Сохраняет в истории шаблон очередного хода.  

---

#### `async set_future_template(self, prompt: str) -> None`  
Сохраняет в истории шаблон предсказания будущего.  

---

#### `async set_past_template(self, prompt: str) -> None`  
Сохраняет в истории шаблон краткого содержания предыдущих событий.  

---

#### `async set_info_template(self, prompt: str) -> None`  
Сохраняет в истории шаблон информации об игре.  

---

#### `async move(self, role: str, content: str) -> None`  
Сохраняет в истории эпизод игры.  

---

#### `async feedback(self, content: str) -> None`  
Отправляет отзыв в канал обратной связи.  

---

#### `async report(self, content: str) -> None`  
Отправляет жалобу в канал обратной связи.  

---

#### `set_incognito(self, incognito: bool) -> None`  
Включает или отключает инкогнито-режим.

