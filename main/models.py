import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager

class DefUser(AbstractUser):
    is_owner = models.BooleanField(default=False)

    username   = None
    name       = models.CharField(max_length=255, blank=True, null=True)
    phone      = models.CharField("Номер телефона", max_length=30, unique=True)

    #for simple users
    cashback   = models.IntegerField(verbose_name=("Cashback"), default=0)
    money      = models.IntegerField(verbose_name=("Кошелек"), default=0)
    date_birthday = models.DateField(verbose_name=("Дата рождения"), auto_now=False, auto_now_add=False, blank=True, null=True)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.phone

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

class Field(models.Model):
    photo      = models.ImageField(upload_to='field_photo', blank=True)
    name       = models.CharField(max_length=100)
    address    = models.CharField(max_length=100)
    phone      = models.CharField(verbose_name="Номер", default="+7 (777) 666-55-44", max_length=18)
    time_start = models.TimeField(verbose_name="Начало работы", auto_now=False, auto_now_add=False, blank=True, null=True)
    time_end   = models.TimeField(verbose_name="До", auto_now=False, auto_now_add=False, blank=True, null=True)
    all_time   = models.BooleanField(verbose_name=("Круглосуточно"), default=False)
    rating     = models.FloatField(default=0.0)
    views      = models.IntegerField(verbose_name=("Количество просмотров"), default=0)
    text       = models.TextField(verbose_name=("Описание"), null=True, blank=True)
    num_phone_see = models.IntegerField(verbose_name=("Сколько раз посмотрели номер"), default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Поле'
        verbose_name_plural = 'Поля'


class FieldType(models.Model):
    field = models.ForeignKey("Field", on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    hours = models.IntegerField(verbose_name=("Сколько часов можно играть"), default=1)
    coast = models.IntegerField()

    def __str__(self):
        return self.field.name + ' | ' + self.title


class Request(models.Model):
    field_type = models.ForeignKey("FieldType", on_delete=models.CASCADE)
    user = models.ForeignKey("DefUser", on_delete=models.CASCADE)
    date = models.CharField(max_length=10)
    time = models.CharField(max_length=10)
    duration = models.IntegerField(default=1)
    paid = models.BooleanField(default=False)

    @property
    def is_ended(self):
        current_datetime = datetime.datetime.now()
        current_date = current_datetime.date()
        current_time = current_datetime.time()
        day = current_date.day
        month = current_date.month
        hour = current_time.hour
        minute = current_time.minute

        req_date = list(map(lambda x: int(x), self.date.split('.')) )
        req_day = req_date[0]
        req_month = req_date[1]

        req_time = list(map(lambda x: int(x), self.time.split(':')) )
        req_hour = req_time[0]
        req_minute = req_time[1]

        return day >= req_day and month >= req_month and hour > req_hour

    class Meta:
        unique_together = ['date', 'time']


class Tag(models.Model):
    field = models.ForeignKey("Field", on_delete=models.CASCADE) #,verbose_name=("")
    icon = models.CharField(max_length=100)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.field.name + ' | ' + self.icon
