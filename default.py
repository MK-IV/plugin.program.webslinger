import xbmc, xbmcaddon, xbmcgui, xbmcplugin,os,base64,sys,xbmcvfs
import shutil
import urllib2,urllib
import re
import time
import ntpath
import webbrowser
import glob




USER_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
addon_id = 'plugin.program.webslinger-master'
ADDON = xbmcaddon.Addon(id=addon_id)
AddonID='plugin.program.webslinger-master'
AddonTitle="Web Slinger"
dialog       =  xbmcgui.Dialog()
HOME =  xbmc.translatePath('special://home/')
dp =  xbmcgui.DialogProgress()
U = ADDON.getSetting('User')
FANART = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
ICON = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
ART = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id + '/resources/art/'))
VERSION = "1.0.0"
PATH = "MK-IV"            
BASEURL = "http://mkiv.ca"
urlbase      =  'None'
get_icon_1 = ADDON.getSetting('icon_1')
icon_1 = ART+xbmc.translatePath(os.path.join(get_icon_1 +'.png'))
get_icon_2 = ADDON.getSetting('icon_2')
icon_2 = ART+xbmc.translatePath(os.path.join(get_icon_2 +'.png'))
get_icon_3 = ADDON.getSetting('icon_3')
icon_3 = ART+xbmc.translatePath(os.path.join(get_icon_3 +'.png'))
get_icon_4 = ADDON.getSetting('icon_4')
icon_4 = ART+xbmc.translatePath(os.path.join(get_icon_4 +'.png'))
get_icon_5 = ADDON.getSetting('icon_5')
icon_5 = ART+xbmc.translatePath(os.path.join(get_icon_5 +'.png'))
get_icon_6 = ADDON.getSetting('icon_6')
icon_6 = ART+xbmc.translatePath(os.path.join(get_icon_6 +'.png'))
get_icon_7 = ADDON.getSetting('icon_7')
icon_7 = ART+xbmc.translatePath(os.path.join(get_icon_7 +'.png'))
get_icon_8 = ADDON.getSetting('icon_8')
icon_8 = ART+xbmc.translatePath(os.path.join(get_icon_8 +'.png'))
get_icon_9 = ADDON.getSetting('icon_9')
icon_9 = ART+xbmc.translatePath(os.path.join(get_icon_9 +'.png'))
get_icon_10 = ADDON.getSetting('icon_10')
icon_10 = ART+xbmc.translatePath(os.path.join(get_icon_10 +'.png'))
Default = ''

#Root menu of addon
def INDEX():
    if ADDON.getSetting('label_1') == "":
        addDir('[COLOR gold]Click here to setup Web Slinger[/COLOR]',BASEURL,11,ART+('settings.png'),FANART,'','') 
    else:   
        addDir(ADDON.getSetting('label_1'),BASEURL,1,icon_1,FANART,'','')
        pass
    if ADDON.getSetting('label_2') != "":
        addDir(ADDON.getSetting('label_2'),BASEURL,2,icon_2,FANART,'','')
    else: 
        pass
    if ADDON.getSetting('label_3') != "":
        addDir(ADDON.getSetting('label_3'),BASEURL,3,icon_3,FANART,'','')
    else:
        pass
    if ADDON.getSetting('label_4') != "":
        addDir(ADDON.getSetting('label_4'),BASEURL,4,icon_4,FANART,'','')
    else:
        pass
    if ADDON.getSetting('label_5') != "":
        addDir(ADDON.getSetting('label_5'),BASEURL,5,icon_5,FANART,'','')
    else:
        pass
    if ADDON.getSetting('label_6') != "":
        addDir(ADDON.getSetting('label_6'),BASEURL,6,icon_6,FANART,'','')
    else:
        pass
    if ADDON.getSetting('label_7') != "":
        addDir(ADDON.getSetting('label_7'),BASEURL,7,icon_7,FANART,'','')
    else:
        pass
    if ADDON.getSetting('label_8') != "":
        addDir(ADDON.getSetting('label_8'),BASEURL,8,icon_8,FANART,'','')
    else:
        pass
    if ADDON.getSetting('label_9') != "":
        addDir(ADDON.getSetting('label_9'),BASEURL,9,icon_9,FANART,'','')
    else:
        pass
    if ADDON.getSetting('label_10') != "":
        addDir(ADDON.getSetting('label_10'),BASEURL,10,icon_10,FANART,'','')
    else:
        pass
   

def Website_1(): #Mode 1
    webbrowser.open_new_tab(ADDON.getSetting('url_1'))

def Website_2(): #Mode 2
    webbrowser.open_new_tab(ADDON.getSetting('url_2'))

def Website_3(): #Mode 3
    webbrowser.open_new_tab(ADDON.getSetting('url_3'))

def Website_4(): #Mode 4
    webbrowser.open_new_tab(ADDON.getSetting('url_4'))

def Website_5(): #Mode 5
    webbrowser.open_new_tab(ADDON.getSetting('url_5'))

def Website_6(): #Mode 6
    webbrowser.open_new_tab(ADDON.getSetting('url_6'))

def Website_7(): #Mode 7
    webbrowser.open_new_tab(ADDON.getSetting('url_7'))

def Website_8(): #Mode 8
    webbrowser.open_new_tab(ADDON.getSetting('url_8'))

def Website_9(): #Mode 9
    webbrowser.open_new_tab(ADDON.getSetting('url_9'))

