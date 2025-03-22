
from django.contrib import admin
from .models import Cargo, Vehicle, Driver, Shipment, Customer

@admin.register(Cargo)
class CargoAdmin(admin.ModelAdmin):
    list_display = ('tracking_number', 'description', 'weight', 'status', 'created_at')
    search_fields = ('tracking_number', 'description')
    list_filter = ('status', 'created_at')

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('vehicle_number', 'vehicle_type', 'capacity', 'status')
    search_fields = ('vehicle_number',)
    list_filter = ('vehicle_type', 'status')

@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ('name', 'license_number', 'phone_number', 'status')
    search_fields = ('name', 'license_number')
    list_filter = ('status',)

@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = ('tracking_number', 'origin', 'destination', 'status', 'departure_time', 'arrival_time')
    search_fields = ('tracking_number', 'origin', 'destination')
    list_filter = ('status', 'departure_time')

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number', 'address')
    search_fields = ('name', 'email')
