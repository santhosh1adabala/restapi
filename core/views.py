from django.shortcuts import render
from rest_framework import viewsets
from .models import Customer, Profession, DataSheet, Document
from .serializers import CustomerSerializer, ProfessionSerializer, DataSheetSerializer, DocumentSerializer
from rest_framework.response import Response

# Create your views here.

class CustomerViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer

    def get_queryset(self):
        activecustomer = Customer.objects.filter(active=True)
        return activecustomer
    def list(self, request, *args, **kwargs):
        coustomer = Customer.objects.filter(id=2)
        serializer = CustomerSerializer(coustomer, many=True)
        return Response(serializer.data)


class ProfessionViewSet(viewsets.ModelViewSet):
    queryset = Profession.objects.all()
    serializer_class = ProfessionSerializer

class DataSheetViewSet(viewsets.ModelViewSet):
    queryset = DataSheet.objects.all()
    serializer_class = DataSheetSerializer

class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer