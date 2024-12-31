from django import forms
from django.core.exceptions import ValidationError

from .models import User, Reservation
from .validators import validate_password


class UserCreateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'phone_number', 'password', 'password_repeat']
    
    password = forms.CharField(label='Hasło', max_length=64, widget=forms.PasswordInput())
    password_repeat = forms.CharField(label='Powtórz hasło', max_length=64, widget=forms.PasswordInput())
    
    def clean(self, *args, **kwargs):
        
        super().clean(*args, **kwargs)

        password = self.cleaned_data['password']
        password_repeat = self.cleaned_data['password_repeat']

        if password != password_repeat:
            self.add_error('password_repeat', 'Hasła róźnią się między sobą')
        
        try:
            validate_password(password=password)
        
        except ValidationError as e:
            self.add_error('password', e)
    
    def save(self, commit=True, *args, **kwargs):
        
        return User.objects.create_user(
            email=self.cleaned_data['email'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            phone_number=self.cleaned_data['phone_number'],
            password=self.cleaned_data['password'],
        )


class UserLoginForm(forms.Form):

    email = forms.CharField(label='Email', max_length=255, widget=forms.EmailInput())
    password = forms.CharField(label='Hasło', max_length=64, widget=forms.PasswordInput())

    def clean(self, *args, **kwargs):

        super().clean(*args, **kwargs)

        email = self.cleaned_data['email']

        if not User.objects.filter(email=email):
            self.add_error('email', 'Brak takiego adresu email')


class UserPasswordForm(forms.Form):

    password = forms.CharField(label='Stare hasło', max_length=64, widget=forms.PasswordInput())
    password_new = forms.CharField(label='Nowe hasło', max_length=64, widget=forms.PasswordInput())
    password_repeat = forms.CharField(label='Powtórz hasło', max_length=64, widget=forms.PasswordInput())
    
    def clean(self, *args, **kwargs):

        super().clean(*args, **kwargs)

        password_new = self.cleaned_data['password_new']
        password_repeat = self.cleaned_data['password_repeat']

        try:
            validate_password(password=password_new)

        except ValidationError as e:
            self.add_error('password_new', e)

        if password_new != password_repeat:
            self.add_error('password_repeat', 'Hasła róźnią się między sobą')


class UserPasswordResetForm(forms.Form):

    email = forms.CharField(label='Email', max_length=255, widget=forms.EmailInput())
    
    def clean(self, *args, **kwargs):

        super().clean(*args, **kwargs)

        email = self.cleaned_data['email']

        if not User.objects.filter(email=email):
            self.add_error('email', 'Brak takiego adresu email')


class UserPasswordSetForm(forms.Form):

    password_new = forms.CharField(label='Nowe hasło', max_length=64, widget=forms.PasswordInput())
    password_repeat = forms.CharField(label='Powtórz hasło', max_length=64, widget=forms.PasswordInput())
    
    def clean(self, *args, **kwargs):

        super().clean(*args, **kwargs)

        password_new = self.cleaned_data['password_new']
        password_repeat = self.cleaned_data['password_repeat']
    
        try:
            validate_password(password=password_new)

        except ValidationError as e:
            self.add_error('password_new', e)

        if password_new != password_repeat:
            self.add_error('password_repeat', 'Hasła róźnią się między sobą')


class RoomSearchForm(forms.Form):

    capacity = forms.IntegerField(
        label=False,
        widget=forms.NumberInput(attrs={'class': 'my-input-search', 'title': 'Min. pojemność'}),
        min_value=1,
        required=False
    )
    is_projector = forms.BooleanField(
        label='',
        widget=forms.CheckboxInput(attrs={'class': 'my-checkbox-search', 'title': 'Projektor'}),
        required=False
    )


class ReservationCreateForm(forms.ModelForm):

    class Meta:
        model = Reservation
        fields = ['room', 'user', 'date', 'message']
        widgets = {
            'room': forms.HiddenInput(),
            'user': forms.HiddenInput(),
            'date': forms.HiddenInput(),
            'message': forms.Textarea(attrs={'rows': '5'})
        }
    
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields['message'].required = False


class UserSearchForm(forms.Form):

    last_name = forms.CharField(
        label=False,
        widget=forms.TextInput(attrs={'class': 'my-input-search', 'title': 'Nazwisko'}),
        required=False
    )


class ContactPageForm(forms.Form):

    email = forms.CharField(label='Email', max_length=255, widget=forms.EmailInput())
    first_name = forms.CharField(label='Imię', max_length=64)
    last_name = forms.CharField(label='Nazwisko', max_length=64)
    subject = forms.CharField(label='Temat', max_length=64)
    message = forms.CharField(label='Wiadomość', widget=forms.Textarea(attrs={'rows': '6'}))
