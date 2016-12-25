from django.db import models

# объект данных "Камера"
class Camera(models.Model):
    name = models.TextField()
    brand = models.ForeignKey('Brand')
    description = models.TextField()
    image = models.TextField()
    page = models.TextField()
    price = models.IntegerField()

# объект данных "Бренд"
class Brand(models.Model):
    name = models.TextField()