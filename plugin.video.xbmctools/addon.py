#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Copyright 2014 Anonymous
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


##############BIBLIOTECAS A IMPORTAR E DEFINICOES####################

import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmc,xbmcaddon,HTMLParser,os,sys,time,subprocess,shutil,hashlib
h = HTMLParser.HTMLParser()

versao = '1.1.3'
addon_id = 'plugin.video.xbmctools'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
if not os.path.exists(addonfolder): addonfolder = addonfolder.decode('utf-8')
artfolder = addonfolder + '/resources/img/'
dialog = xbmcgui.Dialog()
xbmc_version = int(xbmc.getInfoLabel("System.BuildVersion" )[0:2])
traducaoma= selfAddon.getLocalizedString

def traducao(texto):
	return traducaoma(texto).encode('utf-8')
	
if selfAddon.getSetting('force-openelec') == "false": forcar_openelec = False
else: forcar_openelec = True
if selfAddon.getSetting('first_run') == "true": first_run = True
else: first_run = False
################################################## 

#MENUS############################################

def CATEGORIES():
	if xbmc.getCondVisibility('system.platform.windows'):
	#WINDOWS
		mensagem_os("Windows")
		dialog.ok(traducao(2000), traducao(2001))
		if xbmc_version < 14: addDir(traducao(2002),"windows",1,artfolder + "keyboard.png")
		addDir(traducao(2003),"windows",3,artfolder + "dll.png",False)
		addDir(traducao(2004),"windows",9,artfolder + "backup.png")
		addLink('','','nothing')
		VersionChecker("windows")
	#-----------------------------------------------------------------------
	elif xbmc.getCondVisibility('System.Platform.OSX'):
		mensagem_os("macOS")
		if first_run:
			if os.uname()[4] == "i686" or os.uname()[4] == "i386": selfAddon.setSetting('mac_bits',value=str(0))
			else:
				if xbmc_bit_version() == "x32": selfAddon.setSetting('mac_bits',value=str(0))
				elif xbmc_bit_version() == "x64": selfAddon.setSetting('mac_bits',value=str(1))
				else:
					ret = dialog.select(traducao(2056), ['x86', 'x64'])
					if ret == -1: sys.exit(0); return;
					selfAddon.setSetting('mac_bits',value=str(ret))
			selfAddon.setSetting('first_run',value='false')
		
		addDir(traducao(2003),"macos",3,artfolder + "dll.png",False)
		addDir(traducao(2004),"macos",9,artfolder + "backup.png")
		addLink('','','nothing')
		VersionChecker("macos")
	elif xbmc.getCondVisibility('system.platform.linux') and not xbmc.getCondVisibility('system.platform.Android'):
		if os.uname()[4] == 'armv6l': 
			#RASPBERRY
			if re.search(os.uname()[1],"openelec",re.IGNORECASE) or forcar_openelec:
				mensagem_os("Openelec")
				addDir(traducao(2003),"raspberry",8,artfolder + "dll.png",False)
				addDir(traducao(2004),"openelec",9,artfolder + "backup.png")
				addLink('','','nothing')
				VersionChecker("openelec")
			else:
				mensagem_os("RaspberryPI (OS)")
				set_librtmp_path()
				if xbmc_version < 14: addDir(traducao(2002),"linux",1,artfolder + "keyboard.png")
				addDir(traducao(2003),"raspberry",7,artfolder + "dll.png",False)
				addDir(traducao(2004),"raspberry",9,artfolder + "backup.png")
				addLink('','','nothing')
				VersionChecker("raspberry")
			#-------------------------------------------------------------------
		elif os.uname()[4] == 'armv7l':
			#ARMv7
			erro_os()
			'''if re.search(os.uname()[1],"openelec",re.IGNORECASE) or forcar_openelec:
				mensagem_os("Openelec")
				addDir(traducao(2003),"raspberry",8,artfolder + "dll.png",False)
				addDir(traducao(2004),"openelec",9,artfolder + "backup.png")
				addLink('','','nothing')
				VersionChecker("openelec")
			else:
				mensagem_os("Linux")
				addDir(traducao(2003),"armv7",3,artfolder + "dll.png",False) 
				addDir(traducao(2004),"armv7",9,artfolder + "backup.png")
				addLink('','','nothing')
				VersionChecker("raspberry")'''
		else: 
			#LINUX
			if re.search(os.uname()[1],"openelec",re.IGNORECASE): 
				mensagem_os("Openelec")
				addDir(traducao(2003),"-",8,artfolder + "dll.png",False)
				addDir(traducao(2004),"openelec",9,artfolder + "backup.png")
				addLink('','','nothing')
				VersionChecker("openelec pc")
			else:
				mensagem_os("Linux")
				set_librtmp_path()
				if xbmc_version < 14: addDir(traducao(2002),"linux",1,artfolder + "keyboard.png")
				addDir(traducao(2003),"linux",7,artfolder + "dll.png",False)
				addDir(traducao(2004),"linux",9,artfolder + "backup.png")
				addLink('','','nothing')
				VersionChecker("linux")
			#-------------------------------------------------------------------
	elif xbmc.getCondVisibility('system.platform.Android'): 
	#ANDROID
		mensagem_os("Android")
		if xbmc_version < 14: addDir(traducao(2002),"android",1,artfolder + "keyboard.png")
		addDir("Download APK","-",11,artfolder + "apk.png",False)
		addDir(traducao(2003)+" [COLOR blue](XBMC Gotham 13)[/COLOR]","-",5,artfolder + "dll.png",False)
		addDir(traducao(2004),"android",9,artfolder + "backup.png")
		addLink('','','nothing')
		VersionChecker("android")
	#-------------------------------------------------------------------
	elif xbmc.getCondVisibility('system.platform.IOS'): 
	#IOS
		mensagem_os("iOS")
		addDir(traducao(2003),"ios",3,artfolder + "dll.png",False)
		addDir(traducao(2004),"ios",9,artfolder + "backup.png")
		addLink('','','nothing')
		VersionChecker("ios")
	#-------------------------------------------------------------------
	else: erro_os()
	
	disponivel=versao_disponivel() # nas categorias
	if disponivel==versao: addLink('[B][COLOR white]'+traducao(2005)+' (' + versao + ')[/COLOR][/B]','',artfolder + 'versao.png')
	elif disponivel=='Erro ao verificar a versão!': addLink('[B][COLOR white]' + traducao(2006) + '[/COLOR][/B]','',artfolder + 'versao.png')
	else: addLink('[B][COLOR white]'+traducao(2007)+' ('+ disponivel + '). '+traducao(2008)+'[/COLOR][/B]','',artfolder + 'versao.png')
	print "--------- XBMC Tools ---------"

