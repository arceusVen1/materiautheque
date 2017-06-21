from django.db import models
from django.conf import settings
import json
import os

# Create your models here.
class Materiau(models.Model):

    NORMATIF_CHOICES = (("NR", "N.R"), ("ECO", "écolo"))

    ASPECT_VISUEL_CHOICES = (
        ('OPAQUE', 'opaque'),
        ('TRANSLUCIDE', 'translucide'),
        ('OPALESCENT', 'opalescent'),
        ('DIFFUSANT', 'diffusant'),
        ('DEPOLI', 'dépoli'),
        ('BROSSE', 'brossé'),
        ('TRANSPARENT', 'transparent'),
        ('BRILLANT', 'brillant'),
        ('SATINE', 'satiné'),
        ('MAT', 'mat'),
        ('TEXTURE', 'texturé'),
        ('REFLECHISSANT', 'réfléchissant'),
        ('ILLUSION_OPTIQUE', 'illusion optique')
    )

    ASPECT_TACTILE_CHOICES = (
        ('LISSE', 'lisse'),
        ('RUGUEUX', 'rugueux'),
        ('SOYEUX', 'soyeux'),
        ('DUVETEUX', 'duveteux'),
        ('PELUCHEUX', 'pelucheux'),
        ('DOUX', 'doux'),
        ('GOMME', 'gommé'),
        ('FLUIDE', 'fluide'),
        ('TEXTURE', 'texturé'),
        ('CHAUD', 'chaud'),
        ('FROID', 'froid'),
        ('REPONSE_AU_CONTACT', 'réponse au contact')
    )

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
    aspect_visuel = models.CharField("Aspect visuel", choices=ASPECT_VISUEL_CHOICES, max_length=50, default=(0,"N.R."))
    aspect_tactile = models.CharField("Aspect tactile", choices=ASPECT_TACTILE_CHOICES, max_length=50, default=(0,"N.R."))


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
    slug = models.CharField(max_length=4, unique=True, verbose_name="Référence")

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


def image_file_name(instance, filename):
    return "materiaux/{}/{}".format(instance.materiau.slug,filename)


class Image(models.Model):

    legende = models.CharField(max_length=255, verbose_name="Légende", default="")
    imagefile = models.ImageField(upload_to=image_file_name, blank=True, verbose_name='Image')
    materiau = models.ForeignKey('Materiau', verbose_name="Matériau associé")

    def save(self):
        super(Image, self).save()

    def delete(self):
        os.remove(os.path.join(settings.MEDIA_ROOT, str(self.imagefile)))
        super().delete()
