# Generated by Django 3.2.8 on 2022-04-08 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0003_auto_20220408_1556'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='auth_token',
            field=models.CharField(default='', max_length=300, null=True),
        ),
    ]
