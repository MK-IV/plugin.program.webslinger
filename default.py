import xbmc, xbmcaddon, xbmcgui, xbmcplugin,os,base64,sys,xbmcvfs
import shutil
import urllib2,urllib
import re
import time
import plugintools
from addon.common.addon import Addon
from addon.common.net import Net
import ntpath
import webbrowser
import glob




USER_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
addon_id = 'plugin.program.webslinger-master'
ADDON = xbmcaddon.Addon(id=addon_id)
AddonID='plugin.program.webslinger-master'
AddonTitle="[COLOR deepskyblue][B]W[/B][/COLOR]eb [COLOR deepskyblue][B]S[/B][/COLOR]linger"
dialog       =  xbmcgui.Dialog()
net = Net()
HOME =  xbmc.translatePath('special://home/')
dp =  xbmcgui.DialogProgress()
U = ADDON.getSetting('User')
FANART = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
ICON = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
ART = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id + '/resources/art/'))
VERSION = "1.0.0"
PATH = "MK-IV"            
BASEURL = "http://mkiv.ca"
H = 'http://'
ARTPATH      =  '' + os.sep
USERDATA     =  xbmc.translatePath(os.path.join('special://home/userdata',''))
MAIN   =  xbmc.translatePath(os.path.join('special://home',''))
ADDON_DATA   =  xbmc.translatePath(os.path.join(USERDATA,'addon_data'))
ADDONS       =  xbmc.translatePath(os.path.join('special://home','addons',''))
notifyart    =  xbmc.translatePath(os.path.join(ADDONS,AddonID,'resources/'))
userdatafolder = xbmc.translatePath(os.path.join(ADDON_DATA,AddonID))
urlbase      =  'None'
Website = 'website.png'
Donate = 'donate.png'
Shop = 'shop.png'
Email = 'email.png'
Forum = 'forum.png'
Repo = 'repo.png'
Facebook = 'facebook.png'
Twitter = 'twitter.png'
Help = 'help.png'
Default = ''

#Root menu of addon
def INDEX():
    if ADDON.getSetting('label_1') == "":
        addDir('Click here to setup [B][COLOR deepskyblue]W[/COLOR][/B]eb [B][COLOR deepskyblue]S[/COLOR][/B]linger',BASEURL,11,ART+('settings.png'),FANART,'','') 
    else   
        addDir(ADDON.getSetting('label_1'),BASEURL,1,ART+ADDON.getSetting('icon_1'),FANART,'','')
    if ADDON.getSetting('label_2') != "":
        addDir(ADDON.getSetting('label_2'),BASEURL,2,ART+ADDON.getSetting('icon_2','.png'),FANART,'','')
    else 
        pass
    if ADDON.getSetting('label_3') != "":
        addDir(ADDON.getSetting('label_3'),BASEURL,3,ART+ADDON.getSetting('icon_3','.png'),FANART,'','')
    else
        pass
    if ADDON.getSetting('label_4') != "":
        addDir(ADDON.getSetting('label_4'),BASEURL,4,ART+ADDON.getSetting('icon_4','.png'),FANART,'','')
    else
        pass
    if ADDON.getSetting('label_5') != "":
        addDir(ADDON.getSetting('label_5'),BASEURL,5,ART+ADDON.getSetting('icon_5'),FANART,'','')
    else
        pass
    if ADDON.getSetting('label_6') != "":
        addDir(ADDON.getSetting('label_6'),BASEURL,6,ART+ADDON.getSetting('icon_6'),FANART,'','')
    else
        pass
    if ADDON.getSetting('label_7') != "":
        addDir(ADDON.getSetting('label_7'),BASEURL,7,ART+ADDON.getSetting('icon_7'),FANART,'','')
    else
        pass
    if ADDON.getSetting('label_8') != "":
        addDir(ADDON.getSetting('label_8'),BASEURL,8,ART+ADDON.getSetting('icon_8'),FANART,'','')
    else
        pass
    if ADDON.getSetting('label_9') != "":
        addDir(ADDON.getSetting('label_9'),BASEURL,9,ART+ADDON.getSetting('icon_9'),FANART,'','')
    else
        pass
    if ADDON.getSetting('label_10') != "":
        addDir(ADDON.getSetting('label_10'),BASEURL,10,ART+ADDON.getSetting('icon_10'),FANART,'','')
    else
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



##########################
####### SPMC Menu ########
########################## 

def SPMC():
    myplatform = platform()
    print "Platform: " + str(myplatform)
    if myplatform == 'android': 
        choice = xbmcgui.Dialog().yesno('Select your Processor Architecture', 'Choose which type of processor your device has to continue', '', '(If unsure try ARM first)', nolabel='x86',yeslabel='ARM')
        if choice == 0:
            APKDOWNWIZ('SPMCx86','http://mkiv.netne.net/Admin/APKs/SPMCx86.zip','SPMC')
        elif choice == 1:
            APKDOWNWIZ('SPMCarm','http://mkiv.netne.net/Admin/APKs/SPMCarm.zip','SPMC')
    elif myplatform != 'android': 
        webbrowser.open_new_tab('http://spmc.semperpax.com/')


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