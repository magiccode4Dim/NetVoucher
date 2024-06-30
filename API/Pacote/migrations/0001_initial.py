# Generated by Django 3.2.25 on 2024-06-30 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pacote',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nome', models.CharField(default='', max_length=100)),
                ('script', models.CharField(default='', max_length=700)),
                ('expira_em', models.CharField(default='0-0-0-0-0-0', max_length=1000)),
                ('device_limit', models.IntegerField(default=1)),
            ],
        ),
    ]
