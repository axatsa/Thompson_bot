from telebot import types

#
# def main_menu():
#     markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     btn_admin = types.KeyboardButton("Я админ")
#     btn_employee = types.KeyboardButton("Я сотрудник")
#     markup.add(btn_admin, btn_employee)
#     return markup
#
#
# def admin_menu():
#     markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     btn_create_group = types.KeyboardButton("Создать группу")
#     btn_total_expenses = types.KeyboardButton("Итог")
#     btn_add_expense = types.KeyboardButton("Добавить расход")
#     btn_modify_expense = types.KeyboardButton("Изменить расход")
#     btn_delete_expense = types.KeyboardButton("Удалить расход")
#     markup.add(btn_create_group, btn_total_expenses, btn_add_expense, btn_modify_expense, btn_delete_expense)
#     return markup
#
#
# def employee_menu():
#     markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     btn_add_expense = types.KeyboardButton("Добавить расход")
#     btn_modify_expense = types.KeyboardButton("Изменить расход")
#     btn_delete_expense = types.KeyboardButton("Удалить расход")
#     btn_total_expenses = types.KeyboardButton("Итог")
#     markup.add(btn_add_expense, btn_modify_expense, btn_delete_expense, btn_total_expenses)
#     return markup

from telebot import types


def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_admin = types.KeyboardButton("Я админ")
    btn_employee = types.KeyboardButton("Я сотрудник")
    markup.add(btn_admin, btn_employee)
    return markup


def admin_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_create_group = types.KeyboardButton("Создать группу")
    btn_total_expenses = types.KeyboardButton("Итог")
    btn_add_expense = types.KeyboardButton("Добавить расход")
    btn_modify_expense = types.KeyboardButton("Изменить расход")
    btn_delete_expense = types.KeyboardButton("Удалить расход")
    markup.add(btn_create_group, btn_total_expenses, btn_add_expense, btn_modify_expense, btn_delete_expense)
    return markup


def employee_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_add_expense = types.KeyboardButton("Добавить расход")
    btn_modify_expense = types.KeyboardButton("Изменить расход")
    btn_delete_expense = types.KeyboardButton("Удалить расход")
    btn_total_expenses = types.KeyboardButton("Итог")
    markup.add(btn_add_expense, btn_modify_expense, btn_delete_expense, btn_total_expenses)
    return markup
