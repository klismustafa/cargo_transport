from django.urls import path
from .views import (
    CargoListCreateView, CargoDetailView,
    VehicleListCreateView, VehicleDetailView,
    DriverListCreateView, DriverDetailView,
    ShipmentListCreateView, ShipmentDetailView,
    CustomerListCreateView, CustomerDetailView
)
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),  # Add this line for the home page
    path('cargos/', CargoListCreateView.as_view(), name='cargo-list'),
    path('cargos/<int:pk>/', CargoDetailView.as_view(), name='cargo-detail'),
    path('vehicles/', VehicleListCreateView.as_view(), name='vehicle-list'),
    path('vehicles/<int:pk>/', VehicleDetailView.as_view(), name='vehicle-detail'),
    path('drivers/', DriverListCreateView.as_view(), name='driver-list'),
    path('drivers/<int:pk>/', DriverDetailView.as_view(), name='driver-detail'),
    path('shipments/', ShipmentListCreateView.as_view(), name='shipment-list'),
    path('shipments/<int:pk>/', ShipmentDetailView.as_view(), name='shipment-detail'),
    path('customers/', CustomerListCreateView.as_view(), name='customer-list'),
    path('customers/<int:pk>/', CustomerDetailView.as_view(), name='customer-detail'),
    path('tracking/', views.tracking_view, name='tracking'),
    path('api/shipments/track/<str:tracking_number>/', views.track_shipment, name='track-shipment'),
]