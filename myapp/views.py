from rest_framework import generics
from .models import Cargo, Vehicle, Driver, Shipment, Customer
from .serializers import (
    CargoSerializer, 
    VehicleSerializer, 
    DriverSerializer, 
    ShipmentSerializer, 
    CustomerSerializer
)
from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Shipment
from django.views.decorators.http import require_http_methods

class CargoListCreateView(generics.ListCreateAPIView):
    queryset = Cargo.objects.all()
    serializer_class = CargoSerializer

class CargoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cargo.objects.all()
    serializer_class = CargoSerializer

class VehicleListCreateView(generics.ListCreateAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer

class VehicleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer

class DriverListCreateView(generics.ListCreateAPIView):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer

class DriverDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer

class ShipmentListCreateView(generics.ListCreateAPIView):
    queryset = Shipment.objects.all()
    serializer_class = ShipmentSerializer

class ShipmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Shipment.objects.all()
    serializer_class = ShipmentSerializer

class CustomerListCreateView(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class CustomerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

def home_view(request):
    """
    Render the home page template
    """
    return render(request, 'home.html')

@require_http_methods(["GET"])
def tracking_view(request):
    """
    Render the tracking page template
    """
    return render(request, 'tracking.html')

@require_http_methods(["GET"])
def track_shipment(request, tracking_number):
    """
    API endpoint to get shipment tracking details
    """
    shipment = get_object_or_404(Shipment, tracking_number=tracking_number)
    
    # In a real application, you would get these coordinates from a GPS tracking system
    # For demo purposes, we'll use dummy coordinates based on the current_location
    current_location_coordinates = {
        'lat': 40.7128,  # Example: New York coordinates
        'lng': -74.0060
    }
    
    data = {
        'status': shipment.status,
        'origin': shipment.origin,
        'destination': shipment.destination,
        'current_location': shipment.current_location,
        'arrival_time': shipment.arrival_time.isoformat(),
        'current_location_coordinates': current_location_coordinates,
        'cargo_description': shipment.cargo.description,
        'vehicle_info': str(shipment.vehicle),
        'drivers': [str(driver) for driver in shipment.drivers.all()]
    }
    
    return JsonResponse(data)
    