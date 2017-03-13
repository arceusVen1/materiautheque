from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.http import Http404
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from propriete.models import Propriete

# Create your views here.

# Proprietes section --------------------------------------------------------------------------------------------------


def index(request):
    proprietes = Propriete.objects.all()
    return render(request, "propriete/index.html", {'proprietes': proprietes})


def show_propriete(request, slug):
    """
    Retourne un materiau à la vue selon la référence

    :param request: the request
    :type request: HttpRequest
    :param slug: le nom de la proprietes
    :type slug: str
    :return: proprietes/show.html

    :raises Http404: si le materiau n'existe pas
    """
    try:
        prop = Propriete.objects.get(slug=slug)
    except Propriete.DoesNotExist:
        raise Http404("La propriété n'existe pas")
    return render(request, "propriete/show.html", {'prop': prop})


class UpdatePropriete(UpdateView):
    """
    Permet la mise à jour d'une proprietes via le template propriete_form.html
    Inclu dans les urls par la méthode as_view()
    """
    model = Propriete
    fields = ['slug', 'unite', 'definition']


class CreatePropriete(CreateView):
    """
    Permet la création d'une proriete de manière générique
    """
    model = Propriete
    fields = ['slug', 'unite', 'definition']


class DeletePropriete(DeleteView):
    """
    Permet la suppression d'une propriété de manière générique
    """
    model = Propriete
    success_url = reverse_lazy('proprietes_path')