# Generated by Django 3.0.7 on 2023-05-12 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30, unique=True)),
                ('quantity', models.IntegerField(default=1)),
                ('is_deleted', models.BooleanField(default=False)),
            ],
        ),
    ]
