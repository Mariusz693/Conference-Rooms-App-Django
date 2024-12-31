from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, FormView, DetailView, UpdateView, DeleteView, ListView, CreateView
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from datetime import date
from dateutil.relativedelta import relativedelta

from .forms import UserCreateForm, UserLoginForm, UserPasswordResetForm, UserPasswordSetForm, UserPasswordForm, \
    RoomSearchForm, ReservationCreateForm
from .models import User, UserUniqueToken, Room, Reservation, ReservationUniqueToken
from .validators import validate_token
from .utils import my_HTMLCalendar

# Create your views here.


class HomePageView(View):

    def get(self, request):

        return render(
            request=request,
            template_name='conference_rooms_app/home_page.html'
        )


class ConfirmationView(View):

    def get(self, request, *args, **kwargs):

        return render(
            request=request,
            template_name='conference_rooms_app/confirmation.html'
        )


class TestMixin1(UserPassesTestMixin):

    def test_func(self):

        if self.request.user.is_authenticated:
            
            return self.request.user.status == 1
        
        else:

            return False

    def handle_no_permission(self):

        if self.request.user.is_authenticated:
            messages.error(self.request, message='Twoje konto nie posiada takich uprawnień')

            return redirect(reverse_lazy('confirmation'))
    
        return redirect(reverse_lazy('user-login')+f'?next={self.request.get_full_path()}')


class TestMixin2(UserPassesTestMixin):

    def test_func(self):

        if self.request.user.is_authenticated:
            
            return self.request.user.status == 2
        
        else:

            return False

    def handle_no_permission(self):

        if self.request.user.is_authenticated:
            messages.error(self.request, message='Twoje konto nie posiada takich uprawnień')

            return redirect(reverse_lazy('confirmation'))
    
        return redirect(reverse_lazy('user-login')+f'?next={self.request.get_full_path()}')


class UserCreateView(FormView):

    form_class = UserCreateForm
    template_name = 'conference_rooms_app/user_create.html'
    success_url = reverse_lazy('confirmation')

    def form_valid(self, form, *args, **kwargs):
        
        user = form.save()
        user_token = UserUniqueToken.objects.create(user=user)
        send_mail(
            subject='Aktywacja konta',
            message=f'Link do aktywacji konta: {self.request.get_host()}{reverse_lazy("user-active")}?token={user_token.token}',
            from_email='service@conference_rooms.com',
            recipient_list=[user.email,]
        )
        messages.add_message(self.request, messages.INFO, message='Twój profil został utworzony, sprawdź pocztę i kliknij link aktywacyjny')

        return super().form_valid(form, *args, **kwargs)


class UserActiveView(View):

    def get(self, request, *args, **kwargs):
        
        token = self.request.GET.get('token')

        if token and validate_token(token) and UserUniqueToken.objects.filter(token=token):
            user_token = UserUniqueToken.objects.get(token=token)
            user = user_token.user
            user.is_active = True
            user.save()
            user_token.delete()
            messages.add_message(self.request, messages.INFO, message='Twój profil został aktywowany')
        
            return redirect(reverse_lazy('user-login'))

        else:
            messages.add_message(self.request, messages.INFO, message='Twój link jest błędny lub źle podany!')
        
            return redirect(reverse_lazy('confirmation'))


