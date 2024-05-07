"""
URL configuration for vendor_manage_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from vendor_manage_app import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/vendors/', views.vendor_profile),
    path('api/vendors/<str:pk>/', views.vendor_profile_management),
    path('api/purchase_orders/', views.purchase_order_track),
    path('api/purchase_orders/<str:pk>', views.purchase_order_management),
    path('api/purchase_orders/<str:pk>/acknowledge', views.acknowledge_po),
    path('api/vendors/<str:pk>/performance', views.vendor_performance),
    path('api/generate_token/', views.VendorTokenObtainPairView.as_view(), name='vendor-token'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
