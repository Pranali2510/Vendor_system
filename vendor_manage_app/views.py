
# Create your views here.
from .models import *
from .serializers import *
from .logger import add_log
import logging, random, string
from django.utils import timezone
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password


class VendorTokenObtainPairView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        try:
            user = User.objects.get(username=username)
            passwords_match = check_password(password, user.password)
            if passwords_match:
                refresh = RefreshToken.for_user(user)
                access = AccessToken.for_user(user)
                return Response({'refresh': str(refresh), 'access': str(access)}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            pass
        return Response({'error': 'Invalid username or password'}, status=status.HTTP_400_BAD_REQUEST)

def create_userdetail(vendor_code,name,length=8):
        """Generate a random password."""
        characters = string.ascii_letters + string.digits
        password = ''.join(random.choice(characters) for i in range(length))
        hashed_password = make_password(password)
        user = User.objects.create(username=vendor_code, password = hashed_password, first_name =name)
        user.save()
        return password

@api_view(['GET', 'POST'])
def vendor_profile(request):
    try:
        permission_classes = [IsAuthenticated]
        pagename = "views.py"
        methodname = 'vendor_profile'
        if request.method == 'POST':
            data = request.data
            is_auto_generated = 0
            if 'vendor_code' not in data:
                is_auto_generated = 1
                vendor_code = "VP"+str(random.randint(1, 99)) + \
                    "ID" + str(random.randint(1, 99999))
                data['vendor_code'] = vendor_code
            serializer = VendorDetailSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                result = serializer.data
                result['username'] = vendor_code
                result['password'] = create_userdetail(vendor_code, data['name'])
                return Response(result)
            else:
                if is_auto_generated == 1 and 'vendor_code' in serializer.errors:
                    vendor_code = "VP" + \
                        str(random.randint(1, 99)) + "ID" + \
                        str(random.randint(1, 99999))
                    data['vendor_code'] = vendor_code
                    serializer = VendorDetailSerializer(data=data)
                    if serializer.is_valid():
                        serializer.save()
                        result = serializer.data
                        result['username'] = vendor_code
                        result['password'] = create_userdetail(vendor_code, data['name'])
                        return Response(result)
                else:
                    add_log(pagename, methodname,serializer.errors, logging.ERROR)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'GET':
            vendors = Vendor.objects.all()
            serializer = VendorDetailSerializer(vendors, many=True)
            if serializer.data == []:
                msg = "Vendor Profiles not available"
                add_log(pagename, methodname, msg, logging.ERROR)
                return Response(msg, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(serializer.data)
    except Exception as e:
        add_log(pagename, methodname, e, logging.ERROR, repr(e))
        return Response("An unexpected error occurred", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET', 'PUT', 'DELETE'])
def vendor_profile_management(request, pk):
    try:
        permission_classes = [IsAuthenticated]
        pagename = "views.py"
        methodname = 'vendor_profile_management'
        try:
            vendor = Vendor.objects.get(vendor_code=pk)
        except Vendor.DoesNotExist:
            msg = f"Vendor Profile with ID - '{pk}' does not exist"
            add_log(pagename, methodname, msg, logging.ERROR)
            return Response(msg, status=status.HTTP_404_NOT_FOUND)
        if request.method == 'GET':
            serializer = VendorDetailSerializer(vendor)
            return Response(serializer.data)
        elif request.method == 'PUT':
            data = request.data
            if 'vendor_code' in data:
                if data['vendor_code'] != pk:
                    msg = "vendor_code should be same as parameter pass in URL"
                    add_log(pagename, methodname, msg, logging.ERROR)
                    return Response(msg, status=status.HTTP_400_BAD_REQUEST)
            data['vendor_code'] = pk
            serializer = VendorDetailSerializer(vendor, data)
            if serializer.is_valid():
                if data['name'] == vendor.name and data['address'] == vendor.address and str(data['contact_details']) == vendor.contact_details:
                    msg = "Please provide values to update Vendor Profile"
                    add_log(pagename, methodname, msg, logging.ERROR)
                    return Response(msg, status=status.HTTP_400_BAD_REQUEST)
                serializer.save()
                return Response("Vendor Profile updated successfully")
            else:
                add_log(pagename, methodname,serializer.errors, logging.ERROR)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'DELETE':
            vendor.delete()
            return Response(f"{pk} - Vendor Profile deleted successfully")
    except Exception as e:
        add_log(pagename, methodname, e, logging.ERROR, repr(e))
        return Response("An unexpected error occurred", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET', 'POST'])
def purchase_order_track(request):
    try:
        permission_classes = [IsAuthenticated]
        pagename = "views.py"
        methodname = 'purchase_order_track'
        if request.method == 'POST':
            data = request.data
            po_number = "PO"+str(random.randint(1, 99)) + \
                "NO" + str(random.randint(1, 99999))
            data['po_number'] = po_number
            if data['status'].lower() == 'completed':
                data['po_deliverd_date'] = timezone.now()
            serializer = PurchaseOrderTrackSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                add_log(pagename, methodname, serializer.errors, logging.ERROR)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'GET':
            purchase_orders = PurchaseOrder.objects.all()
            serializer = PurchaseOrderTrackSerializer(
                purchase_orders, many=True)
            if serializer.data == []:
                msg = "Purchase Orders not available"
                add_log(pagename, methodname, msg, logging.ERROR)
                return Response(msg, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(serializer.data)
    except Exception as e:
        add_log(pagename, methodname, e, logging.ERROR, repr(e))
        return Response("An unexpected error occurred", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET', 'PUT', 'DELETE'])
def purchase_order_management(request, pk):
    try:
        permission_classes = [IsAuthenticated]
        pagename = "views.py"
        methodname = 'purchase_order_management'
        try:
            purchase_order = PurchaseOrder.objects.get(po_number=pk)
        except PurchaseOrder.DoesNotExist:
            return Response(f"Purchase Order with PO Number - '{pk}' does not exist", status=status.HTTP_404_NOT_FOUND)
        if request.method == 'GET':
            serializer = PurchaseOrderTrackSerializer(purchase_order)
            return Response(serializer.data)
        elif request.method == 'DELETE':
            purchase_order.delete()
            return Response("Purchase Order deleted successfully")
        elif request.method == 'PUT':
            data = request.data
            data['po_number'] = pk
            serializer = PurchaseOrderSerializer(purchase_order, data)
            if serializer.is_valid():
                if data['status'].lower() == 'completed':
                    data['po_deliverd_date'] = timezone.now()
                serializer.save()
                return Response("Purchase Order updated successfully")
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        add_log(pagename, methodname, e, logging.ERROR, repr(e))
        return Response("An unexpected error occurred", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def acknowledge_po(request, pk):
    try:
        permission_classes = [IsAuthenticated]
        pagename = "views.py"
        methodname = 'acknowledge_po'
        purchase_order = PurchaseOrder.objects.get(po_number=pk)
        purchase_order.acknowledgment_date = timezone.now()
        purchase_order.save()
        return Response("Purchase Order is acknowledged")
    except PurchaseOrder.DoesNotExist as e:
        add_log(pagename, methodname, e, logging.ERROR, repr(e))
        return Response(f"Purchase Order with PO Number - '{pk}' does not exist", status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        add_log(pagename, methodname, e, logging.ERROR, repr(e))
        return Response("An unexpected error occurred", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def vendor_performance(request, pk):
    try:
        permission_classes = [IsAuthenticated]
        pagename = "views.py"
        methodname = 'vendor_performance'
        vendor = Vendor.objects.get(vendor_code=pk)
        if request.method == 'GET':
            serializer = VendorSerializer(vendor)
            return Response(serializer.data)
    except Vendor.DoesNotExist as e:
        add_log(pagename, methodname, e, logging.ERROR, repr(e))
        return Response(f"Vendor Performance Metrics with ID - '{pk}' does not exist", status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        add_log(pagename, methodname, e, logging.ERROR, repr(e))
        return Response("An unexpected error occurred", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
