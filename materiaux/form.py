from django import forms
from materiaux.models import SousFamille
from propriete.models import Propriete

class MateriauForm(forms.Form):


    #FAMILLE_CHOICES = [(ssfamille.reference, ssfamille.reference + " - " + ssfamille.matiere) for ssfamille in SousFamille.objects.all()]
    ssfamille = forms.ModelChoiceField(label="Sous-familles", queryset=SousFamille.objects.all())
    fournisseur = forms.CharField(max_length=255, label="Fournisseur", initial="N.R.")
    normatif = forms.CharField(max_length=255, label="Critère normatif")
    disponible = forms.BooleanField(label="Objet disponible")

    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        for propriete in Propriete.objects.all():
            self.fields[propriete.slug] = forms.DecimalField(label=str(propriete.slug))