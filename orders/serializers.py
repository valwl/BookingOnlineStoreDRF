from rest_framework import serializers
from . models import BasketItem, Basket, Orders


class BasketSerializer(serializers.ModelSerializer):
    # items = BasketItemSerializer(many=True, read_only=True)
    user = serializers.CharField(source='user.first_name', read_only=True)

    class Meta:
        model = Basket
        fields = ['id', 'user', 'items']


class BasketItemSerializer(serializers.ModelSerializer):
    quantity = serializers.IntegerField()
    title = serializers.CharField(source='product.product.title', read_only=True)
    colour = serializers.CharField(source='product.colour.colour', read_only=True)
    size = serializers.CharField(source='product.size.size', read_only=True)
    images = serializers.ImageField(source='product.img', read_only=True)
    id = serializers.CharField(source='product.id', read_only=True)

    price = serializers.DecimalField(source='product.product.price', max_digits=10, decimal_places=2)

    class Meta:
        model = BasketItem
        fields = ['id', 'quantity',  'product', 'title', 'colour', 'size', 'price', 'basket', 'images']

    #user = serializers.CharField(source='basket.user', read_only=True)
#почему данный serializer cсылается на product_variant а не на basketItems  я думаю что дело может быть в данной строке модели
# Basket  items = models.ManyToManyField(ProductVariant, through=BasketItem)



class OrdersCreateSerializer(serializers.ModelSerializer):
    basket = BasketSerializer(read_only=True)

    class Meta:
        model = Orders
        fields = ['id', 'basket', 'phone', 'address', 'total_coast', 'delivery_instructions']
        #read_only_fields = ['total_cost', 'create', 'status', 'number']













# 1. в чем отличия двух данных подходов
# product_colour = serializers.CharField(source='product.colour', read_only=True)
#     product_colour = serializers.SerializerMethodField()


#2. еще раз что означают source

#3.  для чего мы устанавливаем read_only=True конкретно в OrderCreateSerializer