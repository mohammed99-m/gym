from django.db import models
from cloudinary.models import CloudinaryField
class Advertisement(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image_url = CloudinaryField("image_url",null=True,blank=True)
    date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)  # optional, useful to hide adverts without deleting

    def __str__(self):
        return self.title