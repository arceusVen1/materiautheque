from django.shortcuts import render, render_to_response
from materiaux.models import Materiau
from homepage.form import SearchForm
import re

# Create your views here.
def home(request):
    last_matx = Materiau.objects.order_by('date')[:5]
    regexp = re.compile(r"\w+")
    search_form = SearchForm(request.POST or None)
    if search_form.is_valid():
        materiaux_criteria = search_form.cleaned_data["materiaux"]
        criteria = regexp.findall(materiaux_criteria)
        materiaux = []
        for crit in criteria:
            materiaux += Materiau.objects.filter(nom__contains=crit)
            materiaux += Materiau.objects.filter(slug__contains=crit)
            materiaux += Materiau.objects.filter(usage__contains=crit)
            materiaux += Materiau.objects.filter(fournisseur__contains=crit)
        return render_to_response("materiautheque/results.html", {"materiaux": materiaux, "cri": materiaux_criteria})
    return render(request, 'materiautheque/homepage.html', {'last_matx': last_matx, "form": search_form})