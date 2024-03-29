# Generated by Django 3.0.3 on 2021-05-06 02:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80)),
                ('tice', models.CharField(max_length=15, unique=True)),
                ('phone', models.CharField(blank=True, max_length=15)),
            ],
        ),
        migrations.AddField(
            model_name='exit',
            name='client',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='client_exits', to='dashboard.Client'),
        ),
    ]
