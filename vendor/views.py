from django.shortcuts import render, get_object_or_404, redirect
from .forms import VendorForm
from accounts.forms import UserProfileForm
from .models import Vendor
from accounts.models import UserProfile
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.views import chek_role_vendor
from menue.models import Category , FoodItem
from menue.forms import categoryForm,FoodItemForm
from django.template.defaultfilters import slugify
from orders.models import Order, OrderedFood

# Create your views here.
def get_vendor(request):
    vendor = Vendor.objects.get(user=request.user)
    return vendor

@login_required(login_url='login')
@user_passes_test(chek_role_vendor)
def vprofile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    vendor = get_object_or_404(Vendor, user=request.user)
    if request.method=='POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        vendor_form = VendorForm(request.POST, request.FILES, instance=vendor)
        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request, "Settings updated")
            return redirect('vprofile')
        else:
            print(profile_form.errors)
            print(vendor_form.errors)
    else:
        profile_form = UserProfileForm(instance=profile)
        vendor_form = VendorForm(instance=vendor)
    context = {
        'profile_form':profile_form,
        'vendor_form':vendor_form,
        'profile':profile,
        'vendor':vendor,
    }
    return render(request, 'vendor/vprofile.html',context)
@login_required(login_url='login')
@user_passes_test(chek_role_vendor)
def menu_builder(request):
    vendor = get_vendor(request)
    categories = Category.objects.filter(vendor=vendor).order_by('created_at')
    conext = {
        'categories' : categories,
    }
    return render(request, 'vendor/menu-builder.html', conext)

@login_required(login_url='login')
@user_passes_test(chek_role_vendor)
def fooditems_by_category(request, pk=None):
    vendor = get_vendor(request)
    category = get_object_or_404(Category, pk=pk)
    fooditems = FoodItem.objects.filter(vendor=vendor, category=category)
    context = {
        'fooditems':fooditems,
        'category' : category,
    }
    return render(request, 'vendor/fooditems_by_category.html', context)

@login_required(login_url='login')
@user_passes_test(chek_role_vendor)
def add_categor(request):
    print(request)
    if request.method == 'POST':
        print('===')
        form = categoryForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.vendor = get_vendor(request)
            category.slug = slugify(category_name)
            form.save()
            messages.success(request, "Category Added Susccessfully")
            return redirect('menu_builder')
        else:
            print(form.errors)
    else:
        form = categoryForm()
    context = {
        'form': form,
    }
    return render(request, 'vendor/add_categor.html', context)

@login_required(login_url='login')
@user_passes_test(chek_role_vendor)
def edit_category(request, pk=None):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = categoryForm(request.POST, instance=category)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.vendor = get_vendor(request)
            category.slug = slugify(category_name)
            form.save()
            messages.success(request, "Category Updated Susccessfully")
            return redirect('menu_builder')
        else:
            print(form.errors)
    else:
        form = categoryForm(instance=category)
    context = {
        'form': form,
        'category':category,
    }
    return render(request,'vendor/edit_categor.html',context )

@login_required(login_url='login')
@user_passes_test(chek_role_vendor)
def delete_category(request, pk=None):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    messages.success(request,"Category has been deleted successfully")
    return redirect('menu_builder')

@login_required(login_url='login')
@user_passes_test(chek_role_vendor)
def add_food(request):
    if request.method == 'POST':
        print('===')
        form = FoodItemForm(request.POST, request.FILES)
        if form.is_valid():
            food_title = form.cleaned_data['food_title']
            food = form.save(commit=False)
            food.vendor = get_vendor(request)
            food.slug = slugify(food_title)
            form.save()
            messages.success(request, "Food Item Added Susccessfully")
            return redirect('fooditems_by_category',food.category.id)
        else:
            print(form.errors)
    else:
        
        form = FoodItemForm()
        form.fields['category'].queryset = Category.objects.filter(vendor=get_vendor(request))
    context = {
        'form':form,
    }
    return render(request, 'vendor/add_food.html',context)


@login_required(login_url='login')
@user_passes_test(chek_role_vendor)
def edit_food(request, pk=None):
    food = get_object_or_404(FoodItem, pk=pk)
    if request.method == 'POST':
        form = FoodItemForm(request.POST, request.FILES, instance=food)
        if form.is_valid():
            food_title = form.cleaned_data['food_title']
            food = form.save(commit=False)
            food.vendor = get_vendor(request)
            food.slug = slugify(food_title)
            form.save()
            messages.success(request, "Food Item Updated Susccessfully")
            return redirect('fooditems_by_category',food.category.id)
        else:
            print(form.errors)
    else:
        form = FoodItemForm(instance=food)
        form.fields['category'].queryset = Category.objects.filter(vendor=get_vendor(request))
    context = {
        'form': form,
        'food' : food,
    }
    return render(request,'vendor/edit_food.html',context )

@login_required(login_url='login')
@user_passes_test(chek_role_vendor)
def delete_food(request, pk=None):
    food = get_object_or_404(FoodItem, pk=pk)
    food.delete()
    messages.success(request,"Food Item has been deleted successfully")
    return redirect('fooditems_by_category',food.category.id)

def order_detail(request,order_number):
    try:
        order = Order.objects.get(order_number=order_number)
        ordered_items = OrderedFood.objects.filter(order=order, fooditem__vendor = get_vendor(request))
        print(ordered_items)
        sub_total = 0
        for item in ordered_items:
            sub_total += item.price * item.quantity
        context = {
            'order' : order,
            'ordered_items' : ordered_items,
            'sub_total' : sub_total,
        }
        return render(request, 'vendor/order_detail.html',context)
    except:
        redirect('vendor')

    