def Website_10(): #Mode 10
    webbrowser.open_new_tab(ADDON.getSetting('url_10'))



#---------------------------------------------------------------------------------------------------
# Function to open addon settings
def Addon_Settings():	
    ADDON.openSettings(sys.argv[0])

#---------------------------------------------------------------------------------------------------
#Get params and clean up into string or integer
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
#---------------------------------------------------------------------------------------------------
#Main addDirectory function - xbmcplugin.addDirectoryItem()
def addDirectoryItem(handle, url, listitem, isFolder):
    xbmcplugin.addDirectoryItem(handle, url, listitem, isFolder)
#---------------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------------
#Function to return the platform XBMC is currently running on.
#Could possibly do away with this and use xbmc.getInfoLabel("System.BuildVersion") in the killxbmc function
def platform():
    if xbmc.getCondVisibility('system.platform.android'):
        return 'android'
    elif xbmc.getCondVisibility('system.platform.linux'):
        return 'linux'
    elif xbmc.getCondVisibility('system.platform.windows'):
        return 'windows'
    elif xbmc.getCondVisibility('system.platform.osx'):
        return 'osx'
    elif xbmc.getCondVisibility('system.platform.atv2'):
        return 'atv2'
    elif xbmc.getCondVisibility('system.platform.ios'):
        return 'ios'

                                                          
#--------------------------------------------------------------------------------------------------------------------------------------------------------
# Addon starts here
params=get_params()
url=None
name=None
buildname=None
updated=None
author=None
version=None
mode=None
iconimage=None
description=None
video=None
link=None
skins=None
videoaddons=None
audioaddons=None
programaddons=None
audioaddons=None
sources=None
local=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        guisettingslink=urllib.unquote_plus(params["guisettingslink"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass
try:
        fanart=urllib.unquote_plus(params["fanart"])
except:
        pass
try:        
        mode=str(params["mode"])
except:
        pass
try:
        link=urllib.unquote_plus(params["link"])
except:
        pass
try:
        skins=urllib.unquote_plus(params["skins"])
except:
        pass
try:
        videoaddons=urllib.unquote_plus(params["videoaddons"])
except:
        pass
try:
        audioaddons=urllib.unquote_plus(params["audioaddons"])
except:
        pass
try:
        programaddons=urllib.unquote_plus(params["programaddons"])
except:
        pass
try:
        pictureaddons=urllib.unquote_plus(params["pictureaddons"])
except:
        pass
try:
        local=urllib.unquote_plus(params["local"])
except:
        pass
try:
        sources=urllib.unquote_plus(params["sources"])
except:
        pass
try:
        adult=urllib.unquote_plus(params["adult"])
except:
        pass
try:
        buildname=urllib.unquote_plus(params["buildname"])
except:
        pass
try:
        updated=urllib.unquote_plus(params["updated"])
except:
        pass
try:
        version=urllib.unquote_plus(params["version"])
except:
        pass
try:
        author=urllib.unquote_plus(params["author"])
except:
        pass
try:        
        description=urllib.unquote_plus(params["description"])
except:
        pass
try:        
        video=urllib.unquote_plus(params["video"])
except:
        pass



        
def OPEN_URL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link


##########################
###DETERMINE PLATFORM#####
##########################
        
def platform():
    if xbmc.getCondVisibility('system.platform.android'):
        return 'android'
    elif xbmc.getCondVisibility('system.platform.linux'):
        return 'linux'
    elif xbmc.getCondVisibility('system.platform.windows'):
        return 'windows'
    elif xbmc.getCondVisibility('system.platform.osx'):
        return 'osx'
    elif xbmc.getCondVisibility('system.platform.atv2'):
        return 'atv2'
    elif xbmc.getCondVisibility('system.platform.ios'):
        return 'ios'

#---------------------------------------------------------------------------------------------------       
        
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


def addDir(name,url,mode,iconimage,fanart,description,version):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+"&description="+urllib.quote_plus(description)+"&version="+urllib.quote_plus(version)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description, "PlayCount": version } )
        liz.setProperty( "Fanart_Image", fanart )
        if mode==90 :
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        else:
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

                      
params=get_params()
url=None
name=None
mode=None
iconimage=None
fanart=None
description=None


try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass
try:        
        mode=int(params["mode"])
except:
        pass
try:        
        fanart=urllib.unquote_plus(params["fanart"])
except:
        pass
try:        
        description=urllib.unquote_plus(params["description"])
except:
        pass
        
        
print str(PATH)+': '+str(VERSION)
print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "IconImage: "+str(iconimage)


def setView(content, viewType):
    # set content type so library shows more views and info
    if content:
        xbmcplugin.setContent(int(sys.argv[1]), content)
    if ADDON.getSetting('auto-view')=='true':
        xbmc.executebuiltin("Container.SetViewMode(%s)" % ADDON.getSetting(viewType) )
        
        
if mode==None or url==None or len(url)<1:
        INDEX()

elif mode==1:
        Website_1()
		
elif mode==2:
        Website_2()

elif mode==3:
        Website_3()

elif mode==4:
        Website_4()

elif mode==5:
        Website_5()

elif mode==6:
        Website_6()
		
elif mode==7:
        Website_7()
		
elif mode==8:
        Website_8()

elif mode==9:
        Website_9()

elif mode==10:
        Website_10()

elif mode==11:
        Addon_Settings()
		
xbmcplugin.endOfDirectory(int(sys.argv[1]))
