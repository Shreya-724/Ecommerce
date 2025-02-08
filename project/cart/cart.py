from app1.models import Product



class Cart:
    def __init__(self, request):
        self.session = request.session

        # Initialize the cart using session key
        cart = self.session.get('session_key')
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        self.cart = cart

    def add(self, product, quantity):
     product_id = str(product.id)

    # Update or set the quantity
     if product_id in self.cart:
        self.cart[product_id] += quantity
     else:
        self.cart[product_id] = quantity

     self.session.modified = True


    def __len__(self):
        # Return the total number of items in the cart
        return len(self.cart)
    def get_prods(self):
     product_ids = self.cart.keys()
     products = Product.objects.filter(id__in=product_ids)
     return products

    def get_quants(self):
     quantities = {int(key): value for key, value in self.cart.items()}
     return quantities

   
    def delete(self,product):
        product_id = str(product)
        if product_id in self.cart:
           del self.cart[product_id]   
        self.session.modified = True  
        
    def update(self, product, quantity):
     product_id = str(product)
     if product_id in self.cart:
        self.cart[product_id] = quantity
     self.session.modified = True
     
