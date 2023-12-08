from django.db import models

# Create your models here.
from django.db import models

from crud_user.models import User


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='owned_product')
    users_favorite = models.ManyToManyField(User, related_name='favorite_products')

    def __str__(self):
        return self.name
