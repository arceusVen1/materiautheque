from django.conf.urls import url
from materiaux import views
from materiaux.models import Materiau, SousFamille, Famille

urlpatterns = [
    url(r'^$', views.index, name='materiaux_path'),
    #url(r'^nouveau/$', views.CreateMateriau.as_view(model=Materiau), name='new_materiau_path'),
    url(r'^nouveau/$', views.create_materiau, name='new_materiau_path'),
    url(r'^(?P<slug>MAT-\w{2}-\d+-\d+)/$', views.show_materiau, name='materiau_path'),
    url(r'^(?P<slug>MAT-\w{2}-\d+-\d+)/edit/$', views.UpdateMateriau.as_view(model=Materiau), name='edit_materiau_path'),
    url(r'^(?P<slug>MAT-\w{2}-\d+-\d+)/delete/$', views.DeleteMateriau.as_view(model=Materiau), name='delete_materiau_path'),
    url(r'^famille/$', views.famille_index, name='familles_path'),
    url(r'^famille/nouvelle/$', views.CreateFamille.as_view(model=Famille), name='new_famille_path'),
    url(r'^famille/(?P<pk>\w{2})/$', views.show_famille, name='famille_path'),
    url(r'^famille/(?P<pk>\w{2})/edit/$', views.UpdateFamille.as_view(model=Famille), name='edit_famille_path'),
    url(r'^famille/(?P<pk>\w{2})/delete/$', views.DeleteFamille.as_view(model=Famille), name='delete_famille_path'),
    url(r'^sous-famille/$', views.sousFamille_index, name='sousFamilles_path'),
    url(r'^sous-famille/nouvelle/$', views.CreateSousFamille.as_view(model=SousFamille), name='new_sousFamille_path'),
    url(r'^sous-famille/(?P<pk>\w{2}-\d+)/$', views.show_sousFamille, name='sousFamille_path'),
    url(r'^sous-famille/(?P<pk>\w{2}-\d+)/edit/$', views.UpdateSousFamille.as_view(model=SousFamille), name='edit_sousFamille_path'),
    url(r'^sous-famille/(?P<pk>\w{2}-\d+)/delete/$', views.DeleteSousFamille.as_view(model=SousFamille), name='delete_sousFamille_path'),
]