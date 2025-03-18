from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm, UserRegistrationForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .models import Contact
from .models import Product
from .forms import ProductForm
from .forms import ContactForm
from django.views.decorators.csrf import csrf_exempt
import base64
import json






# Create your views here.
#User registration and login views
def user_register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Get form data
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']

            # Additional validation
            if password != confirm_password:
                messages.error(request, "Passwords don't match")
                return render(request, 'registration/register.html', {'form': form})

            # Check if username or email already exists
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists")
                return render(request, 'registration/register.html', {'form': form})
            if User.objects.filter(email=email).exists():
                messages.error(request, "Email already exists")
                return render(request, 'registration/register.html', {'form': form})

            # Create new user
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()

            # Log the user in after registration
           # login(request, user)

            messages.success(request, "Registration successful. You can now log in!")
            return redirect('login')  # Redirect to login after successful registration
        else:
            # If the form is not valid, show error messages
            messages.error(request, "There were errors in your form.")
            return render(request, 'registration/register.html', {'form': form})

    else:
        form = UserRegistrationForm()

    return render(request, 'registration/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "You have logged in successfully!")
            return redirect('product_list')  # Redirect to the product list page after successful login
        else:
            messages.error(request, "Invalid username or password. Please try again.")
    else:
        form = AuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})


def index(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')

def contact_success(request):
    return render(request, 'contact_success.html')

def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            # Save the form data to the database
            form.save()

            # Send an email notification to the admin
            subject = form.cleaned_data['subject']
            message = f"Message from {form.cleaned_data['name']} ({form.cleaned_data['email']}):\n\n{form.cleaned_data['message']}"
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [settings.EMAIL_HOST_USER],  # You can add other recipient emails here if needed
                fail_silently=False,
            )

            # Show success message
            messages.success(request, "Your message has been sent successfully!")

            # Redirect to the same page or another page after successful submission
            return redirect('contact')  # Make sure this is your correct URL name
        else:
            # Form validation errors
            messages.error(request, "There was an error in your form. Please correct it and try again.")
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})



#Products
#Display products

def product_list(request):
    products = Product.objects.all().order_by('-updated_at')
    return render(request, 'product_list.html', {'products': products})

# Display product details
def product_detail(request, product_id):
    # Get the product by ID or return a 404 error if not found
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})


#CART FUNCTIONALITY
def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})

    if product_id in cart:
        cart[product_id] += 1
    else:
        cart[product_id] = 1

    request.session['cart'] = cart
    request.session.modified = True  # Ensures session data is saved
    return redirect('view_cart')

def view_cart(request):
    cart = request.session.get('cart', {})
    cart_items = []

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'total_price': product.price * quantity
        })

    return render(request, 'cart.html', {'cart_items': cart_items})

def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})

    product_id = str(product_id)  # Convert to string for consistent session key

    if product_id in cart:
        del cart[product_id]  # Remove item from cart
        request.session['cart'] = cart
        request.session.modified = True  # Mark session as modified

    return redirect('view_cart')


def clear_cart(request):
    request.session['cart'] = {}
    request.session.modified = True
    return redirect('view_cart')

