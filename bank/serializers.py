from rest_framework import serializers
from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    amount = serializers.DecimalField(max_digits=6 ,decimal_places=2 ,read_only=True)
    
    class Meta:
        model = Payment
        fields = (
           'id',
           'ticket',
           'status',
           'payment_method',
        ) 
