#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright (C) 2019 by Loki1979
import os,sys,re,hashlib
import xml.etree.ElementTree as ET

if sys.version_info.major < 3:
	sys.stdout.write("Dieses Script wurde auf Python 3.X.X ausgelegt !")
	sys.stdout.flush()
	sys.exit(0)

_script_path = os.path.normpath(os.path.dirname(os.path.realpath(sys.argv[0])))

def _stdout_writer(s):
	try:
		sys.stdout.buffer.write(s.encode("UTF-8"))
		sys.stdout.flush()

	except Exception as e:_stdout_writer("STDOUT WRITER ERROR :{0}".format(e))

def _repo_updater(script_path):

	_stdout_writer("Kodi Repo Updater Copyright (C) 2019 by Loki1979\n")
	_stdout_writer("Python Version : {0}\n\n".format(sys.version))
	_stdout_writer("Starte Repo ( XML & XML.MD5 ) Updater !\n\n")

	try:

		addon_counter = 0
		_stdout_writer("Durchlaufe Repo Addons :\n{0}\n\n".format(script_path))
		addons_xml = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>\n<addons>\n"

		for addon in os.listdir(script_path):
			if (re.search("(context|metadata|plugin|repo|resource|script|service|skin|weather)",addon) and not re.search(".zip",addon)):

				addon_xml_path = os.path.join(script_path,addon,"addon.xml")
				if os.path.exists(addon_xml_path):

					name="";id="";version="";provider=""
					for elem in ET.parse(addon_xml_path).getroot().iter('addon'):
						name = re.sub("\[[^\]]*\]","",elem.attrib['name'])
						id = elem.attrib['id']
						version = "-" + elem.attrib['version']
						provider =  re.sub("\[[^\]]*\]","",elem.attrib['provider-name'])
						_stdout_writer("Addon Name       : {0}\nAddon ID         : {1}\nAddon Ver        : {2}\nErsteller        : {3}\n\n".format(name,id,version[1:],provider))

					addon_xml_content = ""
					with open(addon_xml_path,"r",encoding="UTF-8") as xml:
						for line in xml.readlines():
							if not (line.find("<?xml") >= 0):addon_xml_content += line.rstrip() + "\n"
					addons_xml += addon_xml_content.rstrip() + "\n\n"

					addon_counter +=1

		if addon_counter > 0:

			addons_xml = addons_xml.strip() + "\n</addons>\n"
			with open(os.path.join(script_path,"addons.xml"),"wb") as fi:fi.write(addons_xml.encode("UTF-8"))

			addons_xml_hash = hashlib.md5(open(os.path.join(script_path,"addons.xml"),"r",encoding="UTF-8").read().encode("UTF-8")).hexdigest()
			with open(os.path.join(script_path,"addons.xml.md5"),"wb") as fi:fi.write(addons_xml_hash.encode("UTF-8"))

			_stdout_writer("Addons in Repo   : {0}\n".format(addon_counter))
			_stdout_writer("Datei erstellt   : addons.xml\n")
			_stdout_writer("Datei erstellt   : addons.xml.md5\n")
			_stdout_writer("Fertig !\n\n")

		else:_stdout_writer("Keine Addons im Repo Ordner :\n{0}\n\n".format(_script_path))

	except Exception as e:_stdout_writer("UPDATER EROR :{0}".format(e))

if __name__ == "__main__":_repo_updater(_script_path)