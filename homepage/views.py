from django.shortcuts import render, render_to_response
from materiaux.models import Materiau
from homepage.form import SearchForm

# Create your views here.
def home(request):
    last_matx = Materiau.objects.order_by('date')[:5]
    search_form = SearchForm(request.POST or None)
    if search_form.is_valid():
        materiaux_criteria = search_form.cleaned_data["materiaux"]
        materiaux = []
        materiaux += Materiau.objects.filter(nom__contains=materiaux_criteria)
        materiaux += Materiau.objects.filter(slug__contains=materiaux_criteria)
        materiaux += Materiau.objects.filter(usage__contains=materiaux_criteria)
        materiaux += Materiau.objects.filter(fournisseur__contains=materiaux_criteria)
        return render_to_response("materiautheque/results.html", {"materiaux": materiaux, "cri": materiaux_criteria})
    return render(request, 'materiautheque/homepage.html', {'last_matx': last_matx, "form": search_form})