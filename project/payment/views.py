import json
import requests
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings
from django.contrib import messages
from cart.cart import Cart
from payment.forms import ShippingForm
from payment.models import ShippingAddress


# --------------------------
# CHECKOUT VIEW
# --------------------------
def checkout(request):
    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities = cart.get_quants()
    totals = cart.cart_total()

    shipping_form = None

    if request.user.is_authenticated:
        try:
            shipping_user = ShippingAddress.objects.get(user=request.user)
        except ShippingAddress.DoesNotExist:
            shipping_user = None

        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
    else:
        shipping_form = ShippingForm(request.POST or None)

    return render(request, "payment/checkout.html", {
        "cart_products": cart_products,
        "quantities": quantities,
        "totals": totals,
        "shipping_form": shipping_form
    })


# --------------------------
# KHALTI PAYMENT INITIATION VIEW
# --------------------------
def khalti_payment(request):
    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities = cart.get_quants()
    totals = cart.cart_total()
    order_id = str(cart.get_cart_id())

    if not cart_products or not quantities:
        return JsonResponse({"error": "Cart is empty or invalid"}, status=400)

    try:
        total_price = float(totals) * 100  # to paisa
    except (ValueError, TypeError):
        return JsonResponse({"error": "Invalid total amount"}, status=400)

    response = _handle_khalti_payment(cart_products, quantities, total_price, order_id)

    # If successful, redirect to Khalti payment page
    if isinstance(response, JsonResponse):
        data = json.loads(response.content)
        payment_url = data.get("payment_url")
        if payment_url:
            return redirect(payment_url)

    return response  # error response


# --------------------------
# KHALTI PAYMENT HELPER
# --------------------------
def _handle_khalti_payment(cart_products, quantities, total_price, order_id):
    cart_products_list = [
        {
            "identity": str(product.id),
            "name": product.name,
            "unit_price": int(float(product.price) * 100),
            "total_price": int(float(product.price) * int(quantities.get(str(product.id), 1)) * 100),
            "quantity": int(quantities.get(str(product.id), 1)),
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
        "Authorization": settings.KHALTI_AUTH_HEADER,
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(settings.KHALTI_URL, headers=headers, data=json.dumps(payment_data))

        # Log the response for debugging
        print("Response Status Code:", response.status_code)
        print("Response Text:", response.text)

        if response.status_code == 503:
            # If Khalti service is down, inform the user
            return JsonResponse({"error": "Khalti payment service is temporarily unavailable. Please try again later."}, status=503)

        if not response.text:
            return JsonResponse({"error": "Empty response from Khalti"}, status=500)

        try:
            data = response.json()
        except ValueError as e:
            print(f"JSON Parsing Error: {e}")
            return JsonResponse({"error": "Invalid JSON response from Khalti", "details": response.text}, status=500)

        if response.status_code != 200:
            return JsonResponse({"error": "Payment initiation failed", "details": data}, status=400)

        payment_url = data.get("payment_url")

        if payment_url:
            return JsonResponse({"payment_url": payment_url})
        else:
            return JsonResponse({"error": "Missing payment_url from Khalti"}, status=400)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": "Request to Khalti failed", "details": str(e)}, status=500)

# --------------------------
# PAYMENT SUCCESS VIEW
# --------------------------
def payment_success(request):
    return render(request, "payment/payment_success.html", {})

