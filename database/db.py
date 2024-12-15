import logging
# noinspection PyUnresolvedReferences
import cryptography
import aiomysql
import pymysql.err

from config.config import load_config


async def on_startup():
    cnfg = load_config().my_sql
    conn = await aiomysql.connect(host=cnfg.host, port=3128, user=cnfg.user, password=cnfg.password, db=cnfg.db)
    async with conn.cursor() as cur:
        await cur.execute(f"CREATE TABLE IF NOT EXISTS marked_products (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, name VARCHAR(256) NOT NULL, saved_price FLOAT NOT NULL, articul INT NOT NULL, user INT NOT NULL);")
        await conn.commit()
        try:
            await cur.execute("ALTER TABLE marked_products ADD CONSTRAINT unique_product UNIQUE (name, saved_price, articul, user);")
            await conn.commit()
        except pymysql.err.OperationalError:
            logging.warning("Index is already exist!")
    conn.close()


async def add_user(user_id: int):
    cnfg = load_config().my_sql
    conn = await aiomysql.connect(host=cnfg.host, port=3128, user=cnfg.user, password=cnfg.password, db=cnfg.db)
    async with conn.cursor() as cur:
        await cur.execute(f"INSERT IGNORE INTO users SET id = %s;", user_id)
        result = await cur.fetchall()
        await conn.commit()
    conn.close()


async def add_bookmark(user_id: int, name: str, articul: str, price: float):
    cnfg = load_config().my_sql
    conn = await aiomysql.connect(host=cnfg.host, port=3128, user=cnfg.user, password=cnfg.password, db=cnfg.db)
    async with conn.cursor() as cur:
        await cur.execute(f"INSERT IGNORE INTO marked_products SET name = %s, saved_price = %s, articul =  %s, user = %s;", (name, price, articul, user_id))
        result = await cur.fetchall()
        await conn.commit()
    conn.close()


async def get_bookmarks(user_id: str | int) -> tuple:
    cnfg = load_config().my_sql
    conn = await aiomysql.connect(host=cnfg.host, port=3128, user=cnfg.user, password=cnfg.password, db=cnfg.db)
    async with conn.cursor() as cur:
        await cur.execute("SELECT * FROM marked_products WHERE user = %s;", (user_id,))
        result = await cur.fetchall()
    conn.close()
    return result


async def delete_bookmark(user_id, articul):
    cnfg = load_config().my_sql
    conn = await aiomysql.connect(host=cnfg.host, port=3128, user=cnfg.user, password=cnfg.password, db=cnfg.db)
    async with conn.cursor() as cur:
        await cur.execute(
            f"DELETE FROM marked_products WHERE user=%s AND articul=%s;",
            (user_id, articul))
        result = await cur.fetchall()
        await conn.commit()
    conn.close()