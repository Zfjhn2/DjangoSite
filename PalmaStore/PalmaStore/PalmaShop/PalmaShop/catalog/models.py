from django.db import models
from django.urls import reverse
import uuid
from django.contrib.auth.models import User


class TypeThing(models.Model):
    name = models.CharField(max_length=200, help_text="Enter thing's type")

    def __str__(self):
        return self.name


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    manufacturer = models.ForeignKey('Manufacturer', on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=1000, help_text="Enter a brief description of the book")
    type = models.ForeignKey(TypeThing, on_delete=models.SET_NULL, null=True, help_text="Select a genre for this book")
    image = models.ImageField(upload_to='images')
    price = models.IntegerField(help_text='Enter the price', null=True)
    order_count = models.IntegerField(default=0)
    view_count = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product-detail', args=[str(self.id)])


class ProductInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this particular thing across whole warehouse")
    product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True)

    LOAN_STATUS = (
        ('i', 'In stock'),
        ('т', 'Not in stock'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='t', help_text='Product availability')


class Manufacturer(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    def get_absolute_url(self):
        return reverse('manufacturer-detail', args=[str(self.id)])

    def __str__(self):
        return '%s, %s' % (self.name, self.country)


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)

    def __str__(self):
        return f"Корзина {self.user.username}"

