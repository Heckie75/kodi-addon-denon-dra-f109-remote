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
    
    __sources = [["analog", "1"],
           ["analog", "2"],
           ["optical"],
           ["cd"],
           ["net"]]


    def __init__(self, *args):

        self.__set_has_played(False)
        self.__set_last_switch("")
        self.__set_last_stop(time.localtime())


    def check_idle(self):

        __now = time.time()
        __turn_off_on_idle = 60 * int(
            settings.getSetting("turn_off_on_idle"))

        if __turn_off_on_idle == 0 or self.isPlaying() \
                or not self.__get_has_played():
            return

        if self.__get_last_stop() + __turn_off_on_idle > __now:
            return

        self.__send_to_denon(["off"])

        self.__set_last_switch("")
        self.__set_last_stop(time.localtime())
        self.__set_has_played(False)


    def __set_last_switch(self, v):
        
        if v == "":
            settings.setSetting("smart_last_switch", "")
        else:
            settings.setSetting("smart_last_switch", 
                            time.strftime("%Y-%m-%d %H:%M:%S", v))
    
    
    def __get_last_switch(self):

        s = settings.getSetting("smart_last_switch")

        if s == "":
            return 0
        else:
            return time.mktime(time.strptime(s, "%Y-%m-%d %H:%M:%S"))

    
    def __set_last_stop(self, v):
        
        if v == "":
            settings.setSetting("smart_last_stop", "")        
        else:
            settings.setSetting("smart_last_stop", 
                            time.strftime("%Y-%m-%d %H:%M:%S", v))

    
    def __get_last_stop(self):

        s = settings.getSetting("smart_last_stop")

        if s == "":
            return 0
        else:
            return time.mktime(time.strptime(s, "%Y-%m-%d %H:%M:%S"))
    
    
    def __set_has_played(self, v):
        
        settings.setSetting("smart_has_played", str(v).lower())
    
    
    def __get_has_played(self):
        
        return settings.getSetting("smart_has_played") == "true"


    def __is_navigation_event(self):
        
        return time.time() < self.__get_last_stop() \
            + self.__MIN_STOP_START_INTERVAL


    def __is_switch_fresh(self):
        
        return time.time() < self.__get_last_switch() \
            + self.__RESWITCH_INTERVAL


    def _now(self):

        t_now  = time.localtime()
        td_now = timedelta(hours = t_now.tm_hour,
                         minutes = t_now.tm_min,
                         seconds = t_now.tm_sec)

        return td_now


    def _is_no_kodi_period(self):

        not_before = self._parse_time(settings.getSetting("auto_kodi_not_before"))
        not_after  = self._parse_time(settings.getSetting("auto_kodi_not_after"))
        now        = self._now()

        if not_before < not_after:
            return now < not_before or now > not_after
        else:
            return not_after < now < not_before


    def onPlayBackStarted(self):

	if self._is_no_kodi_period():
            return

        __now = time.time()

        if self.__is_navigation_event():
            self.__set_last_switch(time.localtime())
            return

        if self.__is_switch_fresh():
            return

        self.__send_to_denon(self.__sources[int(
            settings.getSetting("kodi_input_source"))])

        self.__set_last_switch(time.localtime())
        self.__set_has_played(True)


    def onPlayBackStopped(self):

        self.__set_last_switch("")
        self.__set_last_stop(time.localtime())
        self.__set_has_played(True)        


    def onPlayBackEnded(self):

        self.__set_last_switch("")
        self.__set_last_stop(time.localtime())
        self.__set_has_played(True)        

        if settings.getSetting("turn_off_on_end") == "true":
            self.__send_to_denon(["off"])


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
