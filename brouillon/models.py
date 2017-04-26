from django.db import models
from django.conf import settings
from django.core.mail import send_mail
from materiaux.models import *
import os


class Brouillon(Materiau):

    # foreign key username -> auteur

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        tampon = self.slug
        self.famille = self.ss_famille.famille
        self.slug = "MAT" + "-" + self.ss_famille.slug + "-"
        if self.id is None:
            try:
                last = Materiau.objects.last()
                self.id = last.id + 1
            except AttributeError:
                self.id = 0
        self.slug += str(self.id)
        # fonction de mail
        # send_mail()
        super().save()