# Generated by Django 5.1.2 on 2024-11-17 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_staff_feedback'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff_feedback',
            name='feedback_reply',
            field=models.TextField(blank=True, null=True),
        ),
    ]