# Generated by Django 3.0.7 on 2023-05-14 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0005_auto_20230513_1343'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salebill',
            name='time',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
