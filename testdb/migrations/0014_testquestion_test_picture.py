# Generated by Django 4.0.4 on 2022-06-20 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testdb', '0013_alter_testanswer_answer'),
    ]

    operations = [
        migrations.AddField(
            model_name='testquestion',
            name='test_picture',
            field=models.ImageField(blank=True, null=True, upload_to='test_pictures/%Y/%m/%d/'),
        ),
    ]
