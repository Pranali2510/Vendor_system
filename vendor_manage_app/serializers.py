# serializers.py
from rest_framework import serializers
from .models import Vendor, PurchaseOrder

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'

class VendorDetailSerializer(VendorSerializer):
    class Meta:
        model = Vendor
        fields = ['vendor_code','name','address','contact_details']

class PurchaseOrderTrackSerializer(serializers.ModelSerializer):
    # order_date = serializers.SerializerMethodField()
    class Meta:
        model = PurchaseOrder
        fields = '__all__'
        # fields = ['id', 'po_number', 'vendor', 'order_date', 'delivery_date', 'items', 'quantity', 'status', 'quality_rating', 'issue_date', 'acknowledgment_date']
    # def get_order_date(self, obj):
    #     return obj.order_date.date() if obj.order_date else None

class PurchaseOrderSerializer(PurchaseOrderTrackSerializer):
    # order_date = serializers.SerializerMethodField()
    class Meta:
        model = PurchaseOrder
        fields = ['po_number','vendor','order_date','issue_date','items','quantity','delivery_date','status']
    # def get_order_date(self, obj):
        # return obj.order_date.date() if obj.order_date else None


