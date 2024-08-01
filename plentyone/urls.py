# plentyone/urls.py
from django.urls import path
from . import views
app_name = 'plentyone'

urlpatterns = [
    path('', views.home, name='home'),
    path('order/', views.order, name='order'),
    path('start/', views.start, name='start'),
    path('service/', views.service, name='service'),
    path('signup/', views.signup_view, name='signup'),
    path('withdraw/', views.withdraw, name='withdraw'),
    path('switch-language/', views.switch_language, name='switch_language'),
    path('product-detail/', views.product_detail, name='product_detail'),
    # path('pay-now/', views.pay_now, name='pay-now'),
    path('process_order/', views.process_order, name='process_order'),
    path('get-invitation-code/', views.get_invitation_code, name='get_invitation_code'),
]