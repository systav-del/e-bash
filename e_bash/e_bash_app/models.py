import os
from django.db import models
from django.conf import settings

# CharField - текстовое поле
# IntegerField - целочисленное поле
# FloatField - дробное поле
# DateField - поле даты

# def images_path():
#     return os.path.join(settings.LOCAL_FILE_DIR, "images")

# def item_description_path():
#     return os.path.join(settings.LOCAL_FILE_DIR, "item_descriptions")

def _str_(self):
    return self_item_titele

class Item(models.Model):
    item_title = models.CharField(max_length = 100) # название товара
    price = models.IntegerField() # цена
    # description = models.FilePathField() # описание
    photo = models.ImageField() # фото товара
    material = models.CharField(max_length = 20) # материал
    clothing_type = models.CharField(max_length = 20) # вид одежды
    clothing_color = models.CharField(max_length = 20) # цвет одежды
    clothing_size = models.CharField(max_length = 3) # размер одежды
    gender = models.CharField(max_length = 7) #мужское/женское/унисекс
    care = models.CharField(max_length = 100) #уход за вещами
    dop_info = models.TextField() # доп. информация

    def __str__(self):
        return self.item_title
