# Generated by Django 3.0.8 on 2020-08-22 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pdfupload',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pdf', models.FileField(upload_to='')),
                ('bankname', models.CharField(max_length=50)),
                ('actype', models.CharField(max_length=50)),
            ],
        ),
    ]
