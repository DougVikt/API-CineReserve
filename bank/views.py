from django.views import reques
# imports drf
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import PaymentSerializer



class PaymentApiView(CreateAPIView):
    permission_classes = [IsAuthenticated]  
    serializer_class = PaymentSerializer
    
    def perform_create(self, serializer):
        ticket = serializer.validated_data['ticket']
        amount = ticket.session.price
        serializer.save(amount=amount)     
   