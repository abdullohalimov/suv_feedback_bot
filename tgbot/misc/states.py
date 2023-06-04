from aiogram.fsm.state import StatesGroup, State
from aiogram.utils.i18n import I18n

i18n = I18n(path="locales", default_locale="de", domain="messages")

i18nn = i18n.gettext

class UserStates(StatesGroup):
    language = State()
    id = State()
    first = State()
    second = State()
    third = State()
    four = State()
    five = State()
    six = State()
    seven = State()
