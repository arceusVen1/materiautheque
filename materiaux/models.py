from django.db import models

# Create your models here.
class Materiau(models.Model):

    NORMATIF_CHOICES = ()
    TYPE_CHOICES = ()

    famille = models.CharField(max_length=255)
    ss_famille = models.CharField(max_length=255)
    fournisseur = models.CharField(max_length=255, default="NR")
    usage = models.TextField(default="NR")
    date = models.DateField(auto_now_add=True)
    disponible = models.BooleanField("Disponibilitée", default=True)
    normatif = models.CharField("Critère normatif", default=((0, "NR")))



    class Meta:
        verbose_name = "Materiau"
        verbose_name_plural = "Materiaux"

