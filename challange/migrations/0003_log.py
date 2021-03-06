# Generated by Django 4.0.1 on 2022-07-14 11:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('challange', '0002_remove_question_answer_alter_member_verifcode_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logtime', models.DateTimeField(auto_now_add=True)),
                ('action', models.CharField(choices=[('l', 'login'), ('a', 'answerQuestion')], max_length=1)),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='challange.member')),
            ],
        ),
    ]
