from rest_framework import serializers
from .models import Sport, League, Season, Keychain, DiscountCode, Sale, SaleItem

# Serializers para lectura
class SportReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sport
        fields = '__all__'


class LeagueReadSerializer(serializers.ModelSerializer):
    sport = SportReadSerializer()

    class Meta:
        model = League
        fields = '__all__'


class SeasonReadSerializer(serializers.ModelSerializer):
    sport = SportReadSerializer()
    league = LeagueReadSerializer()

    class Meta:
        model = Season
        fields = '__all__'


class KeychainReadSerializer(serializers.ModelSerializer):
    season = SeasonReadSerializer()

    class Meta:
        model = Keychain
        fields = '__all__'


class DiscountCodeReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscountCode
        fields = '__all__'


class SaleItemReadSerializer(serializers.ModelSerializer):
    keychain = KeychainReadSerializer()

    class Meta:
        model = SaleItem
        fields = ['id', 'keychain', 'quantity', 'subtotal']


class SaleReadSerializer(serializers.ModelSerializer):
    items = SaleItemReadSerializer(many=True)
    code = DiscountCodeReadSerializer()

    class Meta:
        model = Sale
        fields = ['id', 'code', 'total', 'items', 'created_at']


# Serializers para escritura
class SportWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sport
        fields = ['name', 'description']


class LeagueWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = League
        fields = ['sport', 'name', 'description']


class SeasonWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Season
        fields = ['sport', 'league', 'name', 'start_year', 'end_year']


class KeychainWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keychain
        fields = ['season', 'name', 'description', 'image', 'price']


class DiscountCodeWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscountCode
        fields = ['name', 'value', 'is_active']


class SaleItemWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleItem
        fields = ['keychain', 'quantity']


class SaleWriteSerializer(serializers.ModelSerializer):
    items = SaleItemWriteSerializer(many=True)

    class Meta:
        model = Sale
        fields = ['code', 'items']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        code = validated_data.get('code', None)

        # Crear la venta
        sale = Sale.objects.create(**validated_data)
        total = 0

        # Crear los ítems de la venta
        for item_data in items_data:
            keychain = item_data['keychain']
            quantity = item_data['quantity']
            subtotal = keychain.price * quantity
            total += subtotal
            SaleItem.objects.create(sale=sale, keychain=keychain, quantity=quantity, subtotal=subtotal)

        # Aplicar descuento si hay un código válido
        if code and code.is_active:
            total -= total * (code.value / 100)

        sale.total = total
        sale.save()
        return sale
