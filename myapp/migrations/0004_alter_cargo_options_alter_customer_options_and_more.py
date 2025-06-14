# Generated by Django 5.1.7 on 2025-05-07 19:04

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_alter_shipment_status_alter_vehicle_vehicle_type'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cargo',
            options={'ordering': ['-created_at']},
        ),
        migrations.AlterModelOptions(
            name='customer',
            options={'ordering': ['-created_at']},
        ),
        migrations.AlterModelOptions(
            name='driver',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='shipment',
            options={'ordering': ['-departure_time']},
        ),
        migrations.AlterModelOptions(
            name='vehicle',
            options={'ordering': ['vehicle_number']},
        ),
        migrations.RemoveField(
            model_name='shipment',
            name='driver',
        ),
        migrations.AddField(
            model_name='vehicle',
            name='driver',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='vehicle', to='myapp.driver'),
        ),
        migrations.AlterField(
            model_name='cargo',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cargos', to='myapp.customer'),
        ),
        migrations.AlterField(
            model_name='cargo',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('in_transit', 'In Transit'), ('delivered', 'Delivered'), ('cancelled', 'Cancelled')], db_index=True, default='pending', max_length=20),
        ),
        migrations.AlterField(
            model_name='cargo',
            name='tracking_number',
            field=models.CharField(db_index=True, max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='cargo',
            name='weight',
            field=models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0.01)]),
        ),
        migrations.AlterField(
            model_name='customer',
            name='email',
            field=models.EmailField(db_index=True, max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='driver',
            name='license_number',
            field=models.CharField(db_index=True, max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='driver',
            name='status',
            field=models.CharField(choices=[('available', 'Available'), ('on_duty', 'On Duty'), ('off_duty', 'Off Duty')], db_index=True, default='available', max_length=20),
        ),
        migrations.AlterField(
            model_name='shipment',
            name='cargo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shipments', to='myapp.cargo'),
        ),
        migrations.AlterField(
            model_name='shipment',
            name='status',
            field=models.CharField(choices=[('scheduled', 'Scheduled'), ('in_transit', 'In Transit'), ('completed', 'Completed'), ('cancelled', 'Cancelled'), ('delayed', 'Delayed')], db_index=True, default='scheduled', max_length=20),
        ),
        migrations.AlterField(
            model_name='shipment',
            name='tracking_number',
            field=models.CharField(db_index=True, max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='shipment',
            name='vehicle',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shipments', to='myapp.vehicle'),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='capacity',
            field=models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0.01)]),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='status',
            field=models.CharField(choices=[('available', 'Available'), ('in_use', 'In Use'), ('maintenance', 'Under Maintenance')], db_index=True, default='available', max_length=20),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='vehicle_number',
            field=models.CharField(db_index=True, max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='vehicle_type',
            field=models.CharField(choices=[('truck', 'Truck'), ('van', 'Van'), ('pickup', 'Pickup'), ('plane', 'Plane'), ('ship', 'Ship')], db_index=True, max_length=20),
        ),
        migrations.AddIndex(
            model_name='cargo',
            index=models.Index(fields=['status', 'created_at'], name='myapp_cargo_status_9318ee_idx'),
        ),
        migrations.AddIndex(
            model_name='customer',
            index=models.Index(fields=['name'], name='myapp_custo_name_2ac257_idx'),
        ),
        migrations.AddIndex(
            model_name='driver',
            index=models.Index(fields=['status'], name='myapp_drive_status_6b54fc_idx'),
        ),
        migrations.AddIndex(
            model_name='shipment',
            index=models.Index(fields=['status', 'departure_time'], name='myapp_shipm_status_18a858_idx'),
        ),
        migrations.AddIndex(
            model_name='vehicle',
            index=models.Index(fields=['status', 'vehicle_type'], name='myapp_vehic_status_edf222_idx'),
        ),
    ]
