import psycopg2

import config

conf = config.config()
logger = conf.logger
# Подключение к базе данных PostgreSQL
with (psycopg2.connect(host=conf.host,
                       database=conf.database,
                       user=conf.user,
                       password=conf.password,
                       port=conf.port
                       ) as conn,
      conn.cursor() as cur):
    # SQL-запрос для создания новой записи
    sql = "INSERT INTO users (user_id) VALUES (%s);"

    try:
        # Выполнение SQL-запроса с передачей параметров
        cur.execute(sql, (123435,))
        # Фиксация изменений в базе данных
        conn.commit()
        logger.info("Запись успешно добавлена!")
    except Exception as e:
        # Если возникла ошибка, откатываем транзакцию
        conn.rollback()
        logger.exception("Ошибка при добавлении записи")
