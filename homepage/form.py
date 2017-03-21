from django import forms


class SearchForm(forms.Form):

    materiaux = forms.CharField(max_length=255, label="Matériaux")