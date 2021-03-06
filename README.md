# kodi-addon-denon-dra-f109-remote
Kodi addon which allows you to control your stereo receiver [Denon DRA-F109](https://www.denon.de/de/product/compactsystem/mini/draf109dab) directly in Kodi. 

After installation of this plugin and connecting your receiver you can remotely control input source, play radio presets or control volume in Kodi. 

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

kodi-addon-denon-dra-f109-remote works only on Linux / Raspberry Pi. It is based on my other Github project [Denon-DRA-F109-Remote](https://github.com/Heckie75/Denon-DRA-F109-Remote/)

From a technical point of view the setup is based on a UART serial interface (e.g. USB -> TTL RS232 5V PL2303 HX Adapter or the UART pins of your Raspberry Pi) which is wired to the receiver's remote connector. See also ["Hacking Denon DRA-F109 remote connector" by Kamil Figiela](https://kfigiela.github.io/2014/06/15/denon-remote-connector/)

Before you can use this plugin you have to manually install [PySerial](https://pythonhosted.org/pyserial/) which should be available in standard repositories. PySerial can be installed like this:
```
apt install python-serial
```

## Install kodi plugin
First of all download the plugin archive file, i.e. [kodi-addon-denon-dra-f109-remote.zip](/kodi-addon-denon-dra-f109-remote.zip)

You must extract this archive in the Kodi plugin folder
```
# change to kodi's addon directory
$ cd ~/.kodi/addons/

# extract plugin
$ tar xzf ~/Downloads/kodi-addon-denon-dra-f109-remote.zip
```

After you have restarted Kodi you must activate the plugin explicitly. 
1. Start Kodi
2. Go to "Addons" menu
3. Select "User addons"
4. Select "Service" addons, select "Denon DRA-F109 Remote (autoswitch)" and activate it
5. Go back to "Addons" menu and select "User addons"
6. Select "Music addons"

There you should find the addon called "Denon DRA-F109 Remote" which is disabled by default. Open addon's dialog and activate it.

After you have activated the addon you click the "Configure" button in the same dialog. It is required to set the correct serial input device. By default it is `/dev/ttyUSB0`. In case that you use a Raspberry Pi connected via GPIO UART pins you should set it to `/dev/ttyAMA0`. You must set it to your serial device which is connected to the denon receiver:

<img src="plugin.audio.denon-dra-f109-remote/resources/assets/screen_settings_01_device.png?raw=true">

Now you can leave the settings dialog and go back to Kodi's home screen. In your "music > addons" section there is a new entry called "Denon DRA-F109 Remote". After you have clicked on it you see a simular screen as shown below:

<img src="plugin.audio.denon-dra-f109-remote/resources/assets/screen_01_overview.png?raw=true">

If the serial device is not available then you see a "no connection" screen instead:
<img src="plugin.audio.denon-dra-f109-remote/resources/assets/screen_no_connection.png?raw=true">

In this case repeat and check the installation instructions.

## Features in practice

### Configure input sources on overview page
The first step should be to configure the input sources that you would like to see on the overview page. Go back to addon's configuration menu and select the tab "Input sources":

<img src="plugin.audio.denon-dra-f109-remote/resources/assets/screen_settings_02_sources.png?raw=true">

In the first section called "Kodi" you can define if the addon should display a "logical" input source for Kodi. By setting "Kodi's input source" you specify via which physical input source your Kodi-PC / Raspberry is connected to the Denon receiver. Physical input sources are: "Analog 1", "Analog 2", "Optical", "CD" or "Network". In my case I have connected it via the optical unput source since I have an external USB sound card with s/pdif output signal.

The next section is about "Radio sources". Here you can define if "FM Radio" and "Digital Radio (DAB)" is displayed as input source. By activating radio presets there will be a folder which contains all radio presets. We will come to it later. Last but not least you can activate the "Tune" menu where you can zap radio presets and toggle between stereo/mono mode. 

In section "Physical input sources" you can diable all input sources that are not connected to any device. 

Note: Take also a look at the "Input labels" configuration tab. Here you can assign meaningful labels to your input source, e.g. "TV" instead of "Analog 1":

<img src="plugin.audio.denon-dra-f109-remote/resources/assets/screen_settings_03_labels.png?raw=true">

Back to the "Input sources" tab you see that other input sources are "logical" onces. These are sources that are implemented as services of other Denon devices, e.g. 
* Denon DCD-F109 is the CD player of the F109-set. You can connect an iPOD or other USB devices
* Denon DNP-F109 is the network player of the F109-set. It has several logical sources, i.e. internet radio,  online music services, home music server (DNLA) and also devices connected via USB

*Note:* I don't have other devices of the Denon 109 series. Therefore I haven't tested if it really works. Actually in earlier days I had the DNP-F109 but since for my taste usability and software stability was poor - especially for the money  that I have paid - I decided to buy an Intel NUC N2830 and a sound card with optical output for the less money. Best decision ever since a new hobby was born too!

### Radio presets

Unfortunately the serial interface of the Denon receiver does not allow to query the names of the radio stations. That's why it is required to enter the names manually in Kode. Take a look at the tab which is called "Radio presets":

<img src="plugin.audio.denon-dra-f109-remote/resources/assets/screen_settings_04_presets.png?raw=true">

Select a preset and press enter in order to give a name. As long as you haven't given a name, which means that it is blank, the entry is hidden in frontend. After you have set up some presets the menu in frontend looks like this:
<img src="plugin.audio.denon-dra-f109-remote/resources/assets/screen_02_presets.png?raw=true">

A click on a preset switches the receiver automatically to input source "Radio" and tunes to the specific preset.

Don't forget to activate the "Radio presets" input source so that it's not hidden.

### Sound settings
In the tab for "Sound settings" you can define if this menu will be displayed or not. 
<img src="plugin.audio.denon-dra-f109-remote/resources/assets/screen_05_sound.png?raw=true">

There are some settings in order to define which volume levels are available in terms of minimal volume, maximal volume and the steps. 
<img src="plugin.audio.denon-dra-f109-remote/resources/assets/screen_settings_05_sound.png?raw=true">

My volume settings start at the level 4 and ends at 20. I have choosen steps of 2 so that there are not so many entries. 

<img src="plugin.audio.denon-dra-f109-remote/resources/assets/screen_07_volume.png?raw=true">

Here you probably would like to ask why there are no "volume up" and "volume down" actions. The answer is easy: The denon serial protocol does not know commands for it. In addition I just send signals to the receiver and don't query the current state. Take a look at my remarks in [kodi-addon-denon-dra-f109-remote.tgz](https://github.com/kodi-addon-denon-dra-f109-remote.tgz).

### Alarm clock and sleep timer
The Denon receiver has it's own alarm clock integrated. Unfortunately the serial protocol does not allow to synchronize the internal clock. Nevertheless, you can setup timers and activate the sleep timer. 

I prefer sleep timers for different situations. That's why you can setup 5 different intervals for the sleep timer. The values are in minutes after the receiver automatically turns off:
<img src="plugin.audio.denon-dra-f109-remote/resources/assets/screen_settings_07_timers.png?raw=true">

After you have configured it the menu looks like this:
<img src="plugin.audio.denon-dra-f109-remote/resources/assets/screen_04_sleep.png?raw=true">

In addition to the sleep timer the Denon receiver has two alarm clocks:
 a) Everyday alarm clock
 b) Onetime alarm clock 

You can configure it as well. It's self explaining ;-)
<img src="plugin.audio.denon-dra-f109-remote/resources/assets/screen_settings_07_timers2.png?raw=true">

After you have configured the timers they are not activated! In order to activate the alarm clock you have to click one of the options in the menu:
<img src="plugin.audio.denon-dra-f109-remote/resources/assets/screen_06_timers.png?raw=true">

### Smart power settings
Let's finalize this manual with my favorite: the "Smart power" settings. 

Maybe you would like that the receiver automatically turns on and switches to "Kodi" after you have started to play something in Kodi. You can do it by activating the "Auto switch to Kodi on playback start" setting. 

<img src="plugin.audio.denon-dra-f109-remote/resources/assets/screen_settings_08_smart.png?raw=true">

But in terms of my equipment and "smart home setup" - I have set up a combined audio device in Linux that feeds speakers in my bedroom via bluetooth too - I don't want that the receiver turns on in the morning when my Kodi timer wakes me up (see my other Kodi plugin [kodi-addon-heckies-timer
](//github.com/Heckie75/kodi-addon-heckies-timer)). Therefore I have defined two settings in order to configure downtimes in the morning and evening. In these periods the addon doesn't tell the receiver to turn on automatically when playback starts. All user explicit commands triggered by the user work, of course. 

There are three other settings which are related to behaviour "on playback end", "on idle" and to combination of stopping playback when receiver has been turned off. 

The first setting is "Turn off on playback end". Actually it should be called "on playlist ends". The addon sends the signal to the receiver in order to turn off after the playlist has been finished. Actually I haven't activated this feauture since the receiver turns off and on very often. 

The next setting is much better since it allows to save our environment. If Kodi isn't playing something and hasn't played something for a certain period the addon sends the signal to turn the receiver off. 

The last one "Stop playback on turn off" does NOT mean that playback in Kodi stops after you have turned of the receiver by pressing its power button! In means that playback in Kodi stops after you have clicked the "Power off" entry of the addon. 

For all these smart settings an internal state machine is required. For debugging reasons the internal states can be seen in the section "internal state", i.e. "last switch", "last stop" and "Kodi has played" (yes/no).

That's it! I hope that you enjoy this addon. Don't hesitate to give me your feedback!
