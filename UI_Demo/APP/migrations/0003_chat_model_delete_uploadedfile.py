# Generated by Django 5.0.6 on 2024-05-15 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('APP', '0002_remove_uploadedfile_file_uploadedfile_files'),
    ]

    operations = [
        migrations.CreateModel(
            name='chat_Model',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chat_user', models.TextField()),
                ('chat_system', models.TextField()),
            ],
        ),
        migrations.DeleteModel(
            name='UploadedFile',
        ),
    ]