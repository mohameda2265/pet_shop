from rest_framework.test import APIClient
from django.test import TestCase
from .models import *
from django.utils import timezone


class PetTest(TestCase):

    def create_pet(self):
        return Pet.objects.create(name="cat", quantity=1, rarity=5)

    def test_pet_creation(self):
        p = self.create_pet()
        self.assertTrue(isinstance(p, Pet))
        self.assertEqual(p.__str__(), p.name)

    def create_pet_item(self):
        p = Pet.objects.create(name="cat", quantity=1, rarity=5)
        return PetItem.objects.create(pet=p, price=100, currency='EGP')

    def test_pet_item_creation(self):
        p = self.create_pet_item()
        self.assertTrue(isinstance(p, PetItem))
        self.assertEqual(p.__str__(), p.pet.name)

    def create_order_item(self):
        return OrderItem.objects.create(pet_name='cat', price=100, currency='EGP', quantity=1)

    def test_order_item_creation(self):
        p = self.create_order_item()
        self.assertTrue(isinstance(p, OrderItem))
        self.assertEqual(p.__str__(), p.pet_name)

    def create_order(self):
        order_item = OrderItem.objects.create(pet_name='cat', price=100, currency='EGP', quantity=1)
        order = Order()
        order.payment_method = 'COD'
        order.save()
        order.items.add(order_item)
        order.save()
        return order

    def test_order_creation(self):
        p = self.create_order()
        self.assertTrue(isinstance(p, Order))
        self.assertEqual(p.__str__(), p.payment_method)


client = APIClient()

create_pet_obj_success = {
    "name": "test pet",
    "rarity": 5,
    "quantity": 20,
    "items": [
        {
            "price": 200,
            "currency": "Dollar"
        },
        {
            "price": 3000,
            "currency": "EGP"
        }
    ]
}
update_pet_obj_success = {
    "name": "test pet",
    "rarity": 5,
    "quantity": 20
}
create_pet_obj_error_data = {
    "name": "test pet",
    "rarity": 5,
    "quantity": 20,
    "items": [
        {
            "price": 0,
            "currency": "Dollar"
        },
        {
            "price": 100,
            "currency": "EGP"
        }
    ]
}
create_pet_obj_missing_data = {
    "name": "test pet",
    "rarity": 10,
    "quantity": 20,
    "items": [
        {
            "price": '100',
            "currency": "Dollar"
        },
        {
            "price": 1000,
            "currency": "EGP"
        }
    ]
}
create_order_success = {
    "orders": [
        {
            "pet_item_id": 2,
            "quantity": 1
        },
        {
            "pet_item_id": 1,
            "quantity": 120
        },
        {
            "pet_item_id": 3,
            "quantity": 101
        }
    ],
    "payment_method": "COD"
}
create_order_error_data = {
    "orders": [
        {
            "pet_item_id": 2,
            "quantity": 1
        },
        {
            "pet_item_id": 1,
            "quantity": 0
        },
        {
            "pet_item_id": 3,
            "quantity": 101
        }
    ],
    "payment_method": "COD"
}

create_pet_request_success = client.post('/api/pet/', create_pet_obj_success, format='json')
create_pet_request_error_data = client.post('/api/pet/', create_pet_obj_error_data, format='json')
create_pet_request_missing_data = client.post('/api/pet/', create_pet_obj_missing_data, format='json')
update_pet_request_success = client.put('/api/pet/80', update_pet_obj_success, format='json')
update_pet_request_error_data = client.put('/api/pet/80', update_pet_obj_success, format='json')
update_pet_request_missing_data = client.put('/api/pet/80', update_pet_obj_success, format='json')
get_pets_request = client.get('/api/pet/', format='json')
delete_pet_request_success = client.delete('/api/pet/1', format='json')
delete_pet_item_request_success = client.delete('/api/pet/item/1', format='json')
create_order_request_success = client.post('/api/pet/order', create_order_success, format='json')
create_order_request_error_data = client.post('/api/pet/order', create_order_error_data, format='json')
update_pet_item_request_success = client.put('/api/pet/80', create_update_pet_obj_success, format='json')
update_pet_item_error_data = client.put('/api/pet/80', create_update_pet_obj_error_data, format='json')
update_pet_item_missing_data = client.put('/api/pet/80', create_update_pet_obj_missing_data, format='json')
