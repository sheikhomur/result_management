from django.urls import path
from .views import LoginView, LogoutView


urlpatterns = [
    path('login/', LoginView.as_view(), name="login_url"),
    path('logout/', LogoutView.as_view(), name="logout_url"),
]
