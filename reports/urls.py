from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    DailyPumpReportViewSet,
    WeeklySocialMediaReportViewSet,
    GlimpsesOfTheMonthViewSet,
    ReportCollageGroupViewSet,
    MonthlyReportContentView,
)

router = DefaultRouter()
router.register(r"daily-pump", DailyPumpReportViewSet)
router.register(r"weekly-social", WeeklySocialMediaReportViewSet)
router.register(r"glimpses-month", GlimpsesOfTheMonthViewSet)
router.register(r"collage-groups", ReportCollageGroupViewSet)

urlpatterns = [
    path("monthly-content/", MonthlyReportContentView.as_view(), name="monthly-content"),
    path("", include(router.urls)),
]
