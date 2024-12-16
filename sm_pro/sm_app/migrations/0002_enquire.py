# Generated by Django 5.1.3 on 2024-12-16 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sm_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Enquire',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('email', models.EmailField(max_length=254)),
                ('product', models.TextField()),
                ('brand', models.TextField()),
                ('enq', models.TextField()),
                ('Phone', models.IntegerField()),
            ],
        ),
    ]
