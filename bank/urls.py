from django.urls import path
from .views import PaymentApiView

urlpatterns = [
    path('' ,PaymentApiView.as_view(),name='payment')
]
