# Generated by Django 4.2.5 on 2023-10-03 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('robots', '0003_alter_robot_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='robot',
            name='serial',
            field=models.CharField(blank=True, max_length=5),
        ),
    ]
