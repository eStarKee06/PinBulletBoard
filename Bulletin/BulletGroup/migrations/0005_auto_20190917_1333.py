# Generated by Django 2.2.4 on 2019-09-17 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BulletGroup', '0004_auto_20190913_1343'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='pseudoName',
            field=models.CharField(max_length=20),
        ),
    ]
