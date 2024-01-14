import asyncio
import logging
import sys
import config as cfg

from aiogram import Bot, Dispatcher, types , F 
from aiogram.filters import CommandStart , Command
from aiogram.enums import ParseMode

from markups import Markups 
from db_1 import Database
from session_service import SessionService as SS


dp = Dispatcher()
db = Database("sqlite:///db_for_bot.db")

   
bot = Bot(cfg.token)
async def main():
    await dp.start_polling(bot)


@dp.message(Command('start'))
async def start(message: types.Message):
    if message.chat.type == "supergroup" and str(message.chat.id) == cfg.admins_chat_id:
        await bot.send_message(message.chat.id, text = "Приветствую", reply_markup= Markups.builder_admin_start_menu.as_markup())
    else:
        if db.check_status(message.from_user.username) == "Null":
            config = SS(message.from_user.id)
            config.cnt = 6
            config.state = "registering"
            config.user_date = 18
            config.user_disc = "Люлбю Дударчука"
            config.user_interes = "girls"
            config.user_location =  "Тернопіль, Тернопільська область"
            config.user_name = "Андрій"
            config.user_sex = "boy"
            config.user_media = "[id1,id2]"
            try:
                db.add_user_data(config)
                print(db.get_user_data(message.chat.id))
            except:
                pass
            if message.chat.type == "private":
                if not db.user_exists(message.from_user.id):
                    start_command = message.text
                    referrer_id = str(start_command[7:])
                    if str(referrer_id) != "":
                        if str(referrer_id) != str(message.from_user.id):
                            db.add_user(message.from_user.id, referrer_id, message.from_user.username)
                            try:
                                await bot.send_message(referrer_id, "По вашей ссылке зарегистрировался новый пользователь")
                            except:
                                pass
                        else:
                            await message.answer(text= "Вы зарегистрировались по собственой реферальной ссылке")
                            db.add_user(message.from_user.id, username=message.from_user.username)
                    else:
                        db.add_user(message.from_user.id, username=message.from_user.username)
                await message.answer(text= "Hallo Moto", reply_markup= Markups.builder_ref.as_markup())
                if db.check_state(message.from_user.id) == 'registering':
                    print(db.check_state(message.from_user.id))
                    data = db.get_user_data(message.from_user.id)
                    SS.user_id = message.from_user.id
                    await bot.send_photo(cfg.admins_chat_id, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS82pdNfeu2dkFiXsw3JlgilgI-RAl67N2twbqx2ZDDIDRsw8OsxG0a3koKYchFXWzImEI&usqp=CAU",caption= f"{data[3]}\n{data[2]}\n{data[0]}", reply_markup=Markups.builder_admins_user_verificated.as_markup())
                    print("ZAEBUMBA")
        else:
            await message.answer(text= "Вы забанены🤷‍♂️")
           

@dp.callback_query(F.data == "ref")
async def  bot_message(call):
    if db.check_status(call.from_user.username) == "Null":
        await call.message.answer(text = f"Ваша реферальная ссылка:\nhttps://t.me/{cfg.bot_nickname}?start={call.from_user.id}\nКоличество рефералов: {db.count_referrals(call.from_user.id)}")
    else:
            await call.message.answer(text= "Вы забанены🤷‍♂️")


@dp.callback_query(F.data == "admin")
async def admin_panel(call):
    await call.message.answer(text = "Панель администратора", reply_markup= Markups.builder_admin.as_markup())

@dp.callback_query(F.data == "ban")
async def ban(call):
    await call.message.answer(text = "Введите команду и <b>username</b> пользователя\nПример: <b>/ban shark_dog</b>", parse_mode = ParseMode.HTML)

@dp.callback_query(F.data == "unban")
async def unban(call):
    await call.message.answer(text = "Введите команду и <b>username</b> пользователя\nПример: <b>/unban shark_dog</b>", parse_mode = ParseMode.HTML)

@dp.message(Command('ban'))
async def ban_user(message: types.Message):
    if int(message.chat.id) == int(cfg.admins_chat_id):
       if len(message.text) > 4:
            db.ban(message.text[5:])
            await message.answer("Пользователь забанен")

@dp.message(Command('unban'))
async def unban_user(message: types.Message):
    if int(message.chat.id) == int(cfg.admins_chat_id):
        if len(message.text) > 7:
            db.unban(message.text[7:])
            await message.answer("Пользователь разбанен")   

@dp.callback_query(F.data == "verificated")
async def verificate_user(call):
    db.update_state(SS.user_id, "verificated")
    await call.message.answer(text = "Пользователя успешно верифицировано")
    print(call)
    await bot.delete_message(cfg.admins_chat_id, call.message.message_id)

@dp.callback_query(F.data == "decline")
async def decline_user(call):
    db.update_state(SS.user_id, "decline")
    await call.message.answer(text = "Верификация пользователя отклонена")
    await bot.delete_message(cfg.admins_chat_id, call.message.message_id)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Bot Stoped!")