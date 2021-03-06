import os
import os.path
import sys

import urlparse
import xbmcgui
import xbmcplugin
import xbmcaddon
import denon

__PLUGIN_ID__ = "plugin.audio.denon-dra-f109-remote"

SOURCES = [["analog", "1"],
           ["analog", "2"],
           ["optical"],
           ["cd"],
           ["net"]]

PLUGIN_PASINK = "plugin.audio.pasink"

settings = xbmcaddon.Addon(id=__PLUGIN_ID__);
addon_handle = int(sys.argv[1])
addon_dir = xbmc.translatePath( settings.getAddonInfo('path') )




def _build_alarm():

    sources = ["preset", "optical", "cd", "cdusb",
               "net", "netusb", "analog1", "analog2"]

    everyday_start = settings.getSetting("alarm_everyday_start")
    everyday_end = settings.getSetting("alarm_everyday_end")
    everyday_source = int(settings.getSetting("alarm_everyday_source"))

    if everyday_source == 0:
        everyday_preset = settings.getSetting("alarm_everyday_preset")
    else:
        everyday_preset = ""

    once_start = settings.getSetting("alarm_once_start")
    once_end = settings.getSetting("alarm_once_end")
    once_source = int(settings.getSetting("alarm_once_source"))

    if once_source == 0:
        once_preset = settings.getSetting("alarm_once_preset")
    else:
        once_preset = ""

    entries = [
        {
            "path" : "off",
            "name" : "Off",
            "icon" : "icon_alarm",
            "send" : ["alarm", "off"]
        }
    ]

    if everyday_start != "" and everyday_end != "":
        entries += [
            {
                "path" : "everyday",
                "name" : "Everyday from %s to %s play %s %s"
                        % (everyday_start, everyday_end,
                           sources[everyday_source], everyday_preset),
                "icon" : "icon_alarm",
                "send" : ["set-alarm", "everyday",
                    everyday_start,
                    everyday_end,
                    sources[everyday_source] + everyday_preset,
                    "wait",
                    "alarm", "everyday"]
            }
        ]

    if once_start != "" and once_end != "":
        entries += [
            {
                "path" : "once",
                "name" : "Once from %s to %s play %s %s"
                        % (once_start, once_end,
                           sources[once_source], once_preset),
                "icon" : "icon_alarm",
                "send" : ["set-alarm", "once",
                    once_start,
                    once_end,
                    sources[once_source] + once_preset,
                    "wait",
                    "alarm", "once"]
            }
        ]

    if everyday_start != "" \
        and everyday_end != "" \
        and once_start != "" \
        and once_end != "":

        entries += [
            {
                "path" : "on",
                "name" : ("Everyday from %s to %s play %s %s\n"
                        + "and Once from %s to %s play %s %s")
                        % (everyday_start, everyday_end,
                           sources[everyday_source], everyday_preset,
                           once_start, once_end,
                           sources[once_source], once_preset),
                "icon" : "icon_alarm",
                "send" : ["set-alarm", "everyday",
                    everyday_start,
                    everyday_end,
                    sources[everyday_source] + everyday_preset,
                    "wait",
                    once_start,
                    once_end,
                    sources[once_source] + once_preset,
                    "wait",
                    "alarm", "on"]
            }
        ]

    return entries




def _build_exec_kodi_stop(source):

    if settings.getSetting("kodi_input_source") == source:
        return ""
    else:
        return "PlayerControl(Stop)"




def _build_exec_power_off():
    if settings.getSetting("stop_on_turn_off") == "true":
        return "PlayerControl(Stop)"
    else:
        return ""




def _send_kodi():

    kodi_input_source = int(settings.getSetting("kodi_input_source"))
    return SOURCES[kodi_input_source]




def _build_presets():

    entries = []

    for i in range(1, 40):
        if settings.getSetting("preset_%s" % str(i)) == "":
            continue

        entries += [
            {
                "path" : str(i),
                "name" : settings.getSetting("preset_%s" % str(i)),
                "icon" : "icon_%s" % (str(i % 10)),
                "send" : ["macro", "preset", str(i)],
                "exec" : "PlayerControl(Stop)"
            }
        ]

    return entries




