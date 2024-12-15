import emoji


def find_articul(articul: str, data: list) -> int:
    for i, el in enumerate(data):
        if int(articul) == el['articul']:
            return i


def get_price_emoji(old_price: float, new_price: str):
    new_price = float(new_price[:-2])
    if old_price == new_price:
        return emoji.emojize(':heavy_equals_sign:')
    elif old_price > new_price:
        return emoji.emojize(':down_arrow:')
    else:
        return emoji.emojize(':up_arrow:')

