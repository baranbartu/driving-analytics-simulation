# Generated by Django 3.0.6 on 2020-05-24 22:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DummyTrip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('operator_name', models.CharField(max_length=255)),
                ('polyline', models.TextField()),
                ('shuttle_identifier', models.CharField(max_length=255)),
            ],
        ),
    ]
