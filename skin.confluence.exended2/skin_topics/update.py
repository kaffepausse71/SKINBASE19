#!/usr/bin/python
# -*- coding: utf-8 -*-
import xbmc,xbmcgui,xbmcaddon,os,sys,socket,math,time,datetime,shutil,re,xbmcvfs
import zipfile,pickle
import urllib.request

def fix_encoding(path):
	if sys.platform.startswith('win'):return path
	else:return path # .encode('iso-8859-2')
		
_show_test_topics_ = False
_skin_id_ = xbmc.getSkinDir()
_addon_ =  xbmcaddon.Addon(id = _skin_id_)
_skin_root_ = fix_encoding(_addon_.getAddonInfo('path'))
_skin_topics_ = os.path.join(_skin_root_,'skin_topics')
_skin_backgrounds_ = os.path.join(_skin_root_,'backgrounds')
_pickle_file_ = os.path.join(_skin_root_,'skin_topics','data_save')
_modified_topics_ = os.path.join(_skin_root_,'skin_topics','modified_topics')
_skin_topics_update_zip_ = os.path.join(_skin_root_,'skin_topics','update.zip')
_original_topics_fake_root_ = os.path.join(_skin_root_,'skin_topics','original_topics')

_server_data_url_ = 'https://raw.githubusercontent.com/kaffepausse71/SKIN-TOPICS/main/confluence/topics_data.txt'

def read_server_data(url):

	error = ''
	server_data = ''
	try:

		req= urllib.request.Request(url)
		socket.setdefaulttimeout(30)
		resp = urllib.request.urlopen(req,timeout = 30)
		server_data = resp.read()
		resp.close()

	except urllib.error.HTTPError as err : error = str(err)
	except urllib.error.URLError as err : error = str(err)
	except socket.timeout as err : error = str(err)

	if error == '' :return server_data.decode('utf-8')
	else :
		xbmcgui.Dialog().ok('SERVER ERROR !',error)
		return False

def server_data_regex(server_data,show_test_topics):

	server_data = server_data.replace("'",'"').strip()

	name_array = []
	url_array = []

	for regex_data in re.compile('name="(.*?)".*?url="(.*?)"', re.DOTALL).findall(server_data):

		if regex_data[0] and regex_data[1] :

			if not regex_data[0].startswith('*') or show_test_topics == True :

				name_array.append(regex_data[0])
				url_array.append(regex_data[1])

	return dict({ 'name_array':name_array , 'url_array':url_array })

def select_dialog(dic_array):

	listitems=[]
	for title,url in zip(dic_array['name_array'],dic_array['url_array']):

		info_image = os.path.dirname(url)
		listitem = xbmcgui.ListItem(label=title,path=url)

		if xbmcvfs.exists(info_image + '/info.jpg'):
			listitem.setArt({'thumb':info_image + '/info.jpg'})
		elif xbmcvfs.exists(info_image + '/info.png'):
			listitem.setArt({'thumb':info_image + '/info.png'})
			
		listitems.append(listitem)

	call = xbmcgui.Dialog().select('[COLOR blue]SKIN TOPICS DOWNLOADER[/COLOR]',listitems,useDetails=True)

	if call < 0 : return False
	else : return dic_array['url_array'][call]

def download_file(file_download_url,file_download_path):

	error = ''
	dp = xbmcgui.DialogProgress()

	def convert_size(size):

		if (size == 0):
			return '0B'

		units = (' B', ' KB', ' MB', ' GB', ' TB', ' PB', ' EB', ' ZB', ' YB')
		i = int(math.floor(math.log(size, 1024 )))
		p = math.pow(1024, i)
		size = "%.3f" % round(( size / p ), 3)

		return '{}{}' .format(size,units[i])

	try:

		req= urllib.request.Request(file_download_url)
		resp = urllib.request.urlopen(req, timeout = 30)

		total_size = int(0)
		downloaded = int(0)
		total_size = int(resp.info().get("Content-length"))

		dp.create('[COLOR blue]TOPICS ZIP DOWNLOADER[/COLOR]', 'Download file !\nPlease wait ...')
		dp.update(0)
		xbmc.sleep(1000)

		CHUNK = 1024*16
		start_time = time.time();xbmc.sleep(1)

		with open( file_download_path,'wb' ) as fw:

			while True:
				chunk = resp.read(CHUNK)
				downloaded += len(chunk)
				if not chunk: break
				fw.write(chunk)

				try:
					percent = int(min(downloaded * 100 / total_size,100))
					speed = (downloaded / (time.time() - start_time))

					if speed > 0: remaining_sec = (( total_size - downloaded ) / speed)
					else: remaining_sec = 0

					s = 'Geladen: %s von %s - ( %s%% )'% (convert_size(downloaded),convert_size(total_size),str(percent))
					ss = 'Geschwindigkeit: %s/s' % (convert_size(speed))
					sss = 'Verbleibende Zeit: %s' % datetime.timedelta(seconds=remaining_sec)

					dp.update(percent,s +'\n'+ ss +'\n'+ sss)
				except:
					dp.update(100)
					fw.close()
					dp.close()

				if dp.iscanceled():
					resp.close()
					fw.close()
					dp.close()
					return False

		dp.update( 100 )
		resp.close()
		fw.close()		
		dp.close()

	except urllib.error.HTTPError as err : error = str(err)
	except urllib.error.URLError as err : error = str(err)
	except socket.timeout as err : error = str(err)
	except IndexError as err : error = str(err)
	if error == '' : return True
	else: 
		xbmcgui.Dialog().ok('ZIP DOWNLOADER ERROR !', error)
		return False

