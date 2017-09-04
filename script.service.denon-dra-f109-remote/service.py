import time
import xbmc
import xbmcaddon
import denon

__PLUGIN_ID__ = "plugin.audio.denon-dra-f109-remote"
settings = xbmcaddon.Addon(id=__PLUGIN_ID__);
addon_dir = xbmc.translatePath( settings.getAddonInfo('path') )

class XBMCPlayer(xbmc.Player):

    __MIN_STOP_START_INTERVAL = 10
    __RESWITCH_INTERVAL = 3600
    
    __last_switch = 0
    __last_stop = 0
    __has_played = False

    __sources = [["analog", "1"],
           ["analog", "2"],
           ["optical"],
           ["cd"],
           ["net"]]

    def __init__(self, *args):

        self.__last_switch = 0
        self.__last_stop = time.time()
        self.__has_played = False


    def check_idle(self):

        __now = time.time()

        xbmc.log('[Denon] enter check_idle: %s\t%s\t%s' % (str(__now), str(self.__last_stop), str(self.__has_played)), xbmc.LOGDEBUG)
        
        __turn_off_on_idle = 60 * int(
            settings.getSetting("turn_off_on_idle"))

        if __turn_off_on_idle == 0 or self.isPlaying() \
                or not self.__has_played:
            return

        if self.__last_stop + __turn_off_on_idle > __now:
            return

        self.__send_to_denon(["off"])

        self.__last_switch = 0
        self.__last_stop = __now
        self.__has_played = False
        
        xbmc.log('[Denon] exit check_idle: %s\t%s\t%s' % (str(__now), str(self.__last_stop), str(self.__has_played)), xbmc.LOGDEBUG)


    def __is_navigation_event(self):
        return time.time() < self.__last_stop + self.__MIN_STOP_START_INTERVAL


    def __is_switch_fresh(self):
        return time.time() < self.__last_switch + self.__RESWITCH_INTERVAL


    def onPlayBackStarted(self):

        __now = time.time()

        xbmc.log('[Denon] enter onPlayBackStarted: %s\t%s\t%s' % (str(__now), str(self.__last_stop), str(self.__has_played)), xbmc.LOGDEBUG)

        if self.__is_navigation_event():
            self.__last_switch = __now
            return

        if self.__is_switch_fresh():
            return

        self.__send_to_denon(self.__sources[int(
            settings.getSetting("kodi_input_source"))])

        self.__last_switch = __now
        self.__has_played = True

        xbmc.log('[Denon] exit onPlayBackStarted: %s\t%s\t%s' % (str(__now), str(self.__last_stop), str(self.__has_played)), xbmc.LOGDEBUG)


    def onPlayBackStopped(self):

        __now = time.time()

        xbmc.log('[Denon] enter onPlayBackStopped: %s\t%s\t%s' % (str(__now), str(self.__last_stop), str(self.__has_played)), xbmc.LOGDEBUG)

        self.__last_switch = 0
        self.__last_stop = __now
        self.__has_played = True        

        xbmc.log('[Denon] exit onPlayBackStopped: %s\t%s\t%s' % (str(__now), str(self.__last_stop), str(self.__has_played)), xbmc.LOGDEBUG)


    def onPlayBackEnded(self):

        __now = time.time()

        xbmc.log('[Denon] enter onPlayBackEnded: %s\t%s\t%s' % (str(__now), str(self.__last_stop), str(self.__has_played)), xbmc.LOGDEBUG)

        self.__last_switch = 0
        self.__last_stop = __now
        self.__has_played = True        

        if settings.getSetting("turn_off_on_end") == "true":
            self.__send_to_denon(["off"])

        xbmc.log('[Denon] exit onPlayBackEnded: %s\t%s\t%s' % (str(__now), str(self.__last_stop), str(self.__has_played)), xbmc.LOGDEBUG)


    def __send_to_denon(self, send_params):

        params = [settings.getSetting("device")]
        params += send_params

        xbmc.executebuiltin("Notification(Send to Denon, " 
                    + " ".join(send_params) 
                    + ", 5000, " + addon_dir + "/icon.png)")

        denon.sendto_denon(params)


if __name__ == "__main__" \
        and settings.getSetting("auto_kodi") == "true":

    xbmc.log('[Denon] Service started', xbmc.LOGNOTICE)

    monitor = xbmc.Monitor()
    player = XBMCPlayer()
    while not monitor.abortRequested():
        if monitor.waitForAbort(10):
            break

        player.check_idle()
