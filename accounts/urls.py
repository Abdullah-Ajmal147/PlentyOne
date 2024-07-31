from django.urls import  path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.setting,name='settings'),
    path('profile/', views.profile_view, name='profile'),
    path('records/', views.records_view, name='records'),
    path('layer-information/', views.layer_information_view, name='layer_information'),
    path('change-password/', views.change_password_view, name='change_password'),
    path('payment-password/', views.payment_password_view, name='payment_password'),
    path('terms/', views.terms_and_conditions, name="terms"),
    path('logout/', views.logout_view, name='logout')


]


