from django import forms
from inscrip.models import Asistira, Sinsevi


class AsistiraForm(forms.ModelForm):
    class Meta:
        model = Asistira
        #solo se listan los campos que se rellenan desde formulario.
        fields = ['cve_curso']


class SinseviForm(forms.ModelForm):
    class Meta:
        model = Sinsevi
        #solo se listan los campos que se rellenan desde formulario.
        fields = ['cve_curso', 'cve_academic']
