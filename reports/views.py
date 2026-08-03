from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import (
    DailyPumpReport,
    WeeklySocialMediaReport,
    GlimpsesOfTheMonth,
    ReportCollageGroup,
    MonthlyReportContent,
)
from .serializers import (
    DailyPumpReportSerializer,
    WeeklySocialMediaReportSerializer,
    GlimpsesOfTheMonthSerializer,
    ReportCollageGroupSerializer,
    MonthlyReportContentSerializer,
)


def _filter_by_month_year(queryset, request):
    month = request.query_params.get("month")
    year = request.query_params.get("year")
    if month:
        queryset = queryset.filter(month=int(month))
    if year:
        queryset = queryset.filter(year=int(year))
    return queryset


def _filter_by_location(queryset, request, user):
    location = request.query_params.get("location")
    section_type = request.query_params.get("section_type")

    # section_type only exists on ReportCollageGroup
    if section_type and hasattr(queryset.model, "section_type"):
        queryset = queryset.filter(section_type=section_type)

    if user.role == "SUPERADMIN":
        if location and location != "All Locations":
            queryset = queryset.filter(location=location)
        return queryset

    return queryset.filter(location=user.location)


class DailyPumpReportViewSet(viewsets.ModelViewSet):
    queryset = DailyPumpReport.objects.all()
    serializer_class = DailyPumpReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(added_by=self.request.user, location=self.request.user.location)

    def get_queryset(self):
        user = self.request.user
        queryset = self.queryset
        location = self.request.query_params.get("location")

        if user.role == "SUPERADMIN":
            if location and location != "All Locations":
                queryset = queryset.filter(location=location)
            return queryset

        return queryset.filter(location=user.location)


class WeeklySocialMediaReportViewSet(viewsets.ModelViewSet):
    queryset = WeeklySocialMediaReport.objects.all()
    serializer_class = WeeklySocialMediaReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(added_by=self.request.user, location=self.request.user.location)

    def get_queryset(self):
        user = self.request.user
        queryset = self.queryset
        location = self.request.query_params.get("location")

        if user.role == "SUPERADMIN":
            if location and location != "All Locations":
                queryset = queryset.filter(location=location)
            return queryset

        return queryset.filter(location=user.location)


class GlimpsesOfTheMonthViewSet(viewsets.ModelViewSet):
    queryset = GlimpsesOfTheMonth.objects.all()
    serializer_class = GlimpsesOfTheMonthSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        location = serializer.validated_data.get("location")
        if user.role != "SUPERADMIN":
            location = user.location
        serializer.save(added_by=user, location=location)

    def perform_update(self, serializer):
        user = self.request.user
        location = serializer.validated_data.get(
            "location", serializer.instance.location
        )
        if user.role != "SUPERADMIN":
            location = user.location
        serializer.save(location=location)

    def get_queryset(self):
        user = self.request.user
        queryset = _filter_by_month_year(self.queryset, self.request)
        return _filter_by_location(queryset, self.request, user)


class ReportCollageGroupViewSet(viewsets.ModelViewSet):
    queryset = ReportCollageGroup.objects.all()
    serializer_class = ReportCollageGroupSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        location = serializer.validated_data.get("location")
        if user.role != "SUPERADMIN":
            location = user.location
        serializer.save(added_by=user, location=location)

    def perform_update(self, serializer):
        user = self.request.user
        location = serializer.validated_data.get(
            "location", serializer.instance.location
        )
        if user.role != "SUPERADMIN":
            location = user.location
        serializer.save(location=location)

    def get_queryset(self):
        user = self.request.user
        queryset = _filter_by_month_year(self.queryset, self.request)
        return _filter_by_location(queryset, self.request, user)


class MonthlyReportContentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        month = request.query_params.get("month")
        year = request.query_params.get("year")
        if not month or not year:
            return Response(
                {"detail": "month and year are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        content, _ = MonthlyReportContent.objects.get_or_create(
            month=int(month),
            year=int(year),
            defaults={"key_achievements": [], "program_summary": ""},
        )
        return Response(MonthlyReportContentSerializer(content).data)

    def put(self, request):
        month = request.data.get("month")
        year = request.data.get("year")
        if not month or not year:
            return Response(
                {"detail": "month and year are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        content, _ = MonthlyReportContent.objects.get_or_create(
            month=int(month),
            year=int(year),
            defaults={"added_by": request.user},
        )

        serializer = MonthlyReportContentSerializer(
            content, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(added_by=request.user)
        return Response(serializer.data)
