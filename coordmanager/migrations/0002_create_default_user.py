# Generated by Django 3.1 on 2020-10-03 07:22

import os
from sys import path
from django.conf import settings
from django.core import serializers
from django.db import migrations

fixture_filename = 'default_users.json'

def load_fixture(apps, schema_editor):
    fixture_file = os.path.join(settings.FIXTURE_DIRS[0], fixture_filename)
    fixture = open(fixture_file, 'rb')
    objects = serializers.deserialize('json', fixture, ignorenonexistent=True)
    for obj in objects:
        obj.save()
    fixture.close()

def unload_fixture(apps, schema_editor):
    "Brutally deleting all entries for this model..."

    MyModel = apps.get_model("auth", "User")
    MyModel.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('coordmanager', '0001_setup_site_name'),
    ]

    operations = [
        migrations.RunPython(load_fixture, reverse_code=unload_fixture),
    ]
