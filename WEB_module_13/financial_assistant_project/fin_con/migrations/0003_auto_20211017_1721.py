# Generated by Django 3.2.8 on 2021-10-17 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fin_con', '0002_auto_20211016_2000'),
    ]

    operations = [
        migrations.AlterField(
            model_name='income',
            name='comment',
            field=models.TextField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='spending',
            name='category',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='spending',
            name='expenses_comment',
            field=models.TextField(blank=True, max_length=200),
        ),
    ]
