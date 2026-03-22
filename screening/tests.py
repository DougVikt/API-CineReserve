# django imports
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
# drf imports
from rest_framework.test import APIClient
from rest_framework import status
# internal imports
from accounts.models import User
from theater.models import Room, Seat
from .models import Movie, Genre, Session, SeatReservation
from datetime import time


class MovieTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.genre = Genre.objects.create(name='Ação')
        self.movie = Movie.objects.create(
            title='Homem Aranha',
            description='Super herói',
            duration=150,
            age_rating='12',
            audio_type='dubbed',
        )
        self.movie.genres.add(self.genre)

    def test_list_movies(self):
        response = self.client.get(reverse('movie-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_list_movies_unauthenticated(self):
        response = self.client.get(reverse('movie-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class SeatReservationTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='senha123@')
        self.room = Room.objects.create(name='Sala 1', capacity=50)
        self.seat = Seat.objects.create(room=self.room, row='A', number=1)
        self.movie = Movie.objects.create(
            title='Homem Aranha',
            description='Super herói',
            duration=150,
            age_rating='12',
            audio_type='dubbed',
        )
        self.session = Session.objects.create(
            movie=self.movie,
            room=self.room,
            date=timezone.now().date(),
            start_time=time(14, 0),
        )
        self.reservation = SeatReservation.objects.create(
            session=self.session,
            seat=self.seat,
            status=SeatReservation.Status.AVAILABLE,
        )
        self.client.force_authenticate(user=self.user)

    def test_reserve_seat_success(self):
        url = reverse('reserve-seat', kwargs={
            'session_id': self.session.id,
            'seat_id': self.seat.id
        })
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'reserved')

    def test_reserve_seat_unavailable(self):
        self.reservation.status = SeatReservation.Status.PURCHASED
        self.reservation.save()
        url = reverse('reserve-seat', kwargs={
            'session_id': self.session.id,
            'seat_id': self.seat.id
        })
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_reserve_seat_unauthenticated(self):
        self.client.force_authenticate(user=None)
        url = reverse('reserve-seat', kwargs={
            'session_id': self.session.id,
            'seat_id': self.seat.id
        })
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)