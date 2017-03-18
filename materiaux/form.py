from django import forms
from materiaux.models import SousFamille, Image
from propriete.models import Propriete
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

class MateriauForm(forms.Form):

    nom = forms.CharField(max_length=255, label="Nom Générique")
    ss_famille = forms.ModelChoiceField(label="Sous-familles", queryset=SousFamille.objects.all().order_by('famille__slug'))
    fournisseur = forms.CharField(max_length=255, label="Fournisseur", initial="N.R.")
    normatif = forms.CharField(max_length=255, label="Critère normatif", initial="N.R.")
    disponible = forms.BooleanField(label="Objet disponible", required=False)
    image = forms.ImageField(label='Sélectionner une image', help_text='Maximum. 50 MB', required=False)


    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        for propriete in Propriete.objects.all():
            self.fields[propriete.slug] = forms.FloatField(label=str(propriete.slug), required=False)

    def clean_content(self):
        content = self.cleaned_data['image']
        content_type = content.content_type.split('/')[0]
        if content_type in settings.CONTENT_TYPES:
            if content._size > settings.MAX_UPLOAD_SIZE:
                raise forms.ValidationError(_('Veuillez sélectionner une image en dessous de %s. La taille actuelle est de %s') % (
                filesizeformat(settings.MAX_UPLOAD_SIZE), filesizeformat(content._size)))
        else:
            raise forms.ValidationError(_('File type is not supported'))
        return content