""" Migration to remove previously created OAI data, making sure only public data are
harvestable.
"""

from django.db import migrations


def forwards(apps, schema_editor):
    oai_data_model = apps.get_model("core_oaipmh_provider_app", "OaiData")
    oai_data_model.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ("core_main_app", "0004_template_ordering"),
        ("core_oaipmh_provider_app", "0002_oai_data_on_delete"),
    ]

    operations = [migrations.RunPython(forwards)]
