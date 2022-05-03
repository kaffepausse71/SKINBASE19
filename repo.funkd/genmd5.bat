@echo on

certutil -hashfile addons.xml MD5  | find /i /v "md5" | find /i /v "certutil" > addons.xml.md5

java -jar D:\KodiDev\RemoveCR.jar addons.xml.md5