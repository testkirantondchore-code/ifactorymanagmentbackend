# Generated manually for monthly report collage support

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("reports", "0002_glimpsesofthemonth"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="ReportCollageGroup",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("month", models.IntegerField()),
                ("year", models.IntegerField()),
                (
                    "section_type",
                    models.CharField(
                        choices=[
                            ("KEY_ACHIEVEMENTS_GLIMPSES", "Key Achievements Glimpses"),
                            ("LOCATION_GLIMPSES", "Location Glimpses"),
                        ],
                        max_length=50,
                    ),
                ),
                ("location", models.CharField(blank=True, max_length=255, null=True)),
                ("title", models.CharField(max_length=500)),
                ("images", models.JSONField(default=list)),
                ("sort_order", models.IntegerField(default=0)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "added_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["sort_order", "created_at"],
            },
        ),
        migrations.CreateModel(
            name="MonthlyReportContent",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("month", models.IntegerField()),
                ("year", models.IntegerField()),
                ("key_achievements", models.JSONField(default=list)),
                ("program_summary", models.TextField(blank=True, default="")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "added_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["-year", "-month"],
                "unique_together": {("month", "year")},
            },
        ),
    ]
