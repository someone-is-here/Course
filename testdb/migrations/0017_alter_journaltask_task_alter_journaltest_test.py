# Generated by Django 4.0.4 on 2022-06-26 19:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('testdb', '0016_journaltest_journaltask'),
    ]

    operations = [
        migrations.AlterField(
            model_name='journaltask',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='testdb.task'),
        ),
        migrations.AlterField(
            model_name='journaltest',
            name='test',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='testdb.coursetest'),
        ),
    ]
