import uuid
from django.db import models
from django.shortcuts import redirect

STATUS = (('In Stock', 'In Stock'), ('Out of Stock', 'Out of STOCK'))
LABEL = (('new', 'New Product'), ('hot', 'Hot Product'), ('sale', 'Sale Product'))

# Create your models here.
from django.urls import reverse


class Categorie(models.Model):
    name = models.CharField(max_length=200)
    slug = models.CharField(max_length=200, unique=True)
    image = models.CharField(max_length=500, blank=True)

    def get_category_url(self):
        return reverse("home:category", kwargs={'slug': self.slug})

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

    def get_brand_url(self):
        return reverse("home:brand", kwargs={'name': self.name})

    def __str__(self):
        return self.name


class Item(models.Model):
    title = models.CharField(max_length=300)
    price = models.IntegerField()
    slug = models.CharField(max_length=300, unique=True)
    discounted_price = models.IntegerField(default=0)
    description = models.TextField()
    category = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    status = models.CharField(max_length=100, choices=STATUS)
    label = models.CharField(max_length=100, choices=LABEL, blank=True)
    image = models.TextField(blank=True)
    image2 = models.TextField(blank=True)
    image3 = models.TextField(blank=True)
    image4 = models.TextField(blank=True)
    image5 = models.TextField(blank=True)
    image6 = models.TextField(blank=True)

    def __str__(self):
        return self.title

    def get_url(self):
        return reverse("home:product", kwargs={'slug': self.slug})

    def get_cart_url(self):
        return reverse("home:add-to-cart", kwargs={'slug': self.slug})

    def minus_cart(self):
        return reverse("home:minus-cart", kwargs={'slug': self.slug})


class Cart(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    slug = models.CharField(max_length=300, unique=True)
    quantity = models.IntegerField(default=1)
    user = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now=True)
    total = models.IntegerField(null=True)

    def __str__(self):
        return self.user

    def delete_cart_url(self):
        return reverse("home:delete-cart", kwargs={'slug': self.slug})


# class Grtotal(models.Model):
#     cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
#     subtotal = models.IntegerField(null=True)
#
#     grandtotal = models.IntegerField(null=True)
#     shippingcost = models.IntegerField(null=True)
#
#     def __str__(self):
#         return self.cart
#
#     def grand_total_url(self):
#         return reverse("home:grand-total", kwargs={'slug': self.slug})

class Contact(models.Model):
    name = models.CharField(max_length=300)
    email = models.CharField(max_length=300)
    subject = models.TextField()
    message = models.TextField()

    def __str__(self):
        return self.name






















































