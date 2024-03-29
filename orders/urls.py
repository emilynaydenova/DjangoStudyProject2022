from django.urls import path

from orders.views.common import HomeView, FoodsByCategoryListView, FoodDetailsView
from orders.views.orders import (
    OrderView,
    OrderCheckoutView,
    OrderSheetView,
    DeliveringInfoCreateView,
    OrderDeleteView,

    OrderItemDeleteView,
    items_qty_plus, items_qty_minus, order_item_add,
)

urlpatterns = [
    path("", HomeView.as_view(), name="home"),  # list_all, create
    path(
        "foods_by_category/",
        FoodsByCategoryListView.as_view(),
        name="foods by category",
    ),
    path("food_and_drinks/<int:pk>/", FoodDetailsView.as_view(), name="food details"),
    path("order/", OrderView.as_view(), name="order"),
    path(
        "order/checkout/<int:pk>/", OrderCheckoutView.as_view(), name="order checkout"
    ),
    path("order/sheet/<int:pk>/", OrderSheetView.as_view(), name="order sheet"),
    path(
        "order/delivering/<int:pk>/",
        DeliveringInfoCreateView.as_view(),
        name="order delivering",
    ),
    path("order/delete/<int:pk>/", OrderDeleteView.as_view(), name="order delete"),
    path("order/add_item/",
         order_item_add,
         name="order_item add"),
    path("order/delete_item/<int:pk>/", OrderItemDeleteView.as_view(),name="order_item delete"),
    path("order/add_item/", order_item_add, name="order_item add"),
    path("order/item_qty_plus/<int:pk>", items_qty_plus, name='item_qty_plus'),
    path("order/item_qty_minus/<int:pk>", items_qty_minus, name='item_qty_minus'),
]
