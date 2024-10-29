from django.db import transaction
from . models import Basket, OrderItem, Orders


class OrderService:
    @staticmethod
    @transaction.atomic
    def create_order(user, phone, address):
        basket, created = Basket.objects.get_or_create(user=user)
        if not basket.items.exists():
            raise ValueError('basket empty')

        total_coast = sum(item.product.product.price * item.quantity for item in basket.basketitem_set.all())

        order = Orders.objects.create(
            basket=basket,
            phone=phone,
            address=address,
            total_coast=total_coast,
            number=OrderService.generate_order_number()
        )

        for item in basket.basketitem_set.all():
            OrderItem.object.reate(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

        basket.items.cleare()
        return order

    @staticmethod
    def generate_order_number():
        return Orders.objects.count() + 1


# откуда берем basketitem_set and расскажи подробно как работате данная строка
# basket = Basket.objects.select_related('user').pprefetch_related('basketitem_set___product').get(user=user)
#так ли нам нужен basket item если у нас уде есть basketItem and VariationProduct