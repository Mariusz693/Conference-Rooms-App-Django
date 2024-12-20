from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

from uuid import uuid4

from .managers import CustomUserManager
from .validators import validate_phone

# Create your models here.


class User(AbstractUser):
    
    class Meta:
        verbose_name = 'Użytkownik'
        verbose_name_plural = 'Użytkownicy'
        ordering = ('last_name', 'first_name')

    STATUS_CHOICE = (
        (1, 'Użytkownik'),
        (2, 'Pracownik')
    )

    username = None
    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        unique=True,
        error_messages={'unique': 'Email już zarejestrowany w bazie'}
        )
    password = models.CharField(verbose_name='Hasło', max_length=128)
    first_name = models.CharField(verbose_name="Imię", max_length=64)
    last_name = models.CharField(verbose_name="Nazwisko", max_length=64)
    phone_number = models.CharField(verbose_name='Numer telefonu', max_length=9, validators=[validate_phone])
    status = models.SmallIntegerField(verbose_name='Status', choices=STATUS_CHOICE, default=1)
    is_active = models.BooleanField(verbose_name='Aktywny', default=False)
    is_superuser = models.BooleanField(verbose_name='Superużytkownik', default=False)
    is_staff = models.BooleanField(verbose_name='Personel', default=False)    
    last_login = models.DateTimeField(verbose_name='Ostatnie logowania', blank=True, null=True)
    date_joined = models.DateTimeField(verbose_name='Data dołączenia', default=timezone.now)
    
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        
        return f'{self.first_name} {self.last_name}'


class UserUniqueToken(models.Model):

    class Meta:
        verbose_name = 'Token użytkownika'
        verbose_name_plural = 'Tokeny użytkowników'
        ordering = ('user',)
        
    user = models.OneToOneField('User', verbose_name='Użytkownik', on_delete=models.CASCADE)
    token = models.UUIDField(
        primary_key=True,
        verbose_name='Token',
        default=uuid4,
        editable=False
        )


class Room(models.Model):

    class Meta:
        verbose_name = 'Sala konferencyjna'
        verbose_name_plural = 'Sale konferencyjne'
        ordering = ('name',)

    name = models.CharField(
        verbose_name='Nazwa',
        max_length=64,
        unique=True,
        error_messages={'unique': 'Nazwa sali już zapisana w bazie'}
        )
    capacity = models.PositiveSmallIntegerField(verbose_name='Pojemność')
    is_projector = models.BooleanField(verbose_name='Projector', default=False)

    def __str__(self):
        
        return self.name


class Reservation(models.Model):

    class Meta:
        verbose_name = 'Rezerwacja sali'
        verbose_name_plural = 'Rezerwacje sal'
        ordering = ('-date',)
        unique_together = ('room', 'date')
    
    room = models.ForeignKey('Room', verbose_name='Sala',on_delete=models.CASCADE)
    user = models.ForeignKey('User', verbose_name='Użytkownik',on_delete=models.CASCADE)
    date = models.DateField(verbose_name='Data rezerwacji')
    message = models.TextField(verbose_name='Uwagi', null=True)
    is_confirmed = models.BooleanField(verbose_name='Potwierdzenie', default=False)

    def __str__(self):
        
        return f'{self.room}, {self.user}, {self.date}'
    
    def unique_error_message(self, model_class, unique_check):

        if unique_check == ('room', 'date'):
            
            return 'Sala już zarezerwowana w tym terminie'

        return super().unique_error_message(model_class, unique_check)


class ReservationUniqueToken(models.Model):

    class Meta:
        verbose_name = 'Token rezerwacji'
        verbose_name_plural = 'Tokeny rezerwacji'
        ordering = ('reservation',)
        
    reservation = models.OneToOneField('Reservation', verbose_name='Rezerwacja', on_delete=models.CASCADE)
    token = models.UUIDField(
        primary_key=True,
        verbose_name='Token',
        default=uuid4,
        editable=False
        )
