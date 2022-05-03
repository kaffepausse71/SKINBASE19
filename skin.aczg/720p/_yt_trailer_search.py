# -*- coding: utf-8 -*-

import xbmc
import sys
import urllib
import webbrowser
import xbmcgui

try:
    if xbmc.getCondVisibility("Player.HasMedia"):
       already_playing = xbmcgui.Dialog().ok("Trailer Search:  Open in Web Browser","Kodi is playing media at the moment.[CR][CR]Please stop playback before using this feature.") 
    else:
        url_base = 'https://www.youtube.com/results?search_query='

        configurl_base = '&sp='
        configurl_only_video = 'EgIQAQ%253D%253D'
        configurl_only_video_short_lenths = 'EgQQARgB'

        url_final = url_base + urllib.quote_plus(sys.argv[1]) + ' ' + urllib.quote_plus(sys.argv[2]) + ' Trailer ' + urllib.quote_plus(sys.argv[3]) + configurl_base + configurl_only_video_short_lenths

        webbrowser.open(url_final)
except:
    pass
