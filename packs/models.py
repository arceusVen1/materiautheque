from django.db import models
from django.conf import settings
import json
import os
from materiaux.models import *

# Create your models here.

class Pack(models.Model):

    NORMATIF_CHOICES = (("NR", "N.R"), ("ECO", "écolo"))

    class Meta:
        verbose_name = "Pack"
        verbose_name_plural = "Packs"

    slug = models.CharField(max_length=255, unique=True, verbose_name="Référence", default="00")
    nom = models.CharField(max_length=255, verbose_name="Nom générique", default="N.R.")
    famille = models.ForeignKey('FamillePack')
    ss_famille = models.ForeignKey('SousFamillePack', verbose_name="Sous-famille")
    marque = models.CharField('Marque', max_length=255, default="N.R.")
    materiaux_employes = models.ManyToManyField('materiaux.Materiau', verbose_name="Matériaux employés", blank=True)
    procedes_employes = models.TextField('Procédés employés', default="N.R.")
    date = models.DateField(auto_now_add=True)
    normatif = models.CharField("Critère normatif", choices=NORMATIF_CHOICES, default=(0, "N.R."), max_length=255)
    disponible = models.BooleanField("Disponibilité", default=True)
    qrcode = models.ImageField(upload_to='packs', null=True, default=None)

    def folder_renaming(self, tampon):
        path = os.path.join(settings.MEDIA_ROOT, "packs")
        if not os.path.exists(os.path.join(path, tampon)):
            return
        os.rename(os.path.join(path, tampon), os.path.join(path, self.slug))

    def generate_qrcode(self):
        import qrcode
        path = os.path.join(settings.MEDIA_ROOT, "packs/" + self.slug)
        qr = qrcode.QRCode(version=20, error_correction=qrcode.constants.ERROR_CORRECT_L)
        qr.add_data(settings.SITE_URL + self.get_absolute_url())
        path = os.path.join(path, self.slug + ".jpg")
        qr.make_image().save(path)
        self.qrcode = "packs/{}/{}.jpg".format(self.slug, self.slug)

    def generate_folder(self):
        path = os.path.join(settings.MEDIA_ROOT, "packs/" + self.slug)
        try:
            os.makedirs(path)
        except OSError as e:
            print(e)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        tampon = self.slug
        self.famille = self.ss_famille.famille
        self.slug = "PACK" + "-" + self.ss_famille.slug + "-"
        if self.id is None:
            try:
                last = Pack.objects.last()
                self.id = last.id + 1
            except AttributeError:
                self.id = 0
        self.slug += str(self.id)
        if self.slug != tampon:
            if tampon is not None:
                try:
                    os.remove(os.path.join(settings.MEDIA_ROOT, str(self.qrcode)))
                except OSError as e:
                    print(e)
                self.folder_renaming(tampon)
            self.generate_folder()
            self.generate_qrcode()
        super().save()

    def get_absolute_url(self):
        return u'/packs/{}'.format(self.slug)

    def __str__(self):
        return self.slug


class FamillePack(models.Model):

    usage = models.CharField(max_length=255)
    slug = models.CharField(max_length=4, unique=True, verbose_name="Référence")

    # slug auto build ?
    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.slug = self.slug.upper()
        for ss_fam in self.sousfamillepack_set.all():
            ss_fam.save()
        super().save()

    def get_absolute_url(self):
        return u'/packs/famille/{}'.format(self.slug)

    def __str__(self):
        return '{} - {}'.format(self.slug, self.usage)


class SousFamillePack(models.Model):

    slug = models.CharField(max_length=6, unique=True, verbose_name="Référence")
    usage = models.CharField(max_length=255)
    numero = models.IntegerField()
    famille = models.ForeignKey('FamillePack')

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        try:
            self.famille.sousfamillepack_set.get(id=self.id)
        except SousFamillePack.DoesNotExist:
            self.numero = self.famille.sousfamillepack_set.count()
        self.slug = self.famille.slug + "-" + str(self.numero)
        for pack in self.pack_set.all():
            pack.save()
        super().save()

    def get_absolute_url(self):
        return u'/packs/sous-famille/{}'.format(self.slug)

    def __str__(self):
        return '{} - {}'.format(self.slug, self.usage)


def image_file_name(instance, filename):
    return "packs/{}/{}".format(instance.pack.slug,filename)


class ImagePack(models.Model):

    legende = models.CharField(max_length=255, verbose_name="Légende", default="")
    imagefile = models.ImageField(upload_to=image_file_name, blank=True, verbose_name='Image')
    packs = models.ForeignKey('Pack', verbose_name="Pack associé")

    def save(self):
        super(ImagePack, self).save()