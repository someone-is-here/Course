# Generated by Django 4.0.4 on 2022-06-03 06:35

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testdb', '0006_alter_coursetest_amount_of_answers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testquestion',
            name='score',
            field=models.IntegerField(validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(1)]),
        ),
    ]
