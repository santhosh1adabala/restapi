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
        customers=Customer.objects.filter(id=3)
        serializer=CustomerSerializer(customers,many=True)
        return Response(serializer.data)
    def create(self, request, *args, **kwargs):
        data = request.data
        customers=Customer.objects.create(name=data['name'],address=data["address"],data_sheet_id=data["data_sheet"])
        profession=Profession.objects.get(id=data["professions"])
        customers.professions.add(profession)
        customers.save()
        serializer=CustomerSerializer(customers)
        return Response(serializer.data)
    def update(self, request, *args, **kwargs):
        customer=self.get_object()
        data=request.data
        customer.name=data["name"]
        customer.address=data["address"]
        customer.data_sheet_id=data["data_sheet"]
        for p in customer.professions.all():
            customer.professions.remove(p)
        profession=Profession.objects.get(id=data["professions"])
        customer.professions.add(profession)
        customer.save()
        serializer=CustomerSerializer(customer)
        return Response(serializer.data)
    def partial_update(self, request, *args, **kwargs):
        customer=self.get_object()
        customer.name=request.data.get('name',customer.name)
        customer.address=request.data.get('address',customer.address)
        customer.data_sheet_id=request.data.get('data_sheet',customer.data_sheet_id)
        customer.save()
        serializer=CustomerSerializer(customer)
        return Response(serializer.data)





#     coustomer = Customer.objects.filter(id=2)
    #    serializer = CustomerSerializer(coustomer, many=True)
     #   return Response(serializer.data)


class ProfessionViewSet(viewsets.ModelViewSet):
    queryset = Profession.objects.all()
    serializer_class = ProfessionSerializer

class DataSheetViewSet(viewsets.ModelViewSet):
    queryset = DataSheet.objects.all()
    serializer_class = DataSheetSerializer

class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer