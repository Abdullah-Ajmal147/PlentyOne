
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import activate
from django.contrib.auth.decorators import login_required
# Create your views here.
# plentyone/views.py
from django.shortcuts import render
from django.conf import settings
from itertools import zip_longest
from orders.models import Item, Layer, Order, OrderItem
from users.models import CustomUser
from profiles.models import UserProfile

def home(request):
    if request.user.is_authenticated:
        print('user login success')
        user= request.user
        try:
            print('test', user)
            user_profile = get_object_or_404(UserProfile, user=user)
            print(user_profile)
            # layer = Layer.objects.#(id=user_profile.layer_information.id)

            layer = Layer.objects.all()
            print('layer', layer)
            context = {
                'current_balance': user_profile.current_balance,
                'commission_earned': user_profile.commision_earned,
                'layer': layer,
                'base_url': settings.BASE_URL,
            }
            return render(request, 'plentyone/home.html', context )
        except:
            return render(request, 'users/login.html' )
    else:
        return render(request, 'users/login.html')

@login_required
@csrf_exempt
def process_order(request):
    if request.method == 'POST':
        try:
            product_id = request.POST.get('product_id')
            quantity = int(request.POST.get('quantity'))
            
            # Fetch the user profile
            user = request.user
            user_profile = get_object_or_404(UserProfile, user=user)
            
            # Fetch the product
            item = get_object_or_404(Item, pk=product_id)
            
            total = item.unit_price * quantity
            
            # Check if user has sufficient balance
            if user_profile.current_balance < total:
                return JsonResponse({'status': 'error', 'message': 'Insufficient balance.'})
            
            # Check if sufficient stock is available
            if item.order_quantity < quantity:
                return JsonResponse({'status': 'error', 'message': 'Requested quantity exceeds available stock.'})
            
            # Deduct the balance
            user_profile.current_balance -= total
            user_profile.save()
            
            # Update item stock
            item.order_quantity -= quantity
            item.save()
            
            # Create the order
            order = Order.objects.create(
                user=user,
                total=total
            )
            
            # Create the order item
            OrderItem.objects.create(
                order=order,
                item=item,
                quantity=quantity,
                price=item.unit_price
            )
            return redirect('home')
            # return render(request, 'plentyone/start.html')
            # return JsonResponse({'status': 'success'})
        except Item.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Product not found.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

@login_required
@csrf_exempt
def order(request):
    user = request.user
    order = Order.objects.filter(user = user)
    if order:
        context={
            'orders': order
        }
        return render(request, 'plentyone/order.html', context)
    else:
        return render(request, 'plentyone/order.html')

def group_by_n(iterable, n):
    """Groups elements of iterable into chunks of size n."""
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=None)

def start(request):
    products = Item.objects.all()
    grouped_products = list(group_by_n(products, 3))
    context = {
        'grouped_products': grouped_products,
        'base_url': settings.BASE_URL,
    }
    return render(request, 'plentyone/start.html', context)

def product_detail(request):
    product_id = request.GET.get('product_id', None)
    print(product_id)
    if product_id: 
        product = get_object_or_404(Item, item_id=product_id)
        order_quantity = product.order_quantity
        return render(request, 'plentyone/product_detail.html', {'product': product, 'order_quantity': order_quantity})
    else:
        # Handle the case where product_id is not provided or invalid
        return render(request, 'error.html', {'message': 'Product not found'})
    
def pay_now(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            product_id = data.get('product_id')
            quantity = data.get('quantity')

            # Process the data, validate stock, etc.
            if not product_id or not quantity:
                return JsonResponse({'success': False, 'error': 'Invalid input.'})

            # Example validation
            if int(quantity) > get_available_stock(product_id):
                return JsonResponse({'success': False, 'error': 'Not enough stock available.'})

            # Further processing and successful response
            return JsonResponse({'success': True})

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request method.'})

def service(request):
    return render(request, 'plentyone/service.html')

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'plentyone/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['phone_number']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            # Return an 'invalid login' error message.
            pass
    return render(request, 'plentyone/login.html')

def withdraw(request):
    return render(request, 'plentyone/partials/withdraw.html')


# myapp/views.py


def switch_language(request):
    lang_code = request.POST.get('language')
    activate(lang_code)
    response = redirect(request.META.get('HTTP_REFERER'))
    response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang_code)
    return response
