import xbmc, xbmcaddon, xbmcgui, xbmcplugin,os,base64,sys,xbmcvfs
import shutil
import urllib2,urllib
import re
import extract
import downloader
import time
import plugintools
from addon.common.addon import Addon
from addon.common.net import Net
import zipfile
import ntpath
import webbrowser
import glob




USER_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
addon_id = 'plugin.program.mkiv'
ADDON = xbmcaddon.Addon(id=addon_id)
AddonID='plugin.program.mkiv'
AddonTitle="[COLOR red][B]MK-IV[/B][/COLOR]"
dialog       =  xbmcgui.Dialog()
net = Net()
HOME         =  xbmc.translatePath('special://home/')
dp           =  xbmcgui.DialogProgress()
U = ADDON.getSetting('User')
FANART = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
ICON = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
ART = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id + '/resources/art/'))
VERSION = "1.0.2"
PATH = "MK-IV"            
BASEURL = "http://mkiv.ca"
phoenix = xbmc.translatePath(os.path.join('special://home/addons/','plugin.video.phstreams'))
Tracker   =  xbmc.translatePath(os.path.join('special://home/userdata/addon_data/'+ addon_id , 'Tracker.xml'))
Trackertmp   =  xbmc.translatePath(os.path.join('special://home/userdata/addon_data/'+ addon_id , 'TempTrackerFile.xml'))
mkivupdate = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id + '/resources/', 'update.zip'))
repo = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id + '/resources/', 'repo.zip'))
repo1 = xbmc.translatePath(os.path.join('special://home/addons/' , 'repository.mkiv-1.0'))
updater   =  xbmc.translatePath(os.path.join('special://home/addons/' , 'script.mkiv'))
update   =  xbmc.translatePath(os.path.join('special://home/addons/script.mkiv/' , 'addon.py'))
updatetemp   =  xbmc.translatePath(os.path.join('special://home/addons/script.mkiv/' , 'addontemp.py'))
updatetempzip = xbmc.translatePath(os.path.join('special://home/addons/script.mkiv/' , 'addontemp.zip'))
H = 'http://'
skin         =  xbmc.getSkinDir()
EXCLUDES     = ['script.areswizard','plugin.program.mkiv','JARVIS.xml','script.module.addon.common','autoexec.py','service.xbmc.versioncheck','metadata.tvdb.com','metadata.common.imdb.com']
zip          =  ADDON.getSetting('zip')
ARTPATH      =  '' + os.sep
USERDATA     =  xbmc.translatePath(os.path.join('special://home/userdata',''))
MEDIA        =  xbmc.translatePath(os.path.join('special://home/media',''))
MAIN   =  xbmc.translatePath(os.path.join('special://home',''))
AUTOEXEC     =  xbmc.translatePath(os.path.join(USERDATA,'autoexec.py'))
AUTOEXECBAK  =  xbmc.translatePath(os.path.join(USERDATA,'autoexec_bak.py'))
ADDON_DATA   =  xbmc.translatePath(os.path.join(USERDATA,'addon_data'))
PLAYLISTS    =  xbmc.translatePath(os.path.join(USERDATA,'playlists'))
ADDONS       =  xbmc.translatePath(os.path.join('special://home','addons',''))
GUISETTINGS  =  os.path.join(USERDATA,'guisettings.xml')
GUI          =  xbmc.translatePath(os.path.join(USERDATA,'guisettings.xml'))
INSTALL      =  xbmc.translatePath(os.path.join(USERDATA,'install.xml'))
FAVS         =  xbmc.translatePath(os.path.join(USERDATA,'favourites.xml'))
SOURCE       =  xbmc.translatePath(os.path.join(USERDATA,'sources.xml'))
ADVANCED     =  xbmc.translatePath(os.path.join(USERDATA,'advancedsettings.xml'))
PROFILES     =  xbmc.translatePath(os.path.join(USERDATA,'profiles.xml'))
RSS          =  xbmc.translatePath(os.path.join(USERDATA,'RssFeeds.xml'))
KEYMAPS      =  xbmc.translatePath(os.path.join(USERDATA,'keymaps','keyboard.xml'))
USB          =  xbmc.translatePath(os.path.join(zip))
notifyart    =  xbmc.translatePath(os.path.join(ADDONS,AddonID,'resources/'))
skin         =  xbmc.getSkinDir()
userdatafolder = xbmc.translatePath(os.path.join(ADDON_DATA,AddonID))
urlbase      =  'None'
password          =  ADDON.getSetting('password')
mastercopy   =  ADDON.getSetting('mastercopy')
JARVIS       =  xbmc.translatePath(os.path.join('special://home/','JARVIS.xml'))
KODI16       =  xbmc.translatePath(os.path.join('special://home/userdata/Database/','Addons20.db'))
log_path   =  xbmc.translatePath('special://logpath/')


#Root menu of addon
def INDEX():
    if os.path.exists(repo1):
        pass
    else:
        print '======================================='
        print ADDONS
        print '======================================='
        extract.all(repo,ADDONS)
        time.sleep(2)
        pass
    addDir('[B][COLOR orangered]MK-IV Menu[/COLOR][/B]',BASEURL,100,ART+'mark4.jpg',FANART,'','')
    addDir('[B][COLOR red]BUILDS[/COLOR][/B]',BASEURL,20,ART+'builds.png',FANART,'','')
    addDir('[COLOR blue][B]Maintenance[/B][/COLOR]',BASEURL,30,ART+'maintenance.png',FANART,'','')
    addDir('[B][COLOR red]Add-ons[/COLOR][/B]',BASEURL,22,ART+'addons.png',FANART,'','')
    addDir('[COLOR blue][B]Builders Tools[/B][/COLOR]',BASEURL,31,ART+'builders.png',FANART,'','')
    myplatform = platform()            
    print "Platform: " + str(myplatform)
    if myplatform != 'android':
        addDir('[B][COLOR red]Download Kodi[/COLOR][/B]',BASEURL,21,ART+'kodi.png',FANART,'','')
        addDir('[B][COLOR blue]Download SPMC[/COLOR][/B]',BASEURL,23,ART+'spmc.png',FANART,'','')
	addDir('[COLOR red][B]End User Info[/B][/COLOR]',BASEURL,8,ART+'enduser.jpg',FANART,'','')
	addDir('[B][COLOR blue]Adult Content[/COLOR][/B]',BASEURL,18,ART+'xxx.jpg',FANART,'','')
	addDir('[COLOR blue][B][/B][/COLOR]',BASEURL,0,ART+'',FANART,'','')
        addDir('[B][COLOR orangered]OPEN MK-IV ON YOUR ANDROID TO UNLOCK EVEN MORE[/COLOR][/B]',BASEURL,0,ART+'mark4.jpg',FANART,'','')
    elif myplatform == 'android':
	addDir('[B][COLOR red]Download Kodi 16[/COLOR][/B]',BASEURL,21,ART+'kodi.png',FANART,'','')
        addDir('[B][COLOR blue]Download SPMC 16 (Recommended)[/COLOR][/B]',BASEURL,23,ART+'spmc.png',FANART,'','')
	addDir('[COLOR red][B]End User Info[/B][/COLOR]',BASEURL,8,ART+'enduser.jpg',FANART,'','')
        addDir('[COLOR lime][B]Android Apps[/B][/COLOR]',BASEURL,40,ART+'apkstore.png',FANART,'','')
	addDir('[B][COLOR blue]Adult Content[/COLOR][/B]',BASEURL,18,ART+'xxx.jpg',FANART,'','')
	addDir('[COLOR blue][B][/B][/COLOR]',BASEURL,0,ART+'',FANART,'','')
        addDir('[B][COLOR orangered]OPEN MK-IV ON YOUR PC TO UNLOCK EVEN MORE[/COLOR][/B]',BASEURL,0,ART+'mark4.jpg',FANART,'','')




