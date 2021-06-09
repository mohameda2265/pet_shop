from .models import *
from rest_framework import serializers


class PetItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PetItem
        fields = '__all__'


class PetSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField('get_pet_items')

    def get_pet_items(self, obj):
        pet_items = obj.pet_items.all()
        return PetItemSerializer(pet_items, many=True).data

    class Meta:
        model = Pet
        fields = '__all__'

    def create(self, validated_data):
        items = self.context.get('items', [])
        pet = Pet.objects.create(**validated_data)
        if pet:
            if items:
                for item in items:
                    item['pet'] = pet.id
                pet_item_serializer = PetItemSerializer(data=items, many=True)
                if pet_item_serializer.is_valid():
                    pet_item_serializer.save()
                else:
                    return serializers.ValidationError(pet_item_serializer.errors)
        return pet


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'
