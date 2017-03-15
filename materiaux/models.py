from django.db import models
from django.conf import settings
import json


# Create your models here.
class Materiau(models.Model):

    NORMATIF_CHOICES = (("NR", "N.R"),("ECO", "écolo"))

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
    qrcode = models.ImageField(upload_to='materiauxpyth', null=True, default=None)


    def set_proprietes(self, proprietes):
        self.proprietes = json.dumps(proprietes)

    def get_proprietes(self):
        return json.loads(self.proprietes)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.famille = self.ss_famille.famille
        self.slug = "MAT" + "-" + self.ss_famille.reference + "-"
        if self.id is None:
            try:
                last = Materiau.objects.last()
                self.id = last.id + 1
            except AttributeError:
                self.id = 0
        self.slug += str(self.id)
        import qrcode
        qr = qrcode.QRCode(version=20, error_correction=qrcode.constants.ERROR_CORRECT_L)
        qr.add_data(settings.SITE_URL + self.get_absolute_url())
        path = settings.MEDIA_URL + 'materiaux/' + self.slug + ".jpg"
        qr.make_image().save("." + path)
        self.qrcode = path
        super().save()

    def get_absolute_url(self):
        return u'/materiaux/{}'.format(self.slug)

    def __str__(self):
        return self.slug


class Famille(models.Model):

    matiere = models.CharField(max_length=255)
    abrege = models.CharField(max_length=4, primary_key=True)

    def __str__(self):
        return self.matiere

    # abrege auto build ?
    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        return super().save()

    def get_absolute_url(self):
        return u'/materiaux/famille/{}'.format(self.abrege)


class SousFamille(models.Model):

    reference = models.CharField(max_length=6, primary_key=True)
    matiere = models.CharField(max_length=255)
    numero = models.IntegerField()
    famille = models.ForeignKey('Famille')

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.numero = self.famille.sousfamille_set.count()
        self.reference = self.famille.abrege + "-" + str(self.numero)
        super().save()

    def get_absolute_url(self):
        return u'/materiaux/sous-famille/{}'.format(self.reference)

    def __str__(self):
        return self.matiere
