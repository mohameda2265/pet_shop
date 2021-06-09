from rest_framework.status import *
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .serializers import *


class PetsAPI(APIView):
    authentication_classes = ()
    permission_classes = []

    def get_pet_object(self, request):
        request_data = {
            'name': request.data.get('name', None),
            'rarity': request.data.get('rarity', None),
            'quantity': request.data.get('quantity', None),
            'items': []
        }
        for item in request.data.get('items', []):
            request_data['items'].append({
                'price': item.get('price', None),
                'currency': item.get('currency', None),
            })
        return request_data

    def validate_pet_data(self, request_data):
        list_items = []
        if request_data.get('items', None):
            for item in request_data.get('items', None):
                list_items.extend(
                    [item.get('price', None),
                     item.get('currency', None)]
                )
            list_items.extend(
                [request_data.get('name', None),
                 request_data.get('rarity', None),
                 request_data.get('quantity', None)]
            )
        return all(list_items)

    def get(self, request):
        pets_data = Pet.objects.prefetch_related('pet_items').all().order_by('-rarity')
        serialized_data = PetSerializer(pets_data, many=True).data
        return Response({'pets_data': serialized_data}, status=HTTP_200_OK)

    def post(self, request):
        # There are three ways to create an object into database.

        request_data = self.get_pet_object(request)
        # first way with serializer:
        if self.validate_pet_data(request_data):
            pet_serializer = PetSerializer(data=request_data, context={'items': request_data.get('items', [])})
            if pet_serializer.is_valid():
                pet_serializer.save()
                return Response({'response': 'success'}, status=HTTP_200_OK)
            else:
                return Response({'response': pet_serializer.errors}, status=HTTP_400_BAD_REQUEST)

        return Response({'response': 'error data'}, status=HTTP_400_BAD_REQUEST)

    def put(self, request, pet_id):
        try:
            request_data = self.get_pet_object(request)
            if self.validate_pet_data(request_data):
                pet = Pet.objects.get(id=pet_id)
                pet_serializer = PetSerializer(pet, data=request_data)
                if pet_serializer.is_valid():
                    pet_serializer.save()
                    return Response({'response': 'success'}, status=HTTP_200_OK)
                else:
                    return Response({'response': pet_serializer.errors}, status=HTTP_400_BAD_REQUEST)
            else:
                return Response({'response': 'error data'}, status=HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'response': str(e)}, status=HTTP_400_BAD_REQUEST)

    def delete(self, request, pet_id):
        pet = get_object_or_404(Pet, pk=pet_id)
        pet.delete()
        return Response({'response': 'success'}, status=HTTP_200_OK)


class PetItemAPI(APIView):
    authentication_classes = ()
    permission_classes = []

    def put(self, request, pet_item_id):
        try:
            data = request.data
            pet_item = PetItem.objects.get(id=pet_item_id)
            data['pet'] = pet_item.pet.id
            print(pet_item)
            pet_item_serializer = PetItemSerializer(pet_item, data=data)
            if pet_item_serializer.is_valid():
                pet_item_serializer.save()
                return Response({'response': 'success'}, status=HTTP_200_OK)
            else:
                print(pet_item_serializer.errors)
                return Response({'response': pet_item_serializer.errors}, status=HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'response': str(e)}, status=HTTP_400_BAD_REQUEST)

    def delete(self, request, pet_item_id):
        pet_item = get_object_or_404(PetItem, pk=pet_item_id)
        pet_item.delete()
        return Response({'response': 'success'}, status=HTTP_200_OK)


class OrderAPI(APIView):
    authentication_classes = ()
    permission_classes = []

    def validate_order_data(self, orders):
        for order in orders.get('orders', []):
            pet_item_id = order.get('pet_item_id', 0)
            quantity = order.get('quantity', 0)
            return True if isinstance(pet_item_id, int) and pet_item_id > 0 \
                           and isinstance(quantity, int) and quantity > 0 else False

    def post(self, request):
        errors = []
        if self.validate_order_data(request.data):
            order_items_list = []
            order = Order()
            order.payment_method = request.data.get('payment_method', 'COD')
            order.save()
            for order_data in request.data.get('orders', []):
                pet_item_id = order_data.get('pet_item_id', 0)
                quantity = order_data.get('quantity', 0)
                try:
                    pet_item = PetItem.objects.select_related('pet').get(id=pet_item_id)
                    if quantity <= pet_item.pet.quantity:
                        order_item_data = {
                            'pet_name': pet_item.pet.name,
                            'price': pet_item.price,
                            'currency': pet_item.currency,
                            'quantity': quantity
                        }
                        order_item = OrderItem.objects.create(**order_item_data)
                        order_items_list.append(order_item)
                        order.items.add(order_item.id)
                        order.save()
                        pet_item.pet.quantity -= quantity
                        pet_item.pet.save()
                    else:
                        errors.append({
                            'pet_item_id': pet_item_id,
                            'error': 'Out of stock'
                        })
                except Exception as e:
                    print(e)
                    errors.append({
                        'pet_item_id': pet_item_id,
                        'error': 'Pet item id does not exist'
                    })
            return Response({
                'response': f"Orders created success : {len(request.data.get('orders', [])) - len(errors)}",
                'errors': errors
            }, status=HTTP_200_OK)
        else:
            return Response({'response': 'Error data'}, status=HTTP_400_BAD_REQUEST)
