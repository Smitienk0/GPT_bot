import psycopg2
import config

conf = config.conf()      
# Подключение к базе данных PostgreSQL
conn = psycopg2.connect(
    host=conf.host,
    database=conf.database,
    user=conf.user,
    password=conf.password,
    port=conf.port
    )

# Создание курсора
cur = conn.cursor()

# SQL-запрос для создания новой записи
sql = "INSERT INTO users (user_id) VALUES (%s);" 

try:
    # Выполнение SQL-запроса с передачей параметров
    cur.execute(sql, (123435,))
    # Фиксация изменений в базе данных
    conn.commit()
    print("Запись успешно добавлена!")
except Exception as e:
    # Если возникла ошибка, откатываем транзакцию
    conn.rollback()
    print("Ошибка при добавлении записи:", e)

# Закрытие курсора и соединения с базой данных
cur.close()
conn.close()
