# Generated by Django 4.1.3 on 2023-06-07 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Imadmin', '0004_hack'),
    ]

    operations = [
        migrations.CreateModel(
            name='Announce',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='Announcement', max_length=50)),
                ('text', models.CharField(max_length=200)),
            ],
        ),
    ]
