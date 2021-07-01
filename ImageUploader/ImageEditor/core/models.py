from django.db import models


class Img(models.Model):
    name = models.CharField(max_length=200, blank=False, null=False)
    width = models.PositiveIntegerField(blank=True)
    height = models.PositiveIntegerField(blank=True)
    image = models.ImageField(upload_to='img/', blank=False, null=False)

    def __str__(self):
        return self.name
