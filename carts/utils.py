from django.db.models import Sum


def recount_cart(cart):
    cart_data = cart.items.aggregate(PRICE=Sum('price'), QTY=Sum('quantity'))
    cart.price = cart_data['PRICE']
    cart.quantity = cart_data['QTY']
    cart.save()