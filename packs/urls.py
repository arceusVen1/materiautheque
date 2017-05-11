from django.conf.urls import url
from packs import views
from packs.models import *

urlpatterns = [
    url(r'^$', views.index, name='packs_path'),
    url(r'^nouveau/$', views.create_or_edit_pack, name='new_pack_path'),
    url(r'^images/(?P<id>\d+)/$', views.show_image, name='imagePack_path'),
    url(r'^images/ajouter$', views.add_image, name='new_imagePack_path'),
    url(r'^(?P<slug>PACK-\w{2}-\d+-\d+)/$', views.show_pack, name='pack_path'),
    url(r'^(?P<slug>PACK-\w{2}-\d+-\d+)/edit/$', views.create_or_edit_pack, name='edit_pack_path'),
    url(r'^(?P<slug>PACK-\w{2}-\d+-\d+)/delete/$', views.DeletePack.as_view(model=Pack), name='delete_pack_path'),
    url(r'^(?P<slug>PACK-\w{2}-\d+-\d+)/generatePDF/$', views.generate_pdf_pack, name='generate_pdf_path'),
    url(r'^famille/$', views.famille_index, name='famillesPack_path'),
    url(r'^famille/nouvelle/$', views.CreateFamille.as_view(model=FamillePack), name='new_famillePack_path'),
    url(r'^famille/(?P<slug>\w{2})/$', views.show_famille, name='famillePack_path'),
    url(r'^famille/(?P<slug>\w{2})/edit/$', views.UpdateFamille.as_view(model=FamillePack), name='edit_famillePack_path'),
    url(r'^famille/(?P<slug>\w{2})/delete/$', views.DeleteFamille.as_view(model=FamillePack), name='delete_famillePack_path'),
    url(r'^sous-famille/$', views.sousFamille_index, name='sousFamillesPack_path'),
    url(r'^sous-famille/nouvelle/$', views.CreateSousFamille.as_view(model=SousFamillePack), name='new_sousFamillePack_path'),
    url(r'^sous-famille/(?P<slug>\w{2}-\d+)/$', views.show_sousFamille, name='sousFamillePack_path'),
    url(r'^sous-famille/(?P<slug>\w{2}-\d+)/edit/$', views.UpdateSousFamille.as_view(model=SousFamillePack), name='edit_sousFamillePack_path'),
    url(r'^sous-famille/(?P<slug>\w{2}-\d+)/delete/$', views.DeleteSousFamille.as_view(model=SousFamillePack), name='delete_sousFamillePack_path'),
]