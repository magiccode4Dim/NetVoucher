# Generated by Django 3.2.25 on 2024-06-12 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Pacote', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pacote',
            name='expira_em',
            field=models.CharField(default='0-0-0-0-0-0', max_length=1000),
        ),
    ]
