import json
from ecomapp import models

from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six
def cookiesData(req):
    try:
        cart = json.loads(req.COOKIES['cart'])
        print('cart', cart)
    except:
        cart = {}
    # print("sss")
    items = []
    order = { 'get_cart_total': 0, 'get_item_total': 0,'is_completed': False}
    cartItem = order['get_item_total']
    for i in cart:
        cartItem += cart[i]['quantity']
        product = models.Product.objects.get(id=i)
        total = product.price * cart[i]['quantity']

        order['get_cart_total'] += total
        order['get_item_total'] += cart[i]['quantity']

        item = {
            'product': {
                'id': product.id,
                'price': product.price,
                'image': product.image,
                'name': product.name

            },
            'quantity': cart[i]['quantity'],
            'get_total': total,
        }
        items.append(item)
    return {"cartItem": cartItem, "orders":order, "items":items}


class PasswordGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
    # Ensure results are consistent across DB backends
        # login_timestamp = '' if user.last_login is None else user.last_login.replace(microsecond=0, tzinfo=None)
        return (
            six.text_type(user.pk) + user.email  
             + six.text_type(timestamp)
        ) 

generate_token = PasswordGenerator()