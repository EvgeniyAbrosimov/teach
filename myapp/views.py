# импортируем метод рендера страниц веб-приложения "myapp"
from django.shortcuts import render
# импортируем обработчик исключения "множественого значения для элемента словаря"
from django.utils.datastructures import MultiValueDictKeyError
# импортируем объекты модели данных (таблицы БД)
from myapp.models import Camera, Brand

# массив брендов для панели выбора бренда
brands = Brand.objects.all()
# максимальная цена товара для панели выбора цены
for price in Camera.objects.raw('''SELECT id, MAX(price) From myapp_camera;'''):
    max_price = price.price

# метод получения данных отображаемых на странице
def main(request):
    # --- формируем строку условия(цена) на языке sql для запроса к БД ---
    chosen_price_min = "0"
    chosen_price_max = str(max_price)
    try:
        chosen_price_min = request.POST['price_min']
    except MultiValueDictKeyError:
        pass
    try:
        chosen_price_max = request.POST['price_max']
    except MultiValueDictKeyError:
        pass

    # ПРОВЕРКА на SQL-иньекцию
    if (chosen_price_min.isnumeric() & chosen_price_max.isnumeric()):
        price_predict = "myapp_camera.price BETWEEN " + chosen_price_min + " AND " + chosen_price_max
    else:
        price_predict = "myapp_camera.price BETWEEN 0 AND " + chosen_price_max
