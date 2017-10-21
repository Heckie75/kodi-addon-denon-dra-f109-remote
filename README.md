# kodi-addon-denon-dra-f109-remote
Kodi addon which allows you to control your stereo receiver [Denon DRA-F109](https://www.denon.de/de/product/compactsystem/mini/draf109dab) directly in Kodi. 

After installation of this plugin and connecting your receiver you can set input source, play radio presets or control volume in Kodi. 
<img src="plugin.audio.denon-dra-f109-remote/resources/assets/screen_01_overview.png?raw=true">

## Overview of features:
* Configurable overview page
* Input sources
  * List of input sources (physical devices e.g. "Analog 1", logical devices e.g. "Server")
  * Meaningful names for sources can be given, e.g. "TV" (instead of "Analog 1")
  * Unused input sources can be hidden
  * Special input source for Kodi with auto-select on playback in Kodi
  * Stop Kodi playback on switch to none-kodi input source, e.g. radio
* Radio presets (fm and dab)
  * Station names can be given in Kodi settings
* Volume control
* Sound control
  * increase/decrease bass, treble
  * balance
  * sdirect on/off
  * SDB on/off
* Activate sleep timer of receiver
  * 5 presets with individual periods can be configured in Kodi settings
* Configuration and activation of "every-day"-timer and "once"-timer
* Smart power settings
  * Power off receiver on Kodi playback end
  * Turn off on idle
  * Stop playback on receiver turn off


## Requirements

kodi-addon-denon-dra-f109-remote works only on Linux / Raspberry Pi. It is based on my other Github project [Denon-DRA-F109-Remote](/Heckie75/Denon-DRA-F109-Remote/)

From a technical point of view the setup is based on a UART serial interface (e.g. USB -> TTL RS232 5V PL2303 HX Adapter) which is wired to the receiver's remote connector. See also ["Hacking Denon DRA-F109 remote connector" by Kamil Figiela](https://kfigiela.github.io/2014/06/15/denon-remote-connector/)

Before you can use this plugin you have to manually install [PySerial](https://pythonhosted.org/pyserial/) which should be available in standard repositories. PySerial can be installed like this:
```
apt install python-serial
```

## Install kodi plugin
First of all download the plugin archive file, i.e. [kodi-addon-denon-dra-f109-remote.tgz](/kodi-addon-denon-dra-f109-remote.tgz)

You must extract this archive in the Kodi plugin folder
```
# change to kodi's addon directory
$ cd ~/.kodi/addons/

# extract plugin
$ tar xzf ~/Downloads/kodi-addon-denon-dra-f109-remote.tgz 
```

After you have restarted Kodi you must activate the plugin explicitly. 
1. Start Kodi
2. Go to "Addons" menu
3. Select "User addons"
4. Select "Music addons"

There you should see the addon called "Denon DRA-F109" which is disabled by default. Open addon's dialog and activate it.

After you have activated the addon you can click on the "Configure" button in the same dialog. It is required to set the correct serial input device. By default it is `/dev/ttyUSB0`. You must set it to your serial device which is connected to the denon receiver:

<img src="plugin.audio.denon-dra-f109-remote/resources/assets/screen_settings_01_device.png?raw=true">
