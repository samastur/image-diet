import os
from os.path import join, dirname
from shutil import copyfile
from subprocess import call, PIPE
from django.test import TestCase
from image_diet import diet

TEST_DIR = join(dirname(__file__), 'test_files')


class DietTest(TestCase):

    def setUp(self):
        image_path = join(TEST_DIR, 'stockholm.jpg')

        self.test_image_path = join(TEST_DIR, 'test_image.jpg')
        copyfile(image_path, self.test_image_path)

    def tearDown(self):
        os.remove(self.test_image_path)

    def have_jpeg_tools(self):
        retcode = call("which jpegoptim || which jpegtran", shell=True,
                       stdout=PIPE)
        return True if retcode is 0 else False

    def test_squeeze_jpeg(self):
        diet.settings.DIET_JPEGOPTIM = False
        diet.settings.DIET_JPEGTRAN = False
        self.assertEqual(diet.squeeze_jpeg(), "")

        diet.settings.DIET_JPEGTRAN = True
        self.assertEqual(
            diet.squeeze_jpeg(),
            (u"jpegtran -copy none -progressive -optimize -outfile '%(file)s'.diet '%(file)s' "
                "&& mv '%(file)s.diet' '%(file)s'")
        )

        diet.settings.DIET_JPEGOPTIM = True
        diet.settings.DIET_JPEGTRAN = False
        self.assertEqual(diet.squeeze_jpeg(), u"jpegoptim -f --strip-all '%(file)s'")

    def test_squeeze_png(self):
        diet.settings.DIET_OPTIPNG = False
        diet.settings.DIET_ADVPNG = False
        diet.settings.DIET_PNGCRUSH = False
        self.assertEqual(diet.squeeze_png(), "")

        diet.settings.DIET_OPTIPNG = True
        diet.settings.DIET_ADVPNG = False
        diet.settings.DIET_PNGCRUSH = False
        self.assertEqual(diet.squeeze_png(), u"optipng -force -o7 '%(file)s'")

        diet.settings.DIET_OPTIPNG = False
        diet.settings.DIET_ADVPNG = True
        diet.settings.DIET_PNGCRUSH = False
        self.assertEqual(diet.squeeze_png(), u"advpng -z4 '%(file)s'")

        diet.settings.DIET_OPTIPNG = False
        diet.settings.DIET_ADVPNG = False
        diet.settings.DIET_PNGCRUSH = True
        self.assertEqual(
            diet.squeeze_png(),
            (u"pngcrush -rem gAMA -rem alla -rem cHRM -rem iCCP -rem sRGB "
             u"-rem time '%(file)s' '%(file)s.diet' "
             u"&& mv '%(file)s.diet' '%(file)s'")
        )

        diet.settings.DIET_OPTIPNG = True
        diet.settings.DIET_ADVPNG = True
        diet.settings.DIET_PNGCRUSH = False
        self.assertEqual(diet.squeeze_png(), u"optipng -force -o7 '%(file)s' && advpng -z4 '%(file)s'")

    def test_squeeze_gif(self):
        diet.settings.DIET_GIFSICLE = True
        self.assertEqual(
            diet.squeeze_gif(),
            (u"gifsicle -O2 b'%(file)s' > '%(file)s'.diet "
                "&& mv '%(file)s.diet' '%(file)s'")
        )

        diet.settings.DIET_GIFSICLE = False
        self.assertEqual(diet.squeeze_gif(), "")

    def test_squeeze(self):
        self.assertEqual(diet.squeeze('/tmp/bla'), None)

        old_size = os.stat(self.test_image_path).st_size

        new_path = diet.squeeze(self.test_image_path)
        new_size = os.stat(new_path).st_size

        if self.have_jpeg_tools():
            self.assertEqual(new_path, self.test_image_path)
            self.assertTrue(new_size < old_size)
        else:
            print "Install jpegtran or jpegoptim to test shrinking"
