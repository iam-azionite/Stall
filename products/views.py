from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product,Cart,CartItem,OrderItem,Order

# Create your views here.
def products(request):
    products=Product.objects.all()
    return render(request,'products.html',{'products':products})

@login_required
def cart(request):
    cart,created=Cart.objects.get_or_create(user=request.user)
    cart_items=CartItem.objects.filter(cart=cart)
    total=0
    for item in cart_items:
        total+=item.quantity * item.product.price
    return render(request,'cart.html',{'cart':cart,'total':total,'cart_items':cart_items})

@login_required
def add_to_cart(request,id):
    cart,created=Cart.objects.get_or_create(user=request.user)
    product=Product.objects.get(id=id)
    if product.stock<=0:
        return redirect('products')
    cart_item,created=CartItem.objects.get_or_create(cart=cart,product=product)
    if not created:
        if cart_item.product.stock>cart_item.quantity:
            cart_item.quantity+=1
            cart_item.save()
    return redirect('cart')

@login_required
def remove_from_cart(request,id):
    cart_item=CartItem.objects.get(id=id)
    cart_item.delete()
    return redirect('cart')

@login_required
def increase_quantity(request,id):
    cart_item=CartItem.objects.get(id=id)
    if cart_item.quantity<cart_item.product.stock:
        cart_item.quantity+=1
        cart_item.save()
    return redirect('cart')

@login_required
def decrease_quantity(request,id):
    cart_item=CartItem.objects.get(id=id)
    if cart_item.quantity>1:
        cart_item.quantity-=1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')

@login_required
def checkout(request):
    cart,created=Cart.objects.get_or_create(user=request.user)
    cart_items=CartItem.objects.filter(cart=cart)
    total=0
    for item in cart_items:
        total+=item.product.price* item.quantity
    if request.method=='POST':
        for item in cart_items:
            if item.quantity > item.product.stock:
                return render(
                    request,
                    'checkout.html',
                    {
                        'cart': cart,
                        'total': total,
                        'cart_items': cart_items,
                        'error': f'Not enough stock for {item.product.name}'
                    }
                )
        name=request.POST.get('name')
        phone=request.POST.get('phone')
        address=request.POST.get('address')
        order=Order.objects.create(user=request.user,name=name,phone=phone,address=address,total=total)
        for item in cart_items:
            OrderItem.objects.create(order=order,product=item.product,quantity=item.quantity,price=item.product.price)
            item.product.stock-=item.quantity
            item.product.save()
        cart_items.delete()
        return redirect('order_success',id=order.id)
    return render(request,'checkout.html',{'cart':cart,'total':total,'cart_items':cart_items})

@login_required
def order_success(request,id):
    order=Order.objects.get(id=id)
    order_items=OrderItem.objects.filter(order=order)
    return render(request,'order_success.html',{'order':order,'order_items':order_items})

def my_orders(request):
    orders=Order.objects.filter(user=request.user)
    return render(request,'my_orders.html',{'orders':orders})

@login_required
def order_detail(request,id):
    order=Order.objects.get(id=id,user=request.user)
    order_items=OrderItem.objects.filter(order=order)
    return render(request,'order_detail.html',{'order':order,'order_items':order_items})

from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User

def is_admin(user):
    return user.is_staff

@user_passes_test(is_admin)
def admin_dashboard(request):

    total_products = Product.objects.count()
    total_users = User.objects.count()
    total_orders = Order.objects.count()

    total_sales = sum(order.total for order in Order.objects.all())

    pending_orders = Order.objects.filter(status='Pending').count()

    low_stock_products = Product.objects.filter(stock__lte=5)
    all_products = Product.objects.all()

    recent_orders = Order.objects.order_by('-id')[:5]
    all_orders = Order.objects.order_by('-id')

    context = {
        'total_products': total_products,
        'total_users': total_users,
        'total_orders': total_orders,
        'total_sales': total_sales,
        'pending_orders': pending_orders,
        'low_stock_products': low_stock_products,
        'recent_orders': recent_orders,
        'all_orders': all_orders,
        'all_products': all_products,

    }

    return render(request, 'admin_dashboard.html', context)

@user_passes_test(is_admin)
def update_order_status(request, order_id):

    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        new_status = request.POST.get('status')

        if new_status in dict(Order._meta.get_field('status').choices):
            order.status = new_status
            order.save()

    return redirect('admin_dashboard')


@user_passes_test(is_admin)
def admin_order_detail(request, order_id):

    order = get_object_or_404(Order, id=order_id)

    order_items = OrderItem.objects.filter(order=order)

    for item in order_items:
        item.subtotal = item.price * item.quantity

    return render(request, 'admin_order_detail.html', {
        'order': order,
        'order_items': order_items,
    })