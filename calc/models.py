from django.db import models

class Image_try(models.Model):
    name= models.CharField(max_length=500)
    imagefile= models.ImageField(upload_to='images/', null=True, verbose_name="")

    def __str__(self):
        return self.name + ": " + str(self.imagefile)
