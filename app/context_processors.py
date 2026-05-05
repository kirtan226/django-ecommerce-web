from django.contrib.auth.decorators import login_required
from . models import Cart

def cart_item_count(request):
    if request.user.is_authenticated:
        user = request.user
        # Fetch the cart items for the authenticated user
        cart_items = Cart.objects.filter(user=user)
        item_count = cart_items.count()  # Use count() to get the number of items
    else:
        # If the user is not authenticated, set the item count to 0
        item_count = 0

        # Return a dictionary with the context variable
    return {'cart_item_count': item_count}
