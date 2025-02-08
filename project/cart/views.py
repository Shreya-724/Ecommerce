from django.shortcuts import render, get_object_or_404
from .cart import Cart
from app1.models import Product
from django.http import JsonResponse

# Create your views here.
def cart_summary(request):
    #get the cart
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    return render(request, "cart_summary.html", {"cart_products":cart_products, "quantities":quantities})

def cart_add(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        product = get_object_or_404(Product, id=product_id)

        cart.add(product=product, quantity=product_qty)
        # Get cart quantity
        cart_quantity = len(cart)  # This now works as expected

        # Return response with the cart quantity
        #response = JsonResponse({'Product Name:' : product.name})
        response = JsonResponse({'qty': cart_quantity})
        return response

def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = request.POST.get('product_id')
        if not product_id:
            return JsonResponse({'error': 'Product ID is required'}, status=400)

        try:
            product_id = int(product_id)
        except ValueError:
            return JsonResponse({'error': 'Invalid Product ID'}, status=400)

        cart.delete(product=product_id)
        return JsonResponse({'product': product_id})

    
    

def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = request.POST.get('product_id')
        product_qty = request.POST.get('product_qty')

        if not product_id or not product_qty:
            return JsonResponse({'error': 'Product ID and quantity are required'}, status=400)

        try:
            product_id = int(product_id)
            product_qty = int(product_qty)
        except ValueError:
            return JsonResponse({'error': 'Invalid input'}, status=400)

        cart.update(product=product_id, quantity=product_qty)
        return JsonResponse({'success': 'Quantity updated'})


        
        
        
        
        
        
        
        
