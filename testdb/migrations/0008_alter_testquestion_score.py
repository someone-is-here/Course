# Generated by Django 4.0.4 on 2022-06-03 07:20

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testdb', '0007_alter_testquestion_score'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testquestion',
            name='score',
            field=models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(1)]),
        ),
    ]
