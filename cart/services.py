from django.conf import settings

try:
    from importlib import import_module
except ImportError:
    from django.utils.importlib import import_module


def get_course_model():
    package, module = settings.CART_COURSE_MODEL.rsplit('.', 1)
    return getattr(import_module(package), module)