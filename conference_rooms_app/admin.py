from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import User, UserUniqueToken, Room, Reservation, ReservationUniqueToken

# Register your models here.


@admin.register(User)
class UserAdmin(DjangoUserAdmin):

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone_number', 'status')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('first_name', 'last_name', 'email', 'phone_number', 'status')
    search_fields = ('first_name', 'last_name', 'email')
    
    ordering = ('last_name', 'first_name')


@admin.register(UserUniqueToken)
class UserUniqueTokenAdmin(admin.ModelAdmin):

    list_display = ('user', 'token')


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    
    list_display = ('name', 'capacity', 'is_projector')


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    
    list_display = ('room', 'user', 'date', 'is_confirmed')


@admin.register(ReservationUniqueToken)
class ReservationUniqueTokenAdmin(admin.ModelAdmin):

    list_display = ('reservation', 'token')
