from django.forms import ModelForm
from .models import Input, Rayleigh

class InputForm(ModelForm):
    class Meta:
        model = Input
        fields = '__all__'


class RayleighForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(RayleighForm, self).__init__(*args, **kwargs)
        for key in self.fields.keys():
            self.fields[key].widget.attrs['readonly'] = True

    class Meta:
        model = Rayleigh
        fields = '__all__'