def BUILDMENU():
	addDir('[COLOR red][B]Canadian Builds[/B][/COLOR]',BASEURL,14,ART+'ca.jpg',FANART,'','')
	addDir('[COLOR blue][B]USA Builds[/B][/COLOR]',BASEURL,15,ART+'us.jpg',FANART,'','')
	addDir('[COLOR red][B]UK Builds[/B][/COLOR]',BASEURL,17,ART+'uk.jpg',FANART,'','')
        addDir('[COLOR yellow][B]ADD YOUR BUILD TO MK-IV[/B][/COLOR]',BASEURL,16,ART+'website.jpg',FANART,'','')




def APKDOWNMENU():
    link = OPEN_URL('http://androidmenu.mkiv.ca').replace('\n','').replace('\r','')
    match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(link)
    for name,url,iconimage,fanart,description in match:
        addDir2(name,url,41,iconimage,fanart,description)



def ADDONMENU():
    link = OPEN_URL('http://addonmenu.mkiv.ca').replace('\n','').replace('\r','')
    match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)').findall(link)
    for name,url,iconimage,fanart,description in match:
        addDir2(name,url,10,iconimage,fanart,description)



def ADULTCONTENT():
    if password == "":
        choice = xbmcgui.Dialog().yesno('MK-IV Wizard', 'This section contains access to adult content', 'To proceed please set a password','', nolabel='Take Me Back',yeslabel='Set Password')
        if choice == 0:
            return
                    
        elif choice == 1:           
            Addon_Settings()
            return
    else:
        vq = _get_keyboard( heading="Please Enter Your Password" )
        if ( not vq ): return False, 0
        title = urllib.quote_plus(vq)
        if title == password:
            pass
        else:
            return
    link = OPEN_URL('http://mkiv.netne.net/Admin/Files/xxx.xml').replace('\n','').replace('\r','')
    match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(link)
    for name,url,iconimage,fanart,description in match:
        addDir2(name,url,10,iconimage,fanart,description)

def MAINTENANCE():
	addDir('[COLOR red][B]FRESH START[/B][/COLOR]','url',6,ART+'freshstart.png',FANART,'','')
	addDir('[COLOR blue][B]DELETE CACHE[/B][/COLOR]','url',4,ART+'deletecache.png',FANART,'','')
	addDir('[COLOR red][B]DELETE THUMBNAILS[/B][/COLOR]','url',11,ART+'deletethumbnails.png',FANART,'','')
	addDir('[COLOR blue][B]DELETE PACKAGES[/B][/COLOR]','url',7,ART+'deletepackages.png',FANART,'','')


def BUILDERS():
        addDir('[COLOR red][B]Convert Physical Paths To Special[/B][/COLOR]',HOME,83,ART+'fixpaths.png',FANART,'','')
	addDir('[COLOR blue][B]Universal Backup[/B][/COLOR]',BASEURL,12,ART+'backup.png',FANART,'','')
	addDir('[COLOR red][B]Test Wizard[/B][/COLOR]',BASEURL,13,ART+'testwizard.png',FANART,'','')
	addDir('[COLOR blue][B]Settings[/B][/COLOR]',BASEURL,51,ART+'settings.png',FANART,'','')
        myplatform = platform()            
        print "Platform: " + str(myplatform)
        if myplatform != 'android':
            addDir('[B][COLOR red]ARES Forum[/COLOR][/B]',BASEURL,77,ART+'ares.jpg',FANART,'','')


def ARESFORUM():
    webbrowser.open_new_tab('https://ares-project.uk/')




def DONATE():
    myplatform = platform()
    print "Platform: " + str(myplatform)
    if myplatform == 'android': 
        xbmcgui.Dialog().ok('Donations','If you would like to donate to CamC and buy him a coffee please visit [COLOR yellow]paypal.me/mkiv[/COLOR]. Thanks in advance for your support!')
    elif myplatform != 'android': 
        webbrowser.open_new_tab('http://paypal.me/mkiv')



def WEBSITE():
    webbrowser.open_new_tab('http://mkiv.ca')


#################################################################################################################################################
#################################################################################################################################################
#################################################################################################################################################


def CANADABUILDS():
####  JARVIS  ####
    addDir('[B][COLOR red]MK-IV[/COLOR][/B]',BASEURL,100,ART+'mark4.jpg',FANART,'','')
    addDir('[B][COLOR blue]AnyTime AnDroid[/COLOR][/B]',BASEURL,101,ART+'atad.jpg',FANART,'','')
    addDir('[B][COLOR red]MagickTV[/COLOR][/B]',BASEURL,103,ART+'magic.png',FANART,'','')





####  ISENGARD  ####








def USABUILDS():
####  JARVIS  ####
    addDir('[B][COLOR red]Elite Kustom Config[/COLOR][/B]',BASEURL,102,ART+'ekc.jpg',FANART,'','')






####  ISENGARD  ####











def UKBUILDS():
####  JARVIS  ####
    addDir('[B][COLOR yellow]Coming Soon...[/COLOR][/B]',BASEURL,20,ART+'uk.jpg',FANART,'','')






####  ISENGARD  ####








##################################################  MK-IV (#0) ####################################################

def MKIVMENU():
        myplatform = platform()            
        print "Platform: " + str(myplatform)
        if myplatform != 'android':
            addDir('[B][COLOR red]Install MK-IV[/COLOR][/B]',BASEURL,200,ART+'mark4.jpg',FANART,'','')
            addDir('[B][COLOR blue]MK-IV Website[/COLOR][/B]',BASEURL,300,ART+'website.jpg',FANART,'','')
            addDir('[B][COLOR red]Donate to MK-IV[/COLOR][/B]',BASEURL,78,ART+'paypal.png',FANART,'','')
        else:
            MKIVWIZARD()

def MKIVWIZARD():
    if not os.path.exists(updater):
        extract.all(mkivupdate,MAIN)
        pass
    extract.all(updatetempzip,updater)
    a=open(updatetemp).read()
    b=a.replace('TEXTLINK', "'http://wizard.mkiv.ca'")
    f = open(updatetemp, mode='w')
    f.write(str(b))
    f.close()
    link = OPEN_URL('http://wizard.mkiv.ca').replace('\n','').replace('\r','')
    match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)".+?ersion="(.+?)"').findall(link)
    for name,url,iconimage,fanart,description,version in match:
        addDir(name,url,90,iconimage,fanart,description,version)


