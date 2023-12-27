from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

titles = (
    "Предсказания🎱",
    "Ответ на вопрос🎱",
    "Легально?⚠",
    "Свой бот🤖",
    "Помощь🚒",
    )

buttons: list[KeyboardButton] = [
        KeyboardButton(text=title) for title in titles
        ]

keyboard = ReplyKeyboardMarkup(
        keyboard=[
            buttons[:2],
            buttons[2:],
            ],
        resize_keyboard=True,
        )
