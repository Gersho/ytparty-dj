from django.forms import ModelForm
from .models import Song

class AddCatalogForm(ModelForm):
    class Meta:
        model = Song
        #fields = '__all__'
        exclude = ['genre','language']
