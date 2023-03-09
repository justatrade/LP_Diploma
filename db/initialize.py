import config
import os
import sqlite3


def create_db():
    """
    Функция для создания базы данных.
    :return:
    """
    try:
        with sqlite3.connect(config.DB_NAME) as db:
            cursor = db.cursor()
            queries = [
                ('CREATE TABLE IF NOT EXISTS users('
                 'user_id INTEGER PRIMARY KEY, '
                 'available_space REAL DEFAULT 20.0, '
                 'is_premium INTEGER DEFAULT 0'
                 ')'
                 ),
                ('CREATE TABLE IF NOT EXISTS files('
                 'id INTEGER PRIMARY KEY AUTOINCREMENT, '
                 'user_id INTEGER, '
                 'full_path TEXT NOT NULL, '
                 'originated_of INTEGER'
                 ')'
                 ),
                # Создаём пользователя по умолчанию для хранения всех снимков неба
                ('INSERT INTO users (user_id, available_space) '
                 'VALUES (1, 150.0)')
                     ]
            for query in queries:
                cursor.execute(query)
            db.commit()
    except sqlite3.Error as e:
        print(e)


def fill_db_space_images():
    """
    Функция заполнения БД снимками космоса с привязкой к техническому пользователю с user_id=1
    :return:
    """
    try:
        with sqlite3.connect(config.DB_NAME) as db:
            cursor = db.cursor()
            img_list = os.listdir(
                os.path.join(config.ROOT_DIR, config.SPACE_IMG_PATH)
            )
            for file in img_list:
                if '_fullres' not in file:
                    full_path = os.path.join(*[
                        config.ROOT_DIR,
                        config.SPACE_IMG_PATH,
                        file
                    ])
                    cursor.execute(
                        f'INSERT INTO files (user_id, full_path) '
                        f'VALUES(1, "{full_path}")'
                    )
            db.commit()
    except sqlite3.Error as e:
        print(e)


if __name__ == '__main__':
    create_db()