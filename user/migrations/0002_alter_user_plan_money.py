# Generated by Django 4.1.3 on 2022-11-04 00:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='plan_money',
            field=models.IntegerField(),
        ),
    ]