###################################################################################
#FUNCOES

def VersionChecker(system):
	if system == "ios":
		librtmp_path = os.path.join(xbmc.translatePath("special://xbmc").replace('XBMCData/XBMCHome','Frameworks'),"librtmp.0.dylib")
		md5 = abrir_url("http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/librtmp/md5/ios.xml.md5")
	elif system == "macos":
		librtmp_path = os.path.join(xbmc.translatePath("special://xbmc").replace('Resources/XBMC','Libraries'),"librtmp.0.dylib")
		if selfAddon.getSetting('mac_bits') == "0": md5 = abrir_url("http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/librtmp/md5/macos_x86.xml.md5")
		elif selfAddon.getSetting('mac_bits') == "1": md5 = abrir_url("http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/librtmp/md5/macos_x64.xml.md5")
		else: return
	elif system == "windows":
		librtmp_path = os.path.join(xbmc.translatePath("special://xbmc"), "system/players/dvdplayer/librtmp.dll")
		md5 = abrir_url("http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/librtmp/md5/windows.xml.md5")
	elif system == "android":		
		librtmp_path = os.path.join(android_xbmc_path(), "lib","librtmp.so")	
		md5 = abrir_url("http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/librtmp/md5/android.xml.md5")
	elif system == "openelec":
		md5 = abrir_url("http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/librtmp/md5/raspberry.xml.md5")
		librtmp_path = "/storage/lib/librtmp.so.0"
	elif system == "openelec pc":
		if os.uname()[4] == "i686" or os.uname()[4] == "i386": md5 = abrir_url("http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/librtmp/md5/linux_x86.xml.md5")
		elif os.uname()[4] == "x86_64": md5 = abrir_url("http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/librtmp/md5/linux_x64.xml.md5")
		else: return
		librtmp_path = "/storage/lib/librtmp.so.0"
	elif system == "linux" or system == "raspberry":
		librtmp_path, lib = _librtmp_path()
		if system == "raspberry": md5 = abrir_url("http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/librtmp/md5/raspberry.xml.md5")
		elif system == "linux": 
			if os.uname()[4] == "i686" or os.uname()[4] == "i386": md5 = abrir_url("http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/librtmp/md5/linux_x86.xml.md5")
			elif os.uname()[4] == "x86_64": md5 = abrir_url("http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/librtmp/md5/linux_x64.xml.md5")
			else: return
			
	if md5sum_verified(librtmp_path) == md5: addLink("[B][COLOR blue]"+traducao(2049)+"[/COLOR][/B]",'',artfolder + "check.png")
	else: addLink("[B][COLOR red]"+traducao(2050)+"[/COLOR][/B]",'',artfolder + "check.png")

def keyboard(url):
	dialog.ok(traducao(2009), traducao(2010))
	if url == "windows":
		addDir("QWERTY","qwerty windows",2,artfolder + "keyboard.png",False)
		addDir("ABCDE","abcde windows",2,artfolder + "keyboard.png",False)
	elif url == "android":
		addDir("QWERTY","qwerty android",2,artfolder + "keyboard.png",False)
		addDir("ABCDE","abcde android",2,artfolder + "keyboard.png",False)
	elif url == "linux":
		addDir("QWERTY","qwerty",6,artfolder + "keyboard.png",False)
		addDir("ABCDE","abcde",6,artfolder + "keyboard.png",False)
		
#########################################	LINUX

