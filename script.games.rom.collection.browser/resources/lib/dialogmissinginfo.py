from __future__ import absolute_import
from builtins import range
from configxmlwriter import *
from util import *
import util, config
import xbmcgui
from dialogbase import DialogBase

ACTION_CANCEL_DIALOG = (9, 10, 51, 92, 110)

CONTROL_BUTTON_EXIT = 5101
CONTROL_BUTTON_SAVE = 6000
CONTROL_BUTTON_CANCEL = 6010

CONTROL_LIST_SHOWHIDEMISSING = 5200

CONTROL_LABEL_ARTWORK_ORGROUP = 5220
CONTROL_BUTTON_ADD_ARTWORK_ORGROUP = 5230
CONTROL_BUTTON_REMOVE_ARTWORK_ORGROUP = 5240
CONTROL_LABEL_ARTWORK_ANDGROUP = 5250
CONTROL_BUTTON_ADD_ARTWORK_ANDGROUP = 5260
CONTROL_BUTTON_REMOVE_ARTWORK_ANDGROUP = 5270

CONTROL_LABEL_INFO_ORGROUP = 5280
CONTROL_BUTTON_ADD_INFO_ORGROUP = 5290
CONTROL_BUTTON_REMOVE_INFO_ORGROUP = 5300
CONTROL_LABEL_INFO_ANDGROUP = 5310
CONTROL_BUTTON_ADD_INFO_ANDGROUP = 5320
CONTROL_BUTTON_REMOVE_INFO_ANDGROUP = 5330


