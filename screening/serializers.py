from rest_framework import serializers
from .models import Movie, Genre, Session, Ticket, SeatReservation


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('id', 'name')


class MovieSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = (
            'id',
            'title',
            'description',
            'banner',
            'duration',
            'age_rating',
            'audio_type',
            'genres',
        )


class SessionSerializer(serializers.ModelSerializer):
    movie = MovieSerializer(read_only=True)
    date = serializers.DateField()
    
    class Meta:
        model = Session
        fields = (
            'id',
            'movie',
            'room',
            'date',
            'start_time',
            'end_time',
        )


class SeatReservationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = SeatReservation
        fields = (
            'id',
            'session',
            'seat',
            'status',
            'expires_at',
        )


class TicketSerializer(serializers.ModelSerializer):
    session = SessionSerializer(read_only=True)

    class Meta:
        model = Ticket
        fields = (
            'id',
            'user',
            'session',
            'seat',
            'generated_at',
        )