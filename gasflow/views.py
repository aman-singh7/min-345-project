from django.shortcuts import render

def home(request):
    context = {
        'solvers': {
            # Name       : Url
            'Fanno Flow': 'f_home',
            'Rayleigh Flow': 'r_home',
        }
    }
    return render(request, 'home.html', context)