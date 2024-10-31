# Generated by Django 4.2.4 on 2024-10-30 16:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_fac', models.CharField(max_length=100)),
                ('group_kaf', models.CharField(max_length=100)),
                ('group_course', models.PositiveIntegerField()),
                ('group_count', models.PositiveIntegerField()),
                ('contact', models.CharField(max_length=100)),
                ('contact_phone', models.CharField(max_length=15)),
                ('photo_url', models.CharField(default='', max_length=254)),
                ('status', models.CharField(default='Действует', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('building', models.CharField(default='ГЗ', max_length=30)),
                ('status', models.CharField(default='черновик', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='OrderGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lesson_time', models.DateTimeField()),
                ('audience', models.CharField(max_length=100)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_screen.group')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_screen.order')),
            ],
            options={
                'unique_together': {('order', 'group')},
            },
        ),
        migrations.AddField(
            model_name='order',
            name='groups',
            field=models.ManyToManyField(through='main_screen.OrderGroup', to='main_screen.group'),
        ),
    ]
