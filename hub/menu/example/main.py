#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from menu import menu
# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.

##########################
# Example Usage
#########################
def menu_callback(action, event_name):
    print("callback", action, event_name)      

def menu_about(event_name):
    print("about", event_name)

menu_config = {
    "properties": {
        "button" : {
            "padding": 1, #px
            "spacing": 2, #px
            "radius": 5, #px
            "height": 30, #px
            #"width": 64, #px
        },
        "text": {
            "padding": 8, #px
            #"alignment": "left", #future - center, right
        },
        #"font" : {
        #    "family": None,
        #    "size": 12,
        #    "bold": True,
        #    "lang": None,
        #}
    },
    "items": [
        {
            "label": "Home",
            "action": "home"
        },
        {
            "label": "About",
            "action": menu_about
        },
        {
            "label": "Start",
            "action": "start"
        },
        {
            "label": "Stop",
            "action": "stop"
        },
    ]
}

ev3 = EV3Brick()
menuInstance = menu(ev3, menu_config, menu_callback)
menuInstance.show()