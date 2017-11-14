from django.db import models


class Topping(models.Model):
    name = models.CharField(max_length=128)


class PizzaType(models.Model):
    name = models.CharField(max_length=128)


class Pizza(models.Model):
    type = models.ForeignKey(PizzaType)
    name = models.CharField(max_length=128)
    toppings = models.ManyToManyField(Topping)
