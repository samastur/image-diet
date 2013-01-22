from django.conf import settings

DIET_DEBUG = getattr(settings, 'DIET_DEBUG', False)

DIET_JPEGOPTIM = getattr(settings, 'DIET_JPEGOPTIM', True)
DIET_JPEGTRAN = getattr(settings, 'DIET_JPEGTRAN', True)
DIET_GIFSICLE = getattr(settings, 'DIET_GIFSICLE', True)
DIET_OPTIPNG = getattr(settings, 'DIET_OPTIPNG', True)
DIET_ADVPNG = getattr(settings, 'DIET_ADVPNG', True)
DIET_PNGCRUSH = getattr(settings, 'DIET_PNGCRUSH', True)
