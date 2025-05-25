from django.db import models
from django.core.validators import MinValueValidator

class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, db_index=True)
    phone_number = models.CharField(max_length=20)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return self.name

class Driver(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('on_duty', 'On Duty'),
        ('off_duty', 'Off Duty'),
    ]

    name = models.CharField(max_length=100)
    license_number = models.CharField(max_length=50, unique=True, db_index=True)
    phone_number = models.CharField(max_length=20)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available', db_index=True)
    current_location = models.CharField(max_length=200, null=True, blank=True)
    vehicles = models.ManyToManyField('Vehicle', related_name='drivers', blank=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return self.name

    def get_current_shipment(self):
        active_shipments = self.shipments.filter(status='in_transit')
        return active_shipments.first()

class Vehicle(models.Model):
    VEHICLE_TYPES = [
        ('truck', 'Truck'),
        ('van', 'Van'),
        ('pickup', 'Pickup'),
        ('plane', 'Plane'),
        ('ship', 'Ship'),
    ]
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('in_use', 'In Use'),
        ('maintenance', 'Under Maintenance'),
    ]

    vehicle_number = models.CharField(max_length=50, unique=True, db_index=True)
    vehicle_type = models.CharField(max_length=20, choices=VEHICLE_TYPES, db_index=True)
    capacity = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available', db_index=True)
    # Removed the OneToOneField driver field and replaced with ManyToMany in Driver model

    class Meta:
        ordering = ['vehicle_number']
        indexes = [
            models.Index(fields=['status', 'vehicle_type']),
        ]

    def __str__(self):
        return f"{self.vehicle_number} - {self.vehicle_type}"

    def get_available_drivers(self):
        return self.drivers.filter(status='available')

class Cargo(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('assigned', 'Assigned'),
        ('in_transit', 'In Transit'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    tracking_number = models.CharField(max_length=50, unique=True, db_index=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='cargos')
    description = models.TextField()
    weight = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    current_location = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'created_at']),
        ]

    def __str__(self):
        return f"{self.tracking_number} - {self.description}"

class Shipment(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('in_transit', 'In Transit'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('delayed', 'Delayed'),
    ]

    tracking_number = models.CharField(max_length=50, unique=True, db_index=True)
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE, related_name='shipments')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='shipments')
    drivers = models.ManyToManyField(Driver, related_name='shipments')  # Changed from ForeignKey to ManyToManyField
    origin = models.CharField(max_length=200)
    destination = models.CharField(max_length=200)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled', db_index=True)
    current_location = models.CharField(max_length=200, null=True, blank=True)
    notes = models.TextField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-departure_time']
        indexes = [
            models.Index(fields=['status', 'departure_time']),
        ]

    def __str__(self):
        return f"Shipment {self.tracking_number}"

    def save(self, *args, **kwargs):
        if self.status == 'in_transit':
            # Update cargo status
            self.cargo.status = 'in_transit'
            self.cargo.current_location = self.current_location
            self.cargo.save()
            
            # Update drivers status
            for driver in self.drivers.all():
                driver.status = 'on_duty'
                driver.current_location = self.current_location
                driver.save()
            
            # Update vehicle status
            self.vehicle.status = 'in_use'
            self.vehicle.save()
        
        elif self.status == 'completed':
            # Update related models' statuses
            self.cargo.status = 'delivered'
            self.cargo.current_location = self.destination
            self.cargo.save()
            
            # Update all drivers status
            for driver in self.drivers.all():
                driver.status = 'available'
                driver.current_location = self.destination
                driver.save()
            
            self.vehicle.status = 'available'
            self.vehicle.save()
        
        super().save(*args, **kwargs)
