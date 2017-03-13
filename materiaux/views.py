from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.http import Http404
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from materiaux.models import Materiau, Famille, SousFamille


# Create your views here.

# Materiaux section ----------------------------------------------------------------------------------------------------

def index(request):
    materiaux = Materiau.objects.all()
    return render(request, 'materiaux/materiaux_index.html', {'materiaux': materiaux})


def show_materiau(request, slug):
    """
    Retourne un materiau à la vue selon la référence

    :param request: the request
    :type request: HttpRequest
    :param slug: la référence du matériau (MAT-FA-SS-ID)
    :type slug: str
    :return: materiau/materiaux_show.html

    :raises Http404: si le materiau n'existe pas
    """
    try:
        mat = Materiau.objects.get(slug=slug)
    except Materiau.DoesNotExist:
        raise Http404("La référence de l'objet n'existe pas")
    return render(request, "materiaux/materiaux_show.html", {'mat': mat})


class CreateMateriau(CreateView):
    """
    Permet la création d'un matériau de manière générique
    """
    model = Materiau
    fields = ['ss_famille', 'fournisseur', 'usage', 'normatif', 'disponible']
    template_name_suffix = "_create"


class UpdateMateriau(UpdateView):
    """
    Permet la mise à jour d'un materiau via le template materiau_form.html
    Inclut dans les urls par la méthode as_view()
    """
    model = Materiau
    fields = ['ss_famille', 'fournisseur', 'usage', 'normatif', 'disponible']
    template_name_suffix = '_update'


class DeleteMateriau(DeleteView):
    """
    Permet la suppression d'un matériau de manière générique
    """
    model = Materiau
    success_url = reverse_lazy('materiaux_path')


# end Materiaux section-------------------------------------------------------------------------------------------------


# start Sous-Famille section--------------------------------------------------------------------------------------------


def sousFamille_index(request):
    ss_fams = SousFamille.objects.all()
    return render(request, 'materiaux/sousFamille_index.html', {'ss_fams': ss_fams})


def show_sousFamille(request, pk):
    """
    Retourne une sous-famille à la vue selon la référence

    :param request: the request
    :type request: HttpRequest
    :param pk: la référence de la sousfamille (SS-00)
    :type pk: str
    :return: materiau/materiaux_show.html

    :raises Http404: si la sousfamille n'existe pas
    """
    try:
        ss_fam = SousFamille.objects.get(reference=pk)
    except SousFamille.DoesNotExist:
        raise Http404("La référence de la sous-famille n'existe pas")
    return render(request, "materiaux/sousFamille_show.html", {'ss_fam': ss_fam})


class CreateSousFamille(CreateView):
    """
    Permet la création d'un matériau de manière générique
    """
    model = SousFamille
    fields = ['matiere', 'famille']
    template_name_suffix = "_create"


class UpdateSousFamille(UpdateView):
    """
    Permet la mise à jour d'un materiau via le template materiau_form.html
    Inclut dans les urls par la méthode as_view()
    """
    model = SousFamille
    fields = ['matiere', 'famille']
    template_name_suffix = "_update"

class DeleteSousFamille(DeleteView):
    """
    Permet la suppression d'un matériau de manière générique
    """
    model = SousFamille
    success_url = reverse_lazy('sousFamilles_path')

# end Sous-Famille section----------------------------------------------------------------------------------------------

# start Famille section-------------------------------------------------------------------------------------------------

def famille_index(request):
    familles = Famille.objects.all()
    return render(request, 'materiaux/famille_index.html', {'familles': familles})

def show_famille(request, pk):
    """
    Retourne une sous-famille à la vue selon la référence

    :param request: the request
    :type request: HttpRequest
    :param pk: la référence de la sousfamille (SS-00)
    :type pk: str
    :return: materiau/materiaux_show.html

    :raises Http404: si la sousfamille n'existe pas
    """
    try:
        famille = Famille.objects.get(abrege=pk)
    except Famille.DoesNotExist:
        raise Http404("La référence de la famille n'existe pas")
    return render(request, "materiaux/famille_show.html", {'famille': famille})


class CreateFamille(CreateView):
    """
    Permet la création d'un matériau de manière générique
    """
    model = Famille
    fields = ['matiere', 'abrege']
    template_name_suffix = "_create"


class UpdateFamille(UpdateView):
    """
    Permet la mise à jour d'un materiau via le template materiau_form.html
    Inclut dans les urls par la méthode as_view()
    """
    model = Famille
    fields = ['matiere', 'abrege']
    template_name_suffix = "_update"


class DeleteFamille(DeleteView):
    """
    Permet la suppression d'un matériau de manière générique
    """
    model = Famille
    success_url = reverse_lazy('familles_path')