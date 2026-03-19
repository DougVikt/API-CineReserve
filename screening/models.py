from django.db import models
from django.utils import timezone 
# extra imports 
from datetime import timedelta


class Genre(models.Model):
    name = models.CharField(max_length=30 , unique=True)
    
    class Meta:
        verbose_name = "Genero"
        verbose_name_plural = "Generos"
        
    def __str__(self):
        return self.name
    


class Movie(models.Model):
    
    class AudioType(models.TextChoices):
        DUBBED = 'dubbed' , 'Dublado'
        SUBTITLED = 'subtitled' , 'Legendado'
        
    class AgeRating(models.TextChoices):
        FREE = 'L' , 'Livre'
        TEN = '10' , '10 anos'
        TWELVE = '12' , '12 anos'
        FOURTEEN = '14' , '14 anos'
        SIXTEEN = '16' ,'16 anos'
        EIGHTEEN = '18' , '18 anos'
        
    title = models.CharField( max_length=200)
    description = models.TextField()
    banner = models.ImageField(upload_to='banners/')
    duration = models.IntegerField(help_text='Duração em minutos')
    age_rating = models.CharField(max_length=3 , choices=AgeRating.choices)
    audio_type = models.CharField( max_length=10 ,choices=AudioType.choices)
    genres = models.ManyToManyField(Genre)
    
    class Meta:
        verbose_name = 'Filme'
        verbose_name_plural = 'Filmes'
        
    def __str__(self):
        return f'{self.title} = {self.audio_type}'
        

class Session(models.Model):
    movie = models.ForeignKey("Movie", on_delete=models.CASCADE , related_name='sessions')
    room = models.ForeignKey("theater.Room", on_delete=models.CASCADE , related_name='sessions')
    date = models.DateField()
    start_time = models.TimeField()
    end_time =models.TimeField(blank=True)
    
    def save(self, *args ,**kwargs):
        if self.start_time and self.movie :
            start = timezone.datetime.combine(self.date , self.start_time)
            end = start + timedelta(minutes=self.movie.duration + 15)
            self.end_time = end.time()
        super().save(*args ,**kwargs )
    
    class Meta:
        verbose_name = 'Sessão'
        verbose_name_plural = 'Sessões'
            
            
    def __str__(self):
        return f'{self.movie.title} - {self.date}, {self.start_time}'
    
    
    
class Ticket(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='tickets')
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='tickets')
    seat = models.ForeignKey('theater.Seat', on_delete=models.CASCADE, related_name='tickets')
    generated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Ingresso'
        verbose_name_plural = 'Ingressos'
        unique_together = ('session', 'seat')

    def __str__(self):
        return f'{self.user.username} - {self.session} - {self.seat}'
    
    
class SeatReservation(models.Model):
    class Status(models.TextChoices):
        AVAILABLE = 'available' , 'Disponivel'
        RESERVED = 'reserved' , 'Reservado'
        PURCHARSED = 'purchased' , 'Comprado'
        
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='reservations')
    seat = models.ForeignKey("theater.Seat", on_delete=models.CASCADE , related_name='reservations')
    user = models.ForeignKey("accounts.User", on_delete=models.SET_NULL ,null=True , blank=True ,related_name='reservations')
    status = models.CharField(max_length=50 ,choices=Status.choices,default=Status.AVAILABLE )
    expires_at = models.DateField(null=True ,blank=True)
    
    class Meta:
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'
        unique_together = ('session' , 'seat')
        
    def __str__(self):
        return f"{self.seat} - {self.session} - {self.status}"
    
        