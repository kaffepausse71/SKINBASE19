# -*- coding: utf-8 -*-

import xbmc
import xbmcaddon
import xbmcvfs

import arrow
from simplecache import use_cache, SimpleCache
from datetime import datetime

# Script constants
__addon__      = xbmcaddon.Addon()
__addonid__    = __addon__.getAddonInfo('id')
__version__    = __addon__.getAddonInfo('version')
__language__   = __addon__.getLocalizedString
__cwd__        = __addon__.getAddonInfo('path')

def log(txt):
    if isinstance (txt,str):
        txt = txt.decode("utf-8")
    message = u'%s: %s' % (__addonid__, txt)
    xbmc.log(msg=message.encode("utf-8"), level=xbmc.LOGDEBUG)



class Main:
    
    api_key = None
    cache = None
    
    _addon, _close_called, _omdb, _tmdb = [None] * 4


    def __init__(self, simplecache=None):
        log("version %s started" % __version__)
        
        self.previousitem = ""
        self.selecteditem = ""
        self.dbid = ""
        self.imdbnumber = ""
        self.itempath = ""
        self.itemfile = ""
        self.itemfilenameandpath = ""
        
        self.cache = SimpleCache()
        
        self.monitor = xbmc.Monitor()
        self.run_service()


    def run_service(self):
        while not self.monitor.abortRequested():
            if self.monitor.waitForAbort(0.2):
                break
            if ((xbmc.getCondVisibility("Window.IsActive(Videos)") and xbmc.getCondVisibility("Window.Is(Videos)")) or (xbmc.getCondVisibility("Window.IsActive(MovieInformation)") and xbmc.getCondVisibility("Window.Is(MovieInformation)"))) and not xbmc.getCondVisibility("Container.Scrolling") and xbmc.getCondVisibility("Container.Content(Movies)") and not xbmc.getInfoLabel("Container.PluginName"):
                self.selecteditem = xbmc.getInfoLabel("ListItem.DBID")
                if (self.selecteditem and self.selecteditem != self.previousitem):
                    self.previousitem = self.selecteditem
                    
                    if (xbmc.getInfoLabel("ListItem.IMDBNumber") and xbmc.getInfoLabel("ListItem.DBID") and xbmc.getInfoLabel("ListItem.DBTYPE") == 'movie' and not xbmc.getCondVisibility("ListItem.IsFolder")):
                        self.dbid = xbmc.getInfoLabel("ListItem.DBID")
                        self.imdbnumber = xbmc.getInfoLabel("ListItem.IMDBNumber")
                        
                        self.itempath = ""
                        self.itemfile = ""
                        self.itemfilenameandpath = ""
                        try:
                            ListItemPath = xbmc.getInfoLabel("ListItem.Path")
                            if ListItemPath:
                                self.itempath = ListItemPath
                            
                            ListItemFile = xbmc.getInfoLabel("ListItem.FileName")
                            if ListItemFile:
                                self.itemfile = ListItemFile
                            
                            ListItemFileNameAndPath = xbmc.getInfoLabel("ListItem.FileNameAndPath")
                            if ListItemFileNameAndPath:
                                self.itemfilenameandpath = ListItemFileNameAndPath
                        except:
                            pass
                        
                        self.set_helper_values()
                        
            else:
                my_container_id = xbmc.getInfoLabel("Window(Home).Property(ListItemHelper.WidgetContainerId)")
                my_container_window = xbmc.getInfoLabel("Window(Home).Property(ListItemHelper.WidgetContainerWindowName)")
                
                if (my_container_id and my_container_window and (xbmc.getCondVisibility("Control.HasFocus("+my_container_id+")") and xbmc.getCondVisibility("Window.IsActive("+my_container_window+")") and xbmc.getCondVisibility("Window.Is("+my_container_window+")")) and not xbmc.getCondVisibility("Window.IsActive(Videos)") and not xbmc.getCondVisibility("Window.IsActive(MovieInformation)")) and not xbmc.getCondVisibility("Container("+my_container_id+").Scrolling") and not xbmc.getInfoLabel("Container("+my_container_id+").PluginName"):
                    self.selecteditem = xbmc.getInfoLabel("Container("+my_container_id+").ListItem.DBID")
                    if (self.selecteditem and self.selecteditem != self.previousitem):
                        self.previousitem = self.selecteditem
                                                
                        if (xbmc.getInfoLabel("Container("+my_container_id+").ListItem.IMDBNumber") and xbmc.getInfoLabel("Container("+my_container_id+").ListItem.DBID") and xbmc.getInfoLabel("Container("+my_container_id+").ListItem.DBTYPE") == 'movie' and not xbmc.getCondVisibility("Container("+my_container_id+").ListItem.IsFolder")):
                            self.dbid = xbmc.getInfoLabel("Container("+my_container_id+").ListItem.DBID")
                            self.imdbnumber = xbmc.getInfoLabel("Container("+my_container_id+").ListItem.IMDBNumber")
                            
                            self.itempath = ""
                            self.itemfile = ""
                            self.itemfilenameandpath = ""
                            try:
                                ListItemPath = xbmc.getInfoLabel("Container("+my_container_id+").ListItem.Path")
                                if ListItemPath:
                                    self.itempath = ListItemPath
                                
                                ListItemFile = xbmc.getInfoLabel("Container("+my_container_id+").ListItem.FileName")
                                if ListItemFile:
                                    self.itemfile = ListItemFile
                                
                                ListItemFileNameAndPath = xbmc.getInfoLabel("Container("+my_container_id+").ListItem.FileNameAndPath")
                                if ListItemFileNameAndPath:
                                    self.itemfilenameandpath = ListItemFileNameAndPath
                            except:
                                pass
                            
                            self.set_helper_values()
                            
            if xbmc.getCondVisibility("Skin.HasSetting(ExperimentalShowNtsFile)") and xbmc.getCondVisibility("Window.IsVisible(1103)") and xbmc.getCondVisibility("Window.IsVisible(MovieInformation)") and not xbmc.getInfoLabel("Window(Home).Property(ListItemHelper.internalnotes)") and not xbmc.getInfoLabel("Window(Home).Property(ListItemHelper.internalnotes2)") and self.dbid:
                try:
                    if(self.itempath):
                        tmp_internalnotes = ""
                        tmp_internalnotes2 = ""
                        
                        media_file = xbmc.translatePath(self.itemfilenameandpath)
                        media_file_present = xbmcvfs.exists(media_file)
                        if(media_file_present):
                            try:
                                f = xbmcvfs.File(media_file)
                                fsizegb = round(f.size()/1e+9,2)
                                f.close()
                                #xbmc.executebuiltin('Notification(dbg,'+str(fsizegb)+',1000)')
                                tmp_internalnotes = tmp_internalnotes + '[COLOR=orange]' + str(fsizegb) + ' GB    \\"' + str(self.itemfile) + '\\"[/COLOR]'
                            except:
                                pass
                            
                            try:
                                st = xbmcvfs.Stat(media_file)
                                modified = st.st_mtime()
                                modified = datetime.fromtimestamp(modified)
                                tmp_internalnotes = tmp_internalnotes + '[COLOR=orange]    ' + str(modified) + '[/COLOR]'
                            except:
                                pass
                        
                        notes_file = xbmc.translatePath(self.itempath)+'.rls-rmx.nts'
                        notes_file_present = xbmcvfs.exists(notes_file)
                        if(notes_file_present):
                            try:
                                f = xbmcvfs.File(notes_file)
                                if(f):
                                    b = f.read()
                                    tmp_internalnotes = tmp_internalnotes + '[CR][CR]' + str(b)
                                f.close()
                            except:
                                pass
                        
                        nfo_file = xbmc.translatePath(self.itempath)+'.nfo.nts'
                        nfo_file_present = xbmcvfs.exists(nfo_file)
                        if(nfo_file_present):
                            try:
                                f = xbmcvfs.File(nfo_file)
                                if(f):
                                    b = f.read()
                                    tmp_internalnotes = tmp_internalnotes + '[CR][CR][CR][CR]' + str(b) + '[CR][CR]'
                                f.close()
                            except:
                                pass
                        
                        mediainfo_file = xbmc.translatePath(self.itempath)+'.mediainfo.nts'
                        mediainfo_file_present = xbmcvfs.exists(mediainfo_file)
                        if(mediainfo_file_present):
                            try:
                                f = xbmcvfs.File(mediainfo_file)
                                if(f):
                                    b = f.read()
                                    tmp_internalnotes2 = tmp_internalnotes2 + str(b)
                                f.close()
                            except:
                                pass
                        xbmc.executebuiltin('SetProperty(ListItemHelper.internalnotes,"'+tmp_internalnotes+'",home)')
                        xbmc.executebuiltin('SetProperty(ListItemHelper.internalnotes2,"'+tmp_internalnotes2+'",home)')
                except:
                    xbmc.executebuiltin('SetProperty(ListItemHelper.internalnotes,"N/A",home)')
                    xbmc.executebuiltin('SetProperty(ListItemHelper.internalnotes2,"N/A",home)')
    #run_service end


    def set_helper_values(self):
        log('set_helper_values')
        
        # OMDB
        xbmc.executebuiltin('SetProperty(ListItemHelper.rating.rottentomatoes.percent,"",home)')
        xbmc.executebuiltin('SetProperty(ListItemHelper.rating.rottentomatoes.image,"",home)')
        xbmc.executebuiltin('SetProperty(ListItemHelper.rating.rottentomatoes.url,"",home)')
        xbmc.executebuiltin('SetProperty(ListItemHelper.rating.rottentomatoes.audience,"",home)')
        xbmc.executebuiltin('SetProperty(ListItemHelper.rating.metacritic.percent,"",home)')
        xbmc.executebuiltin('SetProperty(ListItemHelper.rating.imdb.percent,"",home)')
        xbmc.executebuiltin('SetProperty(ListItemHelper.rating.imdb,"",home)')
        xbmc.executebuiltin('SetProperty(ListItemHelper.rating.imdb.votes,"",home)')
        xbmc.executebuiltin('SetProperty(ListItemHelper.awards,"",home)')
        xbmc.executebuiltin('SetProperty(ListItemHelper.revenue.boxoffice,"",home)')
        
        # TMDB
        xbmc.executebuiltin('SetProperty(ListItemHelper.budget,"",home)')
        xbmc.executebuiltin('SetProperty(ListItemHelper.budget.million,"",home)')
        xbmc.executebuiltin('SetProperty(ListItemHelper.budget.formatted,"",home)')
        xbmc.executebuiltin('SetProperty(ListItemHelper.revenue,"",home)')
        xbmc.executebuiltin('SetProperty(ListItemHelper.revenue.million,"",home)')
        xbmc.executebuiltin('SetProperty(ListItemHelper.revenue.formatted,"",home)')
        
        # General
        xbmc.executebuiltin('SetProperty(ListItemHelper.DBID,"'+str(self.dbid)+'",home)')
        xbmc.executebuiltin('SetProperty(ListItemHelper.IMDBNumber,"'+str(self.imdbnumber)+'",home)')
        
        # Internal Notes files
        xbmc.executebuiltin('SetProperty(ListItemHelper.internalnotes,"",home)')
        xbmc.executebuiltin('SetProperty(ListItemHelper.internalnotes2,"",home)')
        
        
        # OMDB
        self.omdb_result = self.get_omdb_info(self.imdbnumber)
        
        if (self.omdb_result) :
            log(self.omdb_result)
            for key, value in self.omdb_result.items():
                # rotten tomatoes
                if key == "rottentomatoes.rating" :
                    xbmc.executebuiltin('SetProperty(ListItemHelper.rating.rottentomatoes.percent,"'+str(value)+'",home)')
                if key == "rottentomatoes.image" :
                    xbmc.executebuiltin('SetProperty(ListItemHelper.rating.rottentomatoes.image,"'+str(value)+'",home)')
                if key == "rottentomatoes.audience" :
                    xbmc.executebuiltin('SetProperty(ListItemHelper.rating.rottentomatoes.audience,"'+str(value)+'",home)')
                # metacritic
                if key == "metacritic.rating" :
                    xbmc.executebuiltin('SetProperty(ListItemHelper.rating.metacritic.percent,"'+str(value)+'",home)')
                # imdb
                if key == "rating.percent.imdb" :
                    xbmc.executebuiltin('SetProperty(ListItemHelper.rating.imdb.percent,'+str(value)+',home)')
                if key == "rating.imdb" :
                    xbmc.executebuiltin('SetProperty(ListItemHelper.rating.imdb,'+str(value)+',home)')
                if key == "votes.imdb" :
                    xbmc.executebuiltin('SetProperty(ListItemHelper.rating.imdb.votes,"'+str(value)+'",home)')
                if key == "rottentomatoes.url" :
                    if(value):
                        xbmc.executebuiltin('SetProperty(ListItemHelper.rating.rottentomatoes.url,"'+str(value)+'",home)')
                # awards
                if key == "awards" :
                    xbmc.executebuiltin('SetProperty(ListItemHelper.awards,"'+str(value)+'",home)')
                # boxoffice
                if key == "boxoffice" :
                    xbmc.executebuiltin('SetProperty(ListItemHelper.revenue.boxoffice,"'+str(value)+'",home)')
        
        
        # TMDB
        self.tmdb_result = self.get_tmdb_details(self.imdbnumber)
        if (self.tmdb_result) :
            log(self.tmdb_result)
            for key, value in self.tmdb_result.items():
                # budget
                if key == "budget" and value :
                    try:
                        tmpval = float(int(value))
                        if (tmpval > 0) :
                            xbmc.executebuiltin('SetProperty(ListItemHelper.budget,"'+str(value)+'",home)')
                            try:
                                tmpval = round(tmpval/1000000, 2)
                                if tmpval.is_integer() :
                                    tmpval = '%.0f' % tmpval
                                else :
                                    if (tmpval >= 10) :
                                        tmpval = round(tmpval,0)
                                        tmpval = '%.0f' % tmpval
                                xbmc.executebuiltin('SetProperty(ListItemHelper.budget.million,"'+str(tmpval)+'",home)')
                            except:
                                pass
                    except:
                        pass
                if key == "budget.formatted" and value :
                    try:
                        if (value != '0') :
                             xbmc.executebuiltin('SetProperty(ListItemHelper.budget.formatted,"'+str(value)+'",home)')
                    except:
                        pass
                # revenue
                if key == "revenue" and value :
                    try:
                        tmpval = float(int(value))
                        if (tmpval > 0) :
                            xbmc.executebuiltin('SetProperty(ListItemHelper.revenue,"'+str(value)+'",home)')
                            try:
                                tmpval = round(tmpval/1000000, 2)
                                if tmpval.is_integer() :
                                    tmpval = '%.0f' % tmpval
                                else :
                                    if (tmpval >= 10) :
                                        tmpval = round(tmpval,0)
                                        tmpval = '%.0f' % tmpval
                                xbmc.executebuiltin('SetProperty(ListItemHelper.revenue.million,"'+str(tmpval)+'",home)')
                            except:
                                pass
                    except:
                        pass
                if key == "revenue.formatted" and value :
                    try:
                        if (value != '0') :
                             xbmc.executebuiltin('SetProperty(ListItemHelper.revenue.formatted,"'+str(value)+'",home)')
                    except:
                        pass
    #set_helper_values end


    def get_omdb_info(self, imdb_id="", title="", year="", content_type=""):
        '''Get (kodi compatible formatted) metadata from OMDB, including Rotten tomatoes details'''
        #title = title.split(" (")[0]  # strip year appended to title
        result = {}
        if imdb_id:
            result = self.omdb.get_details_by_imdbid(imdb_id)
        '''
        elif title and content_type in ["seasons", "season", "episodes", "episode", "tvshows", "tvshow"]:
            result = self.omdb.get_details_by_title(title, "", "tvshows")
        elif title and year:
            result = self.get_details_by_title(title, year, content_type)
         if result and result.get("status"):
             result["status"] = self.translate_string(result["status"])
         if result and result.get("runtime"):
             result["runtime"] = result["runtime"] / 60
             result.update(self.get_duration(result["runtime"]))
        '''
        return result


    def get_tmdb_details(self, imdb_id="", tvdb_id="", title="", year="", media_type="",
                         preftype="", manual_select=False, ignore_cache=False):
        '''returns details from tmdb'''
        result = {}
        if imdb_id:
            result = self.tmdb.get_videodetails_by_externalid(
                imdb_id, "imdb_id")
        '''
        elif tvdb_id:
            result = self.tmdb.get_videodetails_by_externalid(
                tvdb_id, "tvdb_id")
        elif title and media_type in ["movies", "setmovies", "movie"]:
            result = self.tmdb.search_movie(
                title, year, manual_select=manual_select, ignore_cache=ignore_cache)
        elif title and media_type in ["tvshows", "tvshow"]:
            result = self.tmdb.search_tvshow(
                title, year, manual_select=manual_select, ignore_cache=ignore_cache)
        elif title:
            result = self.tmdb.search_video(
                title, year, preftype=preftype, manual_select=manual_select, ignore_cache=ignore_cache)
        if result and result.get("status"):
            result["status"] = self.translate_string(result["status"])
        if result and result.get("runtime"):
            result["runtime"] = result["runtime"] / 60
            result.update(self.get_duration(result["runtime"]))
        '''
        return result


    @property
    def omdb(self):
        '''public omdb object - for lazy loading'''
        if not self._omdb:
            from lib.omdb import ListItemHelperOmdb
            self._omdb = ListItemHelperOmdb(self.cache)
        return self._omdb


    @property
    def tmdb(self):
        '''public Tmdb object - for lazy loading'''
        if not self._tmdb:
            from lib.tmdb import Tmdb
            self._tmdb = Tmdb(self.cache)
        return self._tmdb


if (__name__ == "__main__"):
    Main()


log('script finished.')