def MKIVWEBSITE():
    webbrowser.open_new_tab('http://mkiv.ca')

def MKIVPAYPAL():
    webbrowser.open_new_tab('https://www.paypal.me/mkiv')


#############################################  ANYTIME ANDROID (#1) ##################################################

def ANYTIMEANDROIDMENU():
        myplatform = platform()            
        print "Platform: " + str(myplatform)
        if myplatform != 'android':
            addDir('[B][COLOR red]Install AnyTime AnDroid[/COLOR][/B]',BASEURL,201,ART+'atad.jpg',FANART,'','')
            addDir('[B][COLOR blue]AnyTime AnDroid Website[/COLOR][/B]',BASEURL,301,ART+'website.jpg',FANART,'','')
            addDir('[B][COLOR red]Donate to AnyTime AnDroid[/COLOR][/B]',BASEURL,401,ART+'paypal.png',FANART,'','')
        else:
            ANYTIMEANDROIDWIZARD()


def ANYTIMEANDROIDWIZARD():
    if not os.path.exists(updater):
        extract.all(mkivupdate,MAIN)
        pass
    extract.all(updatetempzip,updater)
    a=open(updatetemp).read()
    b=a.replace('TEXTLINK', "'http://anytimeandroid.comlu.com/Files/Wizard.xml'")
    f = open(updatetemp, mode='w')
    f.write(str(b))
    f.close()
    link = OPEN_URL('http://archive.org/download/tom902wizard/AresWizard.txt').replace('\n','').replace('\r','')
    match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)".+?ersion="(.+?)"').findall(link)
    for name,url,iconimage,fanart,description,version in match:
        addDir(name,url,90,iconimage,fanart,description,version)


def ANYTIMEANDROIDWEBSITE():
    choice = xbmcgui.Dialog().yesno('MK-IV Wizard', '[CR]You are about to open a web page outside of MK-IV Wizard.', '[CR]We have no control over the content.','Would you like to continue?', nolabel='Take Me Back',yeslabel='Continue')
    if choice == 0:
        return
                    
    elif choice == 1:           
        webbrowser.open_new_tab('http://anytimeandroid.ca')

def ANYTIMEANDROIDPAYPAL():
    choice = xbmcgui.Dialog().yesno('MK-IV Wizard', '[CR]You are about to open a web page outside of MK-IV Wizard.', '[CR]We have no control over the content.','Would you like to continue?', nolabel='Take Me Back',yeslabel='Continue')
    if choice == 0:
        return
                    
    elif choice == 1: 
        webbrowser.open_new_tab('https://www.paypal.me/anytimeandroid')


#####################################################  Elite Kustom Config (#2) ##############################################

def EKCMENU():
        myplatform = platform()            
        print "Platform: " + str(myplatform)
        if myplatform != 'android':
            addDir('[B][COLOR red]Install Elite Kustom Config[/COLOR][/B]',BASEURL,202,ART+'ekc.jpg',FANART,'','')
            addDir('[B][COLOR red]Donate to Elite Kustom Config[/COLOR][/B]',BASEURL,400,ART+'paypal.png',FANART,'','')
        else:
            ECKWIZARD()

def EKCWIZARD():
    if not os.path.exists(updater):
        extract.all(mkivupdate,MAIN)
        pass
    extract.all(updatetempzip,updater)
    a=open(updatetemp).read()
    b=a.replace('TEXTLINK', "'http://mkiv.netne.net/ProgramBuilds/EliteKustomConfig.xml'")
    f = open(updatetemp, mode='w')
    f.write(str(b))
    f.close()
    link = OPEN_URL('http://mkiv.netne.net/ProgramBuilds/EliteKustomConfig.xml').replace('\n','').replace('\r','')
    match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)".+?ersion="(.+?)"').findall(link)
    for name,url,iconimage,fanart,description,version in match:
        addDir(name,url,91,iconimage,fanart,description,version)



def EKCWEBSITE():
    choice = xbmcgui.Dialog().yesno('MK-IV Wizard', '[CR]You are about to open a web page outside of MK-IV Wizard.', '[CR]We have no control over the content.','Would you like to continue?', nolabel='Take Me Back',yeslabel='Continue')
    if choice == 0:
        return
                    
    elif choice == 1: 
        webbrowser.open_new_tab('http://')

def EKCPAYPAL():
    choice = xbmcgui.Dialog().yesno('MK-IV Wizard', '[CR]You are about to open a web page outside of MK-IV Wizard.', '[CR]We have no control over the content.','[CR]Would you like to continue?', nolabel='Take Me Back',yeslabel='Continue')
    if choice == 0:
        return
                    
    elif choice == 1: 
        webbrowser.open_new_tab('https://www.paypal.me/elitekustomconfig')



##################################################  MAGIC (#3) ####################################################

def MAGICMENU():
        myplatform = platform()            
        print "Platform: " + str(myplatform)
        if myplatform != 'android':
            addDir('[B][COLOR red]Install MagickTV[/COLOR][/B]',BASEURL,203,ART+'magic.png',FANART,'','')
            addDir('[B][COLOR blue]MagickTV Website[/COLOR][/B]',BASEURL,303,ART+'website.jpg',FANART,'','')
        else:
            MAGICWIZARD()


def MAGICWIZARD():
    if not os.path.exists(updater):
        extract.all(mkivupdate,MAIN)
        pass
    extract.all(updatetempzip,updater)
    a=open(updatetemp).read()
    b=a.replace('TEXTLINK', "'http://www.magickbox.tv/Build/Wizard.txt'")
    f = open(updatetemp, mode='w')
    f.write(str(b))
    f.close()
    link = OPEN_URL('http://www.magickbox.tv/Build/Wizard.txt').replace('\n','').replace('\r','')
    match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)".+?ersion="(.+?)"').findall(link)
    for name,url,iconimage,fanart,description,version in match:
        addDir(name,url,90,iconimage,fanart,description,version)


def MAGICWEBSITE():
    choice = xbmcgui.Dialog().yesno('MK-IV Wizard', '[CR]You are about to open a web page outside of MK-IV Wizard.', '[CR]We have no control over the content.','Would you like to continue?', nolabel='Take Me Back',yeslabel='Continue')
    if choice == 0:
        return
                    
    elif choice == 1: 
        webbrowser.open_new_tab('http://www.magickbox.tv/')

def MAGICPAYPAL():
    choice = xbmcgui.Dialog().yesno('MK-IV Wizard', '[CR]You are about to open a web page outside of MK-IV Wizard.', '[CR]We have no control over the content.','Would you like to continue?', nolabel='Take Me Back',yeslabel='Continue')
    if choice == 0:
        return
                    
    elif choice == 1: 
        webbrowser.open_new_tab('https://www.paypal.me/')



#################################################################################################################################################
#################################################################################################################################################
#################################################################################################################################################

