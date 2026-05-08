import secrets
from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from transliterate import translit
from django.contrib.auth.models import User

def generate_good_token():
    return secrets.token_hex(3)

# CharField - текстовое поле
# IntegerField - целочисленное поле
# FloatField - дробное поле
# DateField - поле даты

# def images_path():
#     return os.path.join(settings.LOCAL_FILE_DIR, "images")

# def item_description_path():
#     return os.path.join(settings.LOCAL_FILE_DIR, "item_descriptions")

class Item(models.Model):

        
    
    clothing_types = (
        ('headwear', 'головные уборы'),
        ('t-shirt', 'футболка'),
        ('underwear', 'штаны'),
        ('sweater', 'свитера'),
        ('boots', 'ботинки'),
        ('gloves', 'перчатки'),
        ('socks', 'носки'),
    )

    def user_directory_path(instance, filename):
        title = str(translit(value = instance.title, language_code = 'ru', reversed = True))
        return f'goods/{instance.good_token}_{title}/{filename}'


    
    item_title = models.CharField(max_length = 100) # название товара
    price = models.IntegerField() # цена
    # description = models.FilePathField() # описание
    photo = models.ImageField() # фото товара
    material = models.CharField(max_length = 20) # материал
    clothing_type = models.CharField(max_length = 20, choices=clothing_types) # вид одежды
    clothing_color = models.CharField(max_length = 20) # цвет одежды
    clothing_size = models.CharField(max_length = 3) # размер одежды
    gender = models.CharField(max_length = 7) #мужское/женское/унисекс
    care = models.CharField(max_length = 100) #уход за вещами
    dop_info = models.TextField() # доп. информация

    def __str__(self):
        return f'{self.id}. {self.item_title}'
    
class EmailCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=30)