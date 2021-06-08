from rest_framework.status import *
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import *


class PetsAPI(APIView):
    authentication_classes = ()
    permission_classes = []

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
        # first way with serializer:
        if self.validate_pet_data(request_data):
            pet_serializer = PetSerializer(data=request_data, context={'items': request_data.get('items', [])})
            if pet_serializer.is_valid():
                pet_serializer.save()
                return Response({'response': 'success'}, status=HTTP_200_OK)
            else:
                return Response({'response': pet_serializer.errors}, status=HTTP_400_BAD_REQUEST)
        return Response({'response': 'error data'}, status=HTTP_400_BAD_REQUEST)
