from subprocess import call, PIPE
from django.core.management.base import BaseCommand
import image_diet.settings as settings


class Command(BaseCommand):
    help = ("Check which external image diet tools are "
            "available and suggest settings.py configuration.")

    def handle(self, *args, **options):
        tools = (
            'jpegoptim',
            'jpegtran',
            'gifsicle',
            'optipng',
            'advpng',
            'pngcrush',
        )
        not_found = []
        for tool in tools:
            setting_name = "DIET_" + tool.upper()
            if getattr(settings, setting_name):
                retcode = call("which %s" % tool, shell=True, stdout=PIPE)
                if retcode == 0:
                    self.stdout.write('Found: %s\n' % tool)
                else:
                    self.stdout.write('MISSING: %s\n' % tool)
                    not_found.append(tool)
            else:  # Tool turned off
                self.stdout.write('Disabled: %s\n' % tool)
        if len(not_found):
            off_settings = ["DIET_%s = False" % tool.upper() for tool
                            in not_found]
            self.stdout.write("\n")
            self.stdout.write("You can disable missing tools by adding following lines to your settings.py: \n")
            self.stdout.write("\n".join(off_settings))
            self.stdout.write("\n")
