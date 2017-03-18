from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.http import Http404
from django.views.generic.edit import UpdateView, CreateView, DeleteView
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
    """
    Permet la génération d'un pdf en construisant un template grâce à un dictionnaire des données
    nécessaires à sa création.

    :param template_src: le template a construire en pdf
    :type template_src: template
    :param context_dict: les données utile à la construction du template
    :type context_dict: dict
    :return: le fichier pdf ou reponse d'erreur
    :rtype: HttpResponse
    """
    template = get_template(template_src)
    context = Context(context_dict)
    html = template.render(context)
    result = BytesIO()

    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))

# Proprietes section --------------------------------------------------------------------------------------------------


def index(request):
    """
    Retournes la liste complètes des propriétés et leurs définition

    :param request: requête du client
    :type request: HttpRequest
    :return: la liste des propriétés
    :rtype: HttpResponse
    """
    proprietes = Propriete.objects.all()
    return render(request, "propriete/index.html", {'proprietes': proprietes})


def show_propriete(request, slug):
    """
    Retourne une propriété à la vue selon sa référence

    :param request: la requête client
    :type request: HttpRequest
    :param slug: la référence de la proprietes
    :type slug: str
    :return: proprietes/show.html

    :raises Http404: si lea propritété n'existe pas n'existe pas
    """
    try:
        prop = Propriete.objects.get(slug=slug)
    except Propriete.DoesNotExist:
        raise Http404("La propriété n'existe pas")
    return render(request, "propriete/show.html", {'prop': prop})


class UpdatePropriete(UpdateView):
    """
    Permet la mise à jour d'une propriete via le template propriete_form.html
    Inclus dans les urls par la méthode as_view()
    """
    model = Propriete
    fields = ['slug', 'unite', 'definition']


class CreatePropriete(CreateView):
    """
    Permet la création d'une proriété de manière générique
    """
    model = Propriete
    fields = ['slug', 'unite', 'definition']


class DeletePropriete(DeleteView):
    """
    Permet la suppression d'une propriété de manière générique
    """
    model = Propriete
    success_url = reverse_lazy('proprietes_path')

def GeneratePDFPropriete(request, slug):
    """
    Permet la génération du pdf concernant une propriété

    :param request: la requête client
    :type request: HttpRequest
    :param slug: la référence de la propriété
    :type slug: str
    :return: fonction de génération de pdf render_to_pdf
    :rtype: HttpResponse
    """
    try:
        prop = Propriete.objects.get(slug=slug)
    except Propriete.DoesNotExist:
        raise Http404("La propriété n'existe pas")
    return render_to_pdf(
            "propriete/show.html", {'prop': prop}
        )