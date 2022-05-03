#!/usr/bin/python
#Based on script.toolbox by phil65 - https://github.com/phil65/script.toolbox/

#################################################################################################

import xbmc
import xbmcaddon
import xbmcvfs
import os
from PIL import ImageFilter,Image,ImageOps

import urllib2 as urllib

from lib.img.helper import *

#################################################################################################

BLUR_CONTAINER = xbmc.getInfoLabel('Skin.String(BlurContainer)') or 100000
BLUR_RADIUS = xbmc.getInfoLabel('Skin.String(BlurRadius)') or ADDON.getSetting('blur_radius') or 4
OLD_IMAGE = ''

#################################################################################################


''' create imgage storage folders
'''
if not os.path.exists(ADDON_DATA_IMG_PATH):
    os.makedirs(ADDON_DATA_IMG_PATH)

if not os.path.exists(ADDON_DATA_IMG_TEMP_PATH):
    os.makedirs(ADDON_DATA_IMG_TEMP_PATH)


''' blur image and store result in addon data folder
'''
def image_blur(prop='listitem',file=None,radius=BLUR_RADIUS):
    global OLD_IMAGE
    image = file if file is not None else xbmc.getInfoLabel('Control.GetLabel(%s)' % BLUR_CONTAINER)

    try:
        radius = int(radius)
    except ValueError:
        log('No valid radius defined for blurring')
        return

    if image:
        if image == OLD_IMAGE:
            log('Image blurring: Image has not changed. Skip %s.' % image, DEBUG)
        else:
            log('Image blurring: Image changed. Blur %s.' % image, DEBUG)
            OLD_IMAGE = image

            blurimgsize = 400
            filename = md5hash(image) + '-' + str(blurimgsize) + '-' + str(radius) + '.png'
            targetfile = os.path.join(ADDON_DATA_IMG_PATH, filename)

            if not xbmcvfs.exists(targetfile):
                img = _getimgcache(image,ADDON_DATA_IMG_PATH,filename)

                if img:
                    img = Image.open(img)
                    img.thumbnail((blurimgsize, blurimgsize), Image.ANTIALIAS)
                    img = img.convert('RGB')
                    img = img.filter(ImageFilter.GaussianBlur(radius))
                    img.save(targetfile)

            else:
                log('Blurred img already created: ' + targetfile, DEBUG)
                img = Image.open(targetfile)

            if img:
                imagecolor = _imgcolors(img)
                winprop(prop + '_blurred', targetfile)
                winprop(prop + '_color', imagecolor)
                winprop(prop + '_color_noalpha', imagecolor[2:])



''' get cached images or copy to temp if file has not been cached yet
'''
def _getimgcache(image,targetpath,filename):
    cachedthumb = xbmc.getCacheThumbName(image)
    vid_cachefile = os.path.join('special://profile/Thumbnails/Video', cachedthumb[0], cachedthumb)
    cachefile_jpg = os.path.join('special://profile/Thumbnails/', cachedthumb[0], cachedthumb[:-4] + '.jpg')
    cachefile_png = os.path.join('special://profile/Thumbnails/', cachedthumb[0], cachedthumb[:-4] + '.png')
    targetfile = os.path.join(targetpath, filename)
    img = None

    for i in range(1, 4):
        try:
            if xbmcvfs.exists(cachefile_jpg):
                img = cachefile_jpg
                log('Get cached file ' + cachefile_jpg, DEBUG)
                break
            elif xbmcvfs.exists(cachefile_png):
                img = cachefile_png
                log('Get cached file ' + cachefile_png, DEBUG)
                break
            elif xbmcvfs.exists(vid_cachefile):
                log('Get cache video file ' + vid_cachefile)
                img = vid_cachefile
                break
            else:
                image = urllib.unquote(image.replace('image://', ''))
                if image.endswith('/'):
                    image = image[:-1]
                log('Copy image from source: ' + image, DEBUG)
                xbmcvfs.copy(image, targetfile)
                img = targetfile
                break
        except Exception as error:
            log('Could not get image for %s (try %i)' % (image, i))
            log(error)
            xbmc.sleep(500)

    img = xbmc.translatePath(img) if img else ''
    return img


''' get average image color
'''
def _imgcolors(img):
    width, height = img.size
    imagecolor = 'FFF0F0F0'

    try:
        pixels = img.load()

        data = []
        for x in range(width / 2):
            for y in range(height / 2):
                cpixel = pixels[x * 2, y * 2]
                data.append(cpixel)

        counter, r, g, b = 0, 0, 0, 0
        for x in range(len(data)):
            brightness = data[x][0] + data[x][1] + data[x][2]
            if brightness > 150 and brightness < 720:
                r += data[x][0]
                g += data[x][1]
                b += data[x][2]
                counter += 1

        if counter > 0:
            rAvg = int(r / counter)
            gAvg = int(g / counter)
            bAvg = int(b / counter)
            Avg = (rAvg + gAvg + bAvg) / 3
            minBrightness = 130

            if Avg < minBrightness:
                Diff = minBrightness - Avg

                if rAvg <= (255 - Diff):
                    rAvg += Diff
                else:
                    rAvg = 255
                if gAvg <= (255 - Diff):
                    gAvg += Diff
                else:
                    gAvg = 255
                if bAvg <= (255 - Diff):
                    bAvg += Diff
                else:
                    bAvg = 255

            imagecolor = 'FF%s%s%s' % (format(rAvg, '02x'), format(gAvg, '02x'), format(bAvg, '02x'))
            log('Average color: ' + imagecolor, DEBUG)

        else:
            raise Exception

    except Exception:
        log('Use fallback average color: ' + imagecolor, DEBUG)
        pass

    return imagecolor