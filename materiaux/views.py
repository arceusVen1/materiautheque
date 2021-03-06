from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.http import Http404, HttpResponseRedirect
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from materiaux.models import Materiau, Famille, SousFamille, Image
from materiaux.form import MateriauForm, ImageForm
from propriete.models import Propriete
from io import BytesIO
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from html import escape


# Create your views here.

# PDF rendering section ------------------------------------------------------------------------------------------------

def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    context = Context(context_dict)
    html = template.render(context)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))


# Materiaux section ----------------------------------------------------------------------------------------------------

def index(request):
    """
    Retourne la liste complètes des matériaux

    :param request: La requête du client
    :type request: HttpRequest
    :return: le template associé à la liste des matériaux
    :rtype: HttpResponse
    """
    materiaux = Materiau.objects.all()
    return render(request, 'materiaux/materiaux_index.html', {'materiaux': materiaux})


def show_materiau(request, slug):
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
        mat = Materiau.objects.get(slug=slug)
        proprietes = mat.get_proprietes()
        for i in range(len(proprietes)):
            try:
                prop = Propriete.objects.get(id=proprietes[i]["id"])
                proprietes[i]["slug"] = prop.slug
                proprietes[i]["unite"] = prop.unite
            except Propriete.DoesNotExist:
                del proprietes[i]
    except Materiau.DoesNotExist:
        raise Http404("La référence de l'objet n'existe pas")
    return render(request, "materiaux/materiaux_show.html", {'mat': mat, "proprietes": proprietes})


def create_or_edit_materiau(request, slug=None):
    """
    Permet la création ou l'édition d'un matériau.
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
            mat = Materiau.objects.get(slug=slug)
        except Materiau.DoesNotExist:
            raise Http404("la référence de l'objet n'existe pas")
    initial = {}
    template = 'materiaux/materiau_create.html'
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
    form = MateriauForm(request.POST or None, request.FILES, initial=initial)
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
            mat = Materiau(nom=nom, ss_famille=ss_famille, fournisseur=fournisseur, normatif=normatif,
                           disponible=disponible)
        mat.set_proprietes(proprietes)
        mat.save()
        return HttpResponseRedirect(reverse('materiau_path', args=[mat.slug]))
    return render(request, template, {'form': form})


class DeleteMateriau(DeleteView):
    """
    Permet la suppression d'un matériau de manière générique
    """
    model = Materiau
    success_url = reverse_lazy('materiaux_path')


def generate_pdf_materiau(request, slug):
    """
    Permet la génération du pdf
    """
    try:
        mat = Materiau.objects.get(slug=slug)
        proprietes = mat.get_proprietes()
        for i in range(len(proprietes)):
            prop = Propriete.objects.get(id=proprietes[i]["id"])
            proprietes[i]["slug"] = prop.slug
    except Materiau.DoesNotExist:
        raise Http404("La référence de l'objet n'existe pas")
    return render_to_pdf(
            'materiaux/materiaux_show.html', {'mat': mat, "proprietes": proprietes}
        )


def add_image(request):
    form = ImageForm(request.POST or None, request.FILES)
    if form.is_valid():
        image = form.save()
        return HttpResponseRedirect(reverse('image_path', args=[image.id]))
    return render(request, 'materiaux/materiau_add_image.html', locals())


def show_image(request, id):
    try:
        image = Image.objects.get(id=id)
    except Image.DoesNotExist:
        raise Http404("La référence de l'image n'existe pas")
    return render(request, "materiaux/image_show.html", {'image' : image})






# end Materiaux section-------------------------------------------------------------------------------------------------


# start Sous-Famille section--------------------------------------------------------------------------------------------


def sousFamille_index(request):
    ss_fams = SousFamille.objects.all()
    return render(request, 'materiaux/sousFamille_index.html', {'ss_fams': ss_fams})


def show_sousFamille(request, slug):
    """
    Retourne une sous-famille à la vue selon la référence

    :param request: the request
    :type request: HttpRequest
    :param slug: la référence de la sousfamille (SS-00)
    :type slug: str
    :return: materiau/materiaux_show.html

    :raises Http404: si la sousfamille n'existe pas
    """
    try:
        ss_fam = SousFamille.objects.get(slug=slug)
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


def show_famille(request, slug):
    """
    Retourne une sous-famille à la vue selon la référence

    :param request: the request
    :type request: HttpRequest
    :param slug: la référence de la sousfamille (SS-00)
    :type slug: str
    :return: materiau/materiaux_show.html

    :raises Http404: si la sousfamille n'existe pas
    """
    try:
        famille = Famille.objects.get(slug=slug)
    except Famille.DoesNotExist:
        raise Http404("La référence de la famille n'existe pas")
    return render(request, "materiaux/famille_show.html", {'famille': famille})


class CreateFamille(CreateView):
    """
    Permet la création d'un matériau de manière générique
    """
    model = Famille
    fields = ['matiere', 'slug']
    template_name_suffix = "_create"


class UpdateFamille(UpdateView):
    """
    Permet la mise à jour d'un materiau via le template materiau_form.html
    Inclut dans les urls par la méthode as_view()
    """
    model = Famille
    fields = ['matiere', 'slug']
    template_name_suffix = "_update"


class DeleteFamille(DeleteView):
    """
    Permet la suppression d'un matériau de manière générique
    """
    model = Famille
    success_url = reverse_lazy('familles_path')


# end Famille section----------------------------------------------------------------------------------------------
