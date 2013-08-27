import logging
from os.path import isfile
from subprocess import call, PIPE
from imghdr import what as determinetype
import image_diet.settings as settings

logger = logging.getLogger('image_diet')


def squeeze_jpeg():
    ''' Prefer jpegtran to jpegoptim since it makes smaller images
    and can create progressive jpegs (smaller and faster to load)'''
    if not settings.DIET_JPEGTRAN and not settings.DIET_JPEGOPTIM:  # Can't do anything
        return ""
    if not settings.DIET_JPEGTRAN:
        return u"jpegoptim -f --strip-all '%(file)s'"
    return (u"jpegtran -copy none -progressive -optimize -outfile '%(file)s'.diet '%(file)s' "
            "&& mv '%(file)s.diet' '%(file)s'")


def squeeze_gif():
    '''Gifsicle only optimizes animations.

    Eventually add support to change gifs to png8.'''
    return (u"gifsicle -O2 '%(file)s' > '%(file)s'.diet "
            "&& mv '%(file)s.diet' '%(file)s'") if settings.DIET_GIFSICLE else ""


def squeeze_png():
    commands = []
    if settings.DIET_OPTIPNG:
        commands.append(u"optipng -force -o7 '%(file)s'")
    if settings.DIET_ADVPNG:
        commands.append(u"advpng -z4 '%(file)s'")
    if settings.DIET_PNGCRUSH:
        commands.append(
            (u"pngcrush -rem gAMA -rem alla -rem cHRM -rem iCCP -rem sRGB "
             u"-rem time '%(file)s' '%(file)s.diet' "
             u"&& mv '%(file)s.diet' '%(file)s'")
        )
    return " && ".join(commands)


def squeeze(path):
    '''Returns path of optimized image or None if something went wrong.'''
    if not isfile(path):
        logger.error("'%s' does not point to a file." % path)
        return None

    if settings.DIET_DEBUG:  # Create a copy of original file for debugging purposes
        call("cp '%(file)s' '%(file)s'.orig" % {'file': path},
             shell=True, stdout=PIPE)

    filetype = determinetype(path)

    squeeze_cmd = ""
    if filetype == "jpeg":
        squeeze_cmd = squeeze_jpeg()
    elif filetype == "gif":
        squeeze_cmd = squeeze_gif()
    elif filetype == "png":
        squeeze_cmd = squeeze_png()

    if squeeze_cmd:
        try:
            retcode = call(squeeze_cmd % {'file': path},
                           shell=True, stdout=PIPE)
        except:
            logger.error('Squeezing failed with parameters:')
            logger.error(squeeze_cmd[filetype] % {'file': path})
            logger.exception()
            return None

        if retcode != 0:
            # Failed.
            logger.error(
                ('Squeezing failed. '
                 'Likely because you are missing one of required utilities.'))
            return None
    return path
