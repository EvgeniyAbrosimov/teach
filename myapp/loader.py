# импортируем метод перенаправления
from django.shortcuts import redirect
# импортируем метод запросов к веб-серверам
import requests
# импортируем регулярные выражения, для поиска блоков на странице
import re
# импортируем фреймворк "Замечательного супа"
from bs4 import BeautifulSoup
# импортируем объекты модели данных (таблицы БД)
from myapp.models import Camera, Brand

# метод обновления БД
def load(request):
    # очистка таблиц
    Camera.objects.all().delete() # таблица видеокамер
    Brand.objects.all().delete() # таблица Брендов

    # получаем веб-страницу с перечнем видеокамер
    sobj1 = BeautifulSoup(requests.get('http://www.dns-shop.ru/catalog/17a89cc016404e77/videokamery/').content,
                          "html.parser")

    # Поиск всех брендов на странице
    brands_array = sobj1.find('div', id=re.compile('^checkbox-list-brand-\w+$')).findAll('input', type="checkbox")
    # запись списка брендов в БД
    for b in brands_array:
        Brand(name = b('span')[0].string).save()

    # цикл заполнения таблицы сущности Видеокамера
    for brand in brands_array:
        # сохраняем страницу, результат, для текущего бренда как обьект "BeautifulSoup"
        sobj2 = BeautifulSoup(requests.get('http://www.dns-shop.ru/catalog/17a89cc016404e77/videokamery/?brand='
                                           + str(brand['value']) + '&mode=list').content, "html.parser")

        # парсим массив ссылок на изображения товаров с текущей страницы
        image_list = sobj2.body.findAll(attrs={"class": "popover-content img-popover"})
        # парсим массив наименований товаров с текущей страницы
        name_list = sobj2.body.findAll(attrs={"class": "item-name"})
        # парсим массив цен на товары с текущей страницы
        prod_prices = sobj2.body.findAll(attrs={"class": "price_g"})
        # парсим массив ссылок на страницы товаров с текущей страницы
        prod_pages = sobj2.body.findAll(attrs={"class": "item-name"})
        # определение значения внешнего ключа Бренда
        # (сопоставляем наименование текущего бренда строке, её идентификатору, в таблице брендов БД)
        prod_id = (Brand.objects.get(name=str(brand('span')[0].string))).id

        # цикл перебора страниц товаров для текущего бренда
        for i in range(0, len(prod_pages)):
            # ссылка на страницу текущего товара
            prod_page = "http://www.dns-shop.ru" + prod_pages[i]('a')[0]['href']
            # сохранение страницы товара как объекта "BeautifulSoup"
            sobj3 = BeautifulSoup(requests.get(prod_page).content, "html.parser")
            # парсим описание товара, с его страницы
            description = sobj3.body.find(attrs={"class": "price_item_description"})('p')[0].string

            # сохраняем текущий товар, его атрибуты, как строку таблицы "Camera" БД
            Camera(name = name_list[i]('a')[0].string,
                   brand_id = prod_id,
                   description = description,
                   image = image_list[i]('img')[0]['data-image-desktop'],
                   page = prod_page,
                   price = int((prod_prices[i]('span')[0].string).replace(" ", ""))).save()

    # после завершения обновления БД перенаправляем на заглавную страницу
    return redirect("/")