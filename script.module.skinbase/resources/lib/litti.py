#!/usr/bin/python
# -*- coding: utf-8 -*-
import os,sys,xbmc,xbmcgui,xbmcplugin,xbmcaddon,urllib
__plugin_handle__ = int(sys.argv[1])
music_playlist=xbmc.PlayList(0)
video_playlist=xbmc.PlayList(1)

def __fix_encoding__(path):
    if sys.version_info.major == 2:

        if sys.platform.startswith('win'):return path.decode('utf-8')
        else:return path.decode('utf-8').encode('ISO-8859-1')

    elif sys.version_info.major == 3:return path
    
def __quote_plus__(s):
    if sys.version_info.major == 2:return urllib.quote_plus(s,safe=safe)
    elif sys.version_info.major == 3:return urllib.parse.quote_plus(s,safe=safe)
    
    
def __unquote_plus__(s):
    if sys.version_info.major == 2:return urllib.unquote_plus(s)
    elif sys.version_info.major == 3:return urllib.parse.unquote_plus(s)

__addon__ =  xbmcaddon.Addon()
__addon_path__ = __fix_encoding__(__addon__.getAddonInfo('path'))
__addon_icon__ = __fix_encoding__(__addon__.getAddonInfo('icon'))
__addon_fanart__ = __fix_encoding__(__addon__.getAddonInfo('fanart'))

sys.path.append(os.path.join(__addon_path__,'resources','lib'))
import cfscraper
import urllib3
import requests
import secretpy


def __set_resolved_url__(url='',headers=''):
    url = __quote_plus__(url) +'|verifypeer=false' + headers
    listitem = xbmcgui.ListItem(path=url)
    xbmcplugin.setResolvedUrl(handle=int(sys.argv[1]),succeeded=True,listitem=listitem)

def __set_content__(content):
    xbmcplugin.setContent(int(sys.argv[1]),content)

def __get_youtube_live_stream__(channel_id):
    return'plugin://plugin.video.youtube/play/?channel_id=%s&live=1' % channel_id

def __get_youtube_video__(video_id):
    return'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % video_id

def __get_youtube_playlist__(playlist_id):
    return'plugin://plugin.video.youtube/playlist/%s/' % playlist_id

def __get_youtube_channel__(channel_id):
    return'plugin://plugin.video.youtube/channel/%s/' % channel_id

def __get_youtube_search__(search_text):
    return'plugin://plugin.video.youtube/search/?q=%s' % search_text
    
def __get_youtube_user__(user_id):
	return'plugin://plugin.video.youtube/user/%s/' % user_id
    
    
def __get_params__():
    argv = __unquote_plus__(sys.argv[2][1:])
    if argv.startswith('{') and argv.endswith('}'):return json.loads(argv)
    else:return None

def __add_items__(items_list=[{'title':'','url':'','image':'','fanart':'','imode':None,'add_info':{},'add_params':{},'add_contextmenu':[['','']],'type':'video','playlist':False,'is_folder':True,'is_playable':False}]):

    item_index = 0
    playlist_index = 0
    music_playlist.clear()
    video_playlist.clear()

    if len(items_list) > 0:

        for item in items_list:

            url = item['url']
            info={'title':item['title']}
            info.update(item['add_info'])

            iparams={'title':item['title'],'url':url,'image':item['image'],'fanart':item['fanart'],'imode':item['imode'],'item_index':item_index,'playlist_index':playlist_index}
            iparams.update(item['add_params'])
            cparams={'title':item['title'],'url':url,'image':item['image'],'fanart':item['fanart'],'item_index':item_index,'playlist_index':playlist_index}
            cparams.update(item['add_params'])

            listitem = xbmcgui.ListItem(label=item['title'],path=url)
            listitem.setInfo(type=item['type'],infoLabels=info)
            listitem.setArt({'icon':item['image'],'poster':item['image'],'banner':item['image'],'fanart':item['fanart']})

            if (item['is_folder'] == True and item['is_playable'] == False):
                url=sys.argv[0] +'?'+ __quote_plus__(json.dumps(iparams))
                listitem.setProperty('IsPlayable','false')

            elif (item['is_folder'] == False and item['is_playable'] == False):
                url=sys.argv[0] +'?'+ __quote_plus__(json.dumps(iparams))
                listitem.setProperty('IsPlayable','true')

            elif (item['is_folder'] == False and item['is_playable'] == True):
                listitem.setProperty('IsPlayable','true')

            cmenu = []
            for title,cmode in item['add_contextmenu']:
                if title and cmode:
                    cparams.update({'cmode':cmode})
                    cmenu.append((title,'XBMC.RunPlugin('+ sys.argv[0] +'?'+ urllib.quote_plus(json.dumps(cparams)) +')'))
            if cmenu:listitem.addContextMenuItems(items=cmenu,replaceItems=True)

            if ((item['playlist'] == True) and (item['type'].lower() == 'music')):music_playlist.add(url=url,listitem=listitem,index=playlist_index);playlist_index +=1
            if ((item['playlist'] == True) and (item['type'].lower() == 'video')):video_playlist.add(url=url,listitem=listitem,index=playlist_index);playlist_index +=1

            xbmcplugin.addDirectoryItem(handle=__plugin_handle__,url=url,listitem=listitem,isFolder=item['is_folder'],totalItems=len(items_list));item_index +=1

        xbmcplugin.endOfDirectory(handle=int(sys.argv[1]),succeeded=True,updateListing=False,cacheToDisc=True)
    else:xbmcgui.Dialog().notification(heading='Items info',message='No items found !',icon=xbmcgui.NOTIFICATION_INFO,time=2000,sound=True)
  
def __end_of_directory__():
    xbmcplugin.endOfDirectory(handle=int(sys.argv[1]),succeeded=True,updateListing=False,cacheToDisc=True)