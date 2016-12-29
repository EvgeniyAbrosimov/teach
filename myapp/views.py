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

        # --- формируем строку условия(бренд) на языке sql для запроса к БД ---
    chosen_brand = ""
    try:
        chosen_brand = request.POST['brand_checkbox']
    except MultiValueDictKeyError:
        pass

    # ПРОВЕРКА на SQl-иньекцию
    if (chosen_brand.replace(" ", "")).isalpha():
        if (chosen_brand != ""):
            brand_predict = " AND myapp_brand.name = '" + chosen_brand + "'"
        else:
            brand_predict = ""
    else:
        brand_predict = ""

        # --- итоговое условие выборки товаров из БД для оператора WHERE
    where_predict = price_predict + \
                    brand_predict

    # массив выбранных видеокамер
    chosen_cameras = []
    # запрос выборки видеокамер из БД, по условию
    for cam in Camera.objects.raw('''SELECT myapp_camera.id,
        myapp_camera.name AS name,
        myapp_camera.image AS image,
        myapp_brand.name AS prod_brand,
        myapp_camera.description AS description,
        myapp_camera.page AS page,
        myapp_camera.price AS price
        FROM myapp_camera
        JOIN myapp_brand ON myapp_camera.brand_id = myapp_brand.id
        WHERE ''' + where_predict +
                                          ''' ORDER BY price'''):
        chosen_cameras.append([cam.image,
                               cam.name,
                               cam.prod_brand,
                               cam.price,
                               cam.page,
                               cam.description])

    return render(request, 'myapp/main.html', {'chosen_cameras': chosen_cameras,
                                               'brands': brands,
                                               'max_price': max_price})