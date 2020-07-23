from django.urls import path
from .views import registration


urlpatterns = [
    path('auth/Signup/', registration, name="registration"),
]
