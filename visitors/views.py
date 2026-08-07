from rest_framework import serializers, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Visitor
import pandas as pd
import io

class VisitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visitor
        fields = '__all__'
        read_only_fields = ['added_by']

class VisitorViewSet(viewsets.ModelViewSet):
    queryset = Visitor.objects.all()
    serializer_class = VisitorSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Visitor.objects.all()
        
        if not user.is_superadmin:
            queryset = queryset.filter(location__iexact=user.location)
        
        location_filter = self.request.query_params.get('location')
        if location_filter and location_filter != 'All Locations':
            queryset = queryset.filter(location__iexact=location_filter)
            
        return queryset

    def perform_create(self, serializer):
        # Default to user's location, or 'Global' if user is a SuperAdmin with no location
        location = self.request.user.location or 'Global iFactory'
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

            # Standardize columns
            df.columns = [c.lower().strip() for c in df.columns]
            
            visitors_to_create = []
            location = self.request.user.location or 'Global iFactory'
            
            for _, row in df.iterrows():
                # Get category with fallback to 'category' or 'visitor_category'
                raw_cat = row.get('categories') or row.get('category') or row.get('visitor_category', '')
                category_str = str(raw_cat).strip()
                category_upper = category_str.upper()
                
                # Get industry with fallback
                raw_ind = row.get('industry_type') or row.get('industry') or ''
                industry_str = str(raw_ind).strip()

                # Map common category names to purpose choices
                purpose_map = {
                    'INDUSTRIAL': 'INDUSTRIAL',
                    'ACADEMIC': 'ACADEMIC',
                    'GOVERNMENT': 'GOVERNMENT',
                    'TRAINING': 'TRAINING',
                    'MEETING': 'MEETING',
                    'SITE VISIT': 'SITE_VISIT',
                    'SITE_VISIT': 'SITE_VISIT',
                }
                purpose = purpose_map.get(category_upper, row.get('purpose', 'OTHER')).upper()
                if purpose not in dict(Visitor.PURPOSE_CHOICES):
                    purpose = 'OTHER'

                visitors_to_create.append(Visitor(
                    first_name=row.get('first_name') or row.get('person_name', 'N/A'),
                    last_name=row.get('last_name', '.'),
                    email=row.get('email', 'no-email@example.com'),
                    phone=row.get('phone', '0000000000'),
                    company=row.get('company') or row.get('organization_name', 'Unknown'),
                    categories=category_str,
                    industry_type=industry_str,
                    photograph_link=row.get('photograph_link', ''),
                    purpose=purpose,
                    location=location,
                    added_by=self.request.user
                ))
            
            Visitor.objects.bulk_create(visitors_to_create)
            return Response({"message": f"Successfully uploaded {len(visitors_to_create)} visitors"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['GET'])
    def download_template(self, request):
        import csv
        from django.http import HttpResponse
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="visitor_template.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['first_name', 'last_name', 'email', 'phone', 'company', 'categories', 'industry_type', 'photograph_link'])
        
        return response
