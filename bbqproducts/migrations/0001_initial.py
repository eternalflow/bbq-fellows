# Generated by Django 2.0.3 on 2018-03-20 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BBQProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_name', models.CharField(default='meat', max_length=20)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
    ]
