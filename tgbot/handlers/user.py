from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, BufferedInputFile
from tgbot.keyboards.inline import score_keyboard, language_keyboard, Factories, continue_step
from tgbot.misc import states as states
from tgbot.misc.states import i18nn as _
from tgbot.services.db import Score
import re
from tgbot.services import api as api

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
    data = await state.get_data()
    await callback.message.edit_text(_("Sertifikatni yuklab olish uchun quyidagi so'rovnomani to'ldiring.", locale=data['language']))
    await callback.message.answer(_('Universitet professor-o\'qituvchisini baholang\n(Suv tejovchi texnologiyalarning afzalliklari va ularni samaradorligi)', locale=data['language']), reply_markup=await score_keyboard(1))
    await state.set_state(states.UserStates.first)
    await state.update_data(language=callback_data.language)


@user_router.callback_query(states.UserStates.first, Factories.Score.filter())
async def first_step(callback: CallbackQuery, callback_data: Factories.Score, state: FSMContext):
    data = await state.get_data()
    await callback.message.edit_text(_("Turk mutaxassisini baholang\n(Zamonaviy sug'orish tizimining ahamiyati va suvdan foydalanish madaniyati)", locale=data['language']), reply_markup=await score_keyboard(2))
    await state.set_state(states.UserStates.second)
    await state.update_data(first=callback_data.id)



@user_router.callback_query(states.UserStates.second, Factories.Score.filter())
async def second(callback: CallbackQuery, callback_data: Factories.Score, state: FSMContext):
    data = await state.get_data()
    await callback.message.edit_text(_("Bank mutaxassisini baholang\n(Iqtisodiy va huquqiy savodxonlik: subsidiya, kafilliklar, soliq imtiyozlari va bank kreditlari)", locale=data['language']), reply_markup=await score_keyboard(3))
    await state.set_state(states.UserStates.third)
    await state.update_data(second=callback_data.id)



@user_router.callback_query(states.UserStates.third, Factories.Score.filter())
async def third(callback: CallbackQuery, callback_data: Factories.Score, state: FSMContext):
    data = await state.get_data()
    await callback.message.edit_text(_("Suv xo'jaligi vazirligi mutaxassisini baholang\n(Iqtisodiy va huquqiy savodxonlik: subsidiya, kafilliklar, soliq imtiyozlari va bank kreditlari)", locale=data['language']), reply_markup=await score_keyboard(4))
    await state.set_state(states.UserStates.four)
    await state.update_data(third=callback_data.id)



@user_router.callback_query(states.UserStates.four, Factories.Score.filter())
async def four(callback: CallbackQuery, callback_data: Factories.Score, state: FSMContext):
    data = await state.get_data()
    await callback.message.edit_text(_("O'quv kursi tashkiliy jarayonlarini baholang\n(o'quv materiallari, esdalik sovg'alar, tushlik va boshqalar)", locale=data['language']), reply_markup=await score_keyboard(5))
    await state.set_state(states.UserStates.five)
    await state.update_data(four=callback_data.id)



@user_router.callback_query(states.UserStates.five, Factories.Score.filter())
async def five(callback: CallbackQuery, callback_data: Factories.Score, state: FSMContext):
    data = await state.get_data()
    await callback.message.edit_text(_("O'quv kursi haqida fikrlaringiz bo'lsa, shu yerda yozib qoldiring (majburiy emas)", locale=data['language']), reply_markup=await continue_step(data['language']))
    await state.set_state(states.UserStates.six)
    await state.update_data(five=callback_data.id)



@user_router.message(states.UserStates.six)
async def six(message: Message, state: FSMContext):
    data = await state.get_data()
    await message.answer(_("So'rovnomada qatnashganingiz uchun minnatdormiz!\nSertifikatni yuklab olish uchun id raqamingizni kiriting", locale=data['language']))
    await state.set_state(states.UserStates.seven)
    await state.update_data(six=message.text)
    # new_recod = Score.create()

@user_router.callback_query(states.UserStates.six)
async def sixdotone(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await callback.message.answer(_("So'rovnomada qatnashganingiz uchun minnatdormiz!\nSertifikatni yuklab olish uchun id raqamingizni kiriting", locale=data['language']))
    await state.set_state(states.UserStates.seven)
    await state.update_data(six='None')

    


@user_router.message(states.UserStates.seven)
async def seven(message: Message, state: FSMContext):
    data = await state.get_data()

    digits_regexp = r'^\d+$'
    if re.match(digits_regexp, message.text):
        data = await state.get_data()

        wait = await message.answer(text=_('⏳ Yuklanmoqda, kutib turing...', locale=data.get("language")))
        request = await api.certificate_download(message.text)
        if request:
            await message.answer_document(
                document=BufferedInputFile(
                    request,
                    filename="certificate-{cert_id}.pdf".format(cert_id=message.text),
                )
            )
            Score.create(
                first=data['first'],
                second=data['second'],
                third=data['third'],
                four=data['four'],
                five=data['five'],
                six=data['six'],
                cert_id=message.text,
            )
            await message.answer(_('Boshqa sertifikat yuklash uchun /start komandasini yozing va so\'rovnomani qayta to\'ldiring', locale=data['language']))

            await state.clear()

        else:
            await message.answer(
                _(
                    "❔ ID notog'ri kiritildi yoki kurs hali yakunlanmagan\n⏳ Kurs yakunlanganidan so‘ng sertifikatingizni yuklab olishingiz mumkin",
                    locale=data.get("language"),
                )
            )

        # await bot.delete_message(chat_id=message.from_user.id, message_id=wait.message_id)
        await wait.delete()

    else:
        await message.answer(_('ID raqami faqat sonlardan iborat bo\'lishi kerak! Iltimos, tekshirib qayta kiritng.', locale=data['language']))    