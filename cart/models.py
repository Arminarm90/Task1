from django.db import models
from accounts.models import User
from products.models import Product
from django.contrib.auth import get_user_model


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.product.title

    def add_amount(self):
        amount = self.product.price * self.quantity
        profile = self.user.profile
        profile.total_price = profile.total_price + amount
        profile.save()
        return True



# class ShoppingCart(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     products = models.ManyToManyField(Product, through='CartItem')

# User = get_user_model()
# class CartItem(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     shopping_cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(default=1)
    
    
# class Cart(models.Model):
#     STATUS_CHOICES = (
#         ("seccessful", "Successful payment"),
#         ("failed", "Payment failed"),
#         ("waiting", "Waiting for payment"),
#     )
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(default=0)
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="waiting")
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     date_added = models.DateTimeField(auto_now_add=True)
 
#     def __str__(self):
#         return f'{self.quantity} x {self.product.title}'


# class Cart(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     products = models.ManyToManyField(Product, through='CartItem')

# class CartItem(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
#     quantity = models.IntegerField(default=1)
    
# class CartItem(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     quantity = models.IntegerField(default=1)
#     added_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         unique_together = ('user', 'product')

#     def total_price(self):
#         return self.quantity * self.product.price