class MissingInfoDialog(DialogBase):
    artworkAndList = []
    artworkOrList = []
    infoAndList = []
    infoOrList = []

    saveConfig = False

    #32157 = ignore
    #32158 = Ignore filter
    #32159 = show
    #32160 = Show only games with missing items
    #32161 = hide
    #32162 = Hide games with missing items
    missingFilterOptions = {util.localize(32157): util.localize(32158),
                            util.localize(32159): util.localize(32160),
                            util.localize(32161): util.localize(32162)}

    def __init__(self, *args, **kwargs):
        Logutil.log('init dialog missing info', util.LOG_LEVEL_INFO)

        self.gui = kwargs["gui"]

        self.doModal()

    def onInit(self):
        Logutil.log('onInit dialog missing info', util.LOG_LEVEL_INFO)

        self.artworkAndList = self.gui.config.missingFilterArtwork.andGroup
        label = self.getControlById(CONTROL_LABEL_ARTWORK_ANDGROUP)
        label.setLabel(', '.join(self.artworkAndList))

        self.artworkOrList = self.gui.config.missingFilterArtwork.orGroup
        label = self.getControlById(CONTROL_LABEL_ARTWORK_ORGROUP)
        label.setLabel(', '.join(self.artworkOrList))

        self.infoAndList = self.gui.config.missingFilterInfo.andGroup
        label = self.getControlById(CONTROL_LABEL_INFO_ANDGROUP)
        label.setLabel(', '.join(self.infoAndList))

        self.infoOrList = self.gui.config.missingFilterInfo.orGroup
        label = self.getControlById(CONTROL_LABEL_INFO_ORGROUP)
        label.setLabel(', '.join(self.infoOrList))

        Logutil.log('add show/hide missing info options', util.LOG_LEVEL_INFO)
        #showHideOptions = ['Ignore filter', 'Show only games with missing items', 'Hide games with missing items']
        self.addItemsToList(CONTROL_LIST_SHOWHIDEMISSING, list(self.missingFilterOptions.values()))

        for i in range(0, len(list(self.missingFilterOptions.keys()))):
            key = list(self.missingFilterOptions.keys())[i]
            if key == self.gui.config.showHideOption:
                listShowHide = self.getControlById(CONTROL_LIST_SHOWHIDEMISSING)
                listShowHide.selectItem(i)

    def onAction(self, action):
        if action.getId() in ACTION_CANCEL_DIALOG:
            self.close()

    def onClick(self, controlID):

        Logutil.log('onClick', util.LOG_LEVEL_INFO)

        if controlID == CONTROL_BUTTON_EXIT:  # Close window button
            Logutil.log('close', util.LOG_LEVEL_INFO)
            self.close()
        elif controlID == CONTROL_BUTTON_ADD_ARTWORK_ORGROUP:
            Logutil.log('Add artwork or', util.LOG_LEVEL_INFO)
            self.artworkOrList = self.addItemToMissingArtworkList(self.artworkOrList, CONTROL_LABEL_ARTWORK_ORGROUP)

        elif controlID == CONTROL_BUTTON_REMOVE_ARTWORK_ORGROUP:
            Logutil.log('Remove artwork or', util.LOG_LEVEL_INFO)
            self.artworkOrList = self.removeFromMissingList(self.artworkOrList, CONTROL_LABEL_ARTWORK_ORGROUP)

        elif controlID == CONTROL_BUTTON_ADD_ARTWORK_ANDGROUP:
            Logutil.log('Add artwork and', util.LOG_LEVEL_INFO)
            self.artworkAndList = self.addItemToMissingArtworkList(self.artworkAndList, CONTROL_LABEL_ARTWORK_ANDGROUP)

        elif controlID == CONTROL_BUTTON_REMOVE_ARTWORK_ANDGROUP:
            Logutil.log('Remove artwork and', util.LOG_LEVEL_INFO)
            self.artworkAndList = self.removeFromMissingList(self.artworkAndList, CONTROL_LABEL_ARTWORK_ANDGROUP)

        elif controlID == CONTROL_BUTTON_ADD_INFO_ORGROUP:
            Logutil.log('Add info or', util.LOG_LEVEL_INFO)
            self.infoOrList = self.addItemToMissingInfoList(self.infoOrList, CONTROL_LABEL_INFO_ORGROUP)

        elif controlID == CONTROL_BUTTON_REMOVE_INFO_ORGROUP:
            Logutil.log('Remove info and', util.LOG_LEVEL_INFO)
            self.infoOrList = self.removeFromMissingList(self.infoOrList, CONTROL_LABEL_INFO_ORGROUP)

        elif controlID == CONTROL_BUTTON_ADD_INFO_ANDGROUP:
            Logutil.log('Add info and', util.LOG_LEVEL_INFO)
            self.infoAndList = self.addItemToMissingInfoList(self.infoAndList, CONTROL_LABEL_INFO_ANDGROUP)

        elif controlID == CONTROL_BUTTON_REMOVE_INFO_ANDGROUP:
            Logutil.log('Remove info and', util.LOG_LEVEL_INFO)
            self.infoAndList = self.removeFromMissingList(self.infoAndList, CONTROL_LABEL_INFO_ANDGROUP)

        #Save
        elif controlID == CONTROL_BUTTON_SAVE:
            Logutil.log('save', util.LOG_LEVEL_INFO)

            showHideList = self.getControlById(CONTROL_LIST_SHOWHIDEMISSING)
            index = showHideList.getSelectedPosition()
            showHideOptions = list(self.missingFilterOptions.keys())
            showHideOption = showHideOptions[index]

            configWriter = ConfigXmlWriter(False)
            success, message = configWriter.writeMissingFilter(showHideOption, self.artworkOrList, self.artworkAndList,
                                                               self.infoOrList, self.infoAndList)

            if success:
                self.saveConfig = True
            self.close()

        #Cancel
        elif controlID == CONTROL_BUTTON_CANCEL:
            Logutil.log('cancel', util.LOG_LEVEL_INFO)
            self.close()

    def onFocus(self, controlId):
        pass

    def addItemToMissingArtworkList(self, inList, labelId):
        tempList = []

        for romCollection in list(self.gui.config.romCollections.values()):
            for mediaPath in romCollection.mediaPaths:
                if (not mediaPath.fileType.name in tempList and not mediaPath.fileType.name in inList):
                    tempList.append(mediaPath.fileType.name)

        dialog = xbmcgui.Dialog()
        tempList = sorted(tempList)
        #32155 = Select Artwork type
        index = dialog.select(util.localize(32155), tempList)
        del dialog
        if index == -1:
            return inList

        inList.append(tempList[index])
        label = self.getControlById(labelId)
        label.setLabel(', '.join(inList))

        return inList

    def addItemToMissingInfoList(self, inList, labelId):

        tempList = []
        keys = list(config.gameproperties.keys())
        keys.sort()
        for item in keys:
            if not item in tempList and not item in inList:
                tempList.append(item)

        dialog = xbmcgui.Dialog()
        index = dialog.select(util.localize(32156), tempList)
        del dialog
        if index == -1:
            return inList

        inList.append(tempList[index])
        label = self.getControlById(labelId)
        label.setLabel(', '.join(inList))

        return inList

    def removeFromMissingList(self, inList, labelId):
        dialog = xbmcgui.Dialog()
        index = dialog.select(util.localize(32856), inList)
        del dialog
        if index == -1:
            return inList
        inList.remove(inList[index])
        label = self.getControlById(labelId)
        label.setLabel(', '.join(inList))

        return inList
