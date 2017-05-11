# Mathériauthèque du Lycée Georges Brassens

Le but de ce projet est de permettre la création d'une matériauthèque modulaire et responsive 
permettant la gestion de différents matériaux et composites dans le cadre du lycée Georges Brassens.
 
Le projet tourne sous Django 1.10 et Python 3.6.
Son installation requiert donc au préalable la présence de Python 3.6 et éventuellement d'un 
environnement virtuel sous cette version. 

Afin d'exécuter la version encore sous développement, il est également nécessaire de disposer
de plusieurs packages Python. Voici la suite de commandes à éxécuter dans un environnement
virtuel dans lequel se situe le projet afin de tester les fonctions pour l'instant implémentées.


```
$ pip install django
$ pip install qrcode
$ pip install reportlab
$ easy_install xhtml2pdf
$ easy_install html5lib
$ easy_install pypdf
$ python manage.py runserver
```

## Matériau Update : 19 Mars 2017

* Base de données des familles, sous-familles, matériaux, propriétés et photos
* Fonctions de création, édition, suppression pour tous les modèles avec les effets cascade pour les dépendances
* Associations illimitées de photos propres à chaque matériau
* Génération automatique de Qrcode pour chaque matériau
* Possibilité de générer un PDF propre à chaque matériau (ne peut pas encore inclure les images)
