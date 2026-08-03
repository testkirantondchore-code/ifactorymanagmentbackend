from django.contrib import admin
from .models import (
    DailyPumpReport,
    WeeklySocialMediaReport,
    GlimpsesOfTheMonth,
    ReportCollageGroup,
    MonthlyReportContent,
)


@admin.register(DailyPumpReport)
class DailyPumpReportAdmin(admin.ModelAdmin):
    list_display = ("date", "location", "added_by", "created_at")
    list_filter = ("location", "date")
    search_fields = ("reason", "po_numbers")


@admin.register(WeeklySocialMediaReport)
class WeeklySocialMediaReportAdmin(admin.ModelAdmin):
    list_display = ("date", "location", "added_by", "created_at")
    list_filter = ("location", "date")
    search_fields = ("photo_link",)


@admin.register(GlimpsesOfTheMonth)
class GlimpsesOfTheMonthAdmin(admin.ModelAdmin):
    list_display = ("month", "year", "location", "title", "added_by", "updated_at")
    list_filter = ("location", "year", "month")
    search_fields = ("title", "location")


@admin.register(ReportCollageGroup)
class ReportCollageGroupAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "section_type",
        "location",
        "month",
        "year",
        "sort_order",
        "created_at",
    )
    list_filter = ("section_type", "location", "year", "month")


@admin.register(MonthlyReportContent)
class MonthlyReportContentAdmin(admin.ModelAdmin):
    list_display = ("month", "year", "added_by", "updated_at")
    list_filter = ("year", "month")