def _build_sleep_timer():
    entries = [
        {
            "path" : "off",
            "name" : "Off",
            "icon" : "icon_sleep",
            "send" : ["sleep", "0"]
        }
    ]

    for i in range(1, 6):
        t = settings.getSetting("sleep_preset_%i" % i)
        entries += [
            {
                "path" : str(i),
                "name" : "%s minutes" % t,
                "icon" : "icon_sleep",
                "send" : ["sleep", t]
            }
        ]

    return entries




def _build_volume():
    entries = [
        {
            "path" : "off",
            "name" : "Mute On",
            "icon" : "icon_mute",
            "send" : ["mute", "on"]
        },
        {
            "path" : "on",
            "name" : "Mute Off",
            "icon" : "icon_mute_off",
            "send" : ["mute", "off"]
        }
    ]


    _min = int(settings.getSetting("vol_min"))
    _max = int(settings.getSetting("vol_max")) + 1
    _step = int(settings.getSetting("vol_step"))

    icons = ["icon_zero", "icon_low", "icon_medium", "icon_full"]
    icon_div = (_max - _min) / (1.0 * len(icons))

    _range = range(_min, _max, _step)

    for i in _range:

        entries += [
            {
                "path" : str(i),
                "name" : str(i),
                "icon" : icons[int(((i - _min) / icon_div))],
                "send" : ["vol", str(i)]
            }
        ]

    return entries




