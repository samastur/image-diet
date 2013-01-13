import os
from os.path import join
from django.core.management.base import BaseCommand
from image_diet.diet import squeeze


class Command(BaseCommand):
    args = '<dir1> [<dir2>...]'
    help = "Scan directories and subdirectories for images and compress them."

    def handle(self, *args, **options):
        for dirname in args:
            for (root, dirs, files) in os.walk(dirname):
                for filename in files:
                    filepath = join(root, filename)
                    squeeze(filepath)
