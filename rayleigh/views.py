import rayleigh.utils as utils

from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import InputForm, RayleighForm

# Create your views here.
def home(request):
    if request.method == "POST":
        param = request.POST.get("choice")
        state = request.POST.get("state")
        value = request.POST.get("value")

        available_pnames = [
            "m",
            "pressure",
            "density",
            "velocity",
            "temperature",
            "total_pressure",
            "total_temperature",
            "entropy",
        ]

        M = None
        try:
            if param not in available_pnames:
                raise ValueError(
                    "param_name not recognized. Must be one of the following:\n{}".format(
                        available_pnames
                    )
                )

            value = float(value)
            if param == "m":
                M = value
                if M < 0:
                    raise ValueError("Mach number must be >= 0")
            elif param == "total_pressure":
                M = utils.m_from_critical_total_pressure_ratio(value, state)
            elif param == "total_temperature":
                M = utils.m_from_critical_total_temperature_ratio(value, state)
            elif param == "entropy":
                M = utils.m_from_critical_entropy(value, state)
            elif param == "pressure":
                M = utils.m_from_critical_pressure_ratio(value)
            elif param == "density":
                M = utils.m_from_critical_density_ratio(value)
            elif param == "temperature":
                M = utils.m_from_critical_temperature_ratio(value)
            elif param == "velocity":
                M = utils.m_from_critical_velocity_ratio(value)
            else:
                raise ValueError("Param Value not recoginized")

            return redirect("r_solver", pk=M)

        except ValueError as err:
            messages.error(request, err)

    form = InputForm()
    context = {"form": form}
    return render(request, "rayleigh/home.html", context)


def solve(request, pk):
    instance = utils.get_ratios_from_mach(float(pk))
    form = RayleighForm(instance=instance)
    context = {"form": form}
    return render(request, "results.html", context)
