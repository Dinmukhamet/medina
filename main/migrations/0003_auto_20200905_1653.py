# Generated by Django 2.2 on 2020-09-05 16:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20200905_1652'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usertoprojects',
            old_name='users',
            new_name='user',
        ),
    ]
