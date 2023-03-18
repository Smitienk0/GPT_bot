import sqlite3

class SQLiteData:
    def __init__(self, db_path):
        try:
            self.db_path = db_path
            self.conn = sqlite3.connect(db_path)
            self.cursor = self.conn.cursor()
        except:
            self.cursor = None
            print("Error connecting to database")
        
    def query(self, sql_query):
        print(sql_query)
        if self.cursor is not None:
            try:
                
                self.cursor.execute(sql_query)
                data = self.cursor.fetchall()
                self.conn.commit()
                if len(data) == 0:
                    return 0
                else:
                    columns = [col[0] for col in self.cursor.description]
                    results = []
                    for row in data:
                        result = {}
                        for i, column in enumerate(columns):
                            result[column] = row[i]
                        results.append(result)
                    return results
            except Exception as e:
                print('sql error is', e)
                return 1
        else:
            print("sql error is not None")
            return 1
    

    def save(self, table_name, data):
        if not isinstance(data, list) or len(data) == 0:
            return 0
        
        try:
            # Извлекаем названия столбцов из первого словаря массива data
            columns = list(data[0].keys())
            # Формируем SQL-запрос на добавление данных в таблицу с названием table_name и значениями из массива data
            sql_query = f"INSERT INTO {table_name} ({','.join(columns)}) VALUES ({','.join(['?' for _ in columns])})"
            # Используем executemany, чтобы добавить несколько строк данных за один раз
            self.cursor.executemany(sql_query, [list(row.values()) for row in data])
            # Сохраняем изменения в базу
            self.conn.commit()
            return 0
        except:
            return 1