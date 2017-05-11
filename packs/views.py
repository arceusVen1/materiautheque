from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.http import Http404, HttpResponseRedirect
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from packs.models import *
from packs.form import *
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


# Packs section ----------------------------------------------------------------------------------------------------

def index(request):
    """
    Retourne la liste complète des packs

    :param request: La requête du client
    :type request: HttpRequest
    :return: le template associé à la liste des packs
    :rtype: HttpResponse
    """
    packs = Pack.objects.all()
    return render(request, 'packs/packs_index.html', {'packs': packs})


def show_pack(request, slug):
    """
    Retourne un pack à la vue selon la référence

    :param request: La requête client
    :type request: HttpRequest
    :param slug: la référence du pack (PACK-FA-SS-ID)
    :type slug: str
    :return: le template associé à un pack
    :rtype: HttpResponse

    :raises Http404: si le pack n'existe pas
    """
    try:
        pack = Pack.objects.get(slug=slug)
    except Pack.DoesNotExist:
        raise Http404("La référence de l'objet n'existe pas")
    return render(request, "packs/packs_show.html", {'pack': pack, "images": pack.imagepack_set.all()})


def create_or_edit_pack(request, slug=None):
    """
    Permet la création ou l'édition d'un pack.
    Si une référence de pack est passé à la vue ce dernier est récupéré et ses valeurs initiales sont chargées
    dans le formulaire d'édition. Les valeurs par défaut des prorpiétés est mis à -1. Cette valeur est prise par défaut
    et permet de comprendre son non-traitement nécessaire lors de la vue d'affichage du pack

    :param request: La requête client
    :type request: HttpRequest
    :param slug: (optionnel) La référence du pack dans le cas d'une édition
    :type slug: str
    :return: Le template associé au formulaire de création ou d'édition d'un pack
    :rtype: HttpResponse
    """
    pack = None
    if slug is not None:
        try:
            pack = Pack.objects.get(slug=slug)
        except Pack.DoesNotExist:
            raise Http404("la référence de l'objet n'existe pas")
    initial = {}
    template = 'packs/pack_create.html'
    if pack is not None:
        initial = dict(nom=pack.nom, ss_famille=pack.ss_famille, marque=pack.marque, normatif=pack.normatif,
                       disponible=pack.disponible)
        template = 'packs/pack_update.html'
    form = PackForm(request.POST or None, initial=initial)
    if form.is_valid():
        nom = form.cleaned_data["nom"]
        ss_famille = form.cleaned_data['ss_famille']
        marque = form.cleaned_data["marque"]
        normatif = form.cleaned_data["normatif"]
        disponible = form.cleaned_data["disponible"]
        if pack is not None:
            pack.nom = nom
            pack.ss_famille = ss_famille
            pack.marque = marque
            pack.normatif = normatif
            pack.disponible = disponible
        else:
            pack = Pack(nom=nom, ss_famille=ss_famille, marque=marque, normatif=normatif,
                           disponible=disponible)
        pack.save()
        return HttpResponseRedirect(reverse('pack_path', args=[pack.slug]))
    return render(request, template, {'object': pack, 'form': form})


class DeletePack(DeleteView):
    """
    Permet la suppression d'un pack de manière générique
    """
    model = Pack
    success_url = reverse_lazy('packs_path')


def generate_pdf_pack(request, slug):
    """
    Permet la génération du pdf
    """
    try:
        pack = Pack.objects.get(slug=slug)
    except Pack.DoesNotExist:
        raise Http404("La référence de l'objet n'existe pas")
    return render_to_pdf(
            'packs/packs_show.html', {'pack': pack}
        )


def add_image(request):
    form = ImageForm(request.POST or None, request.FILES)
    if form.is_valid():
        image = form.save()
        return HttpResponseRedirect(reverse('imagePack_path', args=[image.id]))
    return render(request, 'packs/pack_add_image.html', locals())


def show_image(request, id):
    try:
        image = Image.objects.get(id=id)
    except Image.DoesNotExist:
        raise Http404("La référence de l'image n'existe pas")
    return render(request, "packs/pack_image_show.html", {'image' : image})






# end Packs section-------------------------------------------------------------------------------------------------


# start Sous-Famille section--------------------------------------------------------------------------------------------


def sousFamille_index(request):
    ss_fams = SousFamillePack.objects.all()
    return render(request, 'packs/sousfamillepack_index.html', {'ss_fams': ss_fams})


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
        ss_fam = SousFamillePack.objects.get(slug=slug)
    except SousFamillePack.DoesNotExist:
        raise Http404("La référence de la sous-famille n'existe pas")
    return render(request, "packs/sousfamillepack_show.html", {'ss_fam': ss_fam})


class CreateSousFamille(CreateView):
    """
    Permet la création d'un matériau de manière générique
    """
    model = SousFamillePack
    fields = ['usage', 'famille']
    template_name_suffix = "_create"


class UpdateSousFamille(UpdateView):
    """
    Permet la mise à jour d'un materiau via le template materiau_form.html
    Inclut dans les urls par la méthode as_view()
    """
    model = SousFamillePack
    fields = ['usage', 'famille']
    template_name_suffix = "_update"


class DeleteSousFamille(DeleteView):
    """
    Permet la suppression d'un matériau de manière générique
    """
    model = SousFamillePack
    success_url = reverse_lazy('sousFamillesPack_path')

# end Sous-Famille section----------------------------------------------------------------------------------------------

# start Famille section-------------------------------------------------------------------------------------------------


def famille_index(request):
    familles = FamillePack.objects.all()
    return render(request, 'packs/famillepack_index.html', {'familles': familles})


def show_famille(request, slug):
    """
    Retourne une famille à la vue selon la référence

    :param request: the request
    :type request: HttpRequest
    :param slug: la référence de la sousfamille (SS-00)
    :type slug: str
    :return: materiau/materiaux_show.html

    :raises Http404: si la sousfamille n'existe pas
    """
    try:
        famille = FamillePack.objects.get(slug=slug)
    except FamillePack.DoesNotExist:
        raise Http404("La référence de la famille n'existe pas")
    return render(request, "packs/famillepack_show.html", {'famille': famille})


class CreateFamille(CreateView):
    """
    Permet la création d'un matériau de manière générique
    """
    model = FamillePack
    fields = ['usage', 'slug']
    template_name_suffix = "_create"


class UpdateFamille(UpdateView):
    """
    Permet la mise à jour d'un materiau via le template materiau_form.html
    Inclut dans les urls par la méthode as_view()
    """
    model = FamillePack
    fields = ['usage', 'slug']
    template_name_suffix = "_update"


class DeleteFamille(DeleteView):
    """
    Permet la suppression d'un matériau de manière générique
    """
    model = FamillePack
    success_url = reverse_lazy('famillesPack_path')


# end Famille section----------------------------------------------------------------------------------------------
