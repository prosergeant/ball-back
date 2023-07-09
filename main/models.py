from django.db import models

class Field(models.Model):
    photo = models.ImageField(upload_to='field_photo', blank=True)
    name    = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phone = models.CharField(verbose_name="Номер", default="+7 (777) 666-55-44", max_length=18)
    time_start = models.TimeField(verbose_name="Начало работы", auto_now=False, auto_now_add=False, blank=True, null=True)
    time_end   = models.TimeField(verbose_name="До", auto_now=False, auto_now_add=False, blank=True, null=True)
    all_time = models.BooleanField(verbose_name=("Круглосуточно"), default=False)
    rating = models.FloatField(default=0.0)
    views = models.IntegerField(verbose_name=("Количество просмотров"), default=0)
    num_phone_see = models.IntegerField(verbose_name=("Сколько раз посмотрели номер"), default=0)
#     tags = models.TextField(verbose_name=("Теги"), blank=True, null=True)
    text = models.TextField(verbose_name=("О клинике"), null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Поле'
        verbose_name_plural = 'Поля'

class Tag(models.Model):
    field = models.ForeignKey("Field", on_delete=models.CASCADE) #,verbose_name=("")
    icon = models.CharField(max_length=100)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.field.name + ' | ' + self.icon
