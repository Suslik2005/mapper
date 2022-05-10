import random

import pygame
import requests
import sys


def show_map(ll_spn=None, map_type="map", add_params=None):
    if ll_spn:
        map_request = f"http://static-maps.yandex.ru/1.x/?{ll_spn}&l={map_type}"
    else:
        map_request = f"http://static-maps.yandex.ru/1.x/?l={map_type}"

    if add_params:
        map_request += "&" + add_params
    response = requests.get(map_request)

    if not response:
        sys.exit(1)

    map_file = "map.png"
    try:
        with open(map_file, "wb") as file:
            file.write(response.content)
    except IOError as ex:
        sys.exit(2)
    pygame.init()
    screen = pygame.display.set_mode((600, 450))
    screen.blit(pygame.image.load(map_file), (0, 0))
    pygame.display.flip()
    while pygame.event.wait().type != pygame.QUIT:
        pass
    pygame.quit()


def get_ll_span(address):
    API_KEY = '40d1649f-0493-4b70-98ba-98533de7710b'
    geocoder_request = f"http://geocode-maps.yandex.ru/1.x/"
    geocoder_params = {
        "apikey": API_KEY,
        "geocode": address,
        "format": "json"}

    # Выполняем запрос.
    response = requests.get(geocoder_request, params=geocoder_params)

    if response:
        # Преобразуем ответ в json-объект
        json_response = response.json()
    else:
        raise RuntimeError(
            "Ошибка выполнения запosa"
        )
    features = json_response["response"]["GeoObjectCollection"]["featureMember"]
    toponym = features[0]["GeoObject"] if features else None

    if not toponym:
        return (None, None)

    # Координаты центра топонима:
    toponym_centre = toponym["Point"]["pos"]
    # Долгота и Широта :
    toponym_longitude, toponym_lattitude = toponym_centre.split(" ")

    # Собираем координаты в параметр ll
    ll = ",".join([toponym_longitude, toponym_lattitude])

    ramka = toponym["boundedBy"]["Envelope"]
    l, b = ramka["lowerCorner"].split(" ")
    r, t = ramka["upperCorner"].split(" ")
    dx = abs(float(l) - float(r)) / 2.0
    dy = abs(float(t) - float(b)) / 2.0
    span = f"{dx},{dy}"

    return ll, span


def main():
    towns = [
        "Ярославль", "Питер",
        "Нижний Новгород",
        "Казань",
        'Москва',
        "Альметьевск",
        "Архангельск",
        "Астрахань"
    ]
    random.shuffle(towns)

    for town in towns:
        print(town)
        # Показываем карту с масштабом, подобранным по заданному объекту.
        ll, spn = get_ll_span(town)
        if random.random() > 0.5:
            spn = "0.001,0.001"
            map_type = "map"
        ll_spn = "ll={ll}&spn={spn}".format(**locals())
        show_map(ll_spn, "sat")


if __name__ == "__main__":
    main()
