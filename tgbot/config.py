from dataclasses import dataclass

from environs import Env


@dataclass
class Redis:
    host: str
    port: int


@dataclass
class TgBot:
    token: str

@dataclass
class ParserApi:
    tm_api: str


@dataclass
class Config:
    tg_bot: TgBot
    redis: Redis
    parsers_api: ParserApi


def load_config(path: str = None):
    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env.str("BOT_TOKEN")
        ),
        redis=Redis(
            host=env.str('REDIS_HOST'),
            port=env.str('REDIS_PORT')
        ),
        parsers_api=ParserApi(
            tm_api=env.str('TM_API_KEY')
        )
    )
