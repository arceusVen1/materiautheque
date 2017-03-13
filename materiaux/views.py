from django.shortcuts import render, redirect
from django.http import Http404
from django.views.generic.edit import UpdateView, CreateView
from materiaux.models import Materiau, Famille, SousFamille


# Create your views here.

# Materiaux section ----------------------------------------------------------------------------------------------------
def index(request):
    materiaux = Materiau.objects.all()
    return render(request, 'materiaux/index.html', {'materiaux': materiaux})


def show_materiau(request, slug):
    """
    Retourne un materiau à la vue selon la référence

    :param request: the request
    :type request: HttpRequest
    :param slug: la référence du matériau (MAT-FA-SS-ID)
    :type slug: str
    :return: materiau/show.html

    :raises Http404: si le materiau n'existe pas
    """
    try:
        mat = Materiau.objects.get(slug=slug)
    except Materiau.DoesNotExist:
        raise Http404("La référence de l'objet n'existe pas")
    return render(request, "materiaux/show.html", {'mat': mat})


def delete_materiau(request, slug):
    """

    :param request: la requête
    :type request: HttpRequest
    :param slug: la référence du matériau (MAT-FA-SS-ID)
    :type slug: str
    :return: redirige vers l'index

    :raises Http404: si le materiau n'existe pas
    """
    try:
        mat = Materiau.objects.get(slug=slug)
    except Materiau.DoesNotExist:
        raise Http404("La référence de l'objet n'existe pas")
    mat.delete()
    return redirect(index)


class UpdateMateriau(UpdateView):
    """
    Permet la mise à jour d'un materiau via le template materiau_form.html
    Inclut dans les urls par la méthode as_view()
    """
    model = Materiau
    fields = ['ss_famille', 'fournisseur', 'usage', 'normatif', 'disponible']
    template_name_suffix = '_form'

class CreateMateriau(CreateView):
    """
    Permet la création d'un matériau de manière générique
    """
    model = Materiau
    fields = ['ss_famille', 'fournisseur', 'usage', 'normatif', 'disponible']
    template_name_suffix = '_form'