from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.http import Http404, HttpResponseRedirect
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from materiaux.models import Materiau, Famille, SousFamille
from materiaux.form import MateriauForm
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
        proprietes = mat.get_proprietes()
    except Materiau.DoesNotExist:
        raise Http404("La référence de l'objet n'existe pas")
    return render(request, "materiaux/materiaux_show.html", {'mat': mat, "proprietes": proprietes})

def create_materiau(request):
    proprietes = []
    form = MateriauForm(request.POST or None)
    if form.is_valid():
        ssfamille = form.cleaned_data['ssfamille']
        fournisseur = form.cleaned_data["fournisseur"]
        normatif = form.cleaned_data["normatif"]
        disponible = form.cleaned_data["disponible"]
        for propriete in Propriete.objects.all():
            proprietes.append({"slug": propriete.slug, "valeur": float(form.cleaned_data[propriete.slug])})
        materiau = Materiau(ss_famille=ssfamille, fournisseur=fournisseur,normatif=normatif, disponible=disponible)
        materiau.set_proprietes(proprietes)
        materiau.save()
        return HttpResponseRedirect(reverse('materiau_path', args= [materiau.slug]))
    return render(request, 'materiaux/materiau_create.html', {'form': form})

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

def GeneratePDFMateriau(request, slug):
    """
    Permet la génération du pdf
    """
    try:
        mat = Materiau.objects.get(slug=slug)
        proprietes = mat.get_proprietes()
    except Materiau.DoesNotExist:
        raise Http404("La référence de l'objet n'existe pas")
    return render_to_pdf(
            'materiaux/materiaux_show.html', {'mat': mat, "proprietes": proprietes}
        )


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


# end Famille section----------------------------------------------------------------------------------------------
