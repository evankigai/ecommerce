# Generated by Django 3.0.8 on 2020-09-10 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_kind_dn'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kind',
            name='dn',
            field=models.IntegerField(default=1),
        ),
    ]
