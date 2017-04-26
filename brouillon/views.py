from django.shortcuts import render
from django.urls import reverse
from brouillon.models import *
from brouillon.form import *
from propriete.models import *
from django.http import Http404, HttpResponseRedirect
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.urls import reverse_lazy, reverse


# Create your views here.


def show_brouillon(request, slug):
    """
    Retourne un materiau à la vue selon la référence

    :param request: La requête client
    :type request: HttpRequest
    :param slug: la référence du matériau (MAT-FA-SS-ID)
    :type slug: str
    :return: le template associé à un matériaux
    :rtype: HttpResponse

    :raises Http404: si le materiau n'existe pas
    """
    try:
        mat = Brouillon.objects.get(slug=slug)
        proprietes = mat.get_proprietes()
        for i in range(len(proprietes)):
            try:
                prop = Propriete.objects.get(id=proprietes[i]["id"])
                proprietes[i]["slug"] = prop.slug
                proprietes[i]["unite"] = prop.unite
            except Propriete.DoesNotExist:
                del proprietes[i]
    except Brouillon.DoesNotExist:
        raise Http404("La référence de l'objet n'existe pas")
    return render(request, "brouillon/brouillon_show.html", {'mat': mat, "proprietes": proprietes})


def to_materiau(request, slug):
    try:
        brouillon = Brouillon.objects.get(slug=slug)
    except Brouillon.DoesNotExist:
        raise Http404("La référence du brouillon n'existe pas")
    mat = Materiau(nom=brouillon.nom, ss_famille=brouillon.ss_famille,
                   fournisseur=brouillon.fournisseur, usage=brouillon.usage,
                   disponible=brouillon.disponible, proprietes=brouillon.proprietes, normatif=brouillon.normatif)
    mat.save()
    brouillon.delete()
    return render(request, "materiaux/materiaux_show.html", {"mat": mat})

def create_or_edit_brouillon(request, slug=None):
    """
    Permet la création ou l'édition d'un brouillon.
    Si une référence de matériau est passé à la vue ce dernier est récupéré et ses valeurs initiale sont chargées
    dans le formulaire d'édition. Les valeurs par défaut des prorpiétés est mis à -1. Cette valeur est prise par défaut
    et permet de comprendre son non-traitement nécessaire lors de la vue d'affichage du matériau

    :param request: La requête client
    :type request: HttpRequest
    :param slug: (optionnel) La référence du matériau dans le cas d'une édition
    :type slug: str
    :return: Le template associé au formulaire de création ou d'édition d'un matériau
    :rtype: HttpResponse
    """
    mat = None
    if slug is not None:
        try:
            mat = Brouillon.objects.get(slug=slug)
        except Brouillon.DoesNotExist:
            raise Http404("la référence de l'objet n'existe pas")
    initial = {}
    template = 'brouillon/brouillon_create.html'
    if mat is not None:
        initial = dict(nom=mat.nom, ss_famille=mat.ss_famille, fournisseur=mat.fournisseur, normatif=mat.normatif,
                       disponible=mat.disponible)
        proprietes = mat.get_proprietes()
        for propriete in proprietes:
            try:
                initial[Propriete.objects.get(id=propriete["id"]).slug] = propriete["valeur"]
            except Propriete.DoesNotExist:
                pass
        template = 'materiaux/materiau_update.html'
    form = BrouillonForm(request.POST or None, request.FILES, initial=initial)
    if form.is_valid():
        proprietes = []
        nom = form.cleaned_data["nom"]
        ss_famille = form.cleaned_data['ss_famille']
        fournisseur = form.cleaned_data["fournisseur"]
        normatif = form.cleaned_data["normatif"]
        disponible = form.cleaned_data["disponible"]
        for propriete in Propriete.objects.all():
            if form.cleaned_data[propriete.slug] is None:
                proprietes.append({"id": propriete.id, "valeur": -1})
            else:
                proprietes.append({"id": propriete.id, "valeur": float(form.cleaned_data[propriete.slug])})
        if mat is not None:
            mat.nom = nom
            mat.ss_famille = ss_famille
            mat.fournisseur = fournisseur
            mat.normatif = normatif
            mat.disponible = disponible
        else:
            mat = Brouillon(nom=nom, ss_famille=ss_famille, fournisseur=fournisseur, normatif=normatif,
                           disponible=disponible)
        mat.set_proprietes(proprietes)
        mat.save()
        return HttpResponseRedirect(reverse('brouillon_path', args=[mat.slug]))
    return render(request, template, {'form': form})


def index(request):
    brouillons = Brouillon.objects.all()
    return render(request, 'brouillon/brouillons_index.html', {'brouillons': brouillons})


class DeleteBrouillon(DeleteView):
    """
    Permet la suppression d'un brouillon de manière générique
    """
    model = Brouillon
    success_url = reverse_lazy('brouillons_path')