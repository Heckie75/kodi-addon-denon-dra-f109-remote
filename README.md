# kodi-addon-denon-dra-f109-remote
Kodi addon which allows you to control your stereo receiver [Denon DRA-F109](https://www.denon.de/de/product/compactsystem/mini/draf109dab) directly in Kodi. 

After installation of this plugin and connecting your receiver you can set input source, play radio presets or control volume in Kodi. 

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

There you should see the addon called "Denon DRA-F109 Remote" which is disabled by default. Open addon's dialog and activate it.

After you have activated the addon you can click on the "Configure" button in the same dialog. It is required to set the correct serial input device. By default it is `/dev/ttyUSB0`. You must set it to your serial device which is connected to the denon receiver:

<img src="plugin.audio.denon-dra-f109-remote/resources/assets/screen_settings_01_device.png?raw=true">

Now you can leave the settings dialog and go back to Kodi's home screens. In your "music > addons" section there should be a new entry called "Denon DRA-F109 Remote". After you click on it you should see a simular screen as shown below.

<img src="plugin.audio.denon-dra-f109-remote/resources/assets/screen_01_overview.png?raw=true">

If the serial device is not available then you see a "no connection" screen instead:
<img src="plugin.audio.denon-dra-f109-remote/resources/assets/screen_no_connection.png?raw=true">

In this case repeat and check the installation instructions.

## Features in practice

### Configure input sources on overview page
You first step should be to configure the input sources that you would like to display on the overview page. In order to do this go back to addon's configuration menu and select the tab "Input sources":

<img src="plugin.audio.denon-dra-f109-remote/resources/assets/screen_settings_02_sources.png?raw=true">

In the first section called "Kodi" you can define if the addon should display an extra (logical) input source for Kodi. By setting "Kodi's input source" you specify how your Kodi-PC / Raspberry is connect to the stereo receiver. Physical input sources of your Denon receiver are: "Analog 1", "Analog 2", "Optical", "CD" or "Network". I am lucky about my sound card which has an optical output.

The next section is about "Radio sources". Here you can define if "FM Radio" and "Digital Radio (DAB)" is displayed as input source. By activating radio presets there will be a folder which contains all radio presets. We will come to it later. Last but not least you can activating the "Tune" menu. In this menu you will find actions in order to zap the radio presets but also in order to switch between stereo/mono mode. 

In section "Physical input sources" you can diable all input sources that are not connected to any device. Take a look at the "Input labels" configuration tab. Here you can assign meaningful labels to your input source, e.g. "TV" instead of "Analog 1":

<img src="plugin.audio.denon-dra-f109-remote/resources/assets/screen_settings_03_labels?raw=true">


