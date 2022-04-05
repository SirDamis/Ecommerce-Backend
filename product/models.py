from django.db import models
from django.conf import settings
from user.models import Seller

class Reviews(models.Model):
    text = models.CharField(max_length=150)
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey("Products", on_delete=models.CASCADE)


class Products(models.Model):
    name  = models.CharField(max_length=50)
    image = models.ImageField(upload_to='images/')
    description = models.CharField(max_length=1000)
    seller = models.ForeignKey(Seller, on_delete=models.SET_NULL, null=True )
    price = models.DecimalField(decimal_places=2, max_digits=20)
    reviewed = models.BooleanField(default=False)
    total_sales = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)