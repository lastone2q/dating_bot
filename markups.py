from aiogram.utils.keyboard import InlineKeyboardBuilder

class Markups():
    builder_ref = InlineKeyboardBuilder()
    builder_ref.button(text = "Запросить реферала", callback_data= "ref")
    builder_ref.adjust(1)

    builder_admin = InlineKeyboardBuilder()
    builder_admin.button(text= "Забанить пользователя", callback_data="ban")
    builder_admin.button(text= "Разбанить пользователя", callback_data="unban") 
    builder_admin.adjust(1)

    builder_admin_start_menu = InlineKeyboardBuilder()
    builder_admin_start_menu.button(text = "Панель администратора", callback_data= "admin")

    builder_admins_user_verificated = InlineKeyboardBuilder()
    builder_admins_user_verificated.button(text = "Верифицировать", callback_data= f"verificated")
    builder_admins_user_verificated.button(text = "Отклонить", callback_data= "decline")