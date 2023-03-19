import dataclasses
from typing import Iterable, Sized

import openai

import config

conf = config.config()


def error_print(e):
    if conf.print_DataUsers_errors:
        conf.logger.exception(e)


@dataclasses.dataclass(frozen=True)
class Message(dict):
    role: str
    content: str

    def __len__(self):
        return len(self.content)


class History(Iterable, Sized):
    def __init__(self):
        self._data: list[Message] = []
        self.opened = False
        self.new = 0

    def trim(self, percent: float = 20):
        """
        Удаляет около 20% символов из начала истории сообщений,
         если по одному их удалять то ответ сети прерываться будет
        """
        length = self.size

        aim_length = length * (1 - percent / 100)

        while self.size > aim_length:
            self._data.pop(0)

    @property
    def size(self):
        return sum(map(len, self._data))

    def clear(self):
        self._data.clear()

    def append(self, message: Message):
        if self.opened:
            self._data.append(message)
            self.new += 1
        else:
            raise RuntimeError('Can append messages only in in context manager mode')

    def extend(self, messages: Iterable[Message]):
        if self.opened:
            before = len(self)
            self._data.extend(messages)
            self.new = len(self) - before
        else:
            raise RuntimeError('Can append messages only in in context manager mode')

    def to_primitive(self):
        return list(
            dataclasses.asdict(x) for x in self
        )

    def __len__(self):
        return len(self._data)

    def __iter__(self):
        return iter(self._data)

    def __enter__(self):
        self.opened = True
        self.new = 0
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.opened = False
        if exc_type is not None:
            self._data = self._data[0:-self.new]


class AI:
    openai.api_key = conf.OpenAi_TOKEN

    def __init__(self, obj):
        self.comp = obj

    def generate_response(self, history: History):
        # принимает историю сообщений для того чтобы сеть понимала контекст
        #  она выглядит так
        #  [{"role": "user", "content": mass},      - сообщение пользователя
        #   {"role": "assistant", "content": ret}]  - ответ сети

        # создаеться запрос, в нем указывается подель и история сообщений
        completion = self.comp.create(model="gpt-3.5-turbo",
                                      messages=history.to_primitive())

        return completion.choices[0].message.content  # возвращаем ответ сети


class User:  # тут есть имя - это id чата по сути и история сообщений
    def __init__(self, id: int, ai: AI):
        self.id = id
        self.history = History()
        self.ai = ai

    def send_message(self, text: str) -> str:  # создаем запрос
        message = Message(role="user", content=text)
        with self.history:
            self.history.append(message)
            while True:
                # передаем историю сообщений в сеть,
                # если ошибка из-за числа токенов то удаляем часть сообщений и пробуем заново.
                try:
                    res = self.ai.generate_response(self.history)
                    ans = Message(role="assistant",
                                  content=res)  # если ошибок нет, то добавляем ответ в историю сообщений
                    self.history.append(ans)
                    return res
                except openai.error.InvalidRequestError as e:
                    self.history.trim()  # удаляем часть сообщений
                    continue


class Users:
    def __init__(self):
        self.users: dict[int, User] = {}  # создаем словарь в котором будут пользователи
        try:
            self.ai = AI(openai.ChatCompletion)
        except Exception as e:
            error_print(e)
            raise

    def get_or_create(self, id: int):  # если пользователя с таким именем нет создаем его
        if id not in self.users:
            usr = User(id, self.ai)
            self.users[id] = usr
            if conf.print_messages:
                print(f'add user - ' + str(id))
        return self.users[id]
