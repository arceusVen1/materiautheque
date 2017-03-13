from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin
from propriete import views
from propriete.models import Propriete

urlpatterns = [
    url(r'^$', views.index, name='proprietes_path'),
    url(r'^nouveau/$', views.CreatePropriete.as_view(model=Propriete), name='new_propriete_path'),
    url(r'^(?P<slug>)/$', views.show_propriete, name='propriete_path'),
    url(r'^(?P<slug>)/edit/$', views.UpdatePropriete.as_view(model=Propriete), name='propriete_path'),
]