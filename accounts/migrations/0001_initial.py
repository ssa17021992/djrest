# Generated by Django 2.0.3 on 2018-03-10 23:15

import accounts.utils
import common.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SignUpCode',
            fields=[
                ('id', models.CharField(editable=False, max_length=22, primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=254, verbose_name='email address')),
                ('code', models.CharField(default=accounts.utils.generate_code, editable=False, max_length=4, verbose_name='code')),
                ('expired', models.DateTimeField(default=accounts.utils.generate_code_expired, editable=False, verbose_name='expired')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
            ],
            options={
                'verbose_name': 'sign up code',
                'verbose_name_plural': 'sign up codes',
                'db_table': 'accounts_sign_up_code',
                'ordering': ('email',),
            },
        ),
        migrations.CreateModel(
            name='SocialLogin',
            fields=[
                ('id', models.CharField(editable=False, max_length=22, primary_key=True, serialize=False)),
                ('social', models.CharField(choices=[('facebook', 'facebook')], max_length=10, verbose_name='social')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
            ],
            options={
                'verbose_name': 'social login',
                'verbose_name_plural': 'social logins',
                'db_table': 'accounts_social_login',
                'ordering': ('created',),
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.CharField(editable=False, max_length=22, primary_key=True, serialize=False)),
                ('firstName', models.CharField(max_length=150, verbose_name='first name')),
                ('middleName', models.CharField(max_length=150, verbose_name='middle name')),
                ('lastName', models.CharField(max_length=150, verbose_name='last name')),
                ('username', models.CharField(max_length=200, unique=True, validators=[django.core.validators.RegexValidator('^[a-z0-9.@_]{4,40}$')], verbose_name='username')),
                ('password', models.CharField(max_length=106, verbose_name='password')),
                ('email', models.EmailField(max_length=254, verbose_name='email address')),
                ('birthday', models.DateField(verbose_name='birthday')),
                ('phone', models.CharField(max_length=15, verbose_name='phone number')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='files/avatars/d%Y%m%d/', validators=[django.core.validators.FileExtensionValidator(['png', 'jpg']), common.validators.FileSizeValidator(max_size=1024.0)], verbose_name='avatar')),
                ('renewed', models.BigIntegerField(blank=True, default=accounts.utils.generate_user_renewed, null=True, verbose_name='renewed')),
                ('isActive', models.BooleanField(default=True, verbose_name='active')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'db_table': 'accounts_user',
                'ordering': ('username',),
            },
        ),
        migrations.AddField(
            model_name='sociallogin',
            name='user',
            field=models.OneToOneField(db_column='user', on_delete=django.db.models.deletion.CASCADE, to='accounts.User', verbose_name='user'),
        ),
    ]