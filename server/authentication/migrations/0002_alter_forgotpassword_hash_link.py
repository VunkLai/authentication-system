# Generated by Django 4.0.5 on 2022-07-01 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forgotpassword',
            name='hash_link',
            field=models.CharField(max_length=64, unique=True),
        ),
    ]
