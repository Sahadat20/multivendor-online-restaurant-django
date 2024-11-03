from django.shortcuts import render, redirect
from marketplace.models import Cart
from marketplace.context_processor import get_cart_amount
from .forms import OrderForm
from .models import Order, OrderedFood
from marketplace.models import Cart
from .utils import generate_order_number
from accounts.utils import send_notification
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url='login')
def place_order(request):
    cart_items = Cart.objects.filter(user=request.user)
    cart_count = cart_items.count()
    if cart_count <=0:
        return redirect('marketplace')
    vendor_ids = []
    for i in cart_items:
        if i.fooditem.vendor.id not in vendor_ids:
            vendor_ids.append(i.fooditem.vendor.id)
    subtotal = get_cart_amount(request)['subtotal']
    tax = get_cart_amount(request)['tax']
    grand_total = get_cart_amount(request)['grand_total']
    order_context = {

    }
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = Order()
            order.first_name = form.cleaned_data['first_name']
            order.last_name = form.cleaned_data['last_name']
            order.phone = form.cleaned_data['phone']
            order.email = form.cleaned_data['email']
            order.address = form.cleaned_data['address']
            order.country = form.cleaned_data['country']
            order.state = form.cleaned_data['state']
            order.city = form.cleaned_data['city']
            order.pin_code = form.cleaned_data['pin_code']
            order.user = request.user
            order.total = grand_total
            order.total_tax = tax
            order.payment_method = request.POST['payment_method']
            order.save()
            order.order_number = generate_order_number(order.id)
            order.vendors.add(*vendor_ids)
            order.save()
            cart_items = Cart.objects.filter(user=request.user) 
            vendor_emails = set()
            ordered_items = []
            for item in cart_items:
                vendor_emails.add(item.fooditem.vendor.user.email)
                ordered_food = OrderedFood()
                ordered_food.order= order
                ordered_food.user = request.user
                ordered_food.fooditem = item.fooditem
                ordered_food.quantity = item.quantity
                ordered_food.price = item.fooditem.price
                ordered_food.amount = item.fooditem.price * item.quantity

                ordered_food.save()
                ordered_items.append(ordered_food)
            order_context = {
                'order' : order,
                'ordered_items' : ordered_items,
            }
            # send notification to custormer billing email
            mail_subject = 'Thank you for ordering from FoodOnline'
            mail_template = 'orders/order_confirmation_email.html'
            context = {
                'user' : request.user,
                'order' : order,
                'to_email' : order.email,
            }
            send_notification(mail_subject, mail_template, context)

            # send notification to vendor
            mail_subject = 'You have received a new order'
            mail_template = 'orders/new_order_received.html'
            # to_emails = []
            # for item in cart_items:
            #     to_emails.append(item.fooditem.vendor.user.email)
            context = {
                'user' : request.user,
                'order' : order,
                'to_email' : vendor_emails,
            }
            send_notification(mail_subject, mail_template, context)
            cart_items.delete()
        else:
            print(form.errors)
    print(order_context)
    return render(request, 'orders/place_order.html',order_context)