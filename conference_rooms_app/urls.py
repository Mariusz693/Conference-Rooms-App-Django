from django.urls import path

from .views import HomePageView, ConfirmationView, UserCreateView, UserActiveView, UserLoginView, \
    UserLogoutView, UserDetailView, UserUpdateView, UserPasswordView, UserDeleteView, UserPasswordResetView, \
    UserPasswordSetView


urlpatterns = [
    path('home_page/', HomePageView.as_view(), name='home-page'),
    path('confirmation/', ConfirmationView.as_view(), name='confirmation'),
    path('user_create/', UserCreateView.as_view(), name='user-create'),
    path('user_active/', UserActiveView.as_view(), name='user-active'),
    path('user_login/', UserLoginView.as_view(), name='user-login'),
    path('user_logout/', UserLogoutView.as_view(), name='user-logout'),
    path('user_detail/', UserDetailView.as_view(), name='user-detail'),
    path('user_update/', UserUpdateView.as_view(), name='user-update'),
    path('user_password/', UserPasswordView.as_view(), name='user-password'),
    path('user_delete/', UserDeleteView.as_view(), name='user-delete'),
    path('user_password_reset/', UserPasswordResetView.as_view(), name='user-password-reset'),
    path('user_password_set/', UserPasswordSetView.as_view(), name='user-password-set'),
]
