from django.db import models

# Create your models here.
class Input(models.Model):
    INPUT_CHOICES = (
        ("m", "Mach number"),
        ("pressure", "Critical Pressure Ratio"),
        ("density", "Critical Density Ratio"),
        ("temperature", "Critical Temperature Ratio"),
        ("total_pressure", "Critical Total Pressure Ratio"),
        ("total_temperature", "Critical Total Temperature Ratio"),
        ("velocity", "Critical Velocity Ratio"),
        ("entropy", "Entropy Parameter"),
    )

    INPUT_STATE = (
        ("sub", "Subsonic"),
        ("super", "Supersonic"),
    )

    choice = models.CharField(max_length=100, choices=INPUT_CHOICES, default="m")
    state = models.CharField(max_length=50,choices=INPUT_STATE,default="sub")


class Rayleigh(models.Model):
    mach = models.CharField(max_length=20, blank=True)
    pressure_ratio = models.CharField(max_length=20, blank=True)
    density_ratio = models.CharField(max_length=20, blank=True)
    temperature_ratio = models.CharField(max_length=20, blank=True)
    total_pressure_ratio = models.CharField(max_length=20, blank=True)
    velocity_ratio = models.CharField(max_length=20, blank=True)
    total_temperature_ratio = models.CharField(max_length=20, blank=True)
    entropy = models.CharField(max_length=20, blank=True)