from django.db import models
from django.conf import settings
import json
import os

# Create your models here.
class Materiau(models.Model):

    NORMATIF_CHOICES = (("NR", "N.R"), ("ECO", "écolo"))

    class Meta:
        verbose_name = "Materiau"
        verbose_name_plural = "Materiaux"

    slug = models.CharField(max_length=255, unique=True, verbose_name="référence", default="00")
    nom = models.CharField(max_length=255, verbose_name="Nom générique", default="N.R.")
    famille = models.ForeignKey('Famille')
    ss_famille = models.ForeignKey('SousFamille', verbose_name="Sous-famille")
    fournisseur = models.CharField(max_length=255, default="N.R.")
    usage = models.TextField(default="N.R.")
    date = models.DateField(auto_now_add=True)
    disponible = models.BooleanField("Disponibilité", default=True)
    normatif = models.CharField("Critère normatif", choices=NORMATIF_CHOICES, default=(0, "N.R."), max_length=255)
    proprietes = models.TextField("Propriétés", null=True, default="{}")
    qrcode = models.ImageField(upload_to='materiaux', null=True, default=None)

    def set_proprietes(self, proprietes):
        self.proprietes = json.dumps(proprietes)

    def get_proprietes(self):
        return json.loads(self.proprietes)

    def folder_renaming(self, tampon):
        path = os.path.join(settings.MEDIA_ROOT, "materiaux")
        if not os.path.exists(os.path.join(path, tampon)):
            return
        os.rename(os.path.join(path, tampon), os.path.join(path, self.slug))

    def generate_qrcode(self):
        import qrcode
        path = os.path.join(settings.MEDIA_ROOT, "materiaux/" + self.slug)
        qr = qrcode.QRCode(version=20, error_correction=qrcode.constants.ERROR_CORRECT_L)
        qr.add_data(settings.SITE_URL + self.get_absolute_url())
        path = os.path.join(path, self.slug + ".jpg")
        qr.make_image().save(path)
        self.qrcode = "materiaux/{}/{}.jpg".format(self.slug, self.slug)

    def generate_folder(self):
        path = os.path.join(settings.MEDIA_ROOT, "materiaux/" + self.slug)
        try:
            os.makedirs(path)
        except OSError as e:
            print(e)

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
        return u'/materiaux/{}'.format(self.slug)

    def __str__(self):
        return self.slug


class Famille(models.Model):

    matiere = models.CharField(max_length=255)
    slug = models.CharField(max_length=4, unique=True)

    # slug auto build ?
    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.slug = self.slug.upper()
        for ss_fam in self.sousfamille_set.all():
            ss_fam.save()
        super().save()

    def get_absolute_url(self):
        return u'/materiaux/famille/{}'.format(self.slug)

    def __str__(self):
        return '{} - {}'.format(self.slug, self.matiere)


class SousFamille(models.Model):

    slug = models.CharField(max_length=6, unique=True)
    matiere = models.CharField(max_length=255)
    numero = models.IntegerField()
    famille = models.ForeignKey('Famille')

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        try:
            self.famille.sousfamille_set.get(id=self.id)
        except SousFamille.DoesNotExist:
            self.numero = self.famille.sousfamille_set.count()
        self.slug = self.famille.slug + "-" + str(self.numero)
        for materiau in self.materiau_set.all():
            materiau.save()
        super().save()

    def get_absolute_url(self):
        return u'/materiaux/sous-famille/{}'.format(self.slug)

    def __str__(self):
        return '{} - {}'.format(self.slug, self.matiere)


class Image(models.Model):
    slug = models.SlugField(max_length=255, unique=True)
    imagefile = models.ImageField(upload_to='materiaux/{}'.format(self.Materiau), blank=True)
    materiau = models.ForeignKey('Materiau')
    famille = models.ForeignKey('Famille', null=True)
    sousfamille = models.ForeignKey('SousFamille', null=True)

    def save(self, *args, **kwargs):
        # INFO Checks if present because admins have option to change slug
        if not self.slug:
            slug_str = '%s' % self.slug
            unique_slugify(self, slug_str)
        super(Image, self).save(*args, **kwargs)
