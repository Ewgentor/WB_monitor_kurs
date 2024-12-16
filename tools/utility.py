import emoji


def find_articul(articul: str, data: list) -> int:
    """
    Поиск артикля в списке со словарями
    :param articul: артикул
    :param data: список со словарями с данными товаров
    :return: индекс
    """
    for i, el in enumerate(data):
        if int(articul) == el['articul']:
            return i


def get_price_emoji(old_price: float, new_price: str) -> str:
    """
    Вывод эмоджи соответствующим изменению цены.
    :param old_price:
    :param new_price:
    :return: эмоджи стрелочки вверх или вниз, либо равно
    """
    new_price = float(new_price[:-2])
    if old_price == new_price:
        return emoji.emojize(':heavy_equals_sign:')
    elif old_price > new_price:
        return emoji.emojize(':down_arrow:')
    else:
        return emoji.emojize(':up_arrow:')

