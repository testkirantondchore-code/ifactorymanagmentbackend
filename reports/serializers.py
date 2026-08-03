from rest_framework import serializers
from .models import (
    DailyPumpReport,
    WeeklySocialMediaReport,
    GlimpsesOfTheMonth,
    ReportCollageGroup,
    MonthlyReportContent,
)


class DailyPumpReportSerializer(serializers.ModelSerializer):
    added_by_name = serializers.ReadOnlyField(source="added_by.get_full_name")

    class Meta:
        model = DailyPumpReport
        fields = "__all__"


class WeeklySocialMediaReportSerializer(serializers.ModelSerializer):
    added_by_name = serializers.ReadOnlyField(source="added_by.get_full_name")

    class Meta:
        model = WeeklySocialMediaReport
        fields = "__all__"


class GlimpsesOfTheMonthSerializer(serializers.ModelSerializer):
    added_by_name = serializers.ReadOnlyField(source="added_by.get_full_name")

    class Meta:
        model = GlimpsesOfTheMonth
        fields = "__all__"

    def validate_images(self, value):
        if not isinstance(value, list):
            raise serializers.ValidationError("Images must be a list.")
        if len(value) != 2:
            raise serializers.ValidationError(
                "Glimpses of the Month must contain exactly 2 images."
            )
        for idx, item in enumerate(value):
            if not isinstance(item, dict) or not item.get("image_data"):
                raise serializers.ValidationError(
                    f"Image {idx + 1} is missing image data."
                )
        return value

    def validate(self, attrs):
        title = attrs.get("title", getattr(self.instance, "title", ""))
        if not (title or "").strip():
            raise serializers.ValidationError(
                {"title": "Bottom title is required for Glimpses of the Month."}
            )
        return attrs


class ReportCollageGroupSerializer(serializers.ModelSerializer):
    added_by_name = serializers.ReadOnlyField(source="added_by.get_full_name")

    class Meta:
        model = ReportCollageGroup
        fields = "__all__"

    def validate_images(self, value):
        if not value:
            raise serializers.ValidationError("At least one image is required.")
        if len(value) not in (2, 4, 6, 8):
            raise serializers.ValidationError(
                "Collage must contain 2, 4, 6, or 8 images."
            )
        return value


class MonthlyReportContentSerializer(serializers.ModelSerializer):
    added_by_name = serializers.ReadOnlyField(source="added_by.get_full_name")

    class Meta:
        model = MonthlyReportContent
        fields = "__all__"
