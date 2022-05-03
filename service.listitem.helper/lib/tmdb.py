#!/usr/bin/python
# -*- coding: utf-8 -*-

'''Get metadata from tmdb'''

from utils import get_json, KODI_LANGUAGE, try_parse_int, int_with_commas, ADDON_ID
from simplecache import use_cache
from operator import itemgetter
import xbmc
import xbmcgui
import xbmcaddon
import datetime


class Tmdb(object):
    '''get metadata from tmdb'''
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
        api_key = addon.getSetting("tmdb_api_key")
        if api_key:
            self.api_key = api_key
        del addon

    def get_movie_details(self, movie_id):
        '''get all moviedetails'''
        params = {
            "append_to_response": "keywords,videos,credits,images",
            "include_image_language": "%s,en" % KODI_LANGUAGE,
            "language": KODI_LANGUAGE
        }
        return self.map_details(self.get_data("movie/%s" % movie_id, params), "movie")

    def get_tvshow_details(self, tvshow_id):
        '''get all tvshowdetails'''
        params = {
            "append_to_response": "keywords,videos,external_ids,credits,images",
            "include_image_language": "%s,en" % KODI_LANGUAGE,
            "language": KODI_LANGUAGE
        }
        return self.map_details(self.get_data("tv/%s" % tvshow_id, params), "tvshow")

    def get_videodetails_by_externalid(self, extid, extid_type):
        '''get metadata by external ID (like imdbid)'''
        params = {"external_source": extid_type, "language": KODI_LANGUAGE}
        results = self.get_data("find/%s" % extid, params)
        if results and results["movie_results"]:
            return self.get_movie_details(results["movie_results"][0]["id"])
        elif results and results["tv_results"]:
            return self.get_tvshow_details(results["tv_results"][0]["id"])
        return {}

    def get_data(self, endpoint, params):
        '''helper method to get data from tmdb json API'''
        url = u'http://api.themoviedb.org/3/%s' % endpoint
        unique_cache_id = 'listitemhelpertmdb.' + url
        if self.api_key:
            # addon provided or personal api key
            params["api_key"] = self.api_key
            rate_limit = None
            expiration = datetime.timedelta(days=3)
        else:
            # fallback api key (rate limited !)
            params["api_key"] = ""
            # without personal (or addon specific) api key = rate limiting and older info from cache
            rate_limit = ("themoviedb.org", 5)
            expiration = datetime.timedelta(days=30)
        cache = self.cache.get(unique_cache_id)
        if cache:
            # data obtained from cache
            result = cache
        elif self.api_key:
            # no cache, grab data from API
            result = get_json(url, params, ratelimit=rate_limit)
            # make sure that we have a plot value (if localized value fails, fallback to english)
            if result and "language" in params and "overview" in result:
                if not result["overview"] and params["language"] != "en":
                    params["language"] = "en"
                    result2 = get_json(url, params)
                    if result2 and result2.get("overview"):
                        result = result2
            if result:
                self.cache.set(unique_cache_id, result, expiration=expiration)
        if self.api_key:
            return result

    def map_details(self, data, media_type):
        '''helper method to map the details received from tmdb to kodi compatible formatting'''
        if not data:
            return {}
        details = {}
        details["tmdb_id"] = data["id"]
        details["rating"] = data["vote_average"]
        details["votes"] = data["vote_count"]
        details["rating.tmdb"] = data["vote_average"]
        details["votes.tmdb"] = data["vote_count"]
        details["popularity"] = data["popularity"]
        details["popularity.tmdb"] = data["popularity"]
        details["plot"] = data["overview"]
        details["genre"] = [item["name"] for item in data["genres"]]
        details["homepage"] = data["homepage"]
        details["status"] = data["status"]
        details["cast"] = []
        details["castandrole"] = []
        details["writer"] = []
        details["director"] = []
        details["media_type"] = media_type
        # cast
        if "credits" in data:
            if "cast" in data["credits"]:
                for cast_member in data["credits"]["cast"]:
                    cast_thumb = ""
                    if cast_member["profile_path"]:
                        cast_thumb = "http://image.tmdb.org/t/p/original%s" % cast_member["profile_path"]
                    details["cast"].append({"name": cast_member["name"], "role": cast_member["character"],
                                            "thumbnail": cast_thumb})
                    details["castandrole"].append((cast_member["name"], cast_member["character"]))
            # crew (including writers and directors)
            if "crew" in data["credits"]:
                for crew_member in data["credits"]["crew"]:
                    cast_thumb = ""
                    if crew_member["profile_path"]:
                        cast_thumb = "http://image.tmdb.org/t/p/original%s" % crew_member["profile_path"]
                    if crew_member["job"] in ["Author", "Writer"]:
                        details["writer"].append(crew_member["name"])
                    if crew_member["job"] in ["Producer", "Executive Producer"]:
                        details["director"].append(crew_member["name"])
                    if crew_member["job"] in ["Producer", "Executive Producer", "Author", "Writer"]:
                        details["cast"].append({"name": crew_member["name"], "role": crew_member["job"],
                                                "thumbnail": cast_thumb})
        # artwork
        details["art"] = {}
        if data.get("images"):
            if data["images"].get("backdrops"):
                fanarts = self.get_best_images(data["images"]["backdrops"])
                details["art"]["fanarts"] = fanarts
                details["art"]["fanart"] = fanarts[0] if fanarts else ""
            if data["images"].get("posters"):
                posters = self.get_best_images(data["images"]["posters"])
                details["art"]["posters"] = posters
                details["art"]["poster"] = posters[0] if posters else ""
        if not details["art"].get("poster") and data.get("poster_path"):
            details["art"]["poster"] = "http://image.tmdb.org/t/p/original%s" % data["poster_path"]
        if not details["art"].get("fanart") and data.get("backdrop_path"):
            details["art"]["fanart"] = "http://image.tmdb.org/t/p/original%s" % data["backdrop_path"]
        # movies only
        if media_type == "movie":
            details["title"] = data["title"]
            details["originaltitle"] = data["original_title"]
            if data["belongs_to_collection"]:
                details["set"] = data["belongs_to_collection"].get("name", "")
            if data.get("release_date"):
                details["premiered"] = data["release_date"]
                details["year"] = try_parse_int(data["release_date"].split("-")[0])
            details["tagline"] = data["tagline"]
            if data["runtime"]:
                details["runtime"] = data["runtime"] * 60
            details["imdbnumber"] = data["imdb_id"]
            details["budget"] = data["budget"]
            details["budget.formatted"] = int_with_commas(data["budget"])
            details["revenue"] = data["revenue"]
            details["revenue.formatted"] = int_with_commas(data["revenue"])
            if data.get("production_companies"):
                details["studio"] = [item["name"] for item in data["production_companies"]]
            if data.get("production_countries"):
                details["country"] = [item["name"] for item in data["production_countries"]]
            if data.get("keywords"):
                details["tag"] = [item["name"] for item in data["keywords"]["keywords"]]
        # tvshows only
        if media_type == "tvshow":
            details["title"] = data["name"]
            details["originaltitle"] = data["original_name"]
            if data.get("created_by"):
                details["director"] += [item["name"] for item in data["created_by"]]
            if data.get("episode_run_time"):
                details["runtime"] = data["episode_run_time"][0] * 60
            if data.get("first_air_date"):
                details["premiered"] = data["first_air_date"]
                details["year"] = try_parse_int(data["first_air_date"].split("-")[0])
            if "last_air_date" in data:
                details["lastaired"] = data["last_air_date"]
            if data.get("networks"):
                details["studio"] = [item["name"] for item in data["networks"]]
            if "origin_country" in data:
                details["country"] = data["origin_country"]
            if data.get("external_ids"):
                details["imdbnumber"] = data["external_ids"].get("imdb_id", "")
                details["tvdb_id"] = data["external_ids"].get("tvdb_id", "")
            if "results" in data["keywords"]:
                details["tag"] = [item["name"] for item in data["keywords"]["results"]]
        # trailer
        for video in data["videos"]["results"]:
            if video["site"] == "YouTube" and video["type"] == "Trailer":
                details["trailer"] = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % video["key"]
                break
        return details

    @staticmethod
    def get_best_images(images):
        '''get the best 5 images based on number of likes and the language'''
        for image in images:
            score = 0
            score += image["vote_count"]
            score += image["vote_average"] * 10
            score += image["height"]
            if "iso_639_1" in image:
                if image["iso_639_1"] == KODI_LANGUAGE:
                    score += 1000
            image["score"] = score
            if not image["file_path"].startswith("http"):
                image["file_path"] = "http://image.tmdb.org/t/p/original%s" % image["file_path"]
        images = sorted(images, key=itemgetter("score"), reverse=True)
        return [image["file_path"] for image in images]
