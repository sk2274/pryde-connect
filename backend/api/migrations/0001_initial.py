# Generated by Django 2.2.3 on 2019-07-17 20:02

from django.conf import settings
import django.contrib.auth.validators
import django.contrib.postgres.fields
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='PUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('role', models.IntegerField(choices=[(1, 'Practitioner'), (2, 'Researcher')], default=None, null=True)),
                ('displayRole', models.IntegerField(choices=[(1, '4-H Educator'), (2, 'Other CCE Role'), (3, 'Practice Focused Role'), (4, 'Cornell Faculty'), (5, 'Cornell Student'), (6, 'Research Focused Role'), (7, '4-H Practitioner')], default=None, null=True)),
                ('affiliation', models.CharField(max_length=100)),
                ('location', models.CharField(default=None, max_length=30, null=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(default=None, max_length=128, null=True, region=None)),
                ('website', models.URLField(default=None, null=True)),
                ('researchInterests', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), default=list, null=True, size=None)),
                ('researchDescription', models.TextField()),
                ('roles', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), default=list, null=True, size=None)),
                ('ageRanges', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), default=list, null=True, size=None)),
                ('youthProgramTypes', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), default=list, null=True, size=None)),
                ('deliveryModes', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), default=list, null=True, size=None)),
                ('researchNeeds', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), default=list, null=True, size=None)),
                ('evaluationNeeds', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), default=list, null=True, size=None)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('status', models.IntegerField(choices=[(1, 'completed'), (2, 'in-progress'), (3, 'not-started')], default=None, null=True)),
                ('summary', models.TextField()),
                ('researchTopics', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), default=None, size=None)),
                ('ageRanges', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), default=None, size=None)),
                ('deliveryModes', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), default=None, size=None)),
                ('timeline', models.CharField(max_length=100)),
                ('commitmentLength', models.CharField(max_length=100)),
                ('incentives', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), default=None, size=None)),
                ('collaborators', django.contrib.postgres.fields.jsonb.JSONField(default=dict)),
                ('additionalInformation', models.TextField()),
                ('additionalFiles', django.contrib.postgres.fields.ArrayField(base_field=models.FileField(upload_to='uploads/'), default=None, size=None)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='projects', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