#---------------------------------------------------------------------------------------------------
#################################
########## APK WIZARD ############
#################################
def APKDOWNWIZ(name,url,description):
    path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
    dp = xbmcgui.DialogProgress()
    dp.create("APK STORE","Downloading your app ",'', 'Please Wait')
    lib=os.path.join(path, name+'.zip')
    try:
       os.remove(lib)
    except:
       pass
    downloader.download(url, lib, dp)
    addonfolder = xbmc.translatePath(os.path.join('sdcard','download'))
    time.sleep(2)
    dp.update(0,"", "Transferring your app to the downloads folder on your device")
    print '======================================='
    print addonfolder
    print '======================================='
    extract.all(lib,addonfolder,dp)
    dialog = xbmcgui.Dialog()
    dialog.ok("DOWNLOAD COMPLETE ", "PLEASE EXIT THE MC AND GO TO YOUR DOWNLOADS FOLDER AND INSTALL YOUR APP")


def line_prepender(filename, line):
    with open(filename, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(line.rstrip('\r\n') + '\n' + content)


def SUBMITREQUEST():
    myplatform = platform()
    print "Platform: " + str(myplatform)
    if myplatform == 'android': 
        xbmcgui.Dialog().ok('Add your build to MK-IV','To have your build added here go to [COLOR yellow]http://submit.mkiv.ca[/COLOR] and fill out the form')
    elif myplatform != 'android': 
        webbrowser.open_new_tab('http://submit.mkiv.ca')


        

def KILLWIZARD(name,url,version):
    if  os.path.exists(phoenix):
        choice = xbmcgui.Dialog().yesno('MK-IV Wizard', 'It is recommended that you perform a Fresh Start before installing.', '','', nolabel='SKIP',yeslabel='FRESH START')
        if choice == 0:
            pass
                    
        elif choice == 1:
            FRESHSTART(params)
    else:
        pass
    print '======================================='
    print ADDONS
    print '======================================='
    extract.all(mkivupdate,ADDONS)
    time.sleep(2)
    path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
    dp = xbmcgui.DialogProgress()
    dp.create("[COLOR redorange][B]MK-IV Wizard[/COLOR][/B]","Downloading required files... ",'', 'Please Wait')
    lib=os.path.join(path, name+'.zip')
    try:
       os.remove(lib)
    except:
       pass
    downloader.download(url, lib, dp)
    if  os.path.exists(updater):
        localfile = open(Tracker, mode='w+')
        localfile.write("name=\""+name+"\"\nversion=\""+version+"\"")
        localfile.close()
        time.sleep(2)
        os.remove(update)
        os.rename(updatetemp,update)
        time.sleep(2)
        localfile = open(AUTOEXEC, mode='w+')
        localfile.write('import xbmc\nxbmc.executebuiltin("RunAddon(script.mkiv)")')
        localfile.close()
    else:
        pass
    addonfolder = xbmc.translatePath(os.path.join('special://','home'))
    time.sleep(2)
    dp.update(0,"Downloading required files... [COLOR lime]DONE[/COLOR]", "Extracting and Writing Files")
    print '======================================='
    print addonfolder
    print '======================================='
    extract.all(lib,addonfolder,dp)
    dialog = xbmcgui.Dialog()
    dialog.ok("Your Setup Is Almost Complete...", 'The only way to get the new changes to stick is', 'to force close the MC. Click ok to force the MC to close,', 'DO NOT use the quit/exit options in the MC., If the Force close does not close for some reason please Restart Device or kill task manaully')
    killxbmc()
        
      
        
def killxbmc():
    myplatform = platform()
    print "Platform: " + str(myplatform)
    if myplatform == 'osx': # OSX
        print "############   try osx force close  #################"
        try: os.system('killall -9 XBMC')
        except: pass
        try: os.system('killall -9 Kodi')
        except: pass
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close the MC [COLOR=lime]DO NOT[/COLOR] exit cleanly via the menu.",'')
    elif myplatform == 'linux': #Linux
        print "############   try linux force close  #################"
        try: os.system('killall XBMC')
        except: pass
        try: os.system('killall Kodi')
        except: pass
        try: os.system('killall -9 xbmc.bin')
        except: pass
        try: os.system('killall -9 kodi.bin')
        except: pass
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close the MC [COLOR=lime]DO NOT[/COLOR] exit cleanly via the menu.",'')
    elif myplatform == 'android': # Android  
        print "############   try android force close  #################"
        try: os.system('su am killall org.xbmc.xbmc')
        except: pass
        try: os.system('su am killall org.xbmc.kodi')
        except: pass
        try: os.system('killall kodi')
        except: pass
        try: os.system('su killall kodi')
        except: pass        
        dialog.ok("[COLOR=red][B]PLEASE READ BELOW !!!![/COLOR][/B]", "Your system has been detected as Android, you ", "[COLOR=yellow][B]MUST[/COLOR][/B] force close the MC. [COLOR=red][B]DO NOT PRESS OK[/COLOR][/B]","Pull the power plug on your AndroidTV box now for changes to take effect.")
    elif myplatform == 'windows': # Windows
        print "############   try windows force close  #################"
        try:
            os.system('@ECHO off')
            os.system('tskill XBMC.exe')
        except: pass
        try:
            os.system('@ECHO off')
            os.system('tskill Kodi.exe')
        except: pass
        try:
            os.system('@ECHO off')
            os.system('TASKKILL /im Kodi.exe /f')
        except: pass
        try:
            os.system('@ECHO off')
            os.system('TASKKILL /im XBMC.exe /f')
        except: pass
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close the MC [COLOR=lime]DO NOT[/COLOR] exit cleanly via the menu.","Use task manager and NOT ALT F4")
    else: #ATV
        print "############   try atv force close  #################"
        try: os.system('killall AppleTV')
        except: pass
        print "############   try raspbmc force close  #################" #OSMC / Raspbmc
        try: os.system('sudo initctl stop kodi')
        except: pass
        try: os.system('sudo initctl stop xbmc')
        except: pass
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close the MC [COLOR=lime]DO NOT[/COLOR] exit via the menu.","Your platform could not be detected so just pull the power cable.")    

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





#################################
####### POPUP TEXT BOXES ########
#################################

def TextBoxes(heading,announce):
  class TextBox():
    WINDOW=10147
    CONTROL_LABEL=1
    CONTROL_TEXTBOX=5
    def __init__(self,*args,**kwargs):
      xbmc.executebuiltin("ActivateWindow(%d)" % (self.WINDOW, )) # activate the text viewer window
      self.win=xbmcgui.Window(self.WINDOW) # get window
      xbmc.sleep(500) # give window time to initialize
      self.setControls()
    def setControls(self):
      self.win.getControl(self.CONTROL_LABEL).setLabel(heading) # set heading
      try: f=open(announce); text=f.read()
      except: text=announce
      self.win.getControl(self.CONTROL_TEXTBOX).setText(str(text))
      return
  TextBox()

def TEXTBOX():
    TextBoxes('[B][COLOR blue]A message from Team Kodi[/COLOR][/B]', '[COLOR blue]   The official Kodi version does not contain any content what so ever. This means that you\nshould provide your own content from a local or remote storage location, DVD, Blu-Ray or any other media carrier that you own. \n[CR]   Additionally Kodi allows you to install third-party plugins that may provide access to content that is freely available on the official content provider website. \n[CR]   The watching or listening of illegal or pirated content which would otherwise need to be paid for is not endorsed or approved by Team Kodi. \n[CR][COLOR yellow]   For more information please go to www.kodi.tv[/COLOR][/COLOR]                                                                                                                                                                                                                                           [COLOR deepskyblue][/COLOR]                                                                                                                                                                                  \n***Neither this addon nor its developer or contents have any affiliation what so ever with Team Kodi, the XBMC Foundation or any of its/their affiliates in any way.***')

    
##########################
####### Kodi Menu ########
##########################   

def KODI():
    myplatform = platform()
    print "Platform: " + str(myplatform)
    if myplatform == 'android': 
        choice = xbmcgui.Dialog().yesno('Select your Processor Architecture', 'Choose which type of processor your device has to continue', '', '(If unsure try ARM first)', nolabel='x86',yeslabel='ARM')
        if choice == 0:
            APKDOWNWIZ('kodix86','http://kodix86.mkiv.ca','Kodi')
        elif choice == 1:
            APKDOWNWIZ('kodiarm','http://kodiarm.mkiv.ca','Kodi')
    elif myplatform != 'android': 
        webbrowser.open_new_tab('https://kodi.tv/download/')

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


#Simple shortcut to create a notification
def Notify(title,message,times,icon):
    icon = notifyart+icon
    xbmc.executebuiltin("XBMC.Notification("+title+","+message+","+times+","+icon+")")

#---------------------------------------------------------------------------------------------------
#Function to archive a single file
def ARCHIVE_SINGLE(source,destination,filestructure):
    zf = zipfile.ZipFile(destination, mode='w')
    zf.write(source, filestructure, zipfile.ZIP_DEFLATED) #Copy guisettings.xml
    zf.close()
#---------------------------------------------------------------------------------------------------
#Convert physical paths to special paths
def FIX_SPECIAL(url):
    dp.create("[COLOR red][B]MK-IV[/B][/COLOR]","Renaming paths...",'', 'Please Wait')
    for root, dirs, files in os.walk(url):  #Search all xml and script.skinshortcuts files and replace physical with special
        for file in files:
            if file.endswith(".xml"):
                 dp.update(0,"Fixing",file, 'Please Wait')
                 a=open((os.path.join(root, file))).read()
                 b=a.replace(USERDATA, 'special://home/userdata/').replace(ADDONS,'special://home/addons/')
                 f = open((os.path.join(root, file)), mode='w')
                 f.write(str(b))
                 f.close()
    for root, dirs, files in os.walk(url):
        for file in files: 
            if file.endswith(".hash"):
                     dp.update(0,"Fixing",file, 'Please Wait')
                     a=open((os.path.join(root, file))).read()
                     b=a.replace(USERDATA, 'special://home/userdata/').replace(ADDONS,'special://home/addons/')
                     f = open((os.path.join(root, file)), mode='w')
                     f.write(str(b))
                     f.close()
    for root, dirs, files in os.walk(url):
        for file in files: 
            if file.endswith(".properties"):
                         dp.update(0,"Fixing",file, 'Please Wait')
                         a=open((os.path.join(root, file))).read()
                         b=a.replace(USERDATA, 'special://home/userdata/').replace(ADDONS,'special://home/addons/')
                         f = open((os.path.join(root, file)), mode='w')
                         f.write(str(b))
                         f.close()

#-----------------------------------------------------------------------------------------------------
#Function to read the contents of a URL
def OPEN_URL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link


#---------------------------------------------------------------------------------------------------
# Function to open addon settings
def Addon_Settings():	
    ADDON.openSettings(sys.argv[0])


#---------------------------------------------------------------------------------------------------
#Get keyboard
def _get_keyboard( default="", heading="", hidden=False ):
    """ shows a keyboard and returns a value """
    keyboard = xbmc.Keyboard( default, heading, hidden )
    keyboard.doModal()
    if ( keyboard.isConfirmed() ):
        return unicode( keyboard.getText(), "utf-8" )
    return default


#---------------------------------------------------------------------------------------------------
#Function to delete the userdata/addon_data folder
def DeleteThumbnails(url):
    print '############################################################       DELETING THUMBNAILS             ###############################################################'
    Thumbnail_cache_path = xbmc.translatePath(os.path.join('special://home/userdata/Thumbnails', ''))
    try:    
        for root, dirs, files in os.walk(Thumbnail_cache_path):
            file_count = 0
            file_count += len(files)
        # Count files and give option to delete
            if file_count > 0:

                            
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))
    except: 
        dialog = xbmcgui.Dialog()
        dialog.ok("[B][COLOR red]MK-IV[/COLOR][/B] [COLOR gold][/COLOR]", "Sorry we were not able to remove Thumbnail Files", "")
      


