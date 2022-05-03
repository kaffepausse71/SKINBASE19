#!/usr/bin/python
# coding: utf-8

########################

import xbmc
import xbmcaddon
import xbmcgui
import json
import os
import hashlib

########################

ADDON = xbmcaddon.Addon()
ADDON_ID = ADDON.getAddonInfo('id')
ADDON_DATA_PATH = os.path.join(xbmc.translatePath("special://profile/addon_data/%s" % ADDON_ID))
ADDON_DATA_IMG_PATH = os.path.join(xbmc.translatePath("special://profile/addon_data/%s/img" % ADDON_ID))
ADDON_DATA_IMG_TEMP_PATH = os.path.join(xbmc.translatePath("special://profile/addon_data/%s/img/tmp" % ADDON_ID))

NOTICE = xbmc.LOGNOTICE
WARNING = xbmc.LOGWARNING
DEBUG = xbmc.LOGDEBUG

DIALOG = xbmcgui.Dialog()

########################

def get_kodiversion():
    build = xbmc.getInfoLabel('System.BuildVersion')
    return int(build[:2])


def addon_setting(skin,setting,save=False):
    profile = xbmc.getInfoLabel('System.ProfileName')
    setting_id = skin + '_' + profile + '_' + setting
    skin_version = xbmcaddon.Addon(skin).getAddonInfo('version')

    if not save:
        if ADDON.getSetting(id=setting_id) == skin_version:
            return True
        return False
    else:
        ADDON.setSetting(id=setting_id, value=skin_version)


def log(txt,loglevel=NOTICE,force=False):
    if ((loglevel == NOTICE or loglevel == WARNING) and get_bool(ADDON.getSetting('log'))) or loglevel == DEBUG or force:

        ''' Python 2 requires to decode stuff at first
        '''
        try:
            if isinstance(txt, str):
                txt = txt.decode('utf-8')
        except AttributeError:
            pass

        message = u'[ %s ] %s' % (ADDON_ID,txt)

        try:
            xbmc.log(msg=message.encode('utf-8'), level=loglevel) # Python 2
        except TypeError:
            xbmc.log(msg=message, level=loglevel)


def remove_quotes(label):
    if not label:
        return ''

    if label.startswith("'") and label.endswith("'"):
        label = label[1:-1]
        if label.startswith('"') and label.endswith('"'):
            label = label[1:-1]
        elif label.startswith('&quot;') and label.endswith('&quot;'):
            label = label[6:-6]

    return label


def execute(cmd):
    log('Execute: %s' % cmd, DEBUG)
    xbmc.executebuiltin(cmd)


def visible(condition):
    return xbmc.getCondVisibility(condition)


def gotopath(path,target='videos'):
    execute('Dialog.Close(all,true)')
    execute('Container.Update(%s)' % path) if visible('Window.IsMedia') else execute('ActivateWindow(%s,%s,return)' % (target,path))


def winprop(key, value=None, clear=False, window_id=10000):
    window = xbmcgui.Window(window_id)

    if clear:
        window.clearProperty(key.replace('.json', '').replace('.bool', ''))

    elif value is not None:

        if key.endswith('.json'):
            key = key.replace('.json', '')
            value = json.dumps(value)

        elif key.endswith('.bool'):
            key = key.replace('.bool', '')
            value = 'true' if value else 'false'

        window.setProperty(key, value)

    else:
        result = window.getProperty(key.replace('.json', '').replace('.bool', ''))

        if result:
            if key.endswith('.json'):
                result = json.loads(result)
            elif key.endswith('.bool'):
                result = result in ('true', '1')

        return result


def get_bool(value,string='true'):
    try:
        if value.lower() == string:
            return True
        raise Exception

    except Exception:
        return False


def md5hash(value):
    return hashlib.md5(str(value)).hexdigest()