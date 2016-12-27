# импортируем метод рендера страниц веб-приложения "myapp"
from django.shortcuts import render
# импортируем обработчик исключения "множественого значения для элемента словаря"
from django.utils.datastructures import MultiValueDictKeyError
# импортируем объекты модели данных (таблицы БД)
from myapp.models import Camera, Brand

# метод получения данных отображаемых на странице
def main(request):
return render(request, 'myapp/main.html', {})