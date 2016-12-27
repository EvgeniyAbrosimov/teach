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

    # после завершения обновления БД перенаправляем на заглавную страницу
    return redirect("/")