# Generated by Django 4.2.7 on 2023-12-05 16:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pickleapi', '0002_alter_court_number_of_courts'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postcategory',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_categories', to='pickleapi.post'),
        ),
    ]
