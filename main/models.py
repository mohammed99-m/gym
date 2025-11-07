from django.db import models
from django.contrib.auth.hashers import make_password
# Create your models here.

class Player(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    age = models.CharField(max_length=3)
    phone_number = models.CharField(max_length=11,unique=True)
    coach_name = models.CharField(max_length=100,blank=True,null=True)
    height = models.DecimalField(max_digits=6,decimal_places=3)
    weight = models.DecimalField(max_digits=6,decimal_places=3)
    gender = models.CharField(max_length=6,null=True,blank=True) 

    chest = models.JSONField(default=list,blank=True,null=True)
    back = models.JSONField(default=list,blank=True,null=True)
    biceps = models.JSONField(default=list,blank=True,null=True)
    triceps = models.JSONField(default=list, blank=True, null=True)
    back = models.JSONField(default=list, blank=True, null=True)
    abs = models.JSONField(default=list, blank=True, null=True)
    shoulders = models.JSONField(default=list, blank=True, null=True)
    legs = models.JSONField(default=list, blank=True, null=True)
    meal_plan = models.JSONField(default=list, blank=True, null=True)

    type = models.CharField(max_length=50)
    situation = models.BooleanField(default=False) 

    password = models.CharField(max_length=128) 

    def save(self, *args, **kwargs):
        # Hash the password before saving if it’s not hashed already
        if not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

