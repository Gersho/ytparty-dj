from django import forms
from .models import Artist, Genre, Language, Song, Group, WaitList, Actions, Blocus



class AddCatalogForm(forms.Form):

    title = forms.CharField(required=True)
    ytid = forms.CharField(required=True, disabled=True)
    artist = forms.ModelMultipleChoiceField(queryset=Artist, required=False)
    group = forms.ModelChoiceField(queryset=Group, required=False)
    duration = forms.CharField(required=True, disabled=True)
    img = forms.CharField(required=True)
