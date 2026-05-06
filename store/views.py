from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Order, OrderItem
from .forms import ContactForm


def home(request):
    return render(request, 'store/home.html')


def product_list(request):
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})


def add_to_cart(request, id):
    cart = request.session.get('cart', {})
    cart[str(id)] = cart.get(str(id), 0) + 1
    request.session['cart'] = cart
    return redirect('cart')


def _get_cart_items(cart):
    items = []
    total = 0

    for product_id, qty in cart.items():
        product = get_object_or_404(Product, id=product_id)
        items.append({
            'product': product,
            'quantity': qty
        })
        total += product.price * qty

    return items, total


def cart(request):
    cart_data = request.session.get('cart', {})
    items, total = _get_cart_items(cart_data)

    return render(request, 'store/cart.html', {
        'items': items,
        'total': total
    })


def checkout(request):
    cart_data = request.session.get('cart', {})
    items, total = _get_cart_items(cart_data)

    if not items:
        return redirect('cart')

    if request.method == 'POST':
        order = Order.objects.create(total=total)
        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                quantity=item['quantity'],
                price=item['product'].price
            )
        request.session['cart'] = {}
        return redirect('order_success', order_id=order.id)

    return render(request, 'store/checkout.html', {
        'items': items,
        'total': total
    })


def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'store/order_success.html', {
        'order': order
    })


def form_view(request):
    form = ContactForm()
    success = False

    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            success = True

    return render(request, 'store/form.html', {
        'form': form,
        'success': success
    })