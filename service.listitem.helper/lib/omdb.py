#!/usr/bin/python
# -*- coding: utf-8 -*-

'''get metadata from omdb'''

from utils import get_json, get_xml, formatted_number, int_with_commas, try_parse_int, KODI_LANGUAGE, ADDON_ID
from simplecache import use_cache
import arrow
import xbmc
import xbmcaddon




class ListItemHelperOmdb(object):
    '''get metadata from omdb'''
    api_key = None  # public var to be set by the calling addon

    def __init__(self, simplecache=None):
        '''Initialize - optionaly provide simplecache object'''
        if not simplecache:
            from simplecache import SimpleCache
            self.cache = SimpleCache()
        else:
            self.cache = simplecache
        addon = xbmcaddon.Addon(id=ADDON_ID)
        # personal api key (preferred over provided api key)
        api_key = addon.getSetting("omdb_api_key")
        if api_key:
            self.api_key = api_key
        del addon

    @use_cache(3)
    def get_details_by_imdbid(self, imdb_id):
        '''get omdb details by providing an imdb id'''
        params = {"i": imdb_id}
        data = self.get_data_xml(params)
        return self.map_details_xml(data) if data else None

    @use_cache(3)
    def get_data_xml(self, params):
        '''helper method to get data from omdb xml API'''
        base_url = 'http://www.omdbapi.com/'
        params["plot"] = "full"
        params["tomatoes"] = "true"
        if self.api_key:
            params["apikey"] = self.api_key
            rate_limit = None
        else:
            # rate limited api key !
            params["apikey"] = ""
            rate_limit = ("omdbapi.com", 2)
        params["r"] = "xml"
        if self.api_key:
            return get_xml(base_url, params, ratelimit=rate_limit)

    @staticmethod
    def map_details_xml(data):
        '''helper method to map the details received from omdb to kodi compatible format'''
        result = {}
        for key, value in data.iteritems():
            # filter the N/A values
            if value in ["N/A", "NA"] or not value:
                continue
            if key.lower() == "title":
                result["title"] = value
            elif key.lower() == "year":
                try:
                    #result["year"] = try_parse_int(value.split("-")[0])
                    result["year"] = value[:4]
                except Exception:
                    result["year"] = value
            elif key.lower() == "rated":
                result["mpaa"] = value.replace("Rated", "")
            elif key.lower() == "title":
                result["title"] = value
            elif key.lower() == "released":
                date_time = arrow.get(value, "DD MMM YYYY")
                result["premiered"] = date_time.strftime(xbmc.getRegion("dateshort"))
                try:
                    result["premiered.formatted"] = date_time.format('DD MMM YYYY', locale=KODI_LANGUAGE)
                except Exception:
                    result["premiered.formatted"] = value
            elif key.lower() == "runtime":
                result["runtime"] = try_parse_int(value.replace(" min", "")) * 60
            elif key.lower() == "genre":
                result["genre"] = value.split(", ")
            elif key.lower() == "director":
                result["director"] = value.split(", ")
            elif key.lower() == "writer":
                result["writer"] = value.split(", ")
            elif key.lower() == "country":
                result["country"] = value.split(", ")
            elif key.lower() == "awards":
                result["awards"] = value
            elif key.lower() == "poster":
                result["thumbnail"] = value
                result["art"] = {}
                result["art"]["thumb"] = value
            elif key.lower() == "imdbvotes":
                result["votes.imdb"] = value
                result["votes"] = try_parse_int(value.replace(",", ""))
            elif key.lower() == "metascore":
                ###### Metacritic ######
                result["metacritic.rating"] = value
                result["rating.mc"] = value
                result["metacritic.rating.percent"] = "%s" % value
                result["rating.mc.text"] = str(value)+'/100'
            elif key.lower() == "imdbrating":
                ###### IMDB ######
                result["rating.percent.imdb"] = "%s" % (try_parse_int(float(value) * 10))
                
                result["rating.imdb.text"] = str(value)+'/10'
                result["rating.imdb"] = value
                result["rating"] = float(value)
            elif key.lower() == "tomatometer":
                ###### Rotten Tomatoes ######
                result["rottentomatoes.rating"] = value
                result["rottentomatoes.rating.percent"] = value
                # additional duplicates
                result["rating.rt"] = value
                result["rottentomatoes.meter"] = value
                result["rottentomatoesmeter"] = value
            elif key.lower() == "tomatofresh":
                ###### Rotten Tomatoes ######
                result["rottentomatoes.fresh"] = value
            elif key.lower() == "tomatorotten":
                ###### Rotten Tomatoes ######
                result["rottentomatoes.rotten"] = value
            elif key.lower() == "tomatoeurl":
                ###### Rotten Tomatoes ######
                result["rottentomatoes.url"] = value
            elif key.lower() == "tomatousermeter":
                ###### Rotten Tomatoes ######
                result["rottentomatoes.audience"] = value
            elif key.lower() == "tomatoimage":
                ###### Rotten Tomatoes ######
                result["rottentomatoes.image"] = value
            elif key.lower() == "tomatourl":
                result["rottentomatoes.url"] = value
            elif key.lower() == "imdbid":
                result["imdbnumber"] = value
            elif key.lower() == "boxoffice":
                result["boxoffice"] = value
            elif key.lower() == "dvd":
                date_time = arrow.get(value, "DD MMM YYYY")
                result["dvdrelease"] = date_time.format('YYYY-MM-DD')
                result["dvdrelease.formatted"] = date_time.format('DD MMM YYYY', locale=KODI_LANGUAGE)
            elif key.lower() == "production":
                result["studio"] = value.split(", ")
            elif key.lower() == "website":
                result["homepage"] = value
            elif key.lower() == "plot":
                result["plot"] = value
                result["imdb.plot"] = value
            elif key.lower() == "type":
                if value == "series":
                    result["type"] = "tvshow"
                else:
                    result["type"] = value
                result["media_type"] = result["type"]
        return result