_menu = [
    { # root
        "path" : "",
        "node" : [
            { # kodi
                "path" : "kodi",
                "name" : "KODI",
                "icon" : "icon_kodi",
                "send" : _send_kodi()
            },
            { # fm
                "path" : "fm",
                "name" : "FM Radio",
                "icon" : "icon_radio",
                "send" : ["fm"],
                "exec" : "PlayerControl(Stop)"
            },
            { # dab
                "path" : "dab",
                "name" : "DAB Radio",
                "icon" : "icon_dab",
                "send" : ["dab"],
                "exec" : "PlayerControl(Stop)"
            },
            { # presets
                "path" : "presets",
                "name" : "Radio presets",
                "node" : _build_presets()
            },
            { # preset
                "path" : "preset",
                "name" : "Tune",
                "node" : [
                    { # preset +
                        "path" : "preset_next",
                        "name" : "Preset +",
                        "icon" : "icon_arrow_up",
                        "send" : ["preset", "%2B"]
                    },
                    { # preset -
                        "path" : "preset_prev",
                        "name" : "Preset -",
                        "icon" : "icon_arrow_down",
                        "send" : ["preset", "-"]
                    },
                    { # mode
                        "path" : "mode",
                        "name" : "Stereo / Mono",
                        "icon" : "icon_stereo",
                        "send" : ["mode"]
                    },
                    { # info
                        "path" : "info",
                        "name" : "Info",
                        "icon" : "icon_info",
                        "send" : ["info"]
                    }
                ]
            },
            { # cd
                "path" : "cd",
                "name" : "CD",
                "icon" : "icon_cd",
                "send" : ["cd"],
                "exec" : _build_exec_kodi_stop("CD")
            },
            { # net
                "path" : "net",
                "name" : "Network",
                "icon" : "icon_net",
                "send" : ["net"],
                "exec" : _build_exec_kodi_stop("Network")
            },
            { # optical
                "path" : "optical",
                "name" : "Optical",
                "icon" : "icon_digital",
                "send" : ["optical"],
                "exec" : _build_exec_kodi_stop("Optical")
            },
            { # analog 1
                "path" : "analog1",
                "name" : "Analog 1",
                "icon" : "icon_analog",
                "send" : ["analog", "1"],
                "exec" : _build_exec_kodi_stop("Analog 1")
            },
            { # analog 2
                "path" : "analog2",
                "name" : "Analog 2",
                "icon" : "icon_analog",
                "send" : ["analog", "2"],
                "exec" : _build_exec_kodi_stop("Analog 2")
            },
            { # cda
                "path" : "cda",
                "name" : "CD Audio",
                "icon" : "icon_cd",
                "send" : ["cda"]
            },
            { # usb
                "path" : "usb",
                "name" : "USB",
                "icon" : "icon_usb",
                "send" : ["usb"]
            },
            { # internet
                "path" : "internet",
                "name" : "Internet radio",
                "icon" : "icon_internet",
                "send" : ["internet"]
            },
            { # online
                "path" : "online",
                "name" : "Online music",
                "icon" : "icon_net",
                "send" : ["online"]
            },
            { # server
                "path" : "server",
                "name" : "Music server",
                "icon" : "icon_server",
                "send" : ["server"]
            },
            { # ipod
                "path" : "ipod",
                "name" : "iPOD",
                "icon" : "icon_usb",
                "send" : ["ipod"]
            },
            { # power off
                "path" : "off",
                "name" : "Power off",
                "icon" : "icon_power",
                "send" : ["off"],
                "exec" : _build_exec_power_off()
            },
            { # power
                "path" : "power",
                "name" : "Timers",
                "node" : [
                    { # sleep
                        "path" : "sleep",
                        "name" : "Sleep timer",
                        "node" : _build_sleep_timer()
                    },
                    { # alarm
                        "path" : "alarm",
                        "name" : "Alarm",
                        "node" : _build_alarm()
                    },
                    { # dimmer
                        "path" : "dimmer",
                        "name" : "Dimmer",
                        "node" : [
                            { # off
                                "path" : "off",
                                "name" : "Off",
                                "icon" : "icon_zero",
                                "send" : ["dimmer", "off"]
                            },
                            { # low
                                "path" : "low",
                                "name" : "Low",
                                "icon" : "icon_low",
                                "send" : ["dimmer", "low"]
                            },
                            { # normal
                                "path" : "normal",
                                "name" : "Normal",
                                "icon" : "icon_medium",
                                "send" : ["dimmer", "normal"]
                            },
                            { # high
                                "path" : "high",
                                "name" : "High",
                                "icon" : "icon_full",
                                "send" : ["dimmer", "high"]
                            }
                        ]
                    },
                    { # power off
                        "path" : "off",
                        "name" : "Power off",
                        "icon" : "icon_power",
                        "send" : ["off"]
                    }
                ]
            },
            { # sound
                "path" : "sound",
                "name" : "Sound settings",
                "node" : [
                    { # volume
                        "path" : "volume",
                        "name" : "Volume",
                        "node" : _build_volume()
                    },
                    { # bass
                        "path" : "bass",
                        "name" : "Bass",
                        "node" : [
                            { # incr
                                "path" : "incr",
                                "name" : "Bass +",
                                "icon" : "icon_sound_up",
                                "send" : ["bass", "%2B"]
                            },
                            { # decr
                                "path" : "decr",
                                "name" : "Bass -",
                                "icon" : "icon_sound_down",
                                "send" : ["bass", "-"]
                            }
                        ]
                    },
                    { # treble
                        "path" : "treble",
                        "name" : "Treble",
                        "node" : [
                            { # incr
                                "path" : "incr",
                                "name" : "Treble +",
                                "icon" : "icon_sound_up",
                                "send" : ["treble", "%2B"]
                            },
                            { # decr
                                "path" : "decr",
                                "name" : "Treble -",
                                "icon" : "icon_sound_down",
                                "send" : ["treble", "-"]
                            }
                        ]
                    },
                    { # balance
                        "path": "balance",
                        "name" : "Balance",
                        "node" : [
                            { # left
                                "path"  : "left",
                                "name" : "Balance left",
                                "icon" : "icon_arrow_left",
                                "send" : ["balance", "left"]
                            },
                            { # right
                                "path" : "right",
                                "name" : "Balance right",
                                "icon" : "icon_arrow_right",
                                "send" : ["balance", "right"]
                            }
                        ]
                    },
                    { # sdirect
                        "path" : "sdirect",
                        "name" : "S.Direct",
                        "node" : [
                            { # off
                                "path" : "off",
                                "name" : "S.Direct Off",
                                "icon" : "icon_off",
                                "send" : ["sdirect", "off"]
                            },
                            { # on
                                "path" : "on",
                                "name" : "S.Direct On",
                                "icon" : "icon_on",
                                "send" : ["sdirect", "on"]
                            }
                        ]
                    },
                    { # sdb
                        "path" : "sdb",
                        "name" : "SDB",
                        "node" : [
                            { # off
                                "path" : "off",
                                "name" : "SDB Off",
                                "icon" : "icon_off",
                                "send" : ["sdb", "off"]
                            },
                            { # on
                                "path" : "on",
                                "name" : "SDB On",
                                "icon" : "icon_on",
                                "send" : ["sdb", "on"]
                            }
                        ]
                    }
                ]
            }
        ]
    }
]




