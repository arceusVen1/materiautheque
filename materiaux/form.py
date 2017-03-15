from django import forms
from materiaux.models import SousFamille
from propriete.models import Propriete

class MateriauForm(forms.Form):


    #FAMILLE_CHOICES = [(ssfamille.reference, ssfamille.reference + " - " + ssfamille.matiere) for ssfamille in SousFamille.objects.all()]
    nom = forms.CharField(max_length=255, label="Nom Générique")
    ss_famille = forms.ModelChoiceField(label="Sous-familles", queryset=SousFamille.objects.all())
    fournisseur = forms.CharField(max_length=255, label="Fournisseur", initial="N.R.")
    normatif = forms.CharField(max_length=255, label="Critère normatif", initial="N.R.")
    disponible = forms.BooleanField(label="Objet disponible")

    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        for propriete in Propriete.objects.all():
            self.fields[propriete.slug] = forms.FloatField(label=str(propriete.slug))