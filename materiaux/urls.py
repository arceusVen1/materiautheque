from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin
from materiaux import views

urlpatterns = [
    url(r'^$', views.index, name='materiaux_paths'),
    url(r'^(?P<reference>MAT-w{2}-[0-9]{2}-\d+)$', views.show_materiau, name='materiau_path'),
]