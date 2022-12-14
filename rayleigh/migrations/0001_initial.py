# Generated by Django 4.1.3 on 2022-11-15 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Input",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "choice",
                    models.CharField(
                        choices=[
                            ("m", "Mach number"),
                            ("pressure", "Critical Pressure Ratio"),
                            ("density", "Critical Density Ratio"),
                            ("temperature", "Critical Temperature Ratio"),
                            ("total_pressure", "Critical Total Pressure Ratio"),
                            ("total_temperature", "Critical Total Temperature Ratio"),
                            ("velocity", "Critical Velocity Ratio"),
                            ("entropy", "Entropy Parameter"),
                        ],
                        default="m",
                        max_length=100,
                    ),
                ),
                (
                    "state",
                    models.CharField(
                        choices=[("sub", "Subsonic"), ("super", "Supersonic")],
                        default="sub",
                        max_length=50,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Rayleigh",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("mach", models.CharField(blank=True, max_length=20)),
                ("pressure_ratio", models.CharField(blank=True, max_length=20)),
                ("density_ratio", models.CharField(blank=True, max_length=20)),
                ("temperature_ratio", models.CharField(blank=True, max_length=20)),
                ("total_pressure_ratio", models.CharField(blank=True, max_length=20)),
                ("velocity_ratio", models.CharField(blank=True, max_length=20)),
                (
                    "total_temperature_ratio",
                    models.CharField(blank=True, max_length=20),
                ),
                ("entropy", models.CharField(blank=True, max_length=20)),
            ],
        ),
    ]
