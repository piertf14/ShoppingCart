from django import template

from cart.shoppingcart import Cart, CART_TEMPLATE_TAG_NAME


register = template.Library()


def get_cart(context, session_key=None, cart_class=Cart):
    request = context['request']
    return cart_class(request.session, session_key=session_key)

register.assignment_tag(takes_context=True, name=CART_TEMPLATE_TAG_NAME)(get_cart)