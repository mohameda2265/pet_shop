from rest_framework.status import *
from rest_framework.views import APIView
from rest_framework.response import Response

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
        try:
            pets_data = Pet.objects.prefetch_related('pet_items').all().order_by('-rarity')
            serialized_data = PetSerializer(pets_data, many=True).data
            return Response({'pets_data': serialized_data}, status=HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=HTTP_400_BAD_REQUEST)

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

        # second step with create an object:

        # pet = Pet()
        # pet.name = request_data['name']
        # pet.quantity = request_data['quantity']
        # pet.rarity = request_data['rarity']
        # pet.save()
        # for item in request_data['items']:
        #     pet_item = PetItem()
        #     pet_item.pet = pet.id
        #     pet_item.price = item['price']
        #     pet_item.currency = item['currency']
        #     pet_item.save()

        # third way to use function create

        # pet = Pet.objects.create(
        #     name=request_data['name'],
        #     quantity=request_data['quantity'],
        #     rarity=request_data['rarity']
        # )
        # for item in request_data['items']:
        #     PetItem.objects.create(
        #         pet=pet.id,
        #         price=item['price'],
        #         currency=item['currency']
        #     )
        return Response({'response': 'error data'}, status=HTTP_400_BAD_REQUEST)

    def put(self, request, pet_id):
        try:
            request_data = self.get_pet_object(request)
            # first way with serializer:
            if self.validate_pet_data(request_data):
                pet = Pet.objects.get(id=pet_id)
                pet_serializer = PetSerializer(pet, data=request_data)
                if pet_serializer.is_valid():
                    pet_serializer.save()
                    return Response({'response': 'success'}, status=HTTP_200_OK)
                else:
                    return Response({'response': pet_serializer.errors}, status=HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'response': str(e)}, status=HTTP_400_BAD_REQUEST)

    def delete(self, request, pet_id):
        try:
            pet = Pet.objects.get(id=pet_id)
            pet.delete()
            return Response({'response': 'success'}, status=HTTP_200_OK)
        except:
            return Response({'response': 'Pet id does not exist'}, status=HTTP_400_BAD_REQUEST)


class PetItemAPI(APIView):
    authentication_classes = ()
    permission_classes = []

    def put(self, request, pet_item_id):
        try:
            data = request.data
            data['pet'] = pet_item_id
            pet_item = PetItem.objects.get(id=pet_item_id)
            pet_item_serializer = PetItemSerializer(pet_item, data=data)
            if pet_item_serializer.is_valid():
                pet_item_serializer.save()
                return Response({'response': 'success'}, status=HTTP_200_OK)
            else:
                return Response({'response': pet_item_serializer.errors}, status=HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'response': str(e)}, status=HTTP_400_BAD_REQUEST)

    def delete(self, request, pet_item_id):
        try:
            pet_item = PetItem.objects.get(id=pet_item_id)
            pet_item.delete()
            return Response({'response': 'success'}, status=HTTP_200_OK)
        except:
            return Response({'response': 'Pet item id does not exist'}, status=HTTP_400_BAD_REQUEST)
