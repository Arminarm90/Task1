from django.db import models
from accounts.models import User
from products.models import Product
from django.contrib.auth import get_user_model


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    

    def __str__(self):
        return self.product.title
    
    def save(self, *args, **kwargs):
        # Calculate total price
        self.total_price = self.quantity * self.product.price
        super().save(*args, **kwargs)





