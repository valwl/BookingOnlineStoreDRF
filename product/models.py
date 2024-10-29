from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class CategoryType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.name}'


class Category(models.Model):
    type = models.ForeignKey(CategoryType, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return f'{self.name}'


class CategoryImage(models.Model):
    category = models.ForeignKey(Category, related_name='images', on_delete=models.CASCADE) # related_name='images'?
    img = models.ImageField(upload_to='images/categories/', null=True, blank=True)


class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.title}'


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    img = models.ImageField(upload_to='images/products/', null=True, blank=True)


class Size(models.Model):
    size = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.size}'


class Colour(models.Model):
    colour = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.colour}'


class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    colour = models.ForeignKey(Colour, on_delete=models.CASCADE)
    available = models.BooleanField(default=False)
    rest = models.PositiveIntegerField()
    img = models.ImageField(upload_to='images/product_variant/', null=True, blank=True)

    class Meta:
        unique_together = ('product', 'size', 'colour')  # перейти на UniqueConstraint

    def __str__(self):
        return f'{self.product}, {self.pk}'

    def save(self, *args, **kwargs):
        if self.rest > 0:
            self.available = True
            super().save(*args, **kwargs)


class Favorit(models.Model):
    product = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.product.product.title}'







# all quations

#1 Serializers,
#1. нужны ли serializers только для функционала list если мы даже данный лист можем прописать в ручную на клиенте
# (MealSizeSerializer, CategoryTypeSerializer), смысл вопроса в том что если в модели храняться 3-4 записи и даже так
# есть ли смысл делать get request на сервер или проще просто прописать их на клиенте,
#2. как делать serializers для variationProduct и нужен ли по факту это же конструктор # хотя нам нужно обрабатывать
# запрос с клиента который содержит variationProduct


#Общие вопросы
#1.для чего нужен метод str
#2. логика для создания calculate_total_price встречается во многих проектах, мне кажется что лучше реализовывать ее на клиенте
#3. как должна называться папка для хранения images, нужны ли какие то дополнительные настройки в setting


#Models
#1. также логика создания Basket тоже часто встречается, сделать схему по работе Basket basketItem orders,
# and payment system
#2. разобпаться в логике работы product and variationProduct
#3. для чего нужен slug и где его необходимо применять
#4. расскаэи подробнее как работает связь ManyToManyField, ForIngeyKey, OneToOneFild и в чем между ними отличия, и какие
# связи лучше использовать в контексте нашего приложения,  а иммено как работает в контексте supplements and Meal

#5. модео ли сделать так чтобы было сразу несколько трениров опционально




#views
#1. same quation about views, если буквалбно несколько items in models(CategoryType, MealSize) есть ли смысл
# делать представления для itemList ( вообщем эти вопросы можно определить вместе с serializers)
#2. иерархия представлений в drf и их методы для переопределения
#3. можно только переопределять методы в классовых представлениях или создлвать свои тоже можно
#4. в  чем отличие запросов для list and detail по факту тот и другой функционал это get запросы



#permissions
#11. правильно ли я сделал данный функционал:
#from rest_framework.permissions import BasePermission
# from rest_framework import permissions
# from django.contrib.auth import get_user_model
#
# User = get_user_model()
#
#
# class IsAuthor(BasePermission):
#     def has_permission(self, request, view):
#         user = request.user
#         if user == User.status.author:
#             return True
#         return False
#
#
# class IsOwnerOrReadOnly(BasePermission):
#     def has_object_permission(self, request, view, obj):
#         if request.method in permissions.SAFE_METHODS:
#             return True
#         return obj.author == request.user
# 12.  как работают два данных метода has_object_permission has_permission и являбтся ли они основными в permissoins


#urls
# 1. как работает defaultRouters in drf