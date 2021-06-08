from django.db import models
from django.template.defaultfilters import slugify

BREED_RARITY = [
    (1, 'Normal'),
    (2, 'Low Rarity'),
    (3, 'Medium Rarity'),
    (4, 'High Rarity'),
    (5, 'Unique'),
]

PAYMENT_METHOD = [
    ('COD', 'Cash On Delivery'),
    ('OP', 'Online Payment'),
]


class Pet(models.Model):
    """
    Pet table to save the following:\n
    Pet name,\n
    Pet slug,\n
    Pet rarity 'scale from 1 to 5'
    """
    name = models.CharField(max_length=254)
    quantity = models.IntegerField(default=1)
    rarity = models.IntegerField(choices=BREED_RARITY, default=0)

    def __str__(self):
        # name appears in admin panel
        return self.name


class PetItem(models.Model):
    """
    Pet Item table to save the following:\n
    'To set many prices and currencies for one pet.'\n
    Pet foreign key,\n
    Pet price,\n
    Price currency,\n
    Pet quantity 'In stock'
    """
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='pet_items')
    price = models.FloatField(default=0.0)
    currency = models.CharField(max_length=20)

    def __str__(self):
        # name appears in admin panel
        return self.pet.name


class OrderItem(models.Model):
    """
    These fields was created to fill data not using a foreign key
    from pet, because if the pet object deleted for any reason,
    First reason the order items would be null and its wrong.
    Second reason if I update the price the old orders would be changed and its wrong too.
    """
    pet_name = models.CharField(max_length=254, blank=True, null=True)
    slug = models.CharField(max_length=254, blank=True, null=True)
    price = models.CharField(max_length=254, blank=True, null=True)
    currency = models.CharField(max_length=20)
    quantity = models.IntegerField()

    def __str__(self):
        # name appears in admin panel
        return self.pet_name


class Order(models.Model):
    items = models.ManyToManyField(OrderItem, related_name='items_order')
    total_price = models.FloatField(max_length=254)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHOD, default='COD')
    created_at = models.DateTimeField(auto_now=True)
