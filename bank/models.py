from django.db import models

class Payment(models.Model):
    
    class Status(models.TextChoices):
        PENDING = 'pending' ,'pendente'
        APPROVED = 'aproved' , 'aprovado'
        FAILED  = 'failed', 'falhou'
        REFUNDED = 'refunded' , 'reembolsado'
        
    class Payment_method(models.TextChoices):
        CREDIT_CARD = 'credit card', 'cartão de credito'
        DEBIT_CARD = 'debit card' , 'cartão de debito'
        PIX = 'pix'
    
    ticket = models.OneToOneField("screening.Ticket", on_delete=models.CASCADE , related_name='payment')
    amount = models.DecimalField( max_digits=6, decimal_places=2)
    status = models.CharField( max_length=50 ,choices=Status.choices , default=Status.PENDING)
    payment_method = models.CharField( max_length=50 ,choices=Payment_method.choices , default=Payment_method.PIX)
    created_at = models.DateTimeField(auto_now=True)
