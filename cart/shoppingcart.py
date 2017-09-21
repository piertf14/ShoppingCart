from decimal import Decimal

from django.conf import settings

from cart import services

CART_SESSION_KEY = getattr(settings, 'CART_SESSION_KEY', 'CART')

CART_TEMPLATE_TAG_NAME = getattr(settings, 'CART_TEMPLATE_TAG_NAME', 'get_cart')


class CartItem(object):

    def __init__(self, course, quantity, price):
        self.course = course
        self.quantity = int(quantity)
        self.price = Decimal(str(price))

    def to_dict(self):
        return {
            'course_pk': self.course.pk,
            'quantity': self.quantity,
            'price': str(self.price),
        }

    @property
    def subtotal(self):
        return self.price * self.quantity


class Cart(object):
    def __init__(self, session, session_key=None):
        self._items_dict = {}
        self.session = session
        self.session_key = session_key or CART_SESSION_KEY
        if self.session_key in self.session:
            cart_representation = self.session[self.session_key]
            ids_in_cart = cart_representation.keys()
            courses_queryset = self.get_queryset().filter(pk__in=ids_in_cart)
            for course in courses_queryset:
                item = cart_representation[str(course.pk)]
                self._items_dict[course.pk] = CartItem(
                    course, item['quantity'], Decimal(item['price'])
                )

    def __contains__(self, product):
        return course in self.courses

    def get_course_model(self):
        return services.get_course_model()

    def filter_courses(self, queryset):
        lookup_parameters = getattr(settings, 'CART_COURSE_LOOKUP', None)
        if lookup_parameters:
            queryset = queryset.filter(**lookup_parameters)
        return queryset

    def get_queryset(self):
        course_model = self.get_course_model()
        queryset = course_model._default_manager.all()
        queryset = self.filter_courses(queryset)
        return queryset

    def update_session(self):
        self.session[self.session_key] = self.cart_serializable
        self.session.modified = True

    def add(self, course, price=None, quantity=1):
       
        quantity = int(quantity)
        if quantity < 1:
            raise ValueError('Quantity must be at least 1 when adding to cart')
        if course in self.courses:
            self._items_dict[course.pk].quantity += quantity
        else:
            if price == None:
                raise ValueError('Missing price when adding to cart')
            self._items_dict[course.pk] = CartItem(course, quantity, price)
        self.update_session()

    def remove(self, course):
        if course in self.courses:
            del self._items_dict[course.pk]
            self.update_session()


    def clear(self):
        self._items_dict = {}
        self.update_session()

    def quantity(self, course):
        return self._items_dict[course.pk].quantity

    @property
    def items(self):
        return self._items_dict.values()

    @property
    def cart_serializable(self):
        
        cart_representation = {}
        for item in self.items:
            course_id = str(item.course.pk)
            cart_representation[course_id] = item.to_dict()
        return cart_representation

    @property
    def courses(self):
        return [item.course for item in self.items]    

    @property
    def total(self):
        return sum([item.subtotal for item in self.items])