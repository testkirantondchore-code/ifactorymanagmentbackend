from django.db import models
from django.conf import settings


class DailyPumpReport(models.Model):
    date = models.DateField()
    po_numbers = models.JSONField(default=list)  # Store list of PO numbers
    reason = models.TextField()
    location = models.CharField(max_length=255, blank=True, null=True)
    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"Daily Pump Report - {self.date}"


class WeeklySocialMediaReport(models.Model):
    date = models.DateField()
    photo_link = models.URLField(max_length=500)
    location = models.CharField(max_length=255, blank=True, null=True)
    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"Weekly Social Media Report - {self.date}"


class GlimpsesOfTheMonth(models.Model):
    """Dedicated 2-image card for Performance Analysis — separate from collage uploads."""

    month = models.IntegerField()  # 1-12
    year = models.IntegerField()
    title = models.CharField(max_length=500, blank=True, default="")
    images = models.JSONField(default=list)  # exactly 2: [{image_data, image_name}]
    # Legacy single-image fields kept nullable for migration compatibility
    image_data = models.TextField(blank=True, default="")
    image_name = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-year", "-month"]
        unique_together = ["month", "year", "location"]

    def __str__(self):
        return f"Glimpses - {self.month}/{self.year} - {self.location}"


class ReportCollageGroup(models.Model):
    SECTION_KEY_ACHIEVEMENTS = "KEY_ACHIEVEMENTS_GLIMPSES"
    SECTION_LOCATION = "LOCATION_GLIMPSES"

    SECTION_CHOICES = [
        (SECTION_KEY_ACHIEVEMENTS, "Key Achievements Glimpses"),
        (SECTION_LOCATION, "Location Glimpses"),
    ]

    month = models.IntegerField()
    year = models.IntegerField()
    section_type = models.CharField(max_length=50, choices=SECTION_CHOICES)
    location = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=500)
    images = models.JSONField(default=list)
    sort_order = models.IntegerField(default=0)
    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["sort_order", "created_at"]

    def __str__(self):
        return f"{self.section_type} - {self.title} ({self.month}/{self.year})"


class MonthlyReportContent(models.Model):
    month = models.IntegerField()
    year = models.IntegerField()
    key_achievements = models.JSONField(default=list)
    program_summary = models.TextField(blank=True, default="")
    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-year", "-month"]
        unique_together = ["month", "year"]

    def __str__(self):
        return f"Report Content - {self.month}/{self.year}"
