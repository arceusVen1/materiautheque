from django.db import models

# Create your models here.
class Propriete(models.Model):

    class Meta:
        verbose_name = "Propriété"
        verbose_name_plural = "Propriétés"

    slug = models.CharField(max_length=255, verbose_name="Nom", unique=True)
    unite = models.CharField(max_length=30, verbose_name="Unité", default="N.R.")
    definition = models.TextField(default="N.R.")

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super().save()

    def get_absolute_url(self):
        return u'/propriete/{}'.format(self.slug)

    def __str__(self):
        return self.slug
