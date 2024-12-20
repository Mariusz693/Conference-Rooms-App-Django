from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

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
