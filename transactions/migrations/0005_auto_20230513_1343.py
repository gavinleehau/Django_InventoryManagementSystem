# Generated by Django 3.0.7 on 2023-05-13 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0004_auto_20230513_1340'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salebill',
            name='time',
            field=models.DateTimeField(null=True),
        ),
    ]
