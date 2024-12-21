from django.urls import path

from .views import HomePageView


urlpatterns = [
    path('home_page/', HomePageView.as_view(), name='home-page'),
]