def _librtmp_path():
	file_path = selfAddon.getSetting('librtmp_path')
	if "librtmp.so.0" in file_path: lib = "librtmp.so.0"
	elif "librtmp.so.1" in file_path: lib = "librtmp.so.1"
	else: lib = "erro"
	return file_path,lib

def set_librtmp_path():
	if selfAddon.getSetting('librtmp_path') != "": return
	mensagemprogresso = xbmcgui.DialogProgress()
	mensagemprogresso.create('XBMC Tools', traducao(3031),traducao(2013))
	mensagemprogresso.update(33)
	file_path = find_abs_path("librtmp.so.0","/lib/")
	if file_path == "erro": file_path = find_abs_path("librtmp.so.1","/lib/")
	mensagemprogresso.update(66)
	selfAddon.setSetting('librtmp_path',value=file_path)
	mensagemprogresso.update(100)
	mensagemprogresso.close()

def file_name(path):
	import ntpath
	head, tail = ntpath.split(path)
	return tail or ntpath.basename(head)

def find_abs_path(str_path, search_str = ""):
	p = subprocess.Popen('find / | grep ' + str_path, stdout=subprocess.PIPE,stderr=subprocess.PIPE, shell=True)
	(output, err) = p.communicate()
	p_status = p.wait()
	
	aux = ""
	paths = []
	letra = False
	
	for x in range(0, len(output)):
		if not letra:
			if output[x] == " " or output[x] == "\n": continue
			else:
				aux = aux + output[x]
				letra = True
		else:
			if output[x] == " " or output[x] == "\n":
				try:
					if output[x+1] == "/" or output[x+1] == " " or output[x+1] == "\n":
						paths.append(aux)
						aux = ""
						letra = False
					else: aux = aux + output[x]
				except: paths.append(aux)
			else: aux = aux + output[x]
	
	if len(paths) == 1:
		if file_name(paths[0]) == str_path: return paths[0]
		else: return "erro"
	if search_str != "":
		for x in range(0, len(paths)):
			if search_str in paths[x] and file_name(paths[x]) == str_path: return paths[x]
		return "erro"
	return paths

def librtmp_openelec(url):
	if url == "raspberry":
		md5 = abrir_url("http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/librtmp/md5/raspberry.xml.md5")
		url_download = "http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/librtmp/RaspberryPI/librtmp.so.0"
	else:
		if os.uname()[4] == "i686" or os.uname()[4] == "i386": 
			url_download = "http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/librtmp/Linux/x86&ATV1/librtmp.so.0"
			md5 = abrir_url("http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/librtmp/md5/linux_x86.xml.md5")
		elif os.uname()[4] == "x86_64": 
			url_download = "http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/librtmp/Linux/x64/librtmp.so.0"
			md5 = abrir_url("http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/librtmp/md5/linux_x64.xml.md5")
		else:
			ret = dialog.select(traducao(2030), ['x86', 'x64'])
			if ret == 0:
				url_download = "http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/librtmp/Linux/x86&ATV1/librtmp.so.0"
				md5 = abrir_url("http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/librtmp/md5/linux_x86.xml.md5")
			elif ret == 1: 
				url_download = "http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/librtmp/Linux/x64/librtmp.so.0"
				md5 = abrir_url("http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/librtmp/md5/linux_x64.xml.md5")
			else: return
		
	if md5sum_verified("/storage/lib/librtmp.so.0") == md5:
		if not dialog.yesno(traducao(2016),traducao(2044),traducao(2045)): return
	
	my_tmp = os.path.join(addonfolder,"resources","temp","librtmp.so.0")
	
	if not download(my_tmp,url_download):
		dialog.ok(traducao(2014), traducao(2015))
		return;
		
	if os.path.exists("/storage/lib/librtmp.so.0") and os.path.exists("/var/tmp/libhack/3rdparty/librtmp.so.0"):
		if not dialog.yesno(traducao(2016),traducao(2053),traducao(2054)):
			subprocess.call("rm /storage/lib/librtmp.so.0", shell=True)
			subprocess.call("cp " + my_tmp + " /storage/lib/librtmp.so.0", shell=True)
			subprocess.call("chmod 755 /storage/lib/librtmp.so.0", shell=True)
			subprocess.call("rm " + my_tmp, shell=True)
			
			if md5sum_verified("/storage/lib/librtmp.so.0") != md5: dialog.ok(traducao(2014),traducao(2042),traducao(2043))
			
			dialog.ok(traducao(2016),traducao(2017))
			subprocess.call("reboot", shell=True)
			return
	
	mensagemprogresso = xbmcgui.DialogProgress()
	mensagemprogresso.create('XBMC Tools', traducao(2012),traducao(2013))
	subprocess.call("mkdir -p /storage/lib", shell=True)
	mensagemprogresso.update(13)
	subprocess.call("curl -L http://is.gd/kBaTzY -o /storage/.config/autostart.sh", shell=True)
	mensagemprogresso.update(26)
	subprocess.call("curl -L http://is.gd/yQUqNm -o /storage/.config/hacklib", shell=True)
	mensagemprogresso.update(39)
	subprocess.call("curl -L http://is.gd/GJdaEY -o /storage/.config/mktmplib", shell=True)
	mensagemprogresso.update(52)
	subprocess.call("cp " + my_tmp + " /storage/lib/librtmp.so.0", shell=True)
	mensagemprogresso.update(65)
	subprocess.call("chmod 755 /storage/lib/librtmp.so.0", shell=True)
	mensagemprogresso.update(78)
	subprocess.call("ln -s /storage/lib/librtmp.so.0 /storage/lib/librtmp.so", shell=True)
	mensagemprogresso.update(90)
	subprocess.call("rm " + my_tmp, shell=True)
	mensagemprogresso.update(100)
	mensagemprogresso.close()
	
	if md5sum_verified("/storage/lib/librtmp.so.0") != md5: dialog.ok(traducao(2014),traducao(2042),traducao(2043))
	
	dialog.ok(traducao(2016),traducao(2017))
	subprocess.call("reboot", shell=True)

