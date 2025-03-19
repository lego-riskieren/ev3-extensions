'''
MIT License

Copyright (c) 2025 Erik Thompson

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

from pybricks.parameters import Button, Color
from pybricks.tools import wait
from pybricks.media.ev3dev import Font
import types

class menu:

    def __init__(self, ev3, config, callback):
        # TODO: add validation
        self._callback = callback
        self._ev3 = ev3
        self._menu_config = config

        self._line_height = self._menu_config.get("properties", {}).get("button", {}).get("height", 32)
        self._radius = self._menu_config.get("properties", {}).get("button", {}).get("radius", 5)
        self._spacing = self._menu_config.get("properties", {}).get("button", {}).get("spacing", 2)
        self._padding = self._menu_config.get("properties", {}).get("button", {}).get("padding", 1)
        self._text_padding = self._menu_config.get("properties", {}).get("text", {}).get("padding", 8)
        self._width = self._menu_config.get("properties", {}).get("width", self._ev3.screen.width)

        font_family = self._menu_config.get("properties", {}).get("font", {}).get("family", None)
        font_size = self._menu_config.get("properties", {}).get("font", {}).get("size", 12)
        font_bold = self._menu_config.get("properties", {}).get("font", {}).get("bold", True)
        # TODO: Extend for additional font characteristics
        self._font = Font(font_family, font_size, font_bold)
        self._font_height = self._font.height
        self._font_offset_top = (self._line_height - self._font_height) / 2


        # TODO: allow for offscreen scrolling of longer menus
        #print(ev3.screen.height)

    def _item_invoked(self, item):
        event_name = "invoked"
        if item is None:
            self._callback(None, event_name)
        else:
            action = item.get("action", None)
            if isinstance(action, types.FunctionType):
                action(event_name)
            else:
                self._callback(action, event_name)        

    def _show_menu_item(self, item, row, selected = False):
        left = self._padding
        top = (self._line_height + self._spacing) * row
        right = self._width - self._padding - left
        bottom = top + self._line_height

        color = Color.BLACK
        background_color = None
        if selected: 
            color = Color.WHITE
            background_color = Color.BLACK

        self._ev3.screen.draw_box(left, top, right, bottom, r=self._radius, fill=selected, color=Color.BLACK)
        self._ev3.screen.draw_text(left + self._text_padding, top + self._font_offset_top, item.get("label", "???"), text_color=color, background_color=background_color)

    def _display_items(self, items, selected_index):
        self._ev3.screen.clear()
        self._ev3.screen.set_font(self._font)
        index = 0
        for item in items:
            self._show_menu_item(item, index, selected_index == index)
            index += 1

    def wait_for_buttons(self):
        btns_pressed = self._ev3.buttons.pressed()
        while(1):
            wait(15)
            recheck = self._ev3.buttons.pressed()
            if not len(recheck) and len(btns_pressed):
                # buttons up, let's see what we got
                print("buttons pressed:", btns_pressed)
                break
            # may have changed in selection
            btns_pressed = recheck
        return btns_pressed

    def show(self):
        selected_index = 0
        items = self._menu_config.get("items", [])
        items_length = len(items)
        self._display_items(items, selected_index)
        
        while (1):
            btns = self.wait_for_buttons()
            if Button.UP in btns:
                if selected_index > 0: selected_index -= 1
                self._display_items(items, selected_index)
            elif Button.DOWN in btns:
                if selected_index < items_length-1: selected_index += 1
                self._display_items(items, selected_index)
            elif Button.CENTER in btns:
                self._item_invoked(items[selected_index])
                