class UserLoginView(FormView):

    form_class = UserLoginForm
    template_name = 'conference_rooms_app/user_login.html'

    def get_success_url(self):

        return self.request.GET.get('next') or reverse_lazy('home-page')

    def form_valid(self, form, *args, **kwargs):

        user = User.objects.get(email=form.cleaned_data['email'])
        
        if user.is_active:
            if authenticate(email=form.cleaned_data['email'], password=form.cleaned_data['password']):
                login(self.request, user=user)

                return super().form_valid(form, *args, **kwargs)

            else:
                form.add_error('password', 'Złe hasło')

                return self.form_invalid(form, *args, **kwargs)
        else:
            user_token, created = UserUniqueToken.objects.get_or_create(user=user)
            send_mail(
                subject='Aktywacja konta',
                message=f'Link do aktywacji konta: {self.request.get_host()}{reverse_lazy("user-active")}?token={user_token.token}',
                from_email='service@conference_rooms.com',
                recipient_list=[user.email,]
            )
            messages.add_message(self.request, messages.INFO, message='Twój profil nie został jeszcze aktywowany, sprawdź pocztę i kliknij link aktywacyjny')
 
            return redirect(reverse_lazy('confirmation'))
        

class UserLogoutView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):

        if self.request.user.is_authenticated:
            logout(request=request)
        
        return redirect(reverse_lazy('home-page'))


class UserDetailView(LoginRequiredMixin, DetailView):

    model = User
    template_name = 'conference_rooms_app/user_detail.html'
    context_object_name = 'user'

    def get_object(self, queryset=None):

        return self.request.user


class UserUpdateView(LoginRequiredMixin, UpdateView):

    model = User
    fields = ['first_name', 'last_name', 'email', 'phone_number']
    template_name = 'conference_rooms_app/user_update.html'
    success_url = reverse_lazy('user-detail')

    def get_object(self, queryset=None):
        
        return self.request.user


class UserPasswordView(LoginRequiredMixin, FormView):

    form_class = UserPasswordForm
    template_name = 'conference_rooms_app/user_password.html'
    success_url = reverse_lazy('user-login')

    def form_valid(self, form, *args, **kwargs):
        
        user = self.request.user
        
        if authenticate(email=user.email, password=form.cleaned_data['password']):
            user.set_password(form.cleaned_data['password_new'])
            user.save()
            logout(self.request)

            return super().form_valid(form, *args, **kwargs)

        else:
            form.add_error('password', 'Złe hasło')

            return self.form_invalid(form, *args, **kwargs)


class UserDeleteView(TestMixin1, DeleteView):

    model = User
    template_name = 'conference_rooms_app/user_delete.html'
    success_url = reverse_lazy('home-page')
    context_object_name = 'user'

    def get_object(self, queryset=None):

        return self.request.user


class UserPasswordResetView(FormView):

    form_class = UserPasswordResetForm
    template_name = 'conference_rooms_app/user_password_reset.html'
    success_url = reverse_lazy('confirmation')

    def form_valid(self, form, *args, **kwargs):
        
        user = User.objects.get(email=form.cleaned_data['email'])
        user_token, created = UserUniqueToken.objects.get_or_create(user=user)
        send_mail(
            subject='Resetowanie',
            message=f'Link do utworzenia nowego hasła: {self.request.get_host()}{reverse_lazy("user-password-set")}?token={user_token.token}',
            from_email='service@conference_rooms.com',
            recipient_list=[user.email,]
        )
        messages.add_message(self.request, messages.INFO, message='Sprawdź pocztę i kliknij link resetujący hasło')

        return super().form_valid(form, *args, **kwargs)


class UserPasswordSetView(FormView):

    form_class = UserPasswordSetForm
    template_name = 'conference_rooms_app/user_password_set.html'
    success_url = reverse_lazy('user-login')

    def get(self, request, *args, **kwargs):
        
        token = self.request.GET.get('token')
        
        if token and validate_token(token) and UserUniqueToken.objects.filter(token=token):
            
            return super().get(request, *args, **kwargs)
        
        else:
            messages.error(self.request, message='Twój link jest błędny lub źle podany.')
        
            return redirect(reverse_lazy('confirmation'))
   
    def form_valid(self, form, *args, **kwargs):
        
        token = self.request.GET.get('token')
        user_token = get_object_or_404(UserUniqueToken, pk=token)
        user = user_token.user
        user.set_password(form.cleaned_data['password_new'])
        user.save()
        user_token.delete()
        messages.add_message(self.request, messages.INFO, message='Twoje hasło zostało zmienione')

        return super().form_valid(form, *args, **kwargs)


