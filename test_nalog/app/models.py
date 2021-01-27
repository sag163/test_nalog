from django.db import models

# Create your models here.
class Nalog(models.Model):
    request_numbers = models.IntegerField(verbose_name="Запрашиваемый ОГРН/ИНН")
    answer = models.CharField(max_length=300, verbose_name="Ответ")
    date_request = models.DateTimeField("date published", auto_now_add=True)
