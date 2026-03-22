from django.urls import path
from .views import (
    MovieListApiView,
    SessionListApiView,
    SeatReservationListApiView,
    TicketListApiView,
    ReserveSeatApiView,
    PurchaseSeatApiView
)

urlpatterns = [
    path('movies/', MovieListApiView.as_view(), name='movie-list'),
    path('movies/<int:movie_id>/sessions/', SessionListApiView.as_view(), name='session-list'),
    path('sessions/<int:session_id>/seats/', SeatReservationListApiView.as_view(), name='seat-list'),
    path('sessions/<int:session_id>/seats/<int:seat_id>/reserve/', ReserveSeatApiView.as_view(), name='reserve-seat'),
    path('sessions/<int:session_id>/seats/<int:seat_id>/purchase/', PurchaseSeatApiView.as_view(), name='purchase-seat'),
    path('tickets/', TicketListApiView.as_view(), name='ticket-list'),
]