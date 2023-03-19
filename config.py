import dataclasses
from functools import lru_cache

import loguru


@dataclasses.dataclass
class Config:
    print_messages: str
    print_DataUsers_errors: str
    print_SQL_errors: str
    use_sql: str
    host: str
    database: str
    user: str
    password: str
    port: str
    Tg_TOKEN: str
    OpenAi_TOKEN: str

    @property
    @lru_cache()
    def logger(self):
        return loguru.logger

    def __hash__(self):
        return id(self)


def get_from_json(file, sec_file):
    import json
    with open(file) as f, open(sec_file) as sf:
        configs = json.load(f)
        secrets = json.load(sf)
        return Config(**configs, **secrets)


def get_from_yaml(file, sec_file):
    import yaml
    with open(file) as f, open(sec_file) as sf:
        configs = yaml.load(f, yaml.Loader)
        secrets = yaml.load(sf, yaml.Loader)
        return Config(**configs, **secrets)


@lru_cache
def config():
    return get_from_yaml('config.yaml', 'tokens.yaml')