def check_zipfile(zip_file_path):

	if os.path.exists(zip_file_path):

		try:return zipfile.ZipFile(zip_file_path, mode='r',compression=zipfile.ZIP_STORED,allowZip64 = True)
		except zipfile.BadZipfile : return 'No zip file !'

	else : return 'No zip file !'

def clear_original_topics(original_topics_fake_root):

	for walk_data in os.walk(original_topics_fake_root,topdown=False):

		for dir in walk_data[1] :
			path = os.path.join(walk_data[0],dir)
			try:os.rmdir(path)
			except:pass

		for file in walk_data[2] :
			path = os.path.join(walk_data[0],file)
			try:os.unlink(path)
			except:pass

	return

def reset_original_skin_topics(pickle_file,skin_root,skin_backgrounds,original_topics_fake_root):

	f = open(pickle_file,'rb')
	files_root_path_array = pickle.load(f)
	f.close()

	for file in files_root_path_array :

		file_path1 = os.path.join(skin_root, file)
		file_path2 = os.path.join(original_topics_fake_root, file)

		if os.path.exists(file_path1) :
			os.remove(file_path1)
		if os.path.exists(file_path2) :
			try:shutil.copy(file_path2, file_path1)
			except:pass

	return
	
def unload_skin() :
	xbmc.executebuiltin('UnloadSkin()')

	return

def reload_skin():
	xbmc.executebuiltin('ReloadSkin()')

	return

def delete_dir(dir_path):

	if os.path.exists(dir_path):
		shutil.rmtree(dir_path, ignore_errors = True)

	return

def delete_file(file_path):

	if os.path.exists(file_path):
		try:os.remove(file_path)
		except:pass

	return

def extract_zip(zipfile,extract_path,zip_pwd = None):

	dp = xbmcgui.DialogProgress()
	dp.create('[COLOR blue]TOPICS ZIP EXTRACTOR[/COLOR]', 'Unpacking data \nPlease wait ...')

	dp.update(0)
	count = int(0)
	xbmc.sleep(1000)

	try:
		nFiles = float(len(zipfile.infolist()))
		for item in zipfile.infolist():

			try:zipfile.extract(item, path=extract_path,pwd = zip_pwd)
			except:pass

			try:
				count += 1
				update = count / nFiles * 100
				dp.update(int(update))
			except:
				dp.update(100)
				zipfile.close()
				dp.close()

			if dp.iscanceled():
				zipfile.close()
				dp.close()
				return False

		zipfile.close()
		dp.close()
		return True

	except Exception as err:
		zipfile.close()
		dp.close()
		xbmcgui.Dialog().ok('ZIP EXTRACTOR ERROR !', str(err))
		return False

time_sleep = int(100)
server_data = read_server_data(_server_data_url_)
if server_data == False :
	sys.exit(0)
else:

	server_data_dict_array = server_data_regex(server_data, _show_test_topics_)
	if len( server_data_dict_array ) < 1 : sys.exit(0)

	select_url = select_dialog(server_data_dict_array)
	if not select_url : sys.exit(0)

	ok = download_file(select_url,_skin_topics_update_zip_)
	if ok == False : sys.exit(0) 
	xbmc.sleep((time_sleep + time_sleep))

	zf= check_zipfile(_skin_topics_update_zip_)
	if zf == 'No zip file !' :sys.exit(0)

	delete_dir(_modified_topics_)
	xbmc.sleep(time_sleep)

	extract_zip(zf,_skin_topics_)
	xbmc.sleep(time_sleep)

	delete_file(_skin_topics_update_zip_)

	if os.path.exists(_pickle_file_):
		unload_skin()
		xbmc.sleep(time_sleep)
		reset_original_skin_topics(_pickle_file_, _skin_root_,_skin_backgrounds_, _original_topics_fake_root_)
		clear_original_topics(_original_topics_fake_root_)
		os.remove(_pickle_file_)
		reload_skin()

	sys.exit(0)

### loki1979 - 27.01.2021 - 19:15 ### PY3 ###