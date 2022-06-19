# Generated by Django 4.0.5 on 2022-06-03 15:16

import api.validators
import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(max_length=64, unique=True, verbose_name='username')),
                ('email', models.EmailField(max_length=255, unique=True, validators=[django.core.validators.EmailValidator], verbose_name='email address')),
                ('first_name', models.CharField(max_length=64, verbose_name='first_name')),
                ('last_name', models.CharField(max_length=64, verbose_name='last_name')),
                ('date_created', models.DateTimeField(validators=[django.core.validators.MaxValueValidator(limit_value=datetime.datetime(2022, 6, 3, 15, 16, 46, 157802, tzinfo=utc))], verbose_name='created')),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Case',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=1024, verbose_name='content')),
                ('date_created', models.DateTimeField(validators=[django.core.validators.MaxValueValidator(limit_value=datetime.datetime(2022, 6, 3, 15, 16, 46, 158217, tzinfo=utc))], verbose_name='created')),
                ('severity', models.IntegerField(validators=[django.core.validators.MinValueValidator(limit_value=1), django.core.validators.MaxValueValidator(limit_value=4)], verbose_name='severity')),
                ('is_closed', models.BooleanField(default=False, verbose_name='is_closed')),
                ('admin_assigned', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='admin_assigned', to=settings.AUTH_USER_MODEL, validators=[api.validators.is_admin_validator])),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='user_created', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CaseUpdate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=1024, verbose_name='comment')),
                ('date_created', models.DateTimeField(validators=[django.core.validators.MaxValueValidator(limit_value=datetime.datetime(2022, 6, 3, 15, 16, 46, 158634, tzinfo=utc))], verbose_name='created')),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.case')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]