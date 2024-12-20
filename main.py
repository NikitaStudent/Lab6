from flask import Flask, render_template
import sqlite3
import os

app = Flask(__name__)

# Путь к базе данных
DB_PATH = 'sql_table.db'


# Функция для создания базы данных, если она не существует
def create_database():
    if not os.path.exists(DB_PATH):  # Если файл базы данных не существует
        # Создаем или подключаемся к базе данных
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Создаем таблицу для хранения подарков
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS gifts (
                id INTEGER PRIMARY KEY,
                name TEXT,
                gift TEXT,
                price INTEGER,
                status TEXT
            )
        ''')

        # Заполняем таблицу данными
        gifts = [
            ('Иван Иванович', 'Санки', 2000, 'куплен'),
            ('Ирина Сергеевна', 'Цветы', 3000, 'некуплен'),
            ('Дмитрий Павлович', 'Часы', 1500, 'куплен'),
            ('Анна Викторовна', 'Книга', 500, 'некуплен'),
            ('Елена Борисовна', 'Шарф', 1000, 'куплен'),
            ('Мария Александровна', 'Техника', 8000, 'некуплен'),
            ('Никита Александрович', 'Игрушка', 1500, 'куплен'),
            ('Ольга Вячеславовна', 'Кофеварка', 4500, 'некуплен'),
            ('Алексей Сергеевич', 'Сумка', 2000, 'куплен'),
            ('Татьяна Геннадьевна', 'Кошелек', 1200, 'некуплен')
        ]

        # Вставляем данные в таблицу
        cursor.executemany('INSERT INTO gifts (name, gift, price, status) VALUES (?, ?, ?, ?)', gifts)

        # Сохраняем изменения и закрываем соединение
        conn.commit()
        conn.close()
        print("База данных была создана и заполнена тестовыми данными.")


# Функция для получения данных из базы данных
def get_gifts():
    # Подключаемся к базе данных
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Выполняем запрос
    cursor.execute('SELECT * FROM gifts')
    gifts = cursor.fetchall()

    conn.close()
    return gifts


# Главная страница
@app.route('/')
def index():
    # Проверяем, существует ли база данных, если нет — создаем её
    create_database()

    # Получаем данные о подарках
    gifts = get_gifts()

    # Отображаем данные в шаблоне
    return render_template('index.html', gifts=gifts)


if __name__ == '__main__':
    app.run(debug=True)