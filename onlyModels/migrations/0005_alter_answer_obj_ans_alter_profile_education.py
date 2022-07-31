# Generated by Django 4.0.6 on 2022-07-16 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onlyModels', '0004_answer_option_alter_profile_role_mcques_maques_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='obj_ans',
            field=models.ManyToManyField(to='onlyModels.option', verbose_name='Objective Answer'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='education',
            field=models.JSONField(blank=True, null=True, verbose_name='Educational Details'),
        ),
    ]
