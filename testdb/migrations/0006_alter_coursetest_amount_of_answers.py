# Generated by Django 4.0.4 on 2022-06-02 22:40

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testdb', '0005_remove_testquestion_amount_of_answers_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursetest',
            name='amount_of_answers',
            field=models.IntegerField(validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(1)]),
        ),
    ]