class RoomListView(ListView):

    model = Room
    template_name = 'conference_rooms_app/room_list.html'
    context_object_name = 'room_list'

    def get_queryset(self):
        
        room_list = super().get_queryset()
        self.form = RoomSearchForm(self.request.GET)

        if self.form.is_valid():
        
            if 'capacity' in self.form.changed_data:
                room_list = room_list.filter(capacity__gte=self.form.cleaned_data['capacity'])

            if 'is_projector' in self.form.changed_data:
                room_list = room_list.filter(is_projector=self.form.cleaned_data['is_projector'])

        return room_list

    def get_context_data(self, *args, **kwargs):
        
        context = super().get_context_data(*args, **kwargs)
        context['form'] = self.form

        return context


class RoomCreateView(TestMixin2, CreateView):

    model = Room
    fields = ['name', 'capacity', 'is_projector']
    template_name = 'conference_rooms_app/room_create.html'
    success_url = reverse_lazy('room-list')


class RoomDetailView(DetailView):

    model = Room
    template_name = 'conference_rooms_app/room_detail.html'
    context_object_name = 'room'

    def get_context_data(self, *args, **kwargs):
        
        context = super().get_context_data(*args, **kwargs)
        actuall_month = date.today().replace(day=1)

        if self.request.GET.get('next'):
            look_month = date.fromisoformat(self.request.GET.get('next'))
            look_month = look_month.replace(day=1)
        
        else:
            look_month = actuall_month
        
        max_month = actuall_month + relativedelta(months=5)
        prev_month = look_month - relativedelta(months=1) if look_month > actuall_month else ''
        next_month = look_month + relativedelta(months=1) if (look_month) < max_month else ''
        my_calendar_html = my_HTMLCalendar(self.get_object(), look_month, self.request.user)
        context['my_calendar'] = my_calendar_html
        context['today'] = look_month
        context['prev_month'] = prev_month
        context['next_month'] = next_month

        return context


class RoomUpdateView(TestMixin2, UpdateView):

    model = Room
    fields = ['name', 'capacity', 'is_projector']
    template_name = 'conference_rooms_app/room_update.html'
    context_object_name = 'room'
    
    def get_success_url(self):
    	
        return reverse_lazy('room-detail', args=[self.get_object().pk,])


class RoomDeleteView(TestMixin2, DeleteView):

    model = Room
    template_name = 'conference_rooms_app/room_delete.html'
    success_url = reverse_lazy('room-list')
    context_object_name = 'room'


class ReservationCreateView(TestMixin1, CreateView):

    model = Reservation
    form_class = ReservationCreateForm
    template_name = 'conference_rooms_app/reservation_create.html'
    success_url = reverse_lazy('confirmation')

    def get_initial(self):

        initial = super().get_initial()
        initial['room'] = get_object_or_404(Room, pk=self.kwargs['room'])
        initial['user'] = self.request.user
        initial['date'] = date.fromisoformat(self.kwargs['date'])
        
        return initial
    
    def get_context_data(self, *args, **kwargs):

        context = super().get_context_data(*args, **kwargs)
        context['room'] = get_object_or_404(Room, pk=self.kwargs['room'])
        context['date'] = date.fromisoformat(self.kwargs['date'])

        return context

    def form_valid(self, form, *args, **kwargs):

        reservation = form.save(commit=True)
        reservation_token = ReservationUniqueToken.objects.create(reservation=reservation)
        send_mail(
            subject='Potwierdzenie rezerwacji',
            message=f'Link do potwierdzenia rezerwacji w dniu {reservation.date}: {self.request.get_host()}{reverse_lazy('reservation-confirm')}?token={reservation_token.token}',
            from_email='service@conference_rooms.com',
            recipient_list=[self.request.user.email,]
        )
        messages.add_message(self.request, messages.INFO, message='Sprawdź pocztę i kliknij link potwierdzający rezerwację sali')

        return super().form_valid(form, *args, **kwargs)


