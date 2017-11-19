from django.db import models


class Topping(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class PizzaType(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Pizza(models.Model):
    type = models.ForeignKey(PizzaType)
    name = models.CharField(max_length=128)
    toppings = models.ManyToManyField(Topping)

    def __str__(self):
        return self.name


class PandorasBox(models.Model):
    int = models.IntegerField()
    pos_int = models.PositiveIntegerField()
    big_int = models.BigIntegerField()
    small_int = models.SmallIntegerField()
    pos_small_int = models.PositiveSmallIntegerField()
    float = models.FloatField()

    char = models.CharField(max_length=128)
    text = models.TextField()