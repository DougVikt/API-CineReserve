# django imports
# from django.shortcuts import render
from django.utils import timezone
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
# others imports
from datetime import timedelta
import json
# drf imports
from rest_framework import generics ,status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
# internal imports
from .models import Movie, Session, Ticket, SeatReservation
from .serializers import (
    MovieSerializer,
    SessionSerializer,
    TicketSerializer,
    SeatReservationSerializer,
)
from .tasks import send_ticket_confirmation



class MovieListApiView(generics.ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [AllowAny]


class SessionListApiView(generics.ListAPIView):
    serializer_class = SessionSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        movie_id = self.kwargs['movie_id']
        return Session.objects.filter(movie_id=movie_id)


class SeatReservationListApiView(generics.ListAPIView):
    serializer_class = SeatReservationSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        session_id = self.kwargs['session_id']
        return SeatReservation.objects.filter(session_id=session_id)


class TicketListApiView(generics.ListAPIView):
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Ticket.objects.filter(user=self.request.user)



class ReserveSeatApiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, session_id, seat_id):
        reservation = SeatReservation.objects.filter(
            session_id=session_id,
            seat_id=seat_id
        ).first()

        if not reservation:
            return Response(
                {'error': 'Assento não encontrado.'},
                status=status.HTTP_404_NOT_FOUND
            )

        cache_key = f'seat_lock:{session_id}:{seat_id}'
        locked = cache.get(cache_key)

        if locked:
            return Response(
                {'error': 'Assento temporariamente bloqueado.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if reservation.status == SeatReservation.Status.PURCHASED:
            return Response(
                {'error': 'Assento já comprado.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        cache.set(cache_key, request.user.id, timeout=600)  # 10 minutos

        reservation.status = SeatReservation.Status.RESERVED
        reservation.user = request.user
        reservation.expires_at = timezone.now() + timedelta(minutes=10)
        reservation.save()

        return Response(
            SeatReservationSerializer(reservation).data,
            status=status.HTTP_200_OK
        )
        
        
class PurchaseSeatApiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, session_id, seat_id):
        reservation = SeatReservation.objects.filter(
            session_id=session_id,
            seat_id=seat_id,
            user=request.user,
            status=SeatReservation.Status.RESERVED
        ).first()

        if not reservation:
            return Response(
                {'error': 'Reserva não encontrada ou não pertence a você.'},
                status=status.HTTP_404_NOT_FOUND
            )

        if reservation.expires_at < timezone.now():
            reservation.status = SeatReservation.Status.AVAILABLE
            reservation.user = None
            reservation.expires_at = None
            reservation.save()
            cache.delete(f'seat_lock:{session_id}:{seat_id}')
            return Response(
                {'error': 'Reserva expirada, selecione o assento novamente.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        reservation.status = SeatReservation.Status.PURCHASED
        reservation.expires_at = None
        reservation.save()

        cache.delete(f'seat_lock:{session_id}:{seat_id}')

        ticket = Ticket.objects.create(
            user=request.user,
            session_id=session_id,
            seat_id=seat_id
        )

        send_ticket_confirmation.delay(ticket.id)

        return Response(
            TicketSerializer(ticket).data,
            status=status.HTTP_201_CREATED
        )
        
        
# endpoints cache       
@method_decorator(cache_page(60 * 5), name='dispatch')  # cache de 5 minutos
class MovieListView(generics.ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [AllowAny]


@method_decorator(cache_page(60 * 5), name='dispatch')  # cache de 5 minutos
class SessionListView(generics.ListAPIView):
    serializer_class = SessionSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        movie_id = self.kwargs['movie_id']
        return Session.objects.filter(movie_id=movie_id)