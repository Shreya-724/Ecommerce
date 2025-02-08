from .cart import Cart



#create a processor so cart page can work on all sites


def cart(request):
    #returining the default data from our cart
    return {'cart': Cart(request)}