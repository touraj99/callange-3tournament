# Generated by Django 4.0.1 on 2022-07-15 15:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('challange', '0009_resultmember'),
    ]

    operations = [
        migrations.AddField(
            model_name='resultmember',
            name='tournament',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='challange.tournament'),
            preserve_default=False,
        ),
    ]