def is_admin():
	import ctypes
	return ctypes.windll.shell32.IsUserAnAdmin() != 0
	
def backup(url):
	addDir("Backup",url + " backup",10,artfolder + "backup.png",False)
	addDir("Restore",url + " restore",10,artfolder + "backup.png",False)
	addDir("Apagar backup",url + " remove",10,artfolder + "backup.png",False)
	
def backup_(url):
	if "backup" in url:
		if not dialog.yesno(traducao(2016), traducao(2018),traducao(2019)): return
	elif "remove" in url:
		if not dialog.yesno(traducao(2016), traducao(2020),traducao(2019)): return
	elif "restore" in url:
		if not dialog.yesno(traducao(2016), traducao(2021),traducao(2019)): return

	if "linux" in url or "raspberry" in url or "openelec" in url:
		if "openelec" in url: librtmp_path = "/storage/lib/librtmp.so.0"
		else:
			librtmp_path, lib = _librtmp_path()
		
		if os.path.exists(librtmp_path) is False:
			dialog.ok(traducao(2014), traducao(2022))
			return
			
		if ("remove" in url or "restore" in url) and not os.path.exists(librtmp_path.replace("librtmp.so.0","librtmp.so.0.bak")): 
			dialog.ok(traducao(2016), traducao(2023))
			return
		
		if "linux" in url or "raspberry" in url:
			if verifica_pass(""): password = ""
			else:
				keyb = xbmc.Keyboard('', traducao(2024)) 
				keyb.setHiddenInput(True)
				keyb.doModal()
				if (keyb.isConfirmed()): password = keyb.getText()
				else: return
				
				if verifica_pass(password) is False: 
					dialog.ok(traducao(2014), traducao(2025))
					return
		if "openelec" in url:
			if "remove" in url or "backup" in url: subprocess.call("rm " + librtmp_path.replace("librtmp.so.0","librtmp.so.0.bak"), shell=True)
			if "backup" in url: subprocess.call("cp " + librtmp_path + " " + librtmp_path.replace("librtmp.so.0","librtmp.so.0.bak"), shell=True)
			if "restore" in url: 
				subprocess.call("rm " + librtmp_path, shell=True)
				subprocess.call("cp " + librtmp_path.replace("librtmp.so.0","librtmp.so.0.bak") + " " + librtmp_path, shell=True)
				subprocess.call("rm " + librtmp_path.replace("librtmp.so.0","librtmp.so.0.bak"), shell=True)
				subprocess.call("chmod 755 " + librtmp_path, shell=True)
			dialog.ok(traducao(2026),traducao(2027))
			return
		
		if "remove" in url or "backup" in url:		
			p = subprocess.Popen("sudo -S rm " + librtmp_path.replace(lib,lib+".bak"), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
			p.communicate(password+"\n") 
		if "backup" in url:
			p = subprocess.Popen("sudo -S cp " + librtmp_path + " " + librtmp_path.replace(lib,lib+".bak"), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
			p.communicate(password+"\n")
		if "restore" in url:
			p = subprocess.Popen("sudo -S rm " + librtmp_path, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
			p.communicate(password+"\n") 
			p = subprocess.Popen("sudo -S cp " + librtmp_path.replace(lib,lib+".bak") + " " + librtmp_path, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
			p.communicate(password+"\n")
			p = subprocess.Popen("sudo -S rm " + librtmp_path.replace(lib,lib+".bak"), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
			p.communicate(password+"\n") 
			p = subprocess.Popen("sudo -S chmod 755 " + librtmp_path, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
			p.communicate(password+"\n") 
		dialog.ok(traducao(2026),traducao(2027))
		return
		
	if "windows" in url or "ios" in url or "macos" in url or "armv7" in url:
		xbmc_folder = xbmc.translatePath("special://xbmc")
		if "windows" in url:
			if not is_admin():
				dialog.ok(traducao(2014),traducao(2028))
				return
			librtmp_path = os.path.join(xbmc_folder, "system/players/dvdplayer/librtmp.dll")
			bak_path = os.path.join(xbmc_folder, "system/players/dvdplayer/librtmp.dll.bak")
		if "ios" in url:
			librtmp_path = os.path.join(xbmc_folder.replace('XBMCData/XBMCHome','Frameworks'),"librtmp.0.dylib")
			bak_path = os.path.join(xbmc_folder.replace('XBMCData/XBMCHome','Frameworks'),"librtmp.0.dylib.bak")
		if "macos" in url:
			librtmp_path = os.path.join(xbmc_folder.replace('Resources/XBMC','Libraries'),"librtmp.0.dylib")
			bak_path = os.path.join(xbmc_folder.replace('Resources/XBMC','Libraries'),"librtmp.0.dylib.bak")
		if "armv7" in url:
			librtmp_path, lib = _librtmp_path()
			bak_path = librtmp_path.replace(lib,lib+'.bak')
		
		if os.path.exists(librtmp_path) is False:
			dialog.ok(traducao(2014), traducao(2022))
			return
		
		if ("remove" in url or "restore" in url) and not os.path.exists(bak_path): 
			dialog.ok(traducao(2016), traducao(2023))
			return
		
		if "remove" in url or "backup" in url: 
			if not remove_ficheiro(bak_path): return
		if "backup" in url: shutil.copy(librtmp_path,bak_path)
		if "restore" in url:
			if not remove_ficheiro(librtmp_path): return
			shutil.copy(bak_path,librtmp_path)
			remove_ficheiro(bak_path)
			if "windows" in url: os.chmod(librtmp_path,755)
		dialog.ok(traducao(2026),traducao(2027))
		return
		
	if "android" in url:
		librtmp_path = os.path.join(android_xbmc_path(), "lib/librtmp.so")
		bak_path = os.path.join(android_xbmc_path(), "lib/librtmp.so.bak")
		
		if ("remove" in url or "restore" in url) and not os.path.exists(bak_path): 
			dialog.ok(traducao(2016), traducao(2023))
			return
		
		if not checksu():
			dialog.ok(traducao(2014),traducao(2029))
			return
			
		if "remove" in url or "backup" in url: os.system("su -c 'rm "+bak_path+"'")
		if "backup" in url: os.system("su -c 'cat "+librtmp_path+" > "+bak_path+"'")
		if "restore" in url:
			os.system("su -c 'rm "+librtmp_path+"'")
			os.system("su -c 'cat "+bak_path+" > "+librtmp_path+"'")
			os.system("su -c 'rm "+bak_path+"'")
			os.system("su -c 'chmod 755 "+librtmp_path+"'")
		dialog.ok(traducao(2026),traducao(2027))
		return
		
def librtmp_linux(url):
	
	if url == "raspberry":
		url_download = "http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/librtmp/RaspberryPI/librtmp.so.0"
		md5 = abrir_url("http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/librtmp/md5/raspberry.xml.md5")
	elif url == "linux":
		if os.uname()[4] == "i686" or os.uname()[4] == "i386": 
			url_download = "http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/librtmp/Linux/x86&ATV1/librtmp.so.0"
			md5 = abrir_url("http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/librtmp/md5/linux_x86.xml.md5")
		elif os.uname()[4] == "x86_64": 
			url_download = "http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/librtmp/Linux/x64/librtmp.so.0"
			md5 = abrir_url("http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/librtmp/md5/linux_x64.xml.md5")
		else:
			ret = dialog.select(traducao(2030), ['x86', 'x64'])
			if ret == 0:
				url_download = "http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/librtmp/Linux/x86&ATV1/librtmp.so.0"
				md5 = abrir_url("http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/librtmp/md5/linux_x86.xml.md5")
			elif ret == 1: 
				url_download = "http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/librtmp/Linux/x64/librtmp.so.0"
				md5 = abrir_url("http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/librtmp/md5/linux_x64.xml.md5")
			else: return
	else: return
		
	file_path, lib = _librtmp_path()

	if os.path.exists(file_path) is False:
		dialog.ok(traducao(2014), traducao(2022))
		return

	librtmp_path = file_path.replace(lib,"")
	my_tmp = os.path.join(addonfolder,"resources","temp",lib)
	
	if md5sum_verified(file_path) == md5:
		if not dialog.yesno(traducao(2016),traducao(2044),traducao(2045)): return
	
	if verifica_pass(""): password = ""
	else:
		keyb = xbmc.Keyboard('', traducao(2024)) 
		keyb.setHiddenInput(True)
		keyb.doModal()
		if (keyb.isConfirmed()): password = keyb.getText()
		else: return
		
		if verifica_pass(password) is False: 
			dialog.ok(traducao(2014), traducao(2025))
			return

	if download(my_tmp,url_download):
		p = subprocess.Popen("sudo -S rm " + file_path, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
		p.communicate(password+"\n") 
		p = subprocess.Popen("sudo -S cp " + my_tmp + " " + librtmp_path, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
		p.communicate(password+"\n") 
		remove_ficheiro(my_tmp)
		p = subprocess.Popen("sudo -S chmod 755 " + file_path, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
		p.communicate(password+"\n") 
		if md5sum_verified(file_path) == md5: dialog.ok(traducao(2016), traducao(2026),traducao(2032))
		else: dialog.ok(traducao(2014),traducao(2042),traducao(2043))
	else: dialog.ok(traducao(2014), traducao(2015))
    

def verifica_pass(password):
	p = subprocess.Popen("sudo -S su ", stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
	(output, err) = p.communicate(password+"\n") 
	rc = p.returncode
	if rc == 0: return True
	return False

def change_keyboard_linux(url):
	mensagemprogresso = xbmcgui.DialogProgress()
	mensagemprogresso.create('XBMC Tools', traducao(3031),traducao(2013))
	mensagemprogresso.update(50)
	file_path = find_abs_path("DialogKeyboard.xml","skin.confluence/720p/")
	
	if (os.path.exists(file_path) and "skin.confluence/720p/DialogKeyboard.xml" in file_path) is False:
		mensagemprogresso.close()
		dialog.ok(traducao(2014), traducao(2034))
		return
	
	keyboard_path = file_path.replace("DialogKeyboard.xml","")
	my_tmp = os.path.join(addonfolder,"resources","temp","DialogKeyboard.xml")
	mensagemprogresso.update(100)
	mensagemprogresso.close()
	
	if verifica_pass(""): password = ""
	else:
		keyb = xbmc.Keyboard('', traducao(2024)) 
		keyb.setHiddenInput(True)
		keyb.doModal()
		if (keyb.isConfirmed()): password = keyb.getText()
		else: return
		
		if verifica_pass(password) is False: 
			dialog.ok(traducao(2014), traducao(2025))
			return
	
	if url == "qwerty": url_download = "http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/keyboard/qwerty/DialogKeyboard.xml"
	elif url == "abcde": url_download = "http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/keyboard/abcd/DialogKeyboard.xml"
	
	if download(my_tmp,url_download):
		p = subprocess.Popen("sudo -S rm " + file_path, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
		p.communicate(password+"\n") 
		p = subprocess.Popen("sudo -S cp " + my_tmp + " " + keyboard_path, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
		p.communicate(password+"\n") 
		remove_ficheiro(my_tmp)
		dialog.ok(traducao(2016), traducao(2026),traducao(2032))
	else: dialog.ok(traducao(2014), traducao(2015))

#########################################	ANDROID
	
def checksu():
	if os.system("su -c ''") == 0: return True
	return False
	
def librtmp_android():
	my_librtmp = os.path.join(addonfolder,"resources","temp","librtmp.so")
	librtmp_path = os.path.join(android_xbmc_path(), "lib", "librtmp.so")
	md5 = abrir_url("http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/librtmp/md5/android.xml.md5")
	
	if os.path.exists(librtmp_path) is False:
		dialog.ok(traducao(2014), traducao(2022))
		return
		
	if md5sum_verified(librtmp_path) == md5:
		if not dialog.yesno(traducao(2016),traducao(2044),traducao(2045)): return 
		
	if not dialog.yesno(traducao(2016), traducao(2033),traducao(2019)): return

	if not checksu():
		dialog.ok(traducao(2014),traducao(2029))
		return
	
	print "////////ANDROID////////"
	print "my_librtmp: " + my_librtmp
	print "librtmp_path: " + librtmp_path
	
	if download(my_librtmp,"http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/librtmp/Android/librtmp.so"):
		c1 = os.system("su -c 'rm "+librtmp_path+"'")
		c2 = os.system("su -c 'cat "+my_librtmp+" > "+librtmp_path+"'")
		c3 = os.system("su -c 'chmod 755 "+librtmp_path+"'")
		remove_ficheiro(my_librtmp)
		if md5sum_verified(librtmp_path) == md5: dialog.ok(traducao(2016), traducao(2026),traducao(2032))
		else: dialog.ok(traducao(2014),traducao(2042),traducao(2043))
		print "Return: " + str(c1) +" "+ str(c2) +" "+ str(c3)
	else: dialog.ok(traducao(2014), traducao(2015))
	
def android_xbmc_path():	#Obrigado enen92!
	xbmcfolder=xbmc.translatePath(addonfolder).split("/")
	i = 0
	found = False
	
	for folder in xbmcfolder:
		if folder.count('.') >= 2 and folder != addon_id :
			found = True
			break
		else:
			i+=1

	if found == True:
		uid = os.getuid()
		app_id = xbmcfolder[i]
		xbmc_data_path = os.path.join("/data", "data", app_id)
		if os.path.exists(xbmc_data_path) and uid == os.stat(xbmc_data_path).st_uid: return xbmc_data_path
	return "erro"
	
def get_mediafire_url(url):
	codigo_fonte = abrir_url(url).replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')    
	try: return re.compile('kNO = "(.+?)"').findall(codigo_fonte)[0]
	except: return "erro"
	
def download_apk():
	dir = dialog.browse(int(3), traducao(2047), 'files')
	if dir == "": return
	if not os.path.exists(dir):
		dialog.ok(traducao(2014),traducao(2046))
		return
	url = abrir_url("http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/apk/url.txt")
	url = get_mediafire_url(url)
	if url == "erro":
		dialog.ok(traducao(2014), traducao(2015))
		return
	if download(os.path.join(dir,file_name(url)),url): dialog.ok(traducao(2026),traducao(2048))
	else: dialog.ok(traducao(2014), traducao(2015))
	
#########################################	WINDOWS, IOS e MAC OSX

def xbmc_bit_version():
	log_path = xbmc.translatePath('special://logpath')
	log = os.path.join(log_path, 'xbmc.log')
	f = open(log,"r")
	aux = f.readlines()
	f.close()
	try: 
		bits = re.compile('XBMC (.+?) build').findall(aux[3])[0]
		if bits == "x32" or bits == "x64": return bits
	except: pass
	try:
		i = aux[3].find("-bit version", 0)
		bits = "x"+aux[3][i-2]+aux[3][i-1]
		if bits == "x32" or bits == "x64": return bits
		else: return "erro"
	except: return "erro"

def librtmp_updater(url):
	xbmc_folder = xbmc.translatePath("special://xbmc")
	if url == "windows": 
		if not is_admin():
			dialog.ok(traducao(2014),traducao(2028))
			return
		librtmp_path = os.path.join(xbmc_folder, "system/players/dvdplayer/librtmp.dll")
		my_librtmp = os.path.join(addonfolder,"resources","temp","librtmp.dll")
		download_url = "http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/librtmp/Windows/librtmp.dll"
		md5 = abrir_url("http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/librtmp/md5/windows.xml.md5")
	elif url == "ios":
		librtmp_path = os.path.join(xbmc_folder.replace('XBMCData/XBMCHome','Frameworks'),"librtmp.0.dylib")
		my_librtmp = os.path.join(addonfolder,"resources","temp","librtmp.0.dylib")
		download_url = "http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/librtmp/iOS/librtmp.0.dylib"
		md5 = abrir_url("http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/librtmp/md5/ios.xml.md5")
	elif url == "macos":
		if selfAddon.getSetting('mac_bits') == "0":
			download_url = "http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/librtmp/macOS/x86/librtmp.0.dylib"
			md5 = abrir_url("http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/librtmp/md5/macos_x86.xml.md5")
		elif selfAddon.getSetting('mac_bits') == "1":
			download_url = "http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/librtmp/macOS/x64/librtmp.0.dylib"
			md5 = abrir_url("http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/librtmp/md5/macos_x64.xml.md5")
		else: return
		librtmp_path = os.path.join(xbmc_folder.replace('Resources/XBMC','Libraries'),"librtmp.0.dylib")
		my_librtmp = os.path.join(addonfolder,"resources","temp","librtmp.0.dylib")
	elif url == "armv7":
		download_url = "http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/librtmp/RaspberryPI/librtmp.so.0"
		md5 = abrir_url("http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/librtmp/md5/raspberry.xml.md5")
		librtmp_path, lib = _librtmp_path()
		my_librtmp = os.path.join(addonfolder,"resources","temp",lib)
	else: return
	
	if os.path.exists(librtmp_path) is False:
		dialog.ok(traducao(2014), traducao(2022))
		return
		
	if md5sum_verified(librtmp_path) == md5:
		if not dialog.yesno(traducao(2016),traducao(2044),traducao(2045)): return 
		
	if download(my_librtmp,download_url):
		if not remove_ficheiro(librtmp_path): return
		shutil.copy(my_librtmp,librtmp_path)
		remove_ficheiro(my_librtmp)
		if url == "windows" or url == "armv7": os.chmod(librtmp_path,755)
		if md5sum_verified(librtmp_path) == md5: dialog.ok(traducao(2016), traducao(2026),traducao(2032))
		else: dialog.ok(traducao(2014),traducao(2042),traducao(2043))
	else: dialog.ok(traducao(2014), traducao(2015))
	
def change_keyboard(url):
	if "windows" in url: 
		if not is_admin():
			dialog.ok(traducao(2014),traducao(2028))
			return
		keyboard_path = os.path.join(xbmc.translatePath("special://xbmc"), "addons/skin.confluence/720p/DialogKeyboard.xml")
	elif "android" in url: keyboard_path = os.path.join(android_xbmc_path(), "cache/apk/assets/addons/skin.confluence/720p/DialogKeyboard.xml")
	else: return
	
	my_tmp = os.path.join(addonfolder,"resources","temp","DialogKeyboard.xml")
	if os.path.exists(keyboard_path) is False:
		dialog.ok(traducao(2014), traducao(2034))
		return
		
	if "qwerty" in url: url_download = "http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/keyboard/qwerty/DialogKeyboard.xml"
	elif "abcde" in url: url_download = "http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/keyboard/abcd/DialogKeyboard.xml"
	else: return
		
	if download(my_tmp,url_download):
		if not remove_ficheiro(keyboard_path): return
		shutil.copy(my_tmp,keyboard_path)
		remove_ficheiro(my_tmp)
		dialog.ok(traducao(2016), traducao(2026),traducao(2032))
	else: dialog.ok(traducao(2014), traducao(2015))

def md5sum_verified(path):	#Obrigado Mafarricos!
	if not os.path.exists(path): return "erro"
	BLOCK_SIZE = 65536
	hasher = hashlib.md5()
	f = open(path,'rb')
	done = 0
	size = os.path.getsize(path)
	while done < size:
		data = f.read(BLOCK_SIZE)
		done += len(data)
		hasher.update(data)
		if not data: break		
	md5sum = hasher.hexdigest()
	return md5sum
	
#########################################

def remove_ficheiro(file_path):
	while os.path.exists(file_path): 
			try: os.remove(file_path); break 
			except:	
				dialog = xbmcgui.Dialog()
				if dialog.yesno(traducao(2014), traducao(2039)): pass
				else: return False
	return True
	
def mensagem_os(so_name):
	dialog.ok(traducao(2016), traducao(2035) + so_name +".",traducao(2036))

def erro_os():
	dialog.ok(traducao(2014), traducao(2037))
	sys.exit(0)
	
def download(mypath,url,md5 = ''):
	if os.path.isfile(mypath) is True:
		if not remove_ficheiro(mypath):
			dialog.ok(traducao(2014),traducao(2038))
			return False

	dp = xbmcgui.DialogProgress()
	dp.create('Download')
	start_time = time.time()		# url - url do ficheiro    mypath - localizacao ex: c:\file.mp3
	try: urllib.urlretrieve(url, mypath, lambda nb, bs, fs: dialogdown(nb, bs, fs, dp, start_time))
	except:
		while os.path.exists(mypath): 
			try: os.remove(mypath); break 
			except: pass
		dp.close()
		return False
	dp.close()
	print "MD5: " + md5sum_verified(mypath)
	if not os.path.isfile(mypath): return False
	if md5 == '': return True
	if md5 == md5sum_verified(mypath): return True
	return False

def dialogdown(numblocks, blocksize, filesize, dp, start_time):
      try:
            percent = min(numblocks * blocksize * 100 / filesize, 100)
            currently_downloaded = float(numblocks) * blocksize / (1024 * 1024) 
            kbps_speed = numblocks * blocksize / (time.time() - start_time) 
            if kbps_speed > 0: eta = (filesize - numblocks * blocksize) / kbps_speed 
            else: eta = 0 
            kbps_speed = kbps_speed / 1024 
            total = float(filesize) / (1024 * 1024) 
            mbs = '%.02f MB %s %.02f MB' % (currently_downloaded,traducao(2040), total) 
            e = ' (%.0f Kb/s) ' % kbps_speed 
            tempo = traducao(2041) + ' %02d:%02d' % divmod(eta, 60) 
            dp.update(percent, mbs + e,tempo)
      except: 
            percent = 100 
            dp.update(percent) 
      if dp.iscanceled(): 
            dp.close()
            raise StopDownloading('Stopped Downloading')

class StopDownloading(Exception):
      def __init__(self, value): self.value = value 
      def __str__(self): return repr(self.value)

def versao_disponivel():
	try:
		codigo_fonte=abrir_url('http://anonymous-repo.googlecode.com/svn/trunk/anonymous-repo/plugin.video.xbmctools/addon.xml')		#ALTERAR NO FIM
		match=re.compile('<addon id="plugin.video.xbmctools" name="XBMC Tools" version="(.+?)"').findall(codigo_fonte)[0]
	except:
		match='Erro ao verificar a versão!'
	return match
	
###################################################################################
#FUNCOES JÁ FEITAS

def abrir_url(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link

def addLink(name,url,iconimage,total=1):
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image', addonfolder + '/fanart.jpg')
	liz.setInfo( type="Video", infoLabels={ "Title": name } )
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz,totalItems=total)
	return ok

def addDir(name,url,mode,iconimage,pasta = True,total=1):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image', addonfolder + '/fanart.jpg')
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta,totalItems=total)
	return ok

############################################################################################################
#                                               GET PARAMS                                                 #
############################################################################################################
              
def get_params():
	param=[]
	paramstring=sys.argv[2]
	if len(paramstring)>=2:
		params=sys.argv[2]
		cleanedparams=params.replace('?','')
		if (params[len(params)-1]=='/'):
			params=params[0:len(params)-2]
		pairsofparams=cleanedparams.split('&')
		param={}
		for i in range(len(pairsofparams)):
			splitparams={}
			splitparams=pairsofparams[i].split('=')
			if (len(splitparams))==2:
				param[splitparams[0]]=splitparams[1] 
	return param

params=get_params()
url=None
name=None
mode=None
iconimage=None

try: url=urllib.unquote_plus(params["url"])
except: pass
try: name=urllib.unquote_plus(params["name"])
except: pass
try: mode=int(params["mode"])
except: pass
try: iconimage=urllib.unquote_plus(params["iconimage"])
except: pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "Iconimage: "+str(iconimage)

###############################################################################################################
#                                                   MODOS                                                     #
###############################################################################################################

if mode==None or url==None or len(url)<1: CATEGORIES()
elif mode==1: keyboard(url)
elif mode==2: change_keyboard(url)
elif mode==3: librtmp_updater(url)
elif mode==5: librtmp_android()
elif mode==6: change_keyboard_linux(url)
elif mode==7: librtmp_linux(url)
elif mode==8: librtmp_openelec(url)
elif mode==9: backup(url)
elif mode==10: backup_(url)
elif mode==11: download_apk()
xbmcplugin.endOfDirectory(int(sys.argv[1]))
