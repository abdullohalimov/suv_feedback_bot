from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from tgbot.keyboards.inline import score_keyboard, language_keyboard, Factories
from tgbot.misc import states as states
from tgbot.misc.states import i18nn as _
from tgbot.services.db import Score

user_router = Router()

@user_router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await message.answer(
        "Тилни танланг..\n\nTilni tanlang..",
        reply_markup=language_keyboard(),
    )
    await state.set_state(states.UserStates.language)


@user_router.callback_query(Factories.Language.filter())
async def user_start(callback: CallbackQuery, callback_data: Factories.Language, state: FSMContext):

    await callback.message.answer(_("Sertifikatni yuklab olish uchun quyidagi so'rovnomani to'ldiring."))
    await callback.message.answer(_('Universitet professor-o\'qituvchisini baholang\n(Suv tejovchi texnologiyalarning afzalliklari va ularni samaradorligi)'), reply_markup=score_keyboard(1))
    await state.set_state(states.UserStates.first)
    await state.update_data(language=callback_data.language)


@user_router.callback_query(states.UserStates.first)
async def first_step(callback: CallbackQuery, callback_data: Factories.Score, state: FSMContext):
    await callback.message.answer(_("Turk mutaxassisini baholang\n(Zamonaviy sug'orish tizimining ahamiyati va suvdan foydalanish madaniyati)"), reply_markup=score_keyboard(2))
    await state.set_state(states.UserStates.second)
    await state.update_data(first_step=callback_data.id)



@user_router.callback_query(states.UserStates.second)
async def second(callback: CallbackQuery, callback_data: Factories.Score, state: FSMContext):
    await callback.message.answer(_("Bank mutaxassisini baholang\n(Iqtisodiy va huquqiy savodxonlik: subsidiya, kafilliklar, soliq imtiyozlari va bank kreditlari)"), reply_markup=score_keyboard(3))
    await state.set_state(states.UserStates.third)
    await state.update_data(second=callback_data.id)



@user_router.callback_query(states.UserStates.third)
async def third(callback: CallbackQuery, callback_data: Factories.Score, state: FSMContext):
    await callback.message.answer(_("Suv xo'jaligi vazirligi mutaxassisini baholang\n(Iqtisodiy va huquqiy savodxonlik: subsidiya, kafilliklar, soliq imtiyozlari va bank kreditlari)"), reply_markup=score_keyboard(4))
    await state.set_state(states.UserStates.four)
    await state.update_data(third=callback_data.id)



@user_router.callback_query(states.UserStates.four)
async def four(callback: CallbackQuery, callback_data: Factories.Score, state: FSMContext):
    await callback.message.answer(_("O'quv kursi tashkiliy jarayonlari (o'quv materiallari, esdalik sovg'alar, tushlik va boshqalar)ni baholang"), reply_markup=score_keyboard(5))
    await state.set_state(states.UserStates.five)
    await state.update_data(four=callback_data.id)



@user_router.callback_query(states.UserStates.five)
async def five(callback: CallbackQuery, callback_data: Factories.Score, state: FSMContext):
    await callback.message.answer(_("O'quv kursi haqida fikrlaringiz bo'lsa, shu yerda yozib qoldiring (majburiy emas)"))
    await state.set_state(states.UserStates.six)
    await state.update_data(five=callback_data.id)



@user_router.message(states.UserStates.six)
async def six(message: Message, state: FSMContext):
    await message.answer(_("So'rovnomada qatnashganingiz uchun minnatdormiz!"))
    await state.set_state(states.UserStates.seven)
    await state.update_data(six=message.text)
    new_recod = Score.create()

    


# @user_router.callback_query(states.UserStates.seven)
# async def seven(callback: CallbackQuery, state: FSMContext):
#     await callback.message.answer(_('Sertifikatni yuklab olish'))
    # await state.set_state(states.UserStates.second)