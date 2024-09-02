
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
from plentyone.forms import WithdrawalForm
from orders.models import Item, Layer, Order, OrderItem
from users.models import CustomUser
from profiles.models import UserProfile, Profile
import secrets
import string

def generate_invitation_code(length=10):
    # Generates a secure random string of letters and digits
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))

@login_required
@csrf_exempt
def home(request):
    if request.user.is_authenticated:
        print('user login success')
        user= request.user
        try:
            print('test', user)
            user_profile = get_object_or_404(UserProfile, user=user)
            print(user_profile)
            if user_profile.invitation_code == None:
                user_profile.invitation_code = generate_invitation_code()
    
                # Save the updated UserProfile
                user_profile.save()
            # layer = Layer.objects.#(id=user_profile.layer_information.id)

            layer = Layer.objects.all()
            context = {
                'current_balance': user_profile.current_balance,
                'commission_earned': user_profile.commision_earned,
                'layers': layer,
                'base_url': settings.BASE_URL,
                'invite_code': user_profile.invitation_code
            }
            return render(request, 'plentyone/home.html', context )
        except Exception as e:
            print(str(e))
            return render(request, 'users/login.html' )
    else:
        return render(request, 'users/login.html')

@login_required
def get_invitation_code(request):
    user = request.user
    if user:
        invitation_code = user.invitation_code
        print(invitation_code)
        return JsonResponse({'success': True, 'invitation_code': invitation_code})
    return JsonResponse({'success': False, 'message': 'User not found.'})

# @login_required
@csrf_exempt
def process_order(request):
    if request.method == 'POST':
        try:
            product_id = request.POST.get('product_id')
            quantity = int(request.POST.get('quantity'))
            print('quantity', quantity)
            
            # Fetch the user profile
            user = request.user
            user_profile = get_object_or_404(UserProfile, user=user)
            
            # Fetch the product
            item = get_object_or_404(Item, pk=product_id)
            
            total = item.unit_price * quantity
            
            # Check if user has sufficient balance
            if user_profile.current_balance < total:
                return JsonResponse({'status': 'error', 'message': 'Insufficient balance.'}, status=400)
            
            # Check if sufficient stock is available
            if item.order_quantity < quantity:
                return JsonResponse({'status': 'error', 'message': 'Requested quantity exceeds available stock.'}, status=400)
            
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
            # return redirect('plentyone:home')
            # return render(request, 'plentyone/start.html')
            # return JsonResponse({'status': 'success'})
            return JsonResponse({'status': 'success', 'message': 'Order placed successfully.'}, status=200)
        except Item.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Product not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)
     
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

@login_required
@csrf_exempt
def order(request):
    user = request.user
    order = Order.objects.filter(user = user)
    if order:
        # Separate orders by status
        pending_orders = order.filter(status='PENDING')
        frozen_orders = order.filter(status='FROZEN')
        completed_orders = order.filter(status='COMPLETED')

        context = {
            'orders': order,
            'pending_orders': pending_orders,
            'frozen_orders': frozen_orders,
            'completed_orders': completed_orders,
            'base_url': settings.BASE_URL,
        }
        return render(request, 'plentyone/order.html', context)
    else:
        return render(request, 'plentyone/order.html')

def group_by_n(iterable, n):
    """Groups elements of iterable into chunks of size n."""
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=None)

@login_required
def start(request):
    user = request.user
    if user:
        order = Order.objects.filter(user = user)
        products = Item.objects.all()
        grouped_products = list(group_by_n(products, 3))
        completed_orders = order.filter(status='COMPLETED').count()
        not_complete = order.count() - completed_orders
        user_profile = get_object_or_404(UserProfile, user=user)
        context = {
            'current_balance': user_profile.current_balance,
            'amount_frozen': user_profile.amount_frozen,
            'credit': user_profile.credit,
            'commision_earned':user_profile.commision_earned,

            'orders': order.count(),
            'not_complete': not_complete,
            'completed_orders': completed_orders,
            'grouped_products': grouped_products,
            'base_url': settings.BASE_URL,
        }
        return render(request, 'plentyone/start.html', context)
    else:
        return render(request, 'users/login.html')
    
    
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


@login_required
def withdraw(request):
    user = request.user
    user_profile = get_object_or_404(UserProfile, user=user)
    # profile = get_object_or_404(Profile, user=user)

    
    if request.method == 'POST':
        form = WithdrawalForm(request.POST, user=user) 
        if form.is_valid():
            withdrawal_request = form.save(commit=False)
            withdrawal_request.user = user
            withdrawal_request.save()
            user_profile.current_balance -= withdrawal_request.amount
            user_profile.save()
            return redirect('plentyone:home')  # Redirect to a success page or home after submission
    else:
        form = WithdrawalForm()
    
    context = {
        'current_balance': user_profile.current_balance,
        'form': form,
    }
    
    return render(request, 'plentyone/partials/withdraw.html', context)


def switch_language(request):
    lang_code = request.POST.get('language')
    activate(lang_code)
    response = redirect(request.META.get('HTTP_REFERER'))
    response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang_code)
    return response
