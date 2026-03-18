from django.db import models


class Room (models.Model):
    name = models.CharField(max_length=50)
    capacity = models.IntegerField()
    
    class Meta: 
        verbose_name = "Sala"
        verbose_name_plural = "Salas"
        
    def __str__(self):
        return self.name
    


class Seat(models.Model):
    room = models.ForeignKey(Room , on_delete=models.CASCADE , related_name='seats')
    row = models.CharField(max_length=5)
    number = models.IntegerField()
    
    class Meta:
        verbose_name = "Assento"
        verbose_name_plural = "Assentos"
        unique_together = ('room' , 'row' ,'number')
        
    def __str__(self):
        return f"{self.row}{self.number} = {self.room}"
    