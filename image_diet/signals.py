from django.dispatch import receiver
from image_diet.diet import squeeze

try:
    from easy_thumbnails.signals import saved_file, thumbnail_created

    @receiver(saved_file)
    def optimize_file(sender, fieldfile, **kwargs):
        squeeze(fieldfile.path)

    @receiver(thumbnail_created)
    def optimize_thumbnail(sender, **kwargs):
        squeeze(sender.path)
except ImportError:
    pass
