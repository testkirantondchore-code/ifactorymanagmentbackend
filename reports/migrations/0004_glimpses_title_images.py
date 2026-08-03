from django.db import migrations, models


def migrate_legacy_images(apps, schema_editor):
    GlimpsesOfTheMonth = apps.get_model("reports", "GlimpsesOfTheMonth")
    for row in GlimpsesOfTheMonth.objects.all():
        if row.images:
            continue
        if row.image_data:
            row.images = [
                {
                    "image_data": row.image_data,
                    "image_name": row.image_name or "",
                }
            ]
            row.save(update_fields=["images"])


class Migration(migrations.Migration):

    dependencies = [
        ("reports", "0003_reportcollagegroup_monthlyreportcontent"),
    ]

    operations = [
        migrations.AddField(
            model_name="glimpsesofthemonth",
            name="title",
            field=models.CharField(blank=True, default="", max_length=500),
        ),
        migrations.AddField(
            model_name="glimpsesofthemonth",
            name="images",
            field=models.JSONField(default=list),
        ),
        migrations.AddField(
            model_name="glimpsesofthemonth",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name="glimpsesofthemonth",
            name="image_data",
            field=models.TextField(blank=True, default=""),
        ),
        migrations.RunPython(migrate_legacy_images, migrations.RunPython.noop),
    ]
