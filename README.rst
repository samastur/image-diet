==========
image-diet
==========

image-diet is a Django application for removing unnecessary bytes from image
files.  It optimizes images without changing their look or visual quality
("losslessly").

It works on images in JPEG, GIF and PNG formats and will leave others
unchanged. Provides a seemless integration with easy_thumbnails app, but can
work with others too.


Installation
============
Add ``image_diet`` to ``INSTALLED_APPS`` setting::

    INSTALLED_APPS = (
        ...
        'image_diet',
    )

Check which tools are already installed by executing:
    ``python manage.py check_diet_tools``

Install those reported missing or disable them as described by command's
output (or ``Usage`` section). ``requirements.txt`` lists all tools together
with their home addresses.

If you are using recent version of easy_thumbnails, then you're done.
'image-diet' will automatically squeeze unnecessary bytes every time
a thumbnail is created.

If you aren't, then read further.


Usage
=====
TBD.


Configuration options
---------------------
``DIET_DEBUG = True``
~~~~~~~~~~~~~~~~~~~~~
This will keep uncompressed versions of images on disk with
an extension ``.diet``. Defaults to ``False``.

``DIET_<TOOLNAME> = False``
~~~~~~~~~~~~~~~~~~~~~~~~~~~
Disable use of ``TOOLNAME``. Name has to be written in uppercase so
``DIET_JPEGOPTIM = False`` will disable jpegoptim. Defaults to ``True``.


TODO/Wishlist
=============
- add extreme compressions (change to b&w, reduce color depth,
  change GIF to PNG8)
- add a Django management command for dieting images from chosen
  directory
- stop depending on tools that processed image will actually be smaller
- add integrations for other image handling Django apps


Known bugs
==========
- app doesn't check if files exist so some operations could lead
  to data loss (if image folders contain files with .diet or .orig extension)
