import telebot
import logging
from telebot import types
from db import add_user, get_user_id, add_expense, get_expenses, get_total_expense, set_admin, is_admin, \
    get_all_users, get_total_expense_for_all, delete_expense

import threading

# Настройка логирования
logging.basicConfig(
    filename='bot_errors.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s',
)

ADMIN_PASSWORD = 'password'


def start_bot(bot_token):
    bot = telebot.TeleBot(bot_token)

    @bot.message_handler(commands=['start'])
    def handle_start(message):
        user_id = message.chat.id
        username = message.from_user.username
        if get_user_id(user_id) is None:
            add_user(user_id, username, 'user')
        show_main_menu(message.chat.id)

    @bot.message_handler(commands=['set_admin'])
    def handle_set_admin(message):
        bot.send_message(message.chat.id, "Введите пароль для установки администратора:")
        bot.register_next_step_handler(message, process_set_admin)

    def process_set_admin(message):
        if message.text == ADMIN_PASSWORD:
            user_id = message.chat.id
            set_admin(user_id)
            bot.send_message(message.chat.id, "Вы успешно стали администратором!")
        else:
            bot.send_message(message.chat.id, "Неправильный пароль.")
        show_main_menu(message.chat.id)

    @bot.message_handler(commands=['add_expense'])
    def handle_add_expense(message):
        bot.send_message(message.chat.id, "Введите сумму расхода:")
        bot.register_next_step_handler(message, process_amount)

    def process_amount(message):
        try:
            amount = float(message.text.replace(',', '.'))
            bot.send_message(message.chat.id, "Цель расхода:")
            bot.register_next_step_handler(message, lambda msg: save_expense(msg, amount))
        except ValueError:
            bot.send_message(message.chat.id, "Пожалуйста, введите корректную сумму.")
            show_main_menu(message.chat.id)

    def save_expense(message, amount):
        description = message.text
        user_id = message.chat.id
        if get_user_id(user_id) is None:
            bot.send_message(message.chat.id, "Пользователь не найден, добавьте пользователя.")
            show_main_menu(message.chat.id)
            return

        add_expense(user_id, amount, description)
        bot.send_message(message.chat.id, "Расход успешно добавлен!")
        show_main_menu(message.chat.id)

    @bot.message_handler(commands=['view_expenses'])
    def handle_view_expenses(message):
        user_id = message.chat.id
        expenses = get_expenses(user_id)
        if not expenses:
            bot.send_message(message.chat.id, "У вас нет записанных расходов.")
        else:
            response = "Ваши расходы:\n"
            for expense in expenses:
                response += f"ID: {expense[0]}, Сумма: {expense[1]:.2f}, Описание: {expense[2]}\n\n"
            bot.send_message(message.chat.id, response.strip())
        show_main_menu(message.chat.id)

    @bot.message_handler(commands=['total'])
    def handle_total(message):
        user_id = message.chat.id
        total_expense = get_total_expense(user_id)
        bot.send_message(message.chat.id, f"Ваш общий расход: {total_expense:.2f} сум.")
        show_main_menu(message.chat.id)

    @bot.message_handler(commands=['admin_total'])
    def handle_admin_total(message):
        user_id = message.chat.id
        if is_admin(user_id):
            users = get_all_users()
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

            # Формируем строки с пользователями в два ряда
            user_rows = []
            for i in range(0, len(users), 2):
                row = []
                if i < len(users):
                    row.append(users[i][1])  # Добавляем имя пользователя
                if i + 1 < len(users):
                    row.append(users[i + 1][1])  # Добавляем имя следующего пользователя, если он есть
                user_rows.append(row)

            # Создаем кнопки для каждого ряда
            for row in user_rows:
                markup.add(*[types.KeyboardButton(username) for username in row])

            bot.send_message(message.chat.id, "Выберите пользователя для просмотра общего расхода:",
                             reply_markup=markup)
            bot.register_next_step_handler(message, lambda msg: admin_view_user_total(msg, users))
        else:
            bot.send_message(message.chat.id, "У вас нет прав администратора.")
            show_main_menu(message.chat.id)

    def admin_view_user_total(message, users):
        selected_username = message.text
        user_id = next((user[0] for user in users if user[1] == selected_username), None)

        if user_id:
            total_expense = get_total_expense(user_id)
            bot.send_message(message.chat.id,
                             f"Общий расход пользователя {selected_username}: {total_expense:.2f} сум.")
        else:
            bot.send_message(message.chat.id, "Пользователь не найден.")

        show_main_menu(message.chat.id)

    @bot.message_handler(commands=['total_all'])
    def handle_total_all(message):
        user_id = message.chat.id
        if is_admin(user_id):
            total = get_total_expense_for_all()
            bot.send_message(message.chat.id, f"Общий расход всех пользователей: {total:.2f} сум.")
        else:
            bot.send_message(message.chat.id, "У вас нет прав администратора.")
        show_main_menu(message.chat.id)

    @bot.message_handler(commands=['delete_expense'])
    def handle_delete_expense(message):
        user_id = message.chat.id
        expenses = get_expenses(user_id)
        if not expenses:
            bot.send_message(message.chat.id, "У вас нет расходов для удаления.")
            show_main_menu(message.chat.id)
            return

        markup = types.InlineKeyboardMarkup()
        for expense in expenses:
            markup.add(types.InlineKeyboardButton(f"ID: {expense[0]}, Сумма: {expense[1]}, Описание: {expense[2]}",
                                                  callback_data=f"del_{expense[0]}"))

        bot.send_message(message.chat.id, "Выберите расход для удаления:", reply_markup=markup)

    @bot.callback_query_handler(func=lambda call: call.data.startswith("del_"))
    def callback_delete_expense(call):
        expense_id = int(call.data.split("_")[1])
        delete_expense(expense_id)
        bot.answer_callback_query(call.id, "Расход удалён.")
        bot.send_message(call.message.chat.id, "Расход успешно удалён!")
        show_main_menu(call.message.chat.id)

    def show_main_menu(chat_id):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add('Добавить расход', 'Просмотр расходов', 'Итог', 'Удалить расход')
        if is_admin(chat_id):
            markup.add('Итог для всех')
        bot.send_message(chat_id, "Выберите действие:", reply_markup=markup)

    @bot.message_handler(func=lambda message: True)
    def handle_buttons(message):
        if message.text == 'Добавить расход':
            handle_add_expense(message)
        elif message.text == 'Просмотр расходов':
            handle_view_expenses(message)
        elif message.text == 'Итог':
            handle_total(message)
        elif message.text == 'Итог для всех':
            handle_admin_total(message)
        elif message.text == 'Удалить расход':
            handle_delete_expense(message)
        else:
            bot.send_message(message.chat.id, "Неизвестная команда.")
            show_main_menu(message.chat.id)

    try:
        bot.polling(none_stop=True)
    except Exception as e:
        logging.error(f"Ошибка запуска бота с токеном {bot_token}: {e}")


if __name__ == '__main__':
    bot_tokens = ['7977052018:AAF42h_ov_dpybta-rWvJ7FklVF4RnPFHxo',#t.me/thompson1_bot
                  '7829645217:AAGJJr90Q1ipUWY5v_YRdMl9307jOVxRaAY',#t.me/Topmson_bot
                  '7117073240:AAG_eYpk6FPy-NLB9cCERmFSjPSdFTtYsXY']#https://t.me/lkjhgy_bot

    threads = []
    for token in bot_tokens:
        thread = threading.Thread(target=start_bot, args=(token,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
