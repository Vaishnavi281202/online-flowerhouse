from django.shortcuts import redirect, render
from.models import Flower
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
# Create your views here.

def flowerinfo(request):
    # flowers=Flower.objects.all()
    flowers = Flower.objects.filter(isAvail=True)  # Get all available flowers
    return render(request, 'flowerinfo.html', {'flowers': flowers})



from django.shortcuts import render, get_object_or_404
from .models import Flower


def flower_detail(request, id):
    flower = get_object_or_404(Flower, id=id)  # Retrieve the flower or return 404
    print(flower)
    return render(request, 'flower_details.html', {'flower': flower})


from django.shortcuts import render, get_object_or_404
from .models import Flower

def buy_flower(request, id):
    flower = get_object_or_404(Flower, id=id)
    if request.method == 'POST':
        # Process the form submission (e.g., save buyer details, handle payment)
        return render(request, 'success.html', {'flower': flower})
    return render(request, 'buy.html', {'flower': flower})


def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    flower = order.flowerid
    return render(request, 'order_confirmation.html', {'order': order, 'flower': flower})


from django.shortcuts import render, get_object_or_404
from .models import Flower, Customer, Order
from django.utils.timezone import now


def buy_flower(request, id):
    flower = get_object_or_404(Flower, id=id)

    if request.method == 'POST':
        # Extract buyer details
        buyer_name = request.POST['buyer-name']
        buyer_email = request.POST['buyer-email']
        buyer_contact = request.POST['buyer-contact']
        buyer_address = request.POST['buyer-address']
        quantity = int(request.POST['quantity'])

        # Get or create customer instance
        customer, created = Customer.objects.get_or_create(
            name=buyer_name,
            email=buyer_email,
            phno=buyer_contact,  # Ensure this matches your Customer model
            address=buyer_address
        )

        # Calculate total price
        total_price = flower.price * quantity

        # Create an Order instance
        order = Order.objects.create(
            customerid=customer,
            flowerid=flower,
            orderdate=now(),
            price=total_price,
            quantity=quantity,
            status="Pending"
        )
        
        # Render the order confirmation page
        # return render(request, 'order_confirmation.html', {'order': order, 'flower': flower})
        return redirect('order_confirmation', order.id)

    return render(request, 'buy.html', {'flower': flower})



from django.shortcuts import render
from .models import Order, Payment

def orders_list(request):
    # Fetch all orders and payment information
    orders = Order.objects.select_related('customerid', 'flowerid')
    payments = Payment.objects.select_related('orderid')

    # Merge payment status into the orders queryset
    for order in orders:
        try:
            payment = Payment.objects.get(orderid=order.id)  # Fetch payment for the current order
            order.payment_status = payment.status  # Attach payment status to order dynamically
        except Payment.DoesNotExist:
            order.payment_status = "No Payment Found"  # Handle cases with no payment record

    return render(request, 'orders_list.html', {'orders': orders})


from django.shortcuts import render

def aboutus(request):
    return render(request, 'aboutus.html')

from django.shortcuts import render

def contactus(request):
    return render(request, 'contactus.html')  # Connects to Contact Us template


from django.shortcuts import render

def supportus(request):
    return render(request, 'supportus.html')  # Loads the Support template


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")  # Redirect to homepage after login
        else:
            return render(request, "login.html", {"error": "Invalid credentials"})

    return render(request, "login.html")

from django.contrib.auth.decorators import login_required

@login_required
def order_view(request):
    return render(request, "order.html")

