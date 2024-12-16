import logging
# noinspection PyUnresolvedReferences
import cryptography
import aiomysql
import pymysql.err

from config.config import load_config


async def on_startup():
    """
    Создание таблиц на запуске бота
    :return: None
    """
    cnfg = load_config().my_sql
    conn = await aiomysql.connect(host=cnfg.host, port=3306, user=cnfg.user, password=cnfg.password, db=cnfg.db)
    async with conn.cursor() as cur:
        await cur.execute(f"CREATE TABLE IF NOT EXISTS marked_products (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, name VARCHAR(256) NOT NULL, saved_price FLOAT NOT NULL, articul INT NOT NULL, user INT NOT NULL);")
        await cur.execute(
            f"CREATE TABLE IF NOT EXISTS users (id INT NOT NULL PRIMARY KEY, premium TINYINT DEFAULT 0);")
        await conn.commit()
        try:
            await cur.execute("ALTER TABLE marked_products ADD CONSTRAINT unique_product UNIQUE (name, saved_price, articul, user);")
            await conn.commit()
        except pymysql.err.OperationalError:
            logging.warning("Index is already exist!")
    conn.close()


async def add_user(user_id: int):
    """
    Добавить пользователя базу данных пользователей
    :param user_id: id пользователя
    :return: None
    """
    cnfg = load_config().my_sql
    conn = await aiomysql.connect(host=cnfg.host, port=3306, user=cnfg.user, password=cnfg.password, db=cnfg.db)
    async with conn.cursor() as cur:
        await cur.execute(f"INSERT IGNORE INTO users SET id = %s;", user_id)
        result = await cur.fetchall()
        await conn.commit()
    conn.close()


async def add_bookmark(user_id: int, name: str, articul: str, price: float):
    """
    Добавить закладку в базу данных
    :param user_id: id пользователя
    :param name: Название товара
    :param articul: Артикул товара
    :param price: Цена товара
    :return: None
    """
    cnfg = load_config().my_sql
    conn = await aiomysql.connect(host=cnfg.host, port=3306, user=cnfg.user, password=cnfg.password, db=cnfg.db)
    async with conn.cursor() as cur:
        await cur.execute(f"INSERT IGNORE INTO marked_products SET name = %s, saved_price = %s, articul =  %s, user = %s;", (name, price, articul, user_id))
        result = await cur.fetchall()
        await conn.commit()
    conn.close()


async def get_bookmarks(user_id: str | int) -> tuple:
    """
    Получить закладки из базы данных
    :param user_id: id пользователя
    :return: tuple данными товаров
    """
    cnfg = load_config().my_sql
    conn = await aiomysql.connect(host=cnfg.host, port=3306, user=cnfg.user, password=cnfg.password, db=cnfg.db)
    async with conn.cursor() as cur:
        await cur.execute("SELECT * FROM marked_products WHERE user = %s;", (user_id,))
        result = await cur.fetchall()
    conn.close()
    return result


async def delete_bookmark(user_id: str | int, articul: str | int):
    """
    Удаляет закладку из базы данных
    :param user_id: id пользователя
    :param articul: артикул удаляемого товара
    :return: None
    """
    cnfg = load_config().my_sql
    conn = await aiomysql.connect(host=cnfg.host, port=3306, user=cnfg.user, password=cnfg.password, db=cnfg.db)
    async with conn.cursor() as cur:
        await cur.execute(
            f"DELETE FROM marked_products WHERE user=%s AND articul=%s;",
            (user_id, articul))
        result = await cur.fetchall()
        await conn.commit()
    conn.close()