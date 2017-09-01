import time
import xbmc
import xbmcaddon
import denon

__PLUGIN_ID__ = "plugin.audio.denon-dra-f109-remote"
settings = xbmcaddon.Addon(id=__PLUGIN_ID__);
addon_dir = xbmc.translatePath( settings.getAddonInfo('path') )

class XBMCPlayer(xbmc.Player):
    
    switched = False
    
    def __init__(self, *args):
        pass

    
    def onPlayBackStarted(self):
        
        if self.switched:
            return
                
        sources = [["analog", "1"],
                   ["analog", "2"],
                   ["optical"], 
                   ["cd"],
                   ["net"]]
        
        send = sources[int(
            settings.getSetting("kodi_input_source"))]
        self.__send_to_denon(send)
        self.switched = True


    def onPlayBackEnded(self):
        self.switched = False
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
    monitor = xbmc.Monitor()
    player = XBMCPlayer()
    while not monitor.abortRequested():
        if monitor.waitForAbort(10):
            break