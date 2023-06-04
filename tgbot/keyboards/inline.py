from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types.inline_keyboard_button import InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData

async def score_keyboard(step):
    keyboard = InlineKeyboardBuilder()

    keyboard.add(InlineKeyboardButton(text='1', callback_data=Factories.Score(id=1, step=step).pack()))
    keyboard.add(InlineKeyboardButton(text='2', callback_data=Factories.Score(id=2, step=step).pack()))
    keyboard.add(InlineKeyboardButton(text='3', callback_data=Factories.Score(id=3, step=step).pack()))
    keyboard.add(InlineKeyboardButton(text='4', callback_data=Factories.Score(id=4, step=step).pack()))
    keyboard.add(InlineKeyboardButton(text='5', callback_data=Factories.Score(id=5, step=step).pack()))

    return keyboard.as_markup()



def language_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(
            text="Ўзбекча", callback_data=Factories.Language(language="uz").pack()
        ),
        # InlineKeyboardButton(
        #     text="🇷🇺 Русcкий", callback_data=Factories.Language(language="ru").pack()
        # ),
        InlineKeyboardButton(
            text="O'zbekcha", callback_data=Factories.Language(language="de").pack()
        ),
    )

    keyboard.adjust(1)
    return keyboard.as_markup()

class Factories:
    class Language(CallbackData, prefix='lang'):
        language: str

    class Score(CallbackData, prefix='score'):
        id: str
        step: str