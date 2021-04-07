import json
from ecomapp import models

def cookiesData(req):
    try:
        cart = json.loads(req.COOKIES['cart'])
        print('cart', cart)
    except:
        cart = {}
    # print("sss")
    items = []
    order = { 'get_cart_total': 0, 'get_item_total': 0}
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