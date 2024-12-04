# Generated by Django 4.2.4 on 2024-11-13 17:57

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main_screen', '0007_alter_lessongroup_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='completion_datetime',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='lesson',
            name='creation_datetime',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lesson',
            name='formation_datetime',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='status',
            field=models.CharField(choices=[('Черновик', 'Draft'), ('Удалён', 'Deleted'), ('Сформирован', 'Formed'), ('Завершён', 'Completed'), ('Отклонён', 'Rejected')], default='Черновик', max_length=30),
        ),
        migrations.AlterModelTable(
            name='lesson',
            table='lessons',
        ),
    ]
