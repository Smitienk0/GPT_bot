import json


class conf:         # достаем переменные из json 

    def __init__(self):
        config = 0
    # Открываем файл
        with open("config.json", "r") as f:
            config = json.load(f)    
        self.print_messages = config["print_messages"]
        self.print_DataUsers_errors = config["print_DataUsers_errors"]
        self.print_SQL_errors = config["print_SQL_errors"]
        self.use_sql = config["use_sql"]
        self.host = config["host"]
        self.database =config["database"]
        self.user = config["user"]
        self.password = config["password"]
        self.port =config["port"]
        self.Tg_TOKEN = config["Tg_TOKEN"]
        self.OpenAi_TOKEN = config["OpenAi_TOKEN"]
   