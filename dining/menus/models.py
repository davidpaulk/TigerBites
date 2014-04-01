from django.db import models
from django.utils import timezone
import datetime


class Hall(models.Model):
    RM = 'RM'
    BW = 'BW'
    WH = 'WH'
    FO = 'FO'
    CJL = 'CJL'
    GRAD = 'GRAD'
    dining_hall = (
        (RM, 'Rockefeller/Mathey'),
        (BW, 'Butler/Wilson'),
        (WH, 'Whitman'),
        (FO, 'Forbes'),
        (CJL, 'Center for Jewish Life'),
        (GRAD, 'Grad College')
    )
    name = models.CharField(max_length = 4, 
                            choices = dining_hall, 
                            default = BW)
    Brunch = 'Brunch'
    Breakfast = 'Breakfast'
    Lunch = 'Lunch'
    Dinner = 'Dinner'
    meal_options = (
        (Brunch, Brunch),
        (Breakfast, Breakfast),
        (Lunch, Lunch),
        (Dinner, Dinner)
    )
    meal = models.CharField(max_length = 9,
                            choices = meal_options,
                            default = Breakfast)

    time = models.DateTimeField('Time')
    
    def __unicode__(self):
        return self.name

    #True if object created in last 24 hours, False otherwise
    def today(self):
        return self.time >= timezone.now() - datetime.timedelta(days = 1)

class Menu(models.Model):
    hall = models.ForeignKey(Hall)
    menu = models.CharField(max_length = 400)
    vegan = models.BooleanField(default = False)
    vegetarian = models.BooleanField(default = False)
    halal = models.BooleanField(default = False)
    pork = models.BooleanField(default = False)

    def __unicode__(self):
        return self.menu

#Create your models here.
