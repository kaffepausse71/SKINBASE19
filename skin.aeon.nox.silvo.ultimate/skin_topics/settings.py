#!/usr/bin/python
# -*- coding: utf-8 -*-
import xbmc,xbmcaddon,xbmcgui,xbmcvfs,sys,os,shutil,re

def fix_encoding(path):
    if sys.platform.startswith('win'):return path
    else:return path # .encode('iso-8859-2')

_skin_id_ = xbmc.getSkinDir()
_addon_ =  xbmcaddon.Addon(id =_skin_id_)
_addon_path_ = fix_encoding(_addon_.getAddonInfo('path'))
_addon_profile_ = fix_encoding(xbmcvfs.translatePath(_addon_.getAddonInfo('profile')))
_new_skin_settings_dir_ = os.path.join(_addon_path_,'skin_topics','settings_xmls')

def get_valid_filename(name):

    bad_chars_dict = {'\\':'','/':'',':':'',';':'','"':'',"'":'',',':'','+':'','*':'','#':'','?':'','<':'','>':'','&':'','%':'','$':'','§':'','ä':'ae','ö':'oe','ü':'ue','Ä':'Ae','Ö':'Oe','Ü':'Ue','ß':'ss'}

    bad_chars_found = ''
    for key,value in bad_chars_dict.items():

        if key in name:
           bad_chars_found += key + ' '
           name = name.replace(key,value)

    if len(bad_chars_found) > 0:
        xbmcgui.Dialog().ok('BAD CHARS FOUND AND REPLACED !',bad_chars_found)

    return fix_encoding(name)

def change_settings_xmls(new_skin_settings_dir,addon_profile):

    skin_settings_xml = os.path.join(addon_profile,'settings.xml')
    if not os.path.exists(addon_profile):os.makedirs(addon_profile)

    list=[]
    if os.path.exists(new_skin_settings_dir):
        list=os.listdir(new_skin_settings_dir)
        list.sort()

    else:os.makedirs(new_skin_settings_dir)

    save_delete_setings_array =['[COLOR red][ SAVE SKIN SETTINGS ][/COLOR]','[COLOR red][ DELETE SETTINGS ][/COLOR]']
    call = xbmcgui.Dialog().select('[COLOR blue]SKIN SETTINGS LOADER[/COLOR]',save_delete_setings_array + list)
    if call < 0:sys.exit(0)
		
    elif call == 0:
        new_xml_name = xbmcgui.Dialog().input(heading='[COLOR red]NEW SETTINGS FILE NAME ?[/COLOR]',defaultt='settings.xml', type=xbmcgui.INPUT_ALPHANUM).strip()
        if new_xml_name == '':change_settings_xmls(_new_skin_settings_dir_,_addon_profile_)
        new_xml_name = get_valid_filename(new_xml_name)
			
        if not new_xml_name.lower().endswith('.xml'):
            new_xml_name = new_xml_name + '.xml'

        save_settings_xml = os.path.join(new_skin_settings_dir,new_xml_name)

        if os.path.exists(save_settings_xml):
            xbmcgui.Dialog().ok('XML FILE ERROR','Filename already exists !')
            change_settings_xmls(_new_skin_settings_dir_,_addon_profile_)

        if os.path.exists(skin_settings_xml):
            shutil.copyfile(skin_settings_xml,save_settings_xml)
        else:xbmcgui.Dialog().ok('SAVE FILE ERROR','No skin settings found !')
        change_settings_xmls(_new_skin_settings_dir_,_addon_profile_)
		
    elif call == 1:
        call = xbmcgui.Dialog().select('[COLOR red]DELETE SETTINGS[/COLOR]',list)
        if call < 0:sys.exit(0)
        delete_settings_xml = os.path.join(new_skin_settings_dir,list[call])
        os.remove(delete_settings_xml)
        change_settings_xmls(_new_skin_settings_dir_,_addon_profile_)

    elif call > 1:

        new_settings_xml = os.path.join(new_skin_settings_dir,list[call-2])

        if os.path.exists(skin_settings_xml):os.remove(skin_settings_xml);xbmc.sleep(250)
        shutil.copyfile(new_settings_xml,skin_settings_xml)
        xbmc.sleep(250)

        profil=xbmc.getInfoLabel('System.ProfileName') 
        xbmc.executebuiltin('LoadProfile('+profil+')')
        sys.exit(0)

change_settings_xmls(_new_skin_settings_dir_,_addon_profile_)
### loki1979 - 27.01.2021 - 19:15 ### PY3 ###