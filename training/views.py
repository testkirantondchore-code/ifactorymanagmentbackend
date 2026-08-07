from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Training, DigitalMaturityAssessment
from .serializers import TrainingSerializer, DigitalMaturityAssessmentSerializer
import pandas as pd
import io
import csv
from django.http import HttpResponse

class TrainingViewSet(viewsets.ModelViewSet):
    queryset = Training.objects.all()
    serializer_class = TrainingSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Training.objects.all()
        if not user.is_superadmin:
            queryset = queryset.filter(location__iexact=user.location)
        
        location_filter = self.request.query_params.get('location')
        if location_filter and location_filter != 'All Locations':
            queryset = queryset.filter(location__iexact=location_filter)
            
        return queryset

    def perform_create(self, serializer):
        location = self.request.user.location or 'Global'
        serializer.save(added_by=self.request.user, location=location)

    @action(detail=False, methods=['POST'])
    def bulk_upload(self, request):
        file = request.FILES.get('file')
        if not file:
            return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            if file.name.endswith('.csv'):
                df = pd.read_csv(io.StringIO(file.read().decode('utf-8')))
            else:
                df = pd.read_excel(file)

            df.columns = [c.lower().strip().replace(' ', '_') for c in df.columns]
            
            entities_to_create = []
            location = self.request.user.location or 'Global'
            
            for _, row in df.iterrows():
                # Expected columns: Date, Organization, Category, Industry, Person Name, Phone, Email, Photograph Link
                entities_to_create.append(Training(
                    date=row.get('date'),
                    organization_name=row.get('organization') or row.get('organization_name'),
                    category=row.get('category'),
                    industry_type=row.get('industry') or row.get('industry_type'),
                    person_name=row.get('person_name'),
                    phone=row.get('phone'),
                    email=row.get('email'),
                    photograph_link=row.get('photograph_link'),
                    location=location,
                    added_by=self.request.user
                ))
            
            Training.objects.bulk_create(entities_to_create)
            return Response({"message": f"Successfully uploaded {len(entities_to_create)} training records"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['GET'])
    def download_template(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="training_template.csv"'
        writer = csv.writer(response)
        writer.writerow(['Date', 'Organization', 'Category', 'Industry', 'Person Name', 'Phone', 'Email', 'Photograph Link'])
        return response

class DigitalMaturityAssessmentViewSet(viewsets.ModelViewSet):
    queryset = DigitalMaturityAssessment.objects.all()
    serializer_class = DigitalMaturityAssessmentSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = DigitalMaturityAssessment.objects.all()
        if not user.is_superadmin:
            queryset = queryset.filter(location__iexact=user.location)
        
        location_filter = self.request.query_params.get('location')
        if location_filter and location_filter != 'All Locations':
            queryset = queryset.filter(location__iexact=location_filter)
            
        return queryset

    def perform_create(self, serializer):
        location = self.request.user.location or 'Global'
        serializer.save(added_by=self.request.user, location=location)

    @action(detail=False, methods=['POST'])
    def bulk_upload(self, request):
        file = request.FILES.get('file')
        if not file:
            return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            if file.name.endswith('.csv'):
                df = pd.read_csv(io.StringIO(file.read().decode('utf-8')))
            else:
                df = pd.read_excel(file)

            df.columns = [c.lower().strip().replace(' ', '_') for c in df.columns]
            
            entities_to_create = []
            location = self.request.user.location or 'Global'
            
            for _, row in df.iterrows():
                # Expected columns: Organization, Activity Type, Total Assessments, Total Impact
                entities_to_create.append(DigitalMaturityAssessment(
                    organization_name=row.get('organization') or row.get('organization_name'),
                    activity_type=row.get('activity_type'),
                    total_assessments=row.get('total_assessments', 0),
                    total_impact=row.get('total_impact'),
                    # payment_type=row.get('payment_type', 'FREE').upper(), # Optional from bulk user but useful
                    location=location,
                    added_by=self.request.user
                ))
            
            DigitalMaturityAssessment.objects.bulk_create(entities_to_create)
            return Response({"message": f"Successfully uploaded {len(entities_to_create)} assessment records"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['GET'])
    def download_template(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="assessment_template.csv"'
        writer = csv.writer(response)
        writer.writerow(['Organization', 'Activity Type', 'Total Assessments', 'Total Impact', 'Photograph Link'])
        return response
