import asyncio
import logging
import sys
import config as cfg

from aiogram import Bot, Dispatcher, types , F 
from aiogram.filters import CommandStart , Command
from aiogram.enums import ParseMode

from markups import Markups 
from db_1 import Database

dp = Dispatcher()
db = Database("sqlite:///db_for_bot.db")

   
bot = Bot(cfg.token)
async def main():
    await dp.start_polling(bot)


@dp.message(Command('start'))
async def start(message: types.Message):
    if db.check_status(message.from_user.username) == "Null":
        try:
            db.add_user_data(message.from_user.id, 6, "registering", 1065819600.0, "Старий Хуй маринований", "girls", "Тернопіль, Тернопільська область", "Shpintal",  "boy", "id1,id2" )
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
    else:
        await message.answer(text= "Вы забанены🤷‍♂️")
            

@dp.callback_query(F.data == "ref")
async def  bot_message(call):
    await call.message.answer(text = f"Ваша реферальная ссылка:\nhttps://t.me/{cfg.bot_nickname}?start={call.from_user.id}\nКоличество рефералов: {db.count_referrals(call.from_user.id)}")


@dp.message(Command('admin'))
async def admin_panel(message: types.Message):
    if int(message.from_user.id) == int(cfg.admin_id):
        await message.answer(text = "Панель администратора", reply_markup= Markups.builder_admin.as_markup())

@dp.callback_query(F.data == "ban")
async def ban(call):
    await call.message.answer(text = "Введите команду и <b>username</b> пользователя\nПример: <b>/ban shark_dog</b>", parse_mode = ParseMode.HTML)

@dp.callback_query(F.data == "unban")
async def unban(call):
    await call.message.answer(text = "Введите команду и <b>username</b> пользователя\nПример: <b>/unban shark_dog</b>", parse_mode = ParseMode.HTML)

@dp.message(Command('ban'))
async def ban_user(message: types.Message):
    if int(message.from_user.id) == int(cfg.admin_id):
       if len(message.text) > 4:
            db.ban(message.text[5:])
            await message.answer("Пользователь забанен")

@dp.message(Command('unban'))
async def unban_user(message: types.Message):
    if int(message.from_user.id) == int(cfg.admin_id):
        if len(message.text) > 7:
            db.unban(message.text[7:])
            await message.answer("Пользователь разбанен")   

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Bot Stoped!")