from rest_framework import serializers
from . models import Category, CategoryImage, Product, ProductVariant, ProductImage, Size, Colour, Favorit, CategoryType
from rest_framework import serializers



class ProductImgSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['img']


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = ['id', 'size']


class ColourSerializer(serializers.ModelSerializer):
    class Meta:
        model = Colour
        fields = ['id', 'colour']


class ProductVariantSerializer(serializers.ModelSerializer):
    size = SizeSerializer()
    colour = ColourSerializer()

    def to_representation(self, instance):
        ret = super().to_representation(instance)

        if instance.rest > 0:
            ret['available'] =True
        return ret

    class Meta:
        model = ProductVariant
        fields = ['id', 'size', 'colour', 'available', 'rest']


class CategoryTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryType
        fields = ['id', 'name']



class CategoryImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryImage
        fields = ['img']


class CategorySerializer(serializers.ModelSerializer):
    images = CategoryImageSerializer(many=True, read_only=True)
    type = CategoryTypeSerializer()

    class Meta:
        model = Category
        fields = ['id', 'type', 'name', 'description', 'images']


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImgSerializer(many=True, read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True, source='productvariant_set')
    category = CategorySerializer(read_only=True)

    sizes = serializers.SerializerMethodField()
    colours = serializers.SerializerMethodField() #что означает SerializerMethodField

    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'category', 'images', 'variants', 'sizes', 'colours']


    def get_sizes(self, obj):
        variants = obj.productvariant_set.all()
        sizes = {variant.size for variant in variants}
        return SizeSerializer(sizes, many=True).data #почему нельзя просто исполбзлвать SizeSerializer

    def get_colours(self, obj):
        variants = obj.productvariant_set.all()
        sizes = {variant.colour for variant in variants}
        return ColourSerializer(sizes, many=True).data  # почему нельзя просто исполбзлвать ColourSerializer


class FavoritSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='product.product.title', read_only=True)
    colour = serializers.CharField(source='product.colour.colour', read_only=True)
    size = serializers.CharField(source='product.size.size', read_only=True)
    price = serializers.DecimalField(source='product.product.price', max_digits=10, decimal_places=2)

    class Meta:
        model = Favorit
        fields = ['id',  'product', 'title', 'colour', 'size', 'price']



