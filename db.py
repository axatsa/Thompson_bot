import sqlite3



# Подключение к базе данных
def connect_db():
    return sqlite3.connect('expenses.db')


# Создание таблицы для пользователей
def create_users_table():
    conn = connect_db()
    with conn:
        conn.execute("""  
            CREATE TABLE IF NOT EXISTS users (  
                id INTEGER PRIMARY KEY,  
                username TEXT UNIQUE NOT NULL,  
                role TEXT NOT NULL  
            )  
        """)


# Создание таблицы для расходов
def create_expenses_table():
    conn = connect_db()
    with conn:
        conn.execute("""  
            CREATE TABLE IF NOT EXISTS expenses (  
                id INTEGER PRIMARY KEY AUTOINCREMENT,  
                user_id INTEGER NOT NULL,  
                amount DECIMAL(10, 2) NOT NULL,  
                description TEXT,  
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )  
        """)


# Создание таблицы для администраторов
def create_admins_table():
    conn = connect_db()
    with conn:
        conn.execute("""  
            CREATE TABLE IF NOT EXISTS admins (  
                id INTEGER PRIMARY KEY,  
                user_id INTEGER NOT NULL UNIQUE  
            )  
        """)


# Инициализация таблиц
create_users_table()
create_expenses_table()
create_admins_table()


def add_user(user_id, username, role):
    conn = connect_db()
    with conn:
        conn.execute("INSERT INTO users (id, username, role) VALUES (?, ?, ?)", (user_id, username, role))


def get_user_id(user_id):
    conn = connect_db()
    with conn:
        cursor = conn.execute("SELECT id FROM users WHERE id = ?", (user_id,))
        return cursor.fetchone()


def add_expense(user_id, amount, description):
    conn = connect_db()
    with conn:
        conn.execute("INSERT INTO expenses (user_id, amount, description) VALUES (?, ?, ?)",
                     (user_id, amount, description))


def get_expenses(user_id):
    conn = connect_db()
    with conn:
        cursor = conn.execute("SELECT id, amount, description, created_at FROM expenses WHERE user_id = ?", (user_id,))
        return cursor.fetchall()


def set_admin(user_id):
    conn = connect_db()
    with conn:
        conn.execute("INSERT INTO admins (user_id) VALUES (?)", (user_id,))


def is_admin(user_id):
    conn = connect_db()
    with conn:
        cursor = conn.execute("SELECT id FROM admins WHERE user_id = ?", (user_id,))
        return cursor.fetchone() is not None


def get_all_users():
    conn = connect_db()
    with conn:
        cursor = conn.execute("SELECT id, username FROM users")
        return cursor.fetchall()


# Функция для получения общей суммы расходов пользователя
def get_total_expense(user_id):
    conn = connect_db()
    with conn:
        total = conn.execute("SELECT SUM(amount) FROM expenses WHERE user_id = ?", (user_id,)).fetchone()
        return total[0] if total[0] else 0


# Функция для получения общей суммы расходов всех пользователей
def get_total_expense_for_all():
    conn = connect_db()
    with conn:
        total = conn.execute("SELECT SUM(amount) FROM expenses").fetchone()
        return total[0] if total[0] else 0


# Функция для удаления расхода
def delete_expense(expense_id):
    conn = connect_db()
    with conn:
        conn.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
