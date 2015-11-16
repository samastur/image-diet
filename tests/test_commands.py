import os
from os.path import join, dirname
from shutil import copyfile
from django.test import TestCase
from image_diet.management.commands import diet_images

TEST_DIR = join(dirname(__file__), 'test_files')


class DietCommandTest(TestCase):
    def setUp(self):
        image_path = join(TEST_DIR, 'stockholm.jpg')

        self.nested_dir = join('dir1', 'dir2', 'dir3')
        self.test_root_dir = join(TEST_DIR, 'dir1')

        os.makedirs(join(TEST_DIR, self.nested_dir))

        self.test_image_path = join(TEST_DIR, self.nested_dir, 'stockholm.jpg')
        copyfile(image_path, self.test_image_path)

    def tearDown(self):
        os.remove(self.test_image_path)
        os.chdir(TEST_DIR)
        os.removedirs(self.nested_dir)

    def test_diet_images(self):
        old_size = os.stat(self.test_image_path).st_size
        action = diet_images.Command()
        action.handle(self.test_root_dir)
        new_size = os.stat(self.test_image_path).st_size

        self.assertTrue(new_size < old_size)
