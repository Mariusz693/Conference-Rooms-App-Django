from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, FormView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .forms import UserCreateForm, UserLoginForm, UserPasswordResetForm, UserPasswordSetForm, UserPasswordForm
from .models import User, UserUniqueToken
from .validators import validate_token

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
