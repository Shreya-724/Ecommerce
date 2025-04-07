import random
import json
import requests

from django.shortcuts import render, redirect
from cart.cart import Cart
from payment.models import ShippingAddress
from payment.forms import ShippingForm
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse


def checkout(request):
    # Get the cart
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()

    if request.user.is_authenticated:
        try:
            # Try to get the shipping address for the logged-in user
            shipping_user = ShippingAddress.objects.get(user=request.user)
        except ShippingAddress.DoesNotExist:
            # If no shipping address exists, set shipping_user to None
            shipping_user = None

        # Create the shipping form (either with an existing shipping_user or as a new form)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        
        # Render the checkout page with the shipping form
        return render(request, "payment/checkout.html", {
            "cart_products": cart_products, 
            "quantities": quantities, 
            "totals": totals, 
            "shipping_form": shipping_form
        })

    else:
        # Checkout as guest (no shipping address for guest)
        shipping_form = ShippingForm(request.POST or None)
        return render(request, "payment/checkout.html", {
            "cart_products": cart_products, 
            "quantities": quantities, 
            "totals": totals, 
            "shipping_form": shipping_form
        })
        
        
def khalti_payment(request):
    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities = cart.get_quants()
    totals = cart.cart_total()
    order_id = str(cart.get_cart_id())  # Ensure order_id is a string

    if not cart_products or not quantities:
        return JsonResponse({"error": "Cart is empty or invalid"}, status=400)

    try:
        total_price = float(totals) * 100  # Convert total to paisa
    except (ValueError, TypeError):
        return JsonResponse({"error": "Invalid total amount"}, status=400)

    response = _handle_khalti_payment(cart_products, quantities, total_price, order_id)

    # Extract the payment URL
    if response.status_code == 200:
        data = json.loads(response.content)  # Convert JSONResponse to Python dict
        payment_url = data.get("payment_url")

        if payment_url:
            return redirect(payment_url)  # 🚀 Redirect user to Khalti
        else:
            return JsonResponse({"error": "Missing payment_url from Khalti"}, status=400)

    return response  # Return original response if something goes wrong
def _handle_khalti_payment(cart_products, quantities, total_price, order_id):
    cart_products_list = [
    {
        "identity": str(product.id),  # Unique product ID (string)
        "name": product.name,  # Product name
        "unit_price": int(float(product.price) * 100),  # Convert to paisa (int)
        "total_price": int(float(product.price) * int(quantities.get(str(product.id), 1)) * 100),  # Convert to paisa (int)
        "quantity": int(quantities.get(str(product.id), 1)),  # Convert quantity to int
    }
    for product in cart_products
]

    payment_data = {
        "return_url": settings.TRANSACTION_REDIRECT_URL,
        "website_url": settings.WEBSITE_URL,
        "amount": total_price,
        "purchase_order_id": order_id,
        "purchase_order_name": "Order",
        "customer_info": {
            "name": settings.KHALTI_CUSTOMER_NAME,
            "email": settings.KHALTI_CUSTOMER_EMAIL,
            "phone": settings.KHALTI_CUSTOMER_PHONE,
        },
        "amount_breakdown": [
            {"label": "Mark Price", "amount": float(total_price)},
            {"label": "VAT", "amount": float(0)},
        ],
        "product_details": cart_products_list,
        "merchant_username": settings.KHALTI_MERCHANT_USERNAME,
        "merchant_extra": "merchant_extra",
    }

    headers = {
    "Authorization": settings.KHALTI_AUTH_HEADER,  # Use fixed auth header
    "Content-Type": "application/json",
    }


    try:
        response = requests.post(settings.KHALTI_URL, headers=headers, data=json.dumps(payment_data))
        data = response.json()

        if response.status_code != 200:
            return JsonResponse({"error": "Payment initiation failed", "details": data}, status=400)

        payment_url = data.get("payment_url")

        if payment_url:
            return JsonResponse({"payment_url": payment_url})
        else:
            return JsonResponse({"error": "Missing payment_url from Khalti"}, status=400)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": "Request to Khalti failed", "details": str(e)}, status=500)

def payment_success(request):
    return render(request, "payment/payment_success.html", {})

