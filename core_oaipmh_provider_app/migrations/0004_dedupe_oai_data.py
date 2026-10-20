"""Dedupe OaiData rows sharing the same `data`.

Required before the next migration (`0005_oai_data_unique_data`) can add a unique
constraint on that field. For each duplicate group, keeps the row with the latest
oai_date_stamp (falling back to the highest pk) and deletes the rest.
"""

from django.db import migrations, models


def dedupe_oai_data(apps, schema_editor):
    OaiData = apps.get_model("core_oaipmh_provider_app", "OaiData")
    from django.db.models import Count

    duplicate_data_ids = (
        OaiData.objects.filter(data__isnull=False)
        .values("data_id")
        .annotate(cnt=Count("id"))
        .filter(cnt__gt=1)
        .values_list("data_id", flat=True)
    )

    for data_id in duplicate_data_ids:
        qs = OaiData.objects.filter(data_id=data_id)
        best = qs.order_by(
            models.F("oai_date_stamp").desc(nulls_last=True), "-pk"
        ).first()
        if best:
            qs.exclude(pk=best.pk).delete()


def noop_reverse(apps, schema_editor):
    """No-op: deleted duplicate rows can't be restored."""


class Migration(migrations.Migration):

    dependencies = [
        ("core_oaipmh_provider_app", "0003_oai_data_bulk_delete"),
    ]

    operations = [
        migrations.RunPython(dedupe_oai_data, noop_reverse),
    ]