def _get_directory_by_path(path):

    if path == "/":
        return _menu[0]

    tokens = path.split("/")[1:]
    directory = _menu[0]

    while len(tokens) > 0:
        path = tokens.pop(0)
        for node in directory["node"]:
            if node["path"] == path:
                directory = node
                break

    return directory




def _fill_directory(path):

    directory = _get_directory_by_path(path)

    for entry in directory["node"]:
        _add_list_item(entry, path)

    xbmcplugin.endOfDirectory(addon_handle)




def _build_param_string(param, values, current = ""):

    if values == None:
        return current

    for v in values:
        current += "?" if len(current) == 0 else "&"
        current += param + "=" + v

    return current




def _add_list_item(entry, path):

    if path == "/":
        path = ""

    item_path = path + "/" + entry["path"]
    item_id = item_path.replace("/", "_")

    if settings.getSetting("display%s" % item_id) == "false":
        return

    param_string = ""
    if "send" in entry:
        param_string = _build_param_string(
            param = "send", 
            values = entry["send"], 
            current = param_string)

    if "exec" in entry:
        param_string = _build_param_string(
            param = "exec", 
            values = entry["exec"], 
            current = param_string)

    if "node" in entry:
        is_folder = True
    else:
        is_folder = False

    label = entry["name"]
    if settings.getSetting("label%s" % item_id) != "":
        label = settings.getSetting("label%s" % item_id)

    if "icon" in entry:
        icon_file = os.path.join(addon_dir, "resources", "assets", entry["icon"] + ".png")
    else:
        icon_file = None

    li = xbmcgui.ListItem(label, iconImage=icon_file)

    xbmcplugin.addDirectoryItem(handle=addon_handle,
                            listitem=li,
                            url="plugin://" + __PLUGIN_ID__
                            + item_path
                            + param_string,
                            isFolder=is_folder)




def _check_hardware():

    dev = settings.getSetting("device")
    if os.path.exists(dev):
        return True

    icon_file = os.path.join(addon_dir, "resources", "assets", "icon_no_connection.png")
    li = xbmcgui.ListItem("No connection", iconImage=icon_file)
    xbmcplugin.addDirectoryItem(handle=addon_handle,
                                listitem=li,
                                url="plugin://" + __PLUGIN_ID__,
                                isFolder=False)

    xbmcplugin.endOfDirectory(addon_handle)

    return False




def _call_denon(send_params, url_params):

    if "silent" not in url_params:
        xbmc.executebuiltin("Notification(Send to Denon, " + " ".join(send_params) + ", 5000, " + addon_dir + "/icon.png)")

    params = [settings.getSetting("device")]
    params += send_params
    denon.sendto_denon(params)




def _handle_audio_sink():

    sink = int(settings.getSetting("kodi_alsa_sink")) - 1
    if sink == -1:
        return

    try:
        pa_settings = xbmcaddon.Addon(id=PLUGIN_PASINK);
	alsa_id = pa_settings.getSetting("alsa_id_%i" % sink)
	xbmc.executebuiltin('PlayMedia(%s)' % ("plugin://" + PLUGIN_PASINK + "/" + alsa_id + "?action=switch"))
    except:
        return




if __name__ == "__main__":

    path = urlparse.urlparse(sys.argv[0]).path
    url_params = urlparse.parse_qs(sys.argv[2][1:])

    if _check_hardware():
        if "exec" in url_params:
            xbmc.executebuiltin(url_params["exec"][0])

	if path == "/kodi":
            _handle_audio_sink()

        if "send" in url_params:
            _call_denon(url_params["send"], url_params)
        else:
            _fill_directory(path)
