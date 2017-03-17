from django import forms
from materiaux.models import SousFamille
from propriete.models import Propriete

class MateriauForm(forms.Form):


    nom = forms.CharField(max_length=255, label="Nom Générique")
    ss_famille = forms.ModelChoiceField(label="Sous-familles", queryset=SousFamille.objects.all().order_by('famille__slug'))
    fournisseur = forms.CharField(max_length=255, label="Fournisseur", initial="N.R.")
    normatif = forms.CharField(max_length=255, label="Critère normatif", initial="N.R.")
    disponible = forms.BooleanField(label="Objet disponible", required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        for propriete in Propriete.objects.all():
            self.fields[propriete.slug] = forms.FloatField(label=str(propriete.slug), required=False)