#---------------------------------------------------------------------------------------------------
#Function to do remove all empty folders after delete       
def REMOVE_EMPTY_FOLDERS():
#initialize the counters
    print"########### Start Removing Empty Folders #########"
    empty_count = 0
    used_count = 0
    for curdir, subdirs, files in os.walk(HOME):
        if len(subdirs) == 0 and len(files) == 0: #check for empty directories. len(files) == 0 may be overkill
            empty_count += 1 #increment empty_count
            os.rmdir(curdir) #delete the directory
            print "successfully removed: "+curdir
        elif len(subdirs) > 0 and len(files) > 0: #check for used directories
            used_count += 1 #increment used_count


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
#Add a standard directory for the builds. Essentially the same as above but grabs unique artwork from previous call
def addBuildDir(name,url,mode,iconimage,fanart,video,description,skins,guisettingslink):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+"&video="+urllib.quote_plus(video)+"&description="+urllib.quote_plus(description)+"&skins="+urllib.quote_plus(skins)+"&guisettingslink="+urllib.quote_plus(guisettingslink)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
        liz.setProperty( "Fanart_Image", fanart )
        liz.setProperty( "Build.Video", video )
        if (mode==None) or (mode=='restore_option') or (mode=='backup_option') or (mode=='cb_root_menu') or (mode=='genres') or (mode=='grab_builds') or (mode=='community_menu') or (mode=='instructions') or (mode=='countries')or (url==None) or (len(url)<1):
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        else:
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok
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



def Delete_Logs():  
    for infile in glob.glob(os.path.join(log_path, 'xbmc_crashlog*.*')):
         File=infile
         print infile
         os.remove(infile)
#--------------------------------------------------------############################################-------------------------------------------
                                                         ############  UNIVERSAL BACKUP  ############
                                                         ############################################
