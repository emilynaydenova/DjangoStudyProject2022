from django import forms

from orders.models.model_choices import PENDING
from orders.models.orders import DeliveringInfo, Order
from orders.tasks import send_mail_for_pending_order


class DeliveringInfoForm(forms.ModelForm):
    class Meta:
        model = DeliveringInfo
        fields = (
            "address",
            "city",
        )
        widgets = {
            "address": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Address..."}
            ),
            "city": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "City..."}
            ),
        }


class CheckoutOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = (
            "status",
            "delivery",
        )

        widgets = {
            "status": forms.HiddenInput(),
        }

    def clean(self):
        #  Order status changed to Pending
        self.cleaned_data["status"] = PENDING
        send_mail_for_pending_order.delay(self.instance.pk)
