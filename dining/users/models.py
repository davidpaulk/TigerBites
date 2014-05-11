from django.db import models

class Item(models.Model):
    isVegan = models.BooleanField(default = False)
    isVegetarian = models.BooleanField(default = False)
    isPork = models.BooleanField(default = False)
    hasNuts = models.BooleanField(default = False)
    
    type = models.CharField(max_length = 10)

    name = models.CharField(unique=True, max_length = 50)

    def __str__(self):
        return self.name

class NetID(models.Model):
    netid = models.CharField(max_length = 15)
    favorites = models.ManyToManyField(Item)
#    favorites_today = models.ManyToManyField(Item)

    def __str__(self):
        return self.id

    def __email__(self):
        return self.id + '@princeton.edu'
    

# Create your models here.
