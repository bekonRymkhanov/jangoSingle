# Generated by Django 5.1.1 on 2024-11-14 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='SomeName', max_length=255)),
                ('student_id', models.IntegerField()),
                ('dob', models.DateField()),
                ('registration_date', models.DateField(auto_now_add=True)),
            ],
        ),
    ]
