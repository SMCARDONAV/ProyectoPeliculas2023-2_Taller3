from django.forms import ModelForm, Textarea
from django import forms

class TableForm(forms.Form):

    descrp = forms.CharField(label='Descripción de la pelicula que desea buscar:')