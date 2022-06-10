from django.test import TestCase
from django.urls import reverse
from django.utils.http import urlencode

from accounts.admin import UserModel
from orders.models import Order, FoodAndDrinks, Category, OrderItem
from orders.models.model_choices import SALAD


class OrderItemViewTests(TestCase):
    user_data = {
        "email": "test@takeaway.com",
        "password": "Ld9876kx",
        "is_staff": False,
        "is_superuser": False,
    }

    category_data = {
        'title': SALAD,
    }

    food_data = {
        "title": "salad one",
        "price": "5.0",
        "category_id": 1,
    }

    def test_add_new_item__expect_new_food_in_order(self):
        user = UserModel.objects.get_or_create(**OrderItemViewTests.user_data)[0]
        self.client.force_login(user)

        Category.objects.create(**OrderItemViewTests.category_data)

        product = FoodAndDrinks.objects.create(**OrderItemViewTests.food_data)

        order = Order.objects.create(user=user)

        item_data = {
            'order': order,
            'product': product,
            'quantity': 3,
        }

        query_args = {'product': 1}
        path = f'{reverse("order_item add")}?{urlencode(query_args)}'

        self.client.post(
            path,
            data=item_data,
        )

        order_item = OrderItem.objects.get(pk=product.pk)
        self.assertEqual(order_item.product.title, "salad one")
        self.assertEqual(OrderItem.objects.count(), 1)
        self.assertEqual(Order.objects.get(pk=1).orderitem_set.count(), 1)
