from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin
from proprietes import views
from proprietes.models import Propriete

urlpatterns = [
    url(r'^$', views.index, name='proprietes_path'),
    url(r'^nouveau/$', views.CreatePropriete.as_view(model=Propriete), name='new_proprietes_path'),
    url(r'^(?P<slug>\w+)/$', views.show_propriete, name='proprietes_path'),
    url(r'^(?P<slug>\w+)/edit/$', views.UpdatePropriete.as_view(model=Propriete), name='proprietes_path'),
    url(r'^(?P<slug>\w+)/delete/$', views.DeletePropriete.as_view(model=Propriete),
        name='delete_proprietes_path'),

]