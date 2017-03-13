from django.db import models


# Create your models here.
class Materiau(models.Model):

    NORMATIF_CHOICES = (("NR", "N.R"),("ECO", "écolo"))

    class Meta:
        verbose_name = "Materiau"
        verbose_name_plural = "Materiaux"

    slug = models.CharField(max_length=255, unique=True, verbose_name="référence", default="00")
    famille = models.ForeignKey('Famille')
    ss_famille = models.ForeignKey('SousFamille', verbose_name="Sous-famille")
    fournisseur = models.CharField(max_length=255, default="N.R.")
    usage = models.TextField(default="N.R.")
    date = models.DateField(auto_now_add=True)
    disponible = models.BooleanField("Disponibilité", default=True)
    normatif = models.CharField("Critère normatif", choices=NORMATIF_CHOICES, default=(0, "N.R."), max_length=255)

    #not working
    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.famille = self.ss_famille.famille
        self.slug = "MAT" + "-" + self.ss_famille.reference + "-"
        if self.id is None:
            last = Materiau.objects.last()
            self.id = last.id + 1
        self.slug += str(self.id)
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
        return u'/materiaux/famille/{}'.format(self.id)


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
