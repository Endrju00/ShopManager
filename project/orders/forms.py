from django import forms

from .models import ItemInOrder
from products.models import DeliveredItems


class ItemInOrderForm(forms.ModelForm):
    class Meta:
        model = ItemInOrder
        fields = ['quantity', 'delivery']

    def __init__(self, *args, **kwargs):
        super(ItemInOrderForm, self).__init__(*args, **kwargs)
        delivered = DeliveredItems.objects.all()
        wanted = set()

        for delivery in delivered:
            quantity = 0
            items = ItemInOrder.objects.filter(delivery__id=delivery.id)
            
            for item in items:
                quantity += item.quantity
            
            if delivery.quantity - quantity > 0:
                wanted.add(delivery.id)

        self.fields['delivery'].queryset = DeliveredItems.objects.filter(id__in=wanted)