#Create a universal backup - this renames paths to special:// and removes unwanted folders
def UNIVERSAL_BACKUP():
    Delete_Logs()
    guisuccess=1
    CHECK_DOWNLOAD_PATH()
    fullbackuppath = xbmc.translatePath(os.path.join(USB,'Backups'))
    if not os.path.exists(fullbackuppath):
        os.makedirs(fullbackuppath)
    vq = _get_keyboard( heading="Enter a name for this backup" )
    if ( not vq ): return False, 0
    title = urllib.quote_plus(vq)
    backup_zip = xbmc.translatePath(os.path.join(fullbackuppath,title+'.zip'))
    exclude_dirs_full =  ['plugin.program.mkiv']
    exclude_files_full = ["xbmc.log","xbmc.old.log","kodi.log","kodi.old.log","spmc.log","spmc.old.log",'JARVIS.xml','enduser_kill_switch.xml','.DS_Store','.setup_complete','XBMCHelper.conf','Addons19.db','Addons20.db']
    exclude_dirs =  ['plugin.program.mkiv', 'cache', 'system','temp','Thumbnails', "peripheral_data",'library','keymaps']
    exclude_files = ["xbmc.log","xbmc.old.log","kodi.log","kodi.old.log","spmc.log","spmc.old.log","Textures13.db",'.DS_Store','Tracker.xml','.setup_complete','XBMCHelper.conf', 'advancedsettings.xml','Addons19.db','Addons20.db']
    message_header = "Creating Universal Backup"
    message1 = "Archiving..."
    message2 = ""
    message3 = "Please Wait"
    FIX_SPECIAL(HOME)
    ARCHIVE_CB(HOME, backup_zip, message_header, message1, message2, message3, exclude_dirs, exclude_files)  
    dialog.ok("[COLOR green][B]SUCCESS![/B][/COLOR]", 'You Are Now Backed Up.')
    dialog.ok("Backup has been saved to:", '[COLOR yellow]'+backup_zip+'[/COLOR]')


#---------------------------------------------------------------------------------------------------
#Function to restore a zip file 
def CHECK_DOWNLOAD_PATH():
#    if zip == '':
#        dialog.ok('[COLOR=red][B]MK-IV[/B][/COLOR][COLOR gold] Toolbox[/COLOR]','You have not set your ZIP Folder.\nPlease update the addon settings and try again.','','')
#        ADDON.openSettings(sys.argv[0])
    path = xbmc.translatePath(os.path.join(zip,'testCBFolder'))
    if not os.path.exists(zip):
        dialog.ok('[COLOR=red][B]MK-IV[/B][/COLOR][COLOR gold] Toolbox[/COLOR]','The download location you have stored does not exist .\nPlease update the addon settings and try again.','','')        
        xbmc.executebuiltin('Addon.OpenSettings(plugin.program.mkiv)')


#---------------------------------------------------------------------------------------------------
#Zip up tree
def ARCHIVE_CB(sourcefile, destfile, message_header, message1, message2, message3, exclude_dirs, exclude_files):
    zipobj = zipfile.ZipFile(destfile , 'w', zipfile.ZIP_DEFLATED)
    rootlen = len(sourcefile)
    for_progress = []
    ITEM =[]
    dp.create(message_header, message1, message2, message3)
    for base, dirs, files in os.walk(sourcefile):
        for file in files:
            ITEM.append(file)
    N_ITEM =len(ITEM)
    for base, dirs, files in os.walk(sourcefile):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        files[:] = [f for f in files if f not in exclude_files]
        for file in files:
            for_progress.append(file) 
            progress = len(for_progress) / float(N_ITEM) * 100  
            dp.update(int(progress),"Backing up:",'[COLOR lime]%s[/COLOR]'%file, 'Please Wait')
            fn = os.path.join(base, file)
            if not 'temp' in dirs:
                if not 'plugin.program.mkiv' in dirs:
                   import time
                   FORCE= '01/01/1980'
                   FILE_DATE=time.strftime('%d/%m/%Y', time.gmtime(os.path.getmtime(fn)))
                   if FILE_DATE > FORCE:
                       zipobj.write(fn, fn[rootlen:])  
    zipobj.close()
    dp.close()                                                     
  ############################
  #####  END UNI BACKUP  #####
  ############################                                                             
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

        
#################################
####BUILD INSTALL################
#################################

def WIZARD(name,url,version):
    if  os.path.exists(JARVIS):
        pass

    elif os.path.exists(KODI16):
        localfile = open(JARVIS, mode='w+')
        localfile.write('DO NOT DELETE THIS FILE')
        localfile.close() 
        pass

    else:
        KILLWIZARD()

    if skin!= "skin.confluence":
        dialog.ok("[COLOR red][B]"+name+"[/B][/COLOR]",'Switch to the default Confluence skin','and press back to start installing.','')
        xbmc.executebuiltin("ActivateWindow(appearancesettings)")
        return
    else:
            if  os.path.exists(phoenix):
                choice = xbmcgui.Dialog().yesno('MK-IV Wizard', 'It is recommended that you perform a Fresh Start before installing.', '','[COLOR lime]If you have just finished installing select "SKIP" then "Quit"[/COLOR]', nolabel='SKIP',yeslabel='FRESH START')
                if choice == 0:
                    pass
                    
                elif choice == 1:
                    FRESHSTART(params)
            else:
                pass
    choice = xbmcgui.Dialog().yesno('Install Wizard', '', '                            [COLOR lime]Select "Apply Changes" to begin[/COLOR]','[CR]', nolabel='Quit',yeslabel='Apply Changes')
    if choice == 0:
        sys.exit()
        time.sleep(1)
    elif choice == 1:
        pass
    if  os.path.exists(updater):
        localfile = open(Tracker, mode='w')
        time.sleep(2)
        localfile.write("name=\""+name+"\"\nversion=\""+version+"\"")
        localfile.close()
        time.sleep(2)
        os.remove(update)
        os.rename(updatetemp,update)
        time.sleep(2)
        localfile = open(AUTOEXEC, mode='w')
        time.sleep(2)
        localfile.write('import xbmc\nxbmc.executebuiltin("RunAddon(script.mkiv)")')
        localfile.close()
        pass
    else:
        pass
    path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
    dp = xbmcgui.DialogProgress()        
    dp.create("[COLOR redorange][B]MK-IV Wizard[/COLOR][/B]","Downloading required files... ",'', 'Please Wait')
    lib=os.path.join(path, name+'.zip')
    try:
       os.remove(lib)
    except:
       pass
    downloader.download(url, lib, dp)
    addonfolder = xbmc.translatePath(os.path.join('special://','home'))
    time.sleep(2)
    dp.update(0,"Downloading required files...[COLOR lime]DONE[/COLOR]", "Extracting")
    print '======================================='
    print addonfolder
    print '======================================='
    extract.all(lib,addonfolder,dp)
    time.sleep(2)
    FIX_SPECIAL(url)
    time.sleep(2)
    xbmc.executebuiltin('UpdateLocalAddons')
    time.sleep(2)
    xbmc.executebuiltin('ReloadSkin()')
    time.sleep(1)
    xbmc.executebuiltin('RefreshRSS')
    time.sleep(1)
    DeletePackages(url)
    dialog.ok('[COLOR redorange]Changes Applied[/COLOR]','Change your skin now to enjoy your new setup!')
    xbmc.executebuiltin("ActivateWindow(appearancesettings)")    
    time.sleep(2)
    sys.exit()


