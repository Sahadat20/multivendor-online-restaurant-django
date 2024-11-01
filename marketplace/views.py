from django.shortcuts import render, get_object_or_404, redirect
from vendor.models import Vendor
from menue.models import Category, FoodItem
from django.db.models import Prefetch
from django.http import HttpResponse, JsonResponse
from .models import Cart
from marketplace.context_processor import get_cart_counter, get_cart_amount
from django.contrib.auth.decorators import login_required
from orders.forms import OrderForm
from accounts.models import UserProfile
# Create your views here.
def marketplace(request):
    vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)
    vendor_count = vendors.count()
    context = {
        'vendors' : vendors,
        'vendor_count':vendor_count,
    }
    return render(request, 'marketplace/listings.html',context)

def vendor_detail(request, vendor_slug):
    vendor = get_object_or_404(Vendor, vendor_slug=vendor_slug )
    categories = Category.objects.filter(vendor=vendor)
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_items = None
    context = {
        'vendor' : vendor,
        'categories' : categories,
        'cart_items' : cart_items,
    }
    return render(request, 'marketplace/vendor_detail.html', context)
@login_required(login_url='login')
def add_to_cart(request, food_id):
    print(request)
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                fooditem = FoodItem.objects.get(id=food_id)
                # check this food is in cart or not
                try:
                    chkCart = Cart.objects.get(user=request.user, fooditem=fooditem)
                    # increase cart qty
                    chkCart.quantity +=1
                    chkCart.save()
                    return JsonResponse({'status':'Success', 'message':'Increased cart qty', 'cart_counter': get_cart_counter(request), 'qty': chkCart.quantity, 'cart_amount': get_cart_amount(request)  })
                except:
                    chkCart = Cart.objects.create(user=request.user, fooditem=fooditem, quantity=1)
                    return  JsonResponse({'status':'Success', 'message':'Added food to the cart', 'cart_counter': get_cart_counter(request), 'qty': chkCart.quantity,  'cart_amount': get_cart_amount(request)})
            except:
                return JsonResponse({'status':'Failed', 'message':'This food does not exist'})
        else:
            return JsonResponse({'status':'Failed', 'message':'Invalid request'})
    else:
        return JsonResponse({'status':'login_required', 'message':'Please login to continue'})
@login_required(login_url='login')    
def decrease_cart(request, food_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                fooditem = FoodItem.objects.get(id=food_id)
                # check this food is in cart or not
                try:
                    chkCart = Cart.objects.get(user=request.user, fooditem=fooditem)
                    # increase cart qty
                    if chkCart.quantity > 1:
                        chkCart.quantity -=1
                        chkCart.save()
                    else:
                        chkCart.delete()
                        chkCart.quantity = 0
                    return JsonResponse({'status':'Success', 'cart_counter': get_cart_counter(request), 'qty': chkCart.quantity, 'cart_amount': get_cart_amount(request)  })
                except:
                    
                    return  JsonResponse({'status':'Failed', 'message':'You does not have item in your card'})
            except:
                return JsonResponse({'status':'Failed', 'message':'This food does not exist'})
        else:
            return JsonResponse({'status':'Failed', 'message':'Invalid request'})
    else:
        return JsonResponse({'status':'login_required', 'message':'Please login to continue'})

@login_required(login_url='login')
def cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    context = {
        'cart_items' : cart_items,
    }
    return render(request, 'marketplace/cart.html',context )
@login_required(login_url='login')
def delete_cart(request, cart_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                cart_item = Cart.objects.get(user=request.user, id=cart_id)
                if cart_item:
                    cart_item.delete()
                    return JsonResponse({'status':'Success','message' : 'Cart item has been deleted' ,'cart_counter': get_cart_counter(request) , 'cart_amount': get_cart_amount(request) })
            except:
                return  JsonResponse({'status':'Failed', 'message':'Cart item does not exists'})

        else:
            return JsonResponse({'status':'Failed', 'message':'Invalid request'})
@login_required(login_url='login')     
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)
    cart_count = cart_items.count()
    if cart_count <=0:
        return redirect('marketplace')
    user_profile = UserProfile.objects.get(user=request.user)
    default_value = {
        'first_name' : request.user.first_name,
        'last_name' : request.user.last_name,
        'phone' : request.user.phone_number,
        'email' : request.user.email,
        'address' : user_profile.address,
        'country' : user_profile.country,
        'state' : user_profile.state,
        'city' : user_profile.city,
        'pin_code' : user_profile.pin_code,

    }
    form = OrderForm(initial=default_value)
    context = {
        'form': form,
        'cart_items' : cart_items
    }
    return render(request, 'marketplace/checkout.html',context)