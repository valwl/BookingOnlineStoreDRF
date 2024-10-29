from django.db import models
from product.models import ProductVariant
from django.contrib.auth import get_user_model
User = get_user_model()




class Basket(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # items = models.ManyToManyField(ProductVariant, through=BasketItem) # возможно проблема с тем что идет ссылка на ProductVariant из-за данного поля
    #items = models.ForeignKey(BasketItem, on_delete=models.CASCADE)

    def __str__(self):
        return f'Basket for {self.user.first_name}, {self.user.id}'


class BasketItem(models.Model):
    quantity = models.PositiveIntegerField()
    product = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE)


    # size = models.CharField(max_length=255)
    # colour = models.CharField(max_length=255)
    # img = models.ImageField(upload_to='images/basketItem/', null=True, blank=True)

    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(fields=['product', 'basket'], name='unique_product_basket')]

    # def __str__(self):
    #     return f'{self.product.product.title}-{self.basket.pk}'

class Orders(models.Model):
    STATUS_CHOICES = [('pending', 'Pending'),
                      ('paid', 'Paid'),
                      ('packed', 'Packed'),
                      ('on_way', 'On_way'),
                      ('complete', 'Complete')]
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE)
    phone = models.CharField(max_length=18)
    address = models.CharField(max_length=255)
    total_coast = models.DecimalField(max_digits=12, decimal_places=2)
    create = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default='pending')
    number = models.PositiveIntegerField(unique=True)
    delivery_instructions = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'Order number: {self.number} - ID:  {self.pk}'


class OrderItem(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.product.product.title} - Order ID: {self.order.pk}'