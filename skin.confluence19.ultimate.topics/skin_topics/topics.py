#!/usr/bin/python
# -*- coding: utf-8 -*-
import xbmc,xbmcgui,xbmcaddon,os,sys,shutil,re
import pickle

def fix_encoding(path):
	if sys.platform.startswith('win'):return path
	else:return path # .encode('iso-8859-2')

_skin_id_ = xbmc.getSkinDir()
_addon_ = xbmcaddon.Addon(id = _skin_id_)
_skin_root_ = fix_encoding(_addon_.getAddonInfo( 'path' ))
_skin_backgrounds_ = os.path.join(_skin_root_,'backgrounds')
_pickle_file_ = os.path.join( _skin_root_,'skin_topics','data_save')
_topics_update_ = os.path.join( _skin_root_,'skin_topics','update.py')
_modified_topics_ = os.path.join( _skin_root_,'skin_topics','modified_topics')
_original_topics_fake_root_ = os.path.join(_skin_root_,'skin_topics','original_topics')

def save_pickle_value(pickle_file,value):
	f = open(pickle_file,'wb')
	pickle.dump(value,f)
	f.close()
	return

def load_pickle_value(pickle_file):
	f = open(pickle_file,'rb')
	value = pickle.load(f)
	f.close()
	return value

def unload_skin() :
	xbmc.executebuiltin('UnloadSkin()')
	return

def reload_skin():
	xbmc.executebuiltin('ReloadSkin()')
	return

def modified_topics(modified_topics):

	modified_topics_array=[]

	if os.path.exists(modified_topics) :

		for folder in os.listdir(modified_topics):
			modified_topics_array.append(folder)

	return modified_topics_array

def select_modified_topics(select_modified_topics_fake_root):

	dirs_root_path_array=[]
	files_root_path_array=[]

	for walk_data in os.walk(select_modified_topics_fake_root,topdown=True,onerror=None,followlinks=True):

		for dir in walk_data[1]:

			dir_rot_path = os.path.join(walk_data[0][len( select_modified_topics_fake_root ) + 1:],dir)
			dirs_root_path_array.append(dir_rot_path)

		for file in walk_data[2]:
			file_root_path = os.path.join(walk_data[0][len(select_modified_topics_fake_root ) + 1:],file)
			files_root_path_array.append(file_root_path)

	return dict({'dirs_root_path_array':dirs_root_path_array,'files_root_path_array':files_root_path_array})

def save_original_skin_topics(dirs_root_path_array,files_root_path_array,skin_root,original_topics_fake_root):

	for dir in dirs_root_path_array :

		dir_path = os.path.join(original_topics_fake_root,dir)
		if not os.path.exists(dir_path):os.makedirs(dir_path)

	for file in files_root_path_array :

		file_path1 = os.path.join(skin_root,file)
		file_path2 = os.path.join(original_topics_fake_root,file)

		if os.path.exists(file_path1)and not os.path.exists(file_path2):
			try:shutil.copy(file_path1,file_path2)
			except:pass

	return

def clear_original_topics(original_topics_fake_root):

	for walk_data in os.walk(original_topics_fake_root,topdown=False):

		for dir in walk_data[1]:
			path = os.path.join(walk_data[0],dir)
			try:os.rmdir(path)
			except:pass

		for file in walk_data[2]:
			path = os.path.join(walk_data[0],file)
			try:os.unlink(path)
			except:pass

	return

def reset_original_skin_topics(files_root_path_array,skin_root,original_topics_fake_root):

	for file in files_root_path_array :

		file_path1 = os.path.join(skin_root,file)
		file_path2 = os.path.join(original_topics_fake_root,file)

		if os.path.exists(file_path1):
			os.remove(file_path1)
		if os.path.exists(file_path2):
			try:shutil.copy(file_path2,file_path1)
			except:pass

	return

def copy_modified_topics_to_skin(files_root_path_array,skin_root,modified_topics_fake_root_call):

	for file in files_root_path_array :

		file_path1 = os.path.join(skin_root,file)
		file_path2 = os.path.join(modified_topics_fake_root_call,file)

		file_path1_path_check = os.path.dirname(file_path1)
		if not os.path.exists(file_path1_path_check):
			os.makedirs(file_path1_path_check)

		if os.path.exists(file_path1):
			os.remove(file_path1)
		if os.path.exists(file_path2):
			try:shutil.copy(file_path2, file_path1)
			except:pass

	return

time_sleep = int(100)
reset_original_topics = ['[COLOR red][ RESET ORIGINAL TOPICS ][/COLOR]']			
modified_topics_list = modified_topics(_modified_topics_)

if len(modified_topics_list) > 0:

	listitems=[]
	for item in reset_original_topics + modified_topics_list:

		listitem = xbmcgui.ListItem(label=item,path=item)

		if len(listitems) == 0:
			listitem.setArt({'thumb':os.path.join( _skin_root_,'skin_topics','reset.png')})
		elif os.path.exists(os.path.join(_modified_topics_,item,'info.jpg')):
			listitem.setArt({'thumb':os.path.join(_modified_topics_,item,'info.jpg')})
		elif os.path.exists(os.path.join(_modified_topics_,item,'info.png')):
			listitem.setArt({'thumb':os.path.join(_modified_topics_,item,'info.png')})
			
		listitems.append(listitem)

	call = xbmcgui.Dialog().select('[COLOR blue]SKIN TOPICS LOADER[/COLOR]',listitems,useDetails=True)
	if call < 0 : sys.exit(0)

	elif call == 0:

		if os.path.exists(_pickle_file_):
			unload_skin()
			xbmc.sleep(time_sleep)
			last_data_dict_array_value = load_pickle_value(_pickle_file_)
			reset_original_skin_topics(last_data_dict_array_value,_skin_root_,_original_topics_fake_root_)
			clear_original_topics(_original_topics_fake_root_)
			os.remove(_pickle_file_)
			reload_skin()

	else:

		unload_skin()
		xbmc.sleep(time_sleep)

		select_modified_topics_path = os.path.join( _modified_topics_,modified_topics_list[call-1])
		data_dict_array = select_modified_topics(select_modified_topics_path)

		save_original_skin_topics(data_dict_array['dirs_root_path_array'],data_dict_array['files_root_path_array'],_skin_root_,_original_topics_fake_root_)
		xbmc.sleep( time_sleep )

		last_data_dict_array_value=[]
		if os.path.exists( _pickle_file_ ):last_data_dict_array_value = load_pickle_value(_pickle_file_)
		if len(last_data_dict_array_value) < 1 :last_data_dict_array_value = data_dict_array['files_root_path_array']

		reset_original_skin_topics(last_data_dict_array_value,_skin_root_,_original_topics_fake_root_)
		xbmc.sleep(time_sleep)

		save_pickle_value(_pickle_file_, data_dict_array['files_root_path_array'])
		xbmc.sleep(time_sleep)

		copy_modified_topics_to_skin(data_dict_array['files_root_path_array'],_skin_root_,select_modified_topics_path)
		xbmc.sleep(time_sleep)

		reload_skin()
		sys.exit(0)

else:
	if os.path.exists(_topics_update_):xbmc.executebuiltin('RunScript('+_topics_update_+ ')')
	else:xbmcgui.Dialog().ok('NO SKIN TOPICS FOUND !','NO SKIN TOPICS OR UPDATE PY FOUND !')
	sys.exit(0)

### loki1979 - 27.01.2021 - 19:15 ### PY3 ###