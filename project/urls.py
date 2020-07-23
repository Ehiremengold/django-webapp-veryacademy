"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import (LogoutView, LoginView,
                                       PasswordResetView, PasswordResetDoneView,
                                       PasswordResetConfirmView, PasswordResetCompleteView)
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import user_profile
from hustle import views
admin.site.site_header = "myHustle Admin"
admin.site.index_title = "myHustle Admin Panel"


urlpatterns = [
    path('', include('hustle.urls')),
    path("api/", include('api.urls')),
    path('search/auto/', views.search_auto, name="search_auto"),
    path('myhustle/admin/', admin.site.urls),
    path('accounts/', include("accounts.urls")),
    path("accounts/auth/login/", LoginView.as_view(template_name="login.html"), name="login"),
    path("accounts/logout/", LogoutView.as_view(template_name="logout.html"), name="logout"),
    path("accounts/auth/password-reset/", PasswordResetView.as_view(template_name="password-reset.html"), name="password_reset"),
    path("accounts/auth/password-reset/done", PasswordResetDoneView.as_view
    (template_name="password-reset-done.html"), name="password_reset_done"),
    path("accounts/auth/password-reset-confirm/<uidb64>/<token>", PasswordResetConfirmView.as_view
    (template_name="password-reset-confirm.html"), name="password_reset_confirm"),
    path('<str:username>/', user_profile, name="profile"),
    path("accounts/auth/password-reset-complete/", PasswordResetCompleteView.as_view(template_name="password-reset-complete.html"),
         name="password_reset_complete"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