class ReservationConfirmView(UpdateView):

    model = Reservation
    fields = []
    template_name = 'conference_rooms_app/reservation_confirm.html'
    success_url = reverse_lazy('confirmation')
    context_object_name = 'reservation'

    def get(self, request, *args, **kwargs):

        token = self.request.GET.get('token')
        
        if token and validate_token(token) and ReservationUniqueToken.objects.filter(token=token):
            reservation_token = ReservationUniqueToken.objects.get(token=self.request.GET.get('token'))

            if reservation_token.reservation.date < date.today():
                messages.error(self.request, message='Termin rezerwacji już minął.')
        
                return redirect(reverse_lazy('confirmation'))
            
            return super().get(request, *args, **kwargs)
        
        else:
            messages.error(self.request, message='Twój link jest błędny lub źle podany.')
        
            return redirect(reverse_lazy('confirmation'))
        
    def get_object(self, queryset=None):
        
        reservation_token = ReservationUniqueToken.objects.get(token=self.request.GET.get('token'))

        return reservation_token.reservation
 
    def form_valid(self, form, *args, **kwargs):
        
        self.object.is_confirmed = True
        self.object.save()
        self.object.reservationuniquetoken.delete()
        messages.error(self.request, message=f'Twoja rezerwacja została potwierdzona.')
        
        return super().form_valid(form, *args, **kwargs)


class UserReservationListView(TestMixin1, ListView):

    model = Reservation
    template_name = 'conference_rooms_app/user_reservation_list.html'
    context_object_name = 'user_reservation_list'

    def get_queryset(self):
        
        return super().get_queryset().filter(user=self.request.user)


class UserReservationDetailView(TestMixin1, DetailView):

    model = Reservation
    template_name = 'conference_rooms_app/user_reservation_detail.html'
    context_object_name = 'reservation'
    
    def get_context_data(self, *args, **kwargs):

        context = super().get_context_data(*args, **kwargs)
        context['today'] = date.today()
        
        return context


class UserReservationDeleteView(TestMixin1, DeleteView):

    model = Reservation
    template_name = 'conference_rooms_app/user_reservation_delete.html'
    success_url = reverse_lazy('user-reservation-list')
    context_object_name = 'reservation'

    def get(self, request, *args, **kwargs):
        
        if self.get_object().date <= date.today():
            messages.error(self.request, message='Termin rezerwacji już minął.')
        
            return redirect(reverse_lazy('confirmation'))
            
        return super().get(request, *args, **kwargs)


class UserReservationConfirmView(TestMixin1, UpdateView):

    model = Reservation
    fields = []
    template_name = 'conference_rooms_app/user_reservation_confirm.html'
    context_object_name = 'reservation'
    
    def get_success_url(self):
    	
        return reverse_lazy('user-reservation-detail', args=[self.get_object().pk,])

    def get(self, request, *args, **kwargs):
        
        if self.get_object().date <= date.today():
            messages.error(self.request, message='Termin rezerwacji już minął.')
        
            return redirect(reverse_lazy('confirmation'))
            
        return super().get(request, *args, **kwargs)

    def form_valid(self, form, *args, **kwargs):
        
        reservation_token, created = ReservationUniqueToken.objects.get_or_create(reservation=self.get_object())
        send_mail(
            subject='Potwierdzenie rezerwacji',
            message=f'Link do potwierdzenia rezerwacji w dniu {self.get_object().date}: {self.request.get_host()}{reverse_lazy('reservation-confirm')}?token={reservation_token.token}',
            from_email='service@conference_rooms.com',
            recipient_list=[self.request.user.email,]
        )
        
        return super().form_valid(form, *args, **kwargs)
