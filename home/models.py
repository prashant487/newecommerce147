from django.db import models

STATUS = (('In Stock', 'In Stock'), ('Out of Stock', 'Out of STOCK'))


# Create your models here.
class Categorie(models.Model):
    name = models.CharField(max_length=200)
    slug = models.CharField(max_length=200, unique=True)
    image = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return self.name


class Slider(models.Model):
    name = models.CharField(max_length=300)
    image = models.TextField()
    description = models.TextField()
    url = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Ad(models.Model):
    name = models.CharField(max_length=300)
    rank = models.IntegerField(unique=True)
    image = models.TextField()
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=300)
    image = models.TextField()
    rank = models.IntegerField()

    def __str__(self):
        return self.name


class Item(models.Model):
    title = models.CharField(max_length=300)
    price = models.IntegerField()
    slug = models.CharField(max_length=300, unique=True)
    discountedprice = models.IntegerField(default=0)
    description = models.TextField()
    category = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    status = models.CharField(max_length=100, choices=STATUS)

    def __str__(self):
        return self.title
