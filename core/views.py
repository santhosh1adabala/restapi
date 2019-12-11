from django.shortcuts import render
from rest_framework import viewsets
from .models import Customer, Profession, DataSheet, Document
from .serializers import CustomerSerializer, ProfessionSerializer, DataSheetSerializer, DocumentSerializer
from rest_framework.response import Response
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action




# Create your views here.

class CustomerViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer
    filter_fields=('name',)
    filter_backends = [DjangoFilterBackend,filters.SearchFilter]

    def get_queryset(self):
        #import pdb;pdb.set_trace()
        address=self.request.query_params.get('address',None)
        status=False if self.request.query_params.get('active')=='False' else True
        if address :

            customer = Customer.objects.filter(address__icontains=address,active=status)
            #import pdb;pdb.set_trace()
        else:
           # import pdb;pdb.set_trace()
            customer = Customer.objects.all()
        return customer
 #   def list(self, request, *args, **kwargs):
  #      customers=self.get_queryset()
   #     serializer=CustomerSerializer(customers,many=True)
    #    return Response(serializer.data)

    #POST modification
    def create(self, request, *args, **kwargs):
        data = request.data
        customers=Customer.objects.create(name=data['name'],address=data["address"],data_sheet_id=data["data_sheet"])
        profession=Profession.objects.get(id=data["professions"])
        customers.professions.add(profession)
        customers.save()
        serializer=CustomerSerializer(customers)
        return Response(serializer.data)

    #PUT modification
    def update(self, request, *args, **kwargs):
        customer=self.get_object()
        data=request.data
        #import pdb;pdb.set_trace()
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

    #PATCH modification
    def partial_update(self, request, *args, **kwargs):
        customer=self.get_object()
        customer.name=request.data.get('name',customer.name)
        customer.address=request.data.get('address',customer.address)
        customer.data_sheet_id=request.data.get('data_sheet',customer.data_sheet_id)
        customer.save()
        serializer=CustomerSerializer(customer)
        return Response(serializer.data)

    #Delete Modificaton
    def destroy(self, request, *args, **kwargs):
        d=self.get_object()
        d.delete()
        return
    #custom actions
    @action(detail=True)
    def deactivate(self,request,**kwargs):
        customer=self.get_object()
        customer.active=False
        customer.save()
        serializer=CustomerSerializer(customer)
        return Response(serializer.data)
    @action(detail=False)
    def deactivate_all(self,request,**kwargs):
        #import pdb;pdb.set_trace()
        customers=Customer.objects.all()
        customers.update(active=False)
        serializer=CustomerSerializer(customers,many=True)
        return Response(serializer.data)
    @action(detail=False)
    def activate_all(self,request,**kwargs):
        #import pdb;pdb.set_trace()
        customers=Customer.objects.all()
        customers.update(active=True)
        serializer = CustomerSerializer(customers,many=True)
        return Response(serializer.data)
    @action(detail=False,methods=['POST'])
    def change_status(self,request,**kwargs):
        status=True if request.data['active'] =='True' else False
        customers=Customer.objects.all()
        customers.update(active=status)
        serializer = CustomerSerializer(customers, many=True)
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