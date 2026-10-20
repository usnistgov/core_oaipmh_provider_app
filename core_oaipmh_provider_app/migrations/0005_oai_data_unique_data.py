from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    """Adds the unique constraint on OaiData.data.

    Must be run after `0004_dedupe_oai_data` to prevent duplicate rows.
    """

    dependencies = [
        ("core_oaipmh_provider_app", "0004_dedupe_oai_data"),
    ]

    operations = [
        migrations.AlterField(
            model_name="oaidata",
            name="data",
            field=models.ForeignKey(
                blank=False,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="core_main_app.data",
                unique=True,
            ),
        ),
    ]
