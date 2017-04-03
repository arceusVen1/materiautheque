from django.conf.urls import url
from brouillon import views
from brouillon.models import *

urlpatterns = [
    url(r'^$', views.index, name='brouillons_path'),
    url(r'^nouveau/$', views.create_or_edit_brouillon, name='new_brouillon_path'),
    url(r'^(?P<slug>MAT-\w{2}-\d+-\d+)/$', views.show_brouillon, name='brouillon_path'),
    url(r'^(?P<slug>MAT-\w{2}-\d+-\d+)/edit/$', views.create_or_edit_brouillon, name='edit_brouillon_path'),
    url(r'^(?P<slug>MAT-\w{2}-\d+-\d+)/publier/$', views.to_materiau, name='to_materiau_path'),
    url(r'^(?P<slug>MAT-\w{2}-\d+-\d+)/delete/$', views.DeleteBrouillon.as_view(model=Brouillon), name='delete_brouillon_path'),
]