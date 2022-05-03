# -*- coding: utf-8 -*-

import xbmc
import xbmcvfs
import xbmcgui

try:
    are_you_sure = xbmcgui.Dialog().yesno("A Confluence ZEITGEIST","Clearing script.module.simplecache cache file. Continue?")
    if are_you_sure :
        some_file = "special://userdata/addon_data/script.module.simplecache/simplecache.db"
        file_is_present = xbmcvfs.exists(some_file)
        if file_is_present:
            xbmcvfs.delete(some_file)
            xbmc.executebuiltin('Notification(script.module.simplecache,cache cleared,5000,DefaultIconWarning.png)')
        else:
            xbmc.executebuiltin('Notification(script.module.simplecache,cache already empty,5000,DefaultIconWarning.png)')
except:
    pass