from rest_framework import routers, serializers, viewsets
from .models import Customer, Profession, DataSheet,Document

class CustomerSerializer(serializers.ModelSerializer):
    num_professions = serializers.SerializerMethodField()
    data_sheet=serializers.StringRelatedField()

    class Meta:
        model = Customer
        fields = [
            'id', 'name', 'address', 'professions', 'data_sheet','active','status_message','num_professions']
    def get_num_professions(self,obj):
            return obj.num_professions()

class ProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields = '__all__'

class DataSheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataSheet
        fields = '__all__'

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'