#!/usr/bin/python
# -*- coding: utf-8 -*-

'''various generic helper methods'''

import xbmcgui
import xbmc
import xbmcvfs
import xbmcaddon
import sys
from traceback import format_exc
import requests
import arrow
from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
import urllib
#import unicodedata
import os
import datetime
import time
import xml.etree.ElementTree as ET

try:
    import simplejson as json
except Exception:
    import json

try:
    from multiprocessing.pool import ThreadPool
    SUPPORTS_POOL = True
except Exception:
    SUPPORTS_POOL = False


ADDON_ID = "service.listitem.helper"
KODI_LANGUAGE = xbmc.getLanguage(xbmc.ISO_639_1)
if not KODI_LANGUAGE:
    KODI_LANGUAGE = "en"
KODI_VERSION = int(xbmc.getInfoLabel("System.BuildVersion").split(".")[0])

# setup requests with some additional options
requests.packages.urllib3.disable_warnings()
SESSION = requests.Session()
RETRIES = Retry(total=5, backoff_factor=5, status_forcelist=[500, 502, 503, 504])
SESSION.mount('http://', HTTPAdapter(max_retries=RETRIES))
SESSION.mount('https://', HTTPAdapter(max_retries=RETRIES))

FORCE_DEBUG_LOG = False
LIMIT_EXTRAFANART = 0
try:
    ADDON = xbmcaddon.Addon(ADDON_ID)
    FORCE_DEBUG_LOG = ADDON.getSetting('debug_log') == 'true'
    LIMIT_EXTRAFANART = int(ADDON.getSetting('max_extrafanarts'))
    del ADDON
except Exception:
    pass


def log_msg(msg, loglevel=xbmc.LOGDEBUG):
    '''log message to kodi logfile'''
    if isinstance(msg, unicode):
        msg = msg.encode('utf-8')
    if loglevel == xbmc.LOGDEBUG and FORCE_DEBUG_LOG:
        loglevel = xbmc.LOGNOTICE
    xbmc.log("%s --> %s" % (ADDON_ID, msg), level=loglevel)


def log_exception(modulename, exceptiondetails):
    '''helper to properly log an exception'''
    log_msg(format_exc(sys.exc_info()), xbmc.LOGWARNING)
    log_msg("ERROR in %s ! --> %s" % (modulename, exceptiondetails), xbmc.LOGERROR)


def rate_limiter(rl_params):
    ''' A very basic rate limiter which limits to 1 request per X seconds to the api'''
    # Please respect the parties providing these free api's to us and do not modify this code.
    # If I suspect any abuse I will revoke all api keys and require all users
    # to have a personal api key for all services.
    # Thank you
    if not rl_params:
        return
    monitor = xbmc.Monitor()
    win = xbmcgui.Window(10000)
    rl_name = rl_params[0]
    rl_delay = rl_params[1]
    cur_timestamp = int(time.mktime(datetime.datetime.now().timetuple()))
    prev_timestamp = try_parse_int(win.getProperty("ratelimiter.%s" % rl_name))
    if (prev_timestamp + rl_delay) > cur_timestamp:
        sec_to_wait = (prev_timestamp + rl_delay) - cur_timestamp
        log_msg(
            "Rate limiter active for %s - delaying request with %s seconds - "
            "Configure a personal API key in the settings to get rid of this message and the delay." %
            (rl_name, sec_to_wait), xbmc.LOGNOTICE)
        while sec_to_wait and not monitor.abortRequested():
            monitor.waitForAbort(1)
            # keep setting the timestamp to create some sort of queue
            cur_timestamp = int(time.mktime(datetime.datetime.now().timetuple()))
            win.setProperty("ratelimiter.%s" % rl_name, "%s" % cur_timestamp)
            sec_to_wait -= 1
    # always set the timestamp
    cur_timestamp = int(time.mktime(datetime.datetime.now().timetuple()))
    win.setProperty("ratelimiter.%s" % rl_name, "%s" % cur_timestamp)
    del monitor
    del win


def get_json(url, params=None, retries=0, ratelimit=None):
    '''get info from a rest api'''
    result = {}
    if not params:
        params = {}
    # apply rate limiting if needed
    rate_limiter(ratelimit)
    try:
        response = requests.get(url, params=params, timeout=20)
        if response and response.content and response.status_code == 200:
            result = json.loads(response.content.decode('utf-8', 'replace'))
            if "results" in result:
                result = result["results"]
            elif "result" in result:
                result = result["result"]
        elif response.status_code in (429, 503, 504):
            raise Exception('Read timed out')
    except Exception as exc:
        result = None
        if "Read timed out" in str(exc) and retries < 5 and not ratelimit:
            # retry on connection error or http server limiting
            monitor = xbmc.Monitor()
            if not monitor.waitForAbort(2):
                result = get_json(url, params, retries + 1)
            del monitor
        else:
            log_exception(__name__, exc)
    # return result
    return result


def get_xml(url, params=None, retries=0, ratelimit=None):
    '''get info from a rest api'''
    result = {}
    if not params:
        params = {}
    # apply rate limiting if needed
    rate_limiter(ratelimit)
    try:
        response = requests.get(url, params=params, timeout=20)
        if response and response.content and response.status_code == 200:
            tree = ET.fromstring(response.content)
            #child = tree.find('movie')
            if(len(tree)):
                child = tree[0]
            #log_exception(__name__, child)
            for attrName, attrValue in child.items():
                result.update({attrName : attrValue})
        elif response.status_code in (429, 503, 504):
            raise Exception('Read timed out')
    except Exception as exc:
        result = None
        if "Read timed out" in str(exc) and retries < 5 and not ratelimit:
            # retry on connection error or http server limiting
            monitor = xbmc.Monitor()
            if not monitor.waitForAbort(2):
                result = get_xml(url, params, retries + 1)
            del monitor
        else:
            log_exception(__name__, exc)
    # return result
    return result


def formatted_number(number):
    '''try to format a number to formatted string with thousands'''
    try:
        number = int(number)
        if number < 0:
            return '-' + formatted_number(-number)
        result = ''
        while number >= 1000:
            number, number2 = divmod(number, 1000)
            result = ",%03d%s" % (number2, result)
        return "%d%s" % (number, result)
    except Exception:
        return ""


def int_with_commas(number):
    '''helper to pretty format a number'''
    try:
        number = int(number)
        if number < 0:
            return '-' + int_with_commas(-number)
        result = ''
        while number >= 1000:
            number, number2 = divmod(number, 1000)
            result = ",%03d%s" % (number2, result)
        return "%d%s" % (number, result)
    except Exception:
        return ""


def try_parse_int(string):
    '''helper to parse int from string without erroring on empty or misformed string'''
    try:
        return int(string)
    except Exception:
        return 0

