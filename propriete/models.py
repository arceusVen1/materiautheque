from django.db import models

# Create your models here.
class Propriete(models.Model):

	NORMATIF_CHOICES = (("NR", "N.R"),("ECO", "écolo"))

	class Meta:
		verbose_name = "Propriété"
		verbose_name_plural = "Propriétés"

	slug = models.CharField(max_length=255, unique=True)
	unite = models.CharField(max_length=30, verbose_name="unité", default="N.R.")
	defintion = models.TextField(default="N.R.")

	def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super().save()

    def get_absolute_url(self):
        return u'/proprietes/{}'.format(self.slug)

    def __str__(self):
        return self.nom

