from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField()
    description = models.TextField()
    image = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    total = models.FloatField()
    status = models.CharField(max_length=50, default='Placed')

    def __str__(self):
        return f"Order #{self.id} - ${self.total:.2f}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.FloatField()

    def __str__(self):
        product_name = self.product.name if self.product else 'Removed Product'
        return f"{product_name} x {self.quantity}"

    @property
    def subtotal(self):
        return self.price * self.quantity