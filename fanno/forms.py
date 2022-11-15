from django.forms import ModelForm
from .models import Fanno, Input

class InputForm(ModelForm):
    class Meta:
        model = Input
        fields = '__all__'


class FannoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(FannoForm, self).__init__(*args, **kwargs)
        for key in self.fields.keys():
            self.fields[key].widget.attrs['readonly'] = True

    class Meta:
        model = Fanno
        fields = '__all__'