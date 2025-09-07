from django.urls import path
from .views import RegisterView, LoginView, LogoutView

app_name = "accounts"
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView, name='login'),
    path('logout/', LogoutView, name='logout'),
]