def TESTWIZARDMENU():
    link = OPEN_URL2('').replace('\n','').replace('\r','')
    match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)".+?ersion="(.+?)"').findall(link)
    for name,url,iconimage,fanart,description in match:
        addDir(name,url,90,iconimage,fanart,description,version)
    setView('movies', 'MAIN')


def OPEN_URL2(url):
#######Open Keyboard to Input Text File URL############
    vq = _get_keyboard( default="https://archive.org/download/" , heading="[COLOR lime]Enter Your Wizard.txt URL[/COLOR]" )
    if ( not vq ): return False, 0
    title = urllib.unquote_plus(vq)
#######Fetch and Read Text File#########
    req = urllib2.Request(title)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link


#################################
###ADDONS INSTALL################
#################################
    
def ADDONWIZ(name,url,description):
    path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
    dp = xbmcgui.DialogProgress()
    dp.create("[B][COLOR red]MK-IV[/COLOR][/B] [COLOR gold][/COLOR]","Downloading ",'', 'Please Wait')
    lib=os.path.join(path, name+'.zip')
    try:
       os.remove(lib)
    except:
       pass
    downloader.download(url, lib, dp)
    addonfolder = xbmc.translatePath(os.path.join('special://','home'))
    time.sleep(2)
    dp.update(0,"", "Extracting Zip Please Wait")
    print '======================================='
    print addonfolder
    print '======================================='
    extract.all(lib,addonfolder,dp)
    xbmc.executebuiltin('UpdateLocalAddons')
    dialog = xbmcgui.Dialog()
    dialog.ok("[B][COLOR red]MK-IV[/COLOR][/B] [COLOR gold][/COLOR]", "Add-on Successfully Installed","")

################################
###DELETE PACKAGES##############
####THANKS GUYS @ XUNITY########

def DeletePackages(url):
    print '############################################################       DELETING PACKAGES             ###############################################################'
    packages_cache_path = xbmc.translatePath(os.path.join('special://home/addons/packages', ''))
    try:    
        for root, dirs, files in os.walk(packages_cache_path):
            file_count = 0
            file_count += len(files)
            
        # Count files and give option to delete
            if file_count > 0:
    
                dialog = xbmcgui.Dialog()
                if dialog.yesno("Delete Package Cache Files", str(file_count) + " files found", "Do you want to delete them?"):
                            
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))
                    dialog = xbmcgui.Dialog()
                    dialog.ok("[B][COLOR red]MK-IV[/COLOR][/B] [COLOR gold][/COLOR]", "Packages Successfuly Removed", "")
                    
    except: 
        dialog = xbmcgui.Dialog()
        dialog.ok("[B][COLOR red]MK-IV[/COLOR][/B] [COLOR gold][/COLOR]", "Sorry we were not able to remove Package Files", "")
    


#################################
###DELETE CACHE##################
####THANKS GUYS @ XUNITY########
	
def deletecachefiles(url):
    print '############################################################       DELETING STANDARD CACHE             ###############################################################'
    xbmc_cache_path = os.path.join(xbmc.translatePath('special://home/'), 'cache')
    if os.path.exists(xbmc_cache_path)==True:    
        for root, dirs, files in os.walk(xbmc_cache_path):
            file_count = 0
            file_count += len(files)
        
        # Count files and give option to delete
            if file_count > 0:
    
                dialog = xbmcgui.Dialog()
                if dialog.yesno("Delete Cache Files", str(file_count) + " files found", "Do you want to delete them?"):
                
                    for f in files:
                        try:
                            os.unlink(os.path.join(root, f))
                        except:
                            pass
                    for d in dirs:
                        try:
                            shutil.rmtree(os.path.join(root, d))
                        except:
                            pass
                        
            else:
                pass
    if xbmc.getCondVisibility('system.platform.ATV2'):
        atv2_cache_a = os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'Other')
        
        for root, dirs, files in os.walk(atv2_cache_a):
            file_count = 0
            file_count += len(files)
        
            if file_count > 0:

                dialog = xbmcgui.Dialog()
                if dialog.yesno("Delete ATV2 Cache Files", str(file_count) + " files found in 'Other'", "Do you want to delete them?"):
                
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))
                        
            else:
                pass
        atv2_cache_b = os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'LocalAndRental')
        
        for root, dirs, files in os.walk(atv2_cache_b):
            file_count = 0
            file_count += len(files)
        
            if file_count > 0:

                dialog = xbmcgui.Dialog()
                if dialog.yesno("Delete ATV2 Cache Files", str(file_count) + " files found in 'LocalAndRental'", "Do you want to delete them?"):
                
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))
                        
            else:
                pass
              # Set path to Cydia Archives cache files
                             

    # Set path to What th Furk cache files
    wtf_cache_path = os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.whatthefurk/cache'), '')
    if os.path.exists(wtf_cache_path)==True:    
        for root, dirs, files in os.walk(wtf_cache_path):
            file_count = 0
            file_count += len(files)
        
        # Count files and give option to delete
            if file_count > 0:
    
                dialog = xbmcgui.Dialog()
                if dialog.yesno("Delete WTF Cache Files", str(file_count) + " files found", "Do you want to delete them?"):
                
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))
                        
            else:
                pass
                
                # Set path to 4oD cache files
    channel4_cache_path= os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.4od/cache'), '')
    if os.path.exists(channel4_cache_path)==True:    
        for root, dirs, files in os.walk(channel4_cache_path):
            file_count = 0
            file_count += len(files)
        
        # Count files and give option to delete
            if file_count > 0:
    
                dialog = xbmcgui.Dialog()
                if dialog.yesno("Delete 4oD Cache Files", str(file_count) + " files found", "Do you want to delete them?"):
                
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))
                        
            else:
                pass
                
                # Set path to BBC iPlayer cache files
    iplayer_cache_path= os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.iplayer/iplayer_http_cache'), '')
    if os.path.exists(iplayer_cache_path)==True:    
        for root, dirs, files in os.walk(iplayer_cache_path):
            file_count = 0
            file_count += len(files)
        
        # Count files and give option to delete
            if file_count > 0:
    
                dialog = xbmcgui.Dialog()
                if dialog.yesno("Delete BBC iPlayer Cache Files", str(file_count) + " files found", "Do you want to delete them?"):
                
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))
                        
            else:
                pass
                
                
                # Set path to Simple Downloader cache files
    downloader_cache_path = os.path.join(xbmc.translatePath('special://profile/addon_data/script.module.simple.downloader'), '')
    if os.path.exists(downloader_cache_path)==True:    
        for root, dirs, files in os.walk(downloader_cache_path):
            file_count = 0
            file_count += len(files)
        
        # Count files and give option to delete
            if file_count > 0:
    
                dialog = xbmcgui.Dialog()
                if dialog.yesno("Delete Simple Downloader Cache Files", str(file_count) + " files found", "Do you want to delete them?"):
                
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))
                        
            else:
                pass
                
                # Set path to ITV cache files
    itv_cache_path = os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.itv/Images'), '')
    if os.path.exists(itv_cache_path)==True:    
        for root, dirs, files in os.walk(itv_cache_path):
            file_count = 0
            file_count += len(files)
        
        # Count files and give option to delete
            if file_count > 0:
    
                dialog = xbmcgui.Dialog()
                if dialog.yesno("Delete ITV Cache Files", str(file_count) + " files found", "Do you want to delete them?"):
                
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))
                        
            else:
                pass
				
                # Set path to temp cache files
    temp_cache_path = os.path.join(xbmc.translatePath('special://home/temp'), '')
    if os.path.exists(temp_cache_path)==True:    
        for root, dirs, files in os.walk(temp_cache_path):
            file_count = 0
            file_count += len(files)
        
        # Count files and give option to delete
            if file_count > 0:
    
                dialog = xbmcgui.Dialog()
                if dialog.yesno("Delete TEMP dir Cache Files", str(file_count) + " files found", "Do you want to delete them?"):
                
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))
                        
            else:
                pass
				

    dialog = xbmcgui.Dialog()
    dialog.ok("[B][COLOR red]MK-IV[/COLOR][/B] [COLOR gold][/COLOR]", " All Cache Files Removed", "")
 
        
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
    
