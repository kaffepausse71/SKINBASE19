#!/usr/bin/python
# -*- coding: utf-8 -*-
import xbmc,xbmcaddon,xbmcplugin,sys,os,xbmcgui,litti
__params__ = litti.__get_params__()

if __params__ is None:
    items=[]
    items.append({'title':'[COLOR orange]Guidos SkinBase Kodi 18[/COLOR]','url':litti.__get_youtube_playlist__('PLHFZfTOXnuNut2krF4lc_iNt7gtcbs2h0'),'image':'https://yt3.ggpht.com/a/AATXAJyb7A_8tLBmUWKPV4ba-HmAryCe_pIOT3v0JaN7kA=s900-c-k-c0xffffffff-no-rj-mo','fanart':'http://repo.guidos-skinbase.de/images/logo.jpg','imode':1,'add_info':{},'add_params':{},'add_contextmenu':[],'type':'video','playlist':True,'is_folder':True,'is_playable':True})
    items.append({'title':'[COLOR orange]Guidos SkinBase Repo[/COLOR]','url':litti.__get_youtube_playlist__('PLHFZfTOXnuNvdD8zlep1sb0nBzIMiuGKA'),'image':'https://yt3.ggpht.com/a/AATXAJyb7A_8tLBmUWKPV4ba-HmAryCe_pIOT3v0JaN7kA=s900-c-k-c0xffffffff-no-rj-mo','fanart':'http://repo.guidos-skinbase.de/images/logo.jpg','imode':1,'add_info':{},'add_params':{},'add_contextmenu':[],'type':'video','playlist':True,'is_folder':True,'is_playable':True})
    items.append({'title':'[COLOR orange]Guidos SkinBase Kodi Tutorials[/COLOR]','url':litti.__get_youtube_playlist__('PLHFZfTOXnuNvSrxUxsiC6ft-q3BysLx81'),'image':'https://yt3.ggpht.com/a/AATXAJyb7A_8tLBmUWKPV4ba-HmAryCe_pIOT3v0JaN7kA=s900-c-k-c0xffffffff-no-rj-mo','fanart':'http://repo.guidos-skinbase.de/images/logo.jpg','imode':1,'add_info':{},'add_params':{},'add_contextmenu':[],'type':'video','playlist':True,'is_folder':True,'is_playable':True})
    items.append({'title':'[COLOR orange]Guidos SkinBase Skin Bearbeiten[/COLOR]','url':litti.__get_youtube_playlist__('PLHFZfTOXnuNuJBJGf7_2v-3lCYHctGB0r'),'image':'https://yt3.ggpht.com/a/AATXAJyb7A_8tLBmUWKPV4ba-HmAryCe_pIOT3v0JaN7kA=s900-c-k-c0xffffffff-no-rj-mo','fanart':'http://repo.guidos-skinbase.de/images/logo.jpg','imode':1,'add_info':{},'add_params':{},'add_contextmenu':[],'type':'video','playlist':True,'is_folder':True,'is_playable':True})
    items.append({'title':'[COLOR orange]Guidos SkinBase Intros[/COLOR]','url':litti.__get_youtube_playlist__('PLHFZfTOXnuNsAfvlyKrBxi0RAHIr8RL73'),'image':'https://yt3.ggpht.com/a/AATXAJyb7A_8tLBmUWKPV4ba-HmAryCe_pIOT3v0JaN7kA=s900-c-k-c0xffffffff-no-rj-mo','fanart':'http://repo.guidos-skinbase.de/images/logo.jpg','imode':1,'add_info':{},'add_params':{},'add_contextmenu':[],'type':'video','playlist':True,'is_folder':True,'is_playable':True})
    items.append({'title':'[COLOR orange]Guidos SkinBase Kodi 17[/COLOR]','url':litti.__get_youtube_playlist__('PLHFZfTOXnuNs0zlhuJ3ztuFmhBScPRrgL'),'image':'https://yt3.ggpht.com/a/AATXAJyb7A_8tLBmUWKPV4ba-HmAryCe_pIOT3v0JaN7kA=s900-c-k-c0xffffffff-no-rj-mo','fanart':'http://repo.guidos-skinbase.de/images/logo.jpg','imode':1,'add_info':{},'add_params':{},'add_contextmenu':[],'type':'video','playlist':True,'is_folder':True,'is_playable':True})
    items.append({'title':'[COLOR orange]Bildbearbeitung[/COLOR]','url':litti.__get_youtube_playlist__('PLHFZfTOXnuNskb0xKBBXSDlHSL0WDbKMU'),'image':'https://yt3.ggpht.com/a/AATXAJyb7A_8tLBmUWKPV4ba-HmAryCe_pIOT3v0JaN7kA=s900-c-k-c0xffffffff-no-rj-mo','fanart':'http://repo.guidos-skinbase.de/images/logo.jpg','imode':1,'add_info':{},'add_params':{},'add_contextmenu':[],'type':'video','playlist':True,'is_folder':True,'is_playable':True})
    litti.__add_items__(items)

elif __params__.get('imode') == 1:
	litti.__set_resolved_url__(__params__.get('url'))


litti.__set_content__('movies') 
litti.__end_of_directory__()

#by Litti19928