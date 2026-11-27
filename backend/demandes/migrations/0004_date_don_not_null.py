
from django.db import migrations, models
from django.utils import timezone
from datetime import timedelta


def remplir_dates_manquantes(apps, schema_editor):
    DemandeSang = apps.get_model("demandes", "DemandeSang")

    demandes = DemandeSang.objects.filter(date_don__isnull=True)
    maintenant = timezone.now()

    for index, demande in enumerate(demandes.iterator()):
        demande.date_don = maintenant + timedelta(days=index + 1)
        demande.save(update_fields=["date_don"])


class Migration(migrations.Migration):

    dependencies = [
        ("demandes", "0003_don_depistage_dossierpredon"),
    ]

    operations = [
        migrations.RunPython(
            remplir_dates_manquantes,
            migrations.RunPython.noop,
        ),
        migrations.AlterField(
            model_name="demandesang",
            name="date_don",
            field=models.DateTimeField(),
        ),
    ]
