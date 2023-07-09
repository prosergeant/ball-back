# Generated by Django 4.2.3 on 2023-07-09 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Field',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(blank=True, upload_to='field_photo')),
                ('name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=100)),
                ('phone', models.CharField(default='+7 (777) 666-55-44', max_length=18, verbose_name='Номер')),
                ('time_start', models.TimeField(blank=True, null=True, verbose_name='Начало работы')),
                ('time_end', models.TimeField(blank=True, null=True, verbose_name='До')),
                ('all_time', models.BooleanField(default=False, verbose_name='Круглосуточно')),
                ('rating', models.FloatField(default=0.0)),
                ('views', models.IntegerField(default=0, verbose_name='Количество просмотров')),
                ('num_phone_see', models.IntegerField(default=0, verbose_name='Сколько раз посмотрели номер')),
                ('text', models.TextField(blank=True, null=True, verbose_name='О клинике')),
            ],
            options={
                'verbose_name': 'Центр',
                'verbose_name_plural': 'Центры',
            },
        ),
    ]
