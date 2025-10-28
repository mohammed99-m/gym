from django.db import models

class Advertisement(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image_url = models.URLField(max_length=1000, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)  # optional, useful to hide adverts without deleting

    def __str__(self):
        return self.title