############################
###FRESH START##############
############################

def FRESHSTART(params):
    choice2 = xbmcgui.Dialog().yesno("[COLOR=red]Are You Sure?[/COLOR]", 'Last chance...', '', 'All addons and settings will be deleted!', yeslabel='[COLOR lime]Yes, Fresh Start[/COLOR]',nolabel='[COLOR red]No[/COLOR]')
    if choice2 == 0:
        return
    elif choice2 == 1:
        dp.create("[COLOR=red][B]MK-IV[/B][/COLOR][COLOR=gold] [/COLOR]","Deleting contents",'[COLOR lime]Screen may turn blackfor a moment, this is normal[/COLOR]', 'Please Wait')
        try:
            for root, dirs, files in os.walk(HOME,topdown=True):
                dirs[:] = [d for d in dirs if d not in EXCLUDES]
                for name in files:
                    try:
                        os.remove(os.path.join(root,name))
                        os.rmdir(os.path.join(root,name))
                    except: pass
                        
                for name in dirs:
                    try: os.rmdir(os.path.join(root,name)); os.rmdir(root)
                    except: pass
        except: pass
    REMOVE_EMPTY_FOLDERS()
    REMOVE_EMPTY_FOLDERS()
    REMOVE_EMPTY_FOLDERS()
    REMOVE_EMPTY_FOLDERS()
    REMOVE_EMPTY_FOLDERS()
    REMOVE_EMPTY_FOLDERS()
    REMOVE_EMPTY_FOLDERS()
    xbmc.executebuiltin('ReloadSkin()')
    time.sleep(2)
    dialog.ok('[COLOR=red][B]MK-IV[/B][/COLOR][COLOR=gold][/COLOR]','Fresh Start Successful','','The MC will now close')
    xbmc.executebuiltin('Quit')

################################
###    FIX REPOS&ADDONS      ###
################################
#---------------------------------------------------------------------------------------------------
#Function to do remove all empty folders after delete       
def REMOVE_EMPTY_FOLDERS():
#initialize the counters
    print"########### Start Removing Empty Folders #########"
    empty_count = 0
    used_count = 0
    for curdir, subdirs, files in os.walk(HOME):
        if len(subdirs) == 0 and len(files) == 0: #check for empty directories. len(files) == 0 may be overkill
            empty_count += 1 #increment empty_count
            os.rmdir(curdir) #delete the directory
            print "successfully removed: "+curdir
        elif len(subdirs) > 0 and len(files) > 0: #check for used directories
            used_count += 1 #increment used_count
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

N = base64.decodestring('')
T = base64.decodestring('L2FkZG9ucy50eHQ=')
B = base64.decodestring('')
F = base64.decodestring('')

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


def addDir2(name,url,mode,iconimage,fanart,description):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+"&description="+urllib.quote_plus(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
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

elif mode==20:
        BUILDMENU()
		
elif mode==21:
        KODI()

elif mode==22:
        ADDONMENU()

elif mode==23:
        SPMC()

elif mode==31:
        BUILDERS()

elif mode==30:
        MAINTENANCE()
		
elif mode==4:
        deletecachefiles(url)
		
elif mode==90:
        WIZARD(name,url,version)

elif mode==91:
        KILLWIZARD(name,url,version)

elif mode==18:
        ADULTCONTENT()

elif mode==17:
        UKBUILDS()

elif mode==16:
        SUBMITREQUEST()

elif mode==15:
        USABUILDS()

elif mode==14:
        CANADABUILDS()

elif mode==13:
        TESTWIZARDMENU()

elif mode==12:
        UNIVERSAL_BACKUP()

elif mode==11:
       DeleteThumbnails(url)

elif mode==6:        
	FRESHSTART(params)
	
elif mode==7:
       DeletePackages(url)

elif mode==8:
       TEXTBOX()
       
elif mode==9:
       donate()
		
elif mode==10:
        ADDONWIZ(name,url,description)

elif mode==83:
        print "############   FIX SPECIAL PATHS   #################"
        FIX_SPECIAL(url)
				
elif mode==51:
        print "############   Open Addon Settings   #################"
        Addon_Settings()
		
elif mode==72:
        print "############   Open Local GUI dialog   #################"
        LocalGUIDialog()

elif mode==76:
        WEBSITE()

elif mode==77:
        ARESFORUM()

elif mode==78:
        DONATE()
		
elif mode==40:
        APKDOWNMENU()
		
elif mode==41:
        APKDOWNWIZ(name,url,description)

##################################################  MODES FOR CommBuilds ##########################################################
###########  MENU        = 100-199
###########  WIZARD URL  = 200-299  #############
###########  WEBSITE URL = 300-399  #############
###########  PAYPAL URL  = 400-499  #############


######  MK-IV  ######

elif mode==100:
        MKIVMENU()

elif mode==200:
        MKIVWIZARD()


elif mode==300:
        MKIVWEBSITE()


elif mode==400:
        MKIVPAYPAL()

elif mode==500:
        MKIVUPDATE()

######  ANYTIME ANDROID    ######

elif mode==101:
        ANYTIMEANDROIDMENU()

elif mode==201:
        ANYTIMEANDROIDWIZARD()

elif mode==301:
        ANYTIMEANDROIDWEBSITE()

elif mode==401:
        ANYTIMEANDROIDPAYPAL()

######  Elite Custom Config  ######


elif mode==102:
        EKCMENU()

elif mode==202:
        EKCWIZARD()

elif mode==302:
        EKCWEBSITE()

elif mode==402:
        EKCPAYPAL()

######  MAGIC  ######


elif mode==103:
        MAGICMENU()

elif mode==203:
        MAGICWIZARD()

elif mode==303:
        MAGICWEBSITE()

elif mode==403:
        MAGICPAYPAL()
		
xbmcplugin.endOfDirectory(int(sys.argv[1]))
