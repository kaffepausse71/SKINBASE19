#!/usr/bin/python

########################

import xbmcgui

from lib.img.helper import *
from lib.img.utils import *

########################

class Main:

    def __init__(self):
        self.action = False
        self._parse_argv()

        if self.action:
            self.getactions()


    def _parse_argv(self):
        args = sys.argv

        for arg in args:
            if arg == ADDON_ID:
                continue
            if arg.startswith('action='):
                self.action = arg[7:].lower()
            else:
                try:
                    self.params[arg.split("=")[0].lower()] = "=".join(arg.split("=")[1:]).strip()
                except:
                    self.params = {}
                    pass


    def getactions(self):
            util = globals()[self.action]
            util(self.params)


if __name__ == "__main__":
    Main()
