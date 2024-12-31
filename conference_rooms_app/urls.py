from django.urls import path

from .views import HomePageView, ConfirmationView, UserCreateView, UserActiveView, UserLoginView, \
    UserLogoutView, UserDetailView, UserUpdateView, UserPasswordView, UserDeleteView, UserPasswordResetView, \
    UserPasswordSetView, RoomListView, RoomCreateView, RoomDetailView, RoomUpdateView, RoomDeleteView, \
    ReservationCreateView, ReservationConfirmView, UserReservationListView, UserReservationDetailView, \
    UserReservationDeleteView, UserReservationConfirmView, AdminUserListView, AdminUserDetailView, \
    AdminReservationDetailView, AdminReservationConfirmView


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
    path('user_reservation_list/', UserReservationListView.as_view(), name='user-reservation-list'),
    path('user_reservation_detail/<int:pk>/', UserReservationDetailView.as_view(), name='user-reservation-detail'),
    path('user_reservation_delete/<int:pk>/', UserReservationDeleteView.as_view(), name='user-reservation-delete'),
    path('user_reservation_confirm/<int:pk>/', UserReservationConfirmView.as_view(), name='user-reservation-confirm'),
    path('room_list/', RoomListView.as_view(), name='room-list'),
    path('room_create/', RoomCreateView.as_view(), name='room-create'),
    path('room_detail/<int:pk>/', RoomDetailView.as_view(), name='room-detail'),
    path('room_update/<int:pk>/', RoomUpdateView.as_view(), name='room-update'),
    path('room_delete/<int:pk>/', RoomDeleteView.as_view(), name='room-delete'),
    path('reservation_create/<int:room>/<str:date>/', ReservationCreateView.as_view(), name='reservation-create'),
    path('reservation_confirm/', ReservationConfirmView.as_view(), name='reservation-confirm'),
    path('admin_user_list/', AdminUserListView.as_view(), name='admin-user-list'),
    path('admin_user_detail/<int:pk>/', AdminUserDetailView.as_view(), name='admin-user-detail'),
    path('admin_reservation_detail/<int:pk>/', AdminReservationDetailView.as_view(), name='admin-reservation-detail'),
    path('admin_reservation_confirm/<int:pk>/', AdminReservationConfirmView.as_view(), name='admin-reservation-confirm'),
]
