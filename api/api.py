import requests


def get_data(article: int) -> dict:
    """
    Strips product data by its article

    | code -1 - Wrong article
    | code 0 - Product not found
    | code 1 - Bad response
    | code 2 - OK
    """
    article = str(article)
    if len(article) not in range(7, 10):
        return {"code": -1}
    else:
        params = {'appType': '1', 'curr': 'rub', 'dest': '-5518666', "nm": article}
        r = requests.get('https://card.wb.ru/cards/v2/detail', params=params)
        if r.status_code != 200:
            return {"code": 1}
        else:
            try:
                prod = r.json()["data"]["products"][0]
            except IndexError:
                return {"code": 0}
            return {
                "code": 2,
                "articul": article,
                "brand": prod["brand"],
                "name": prod["name"],
                "supplier": prod["supplier"],
                "price": __get_price(prod),
                "img": __get_img(article=article)
            }


def __get_img(article: str) -> str:
    """
    Inner function for img parsing
    :param article: product article
    :return: img url
    """
    for i in range(1, 21):
        url = (f"https://basket-{str(i).zfill(2)}.wbbasket.ru"
               f"/vol{article[:len(article)-5]}"
               f"/part{article[:len(article)-3]}"
               f"/{article}/images/big/1.webp")
        r = requests.get(url)
        if r.status_code != 404:
            return url


def __get_price(prod: dict) -> str | None:
    """
    Inner function for price parsing
    :param prod: product data
    :return: price
    """
    for i in range(len(prod["sizes"])):
        if "price" in prod["sizes"][i].keys():
            price = "{:.2f}".format(prod["sizes"][i]["price"]["total"]/100) + " ₽"
            return price
    return None


if __name__ == "__main__":
    print(get_data(100258998))
