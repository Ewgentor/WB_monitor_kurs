from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    token: str  # Токен для доступа к телеграм-боту

@dataclass
class MySql:
    user: str
    password: str
    host: str

@dataclass
class Config:
    tg_bot: TgBot
    my_sql: MySql
    provider_id: str
    shop_article_id: str


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(token=env('BOT_TOKEN')),
        my_sql=MySql(user=env('mySqlUser'), password=env('mySqlPassword'), host=env('mySqlHost')),
        provider_id=env('providerId'),
        shop_article_id=env('shopArticleId')
    )
