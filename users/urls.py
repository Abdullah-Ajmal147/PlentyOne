from django.urls import path

from .forms import PhoneLoginForm
from .views import RegisterView, LoginView, share, logout_view, user_view

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('share/', share, name='share'),
    path('logout/', logout_view, name='logout'),
    # path('register/', user_view, name='register'),
    # path('login/', user_view, name='login'),

]
