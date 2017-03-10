from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin
from materiaux import views
from materiaux.models import Materiau

urlpatterns = [
    url(r'^$', views.index, name='materiaux_paths'),
    url(r'^nouveau/$', views.CreateMateriau.as_view(model=Materiau), name='new_materiau_path'),
    url(r'^(?P<slug>MAT-\w{2}-\d+-\d+)/$', views.show_materiau, name='materiau_path'),
    url(r'^(?P<slug>MAT-\w{2}-\d+-\d+)/edit/$', views.UpdateMateriau.as_view(model=Materiau), name='materiau_path'),
]