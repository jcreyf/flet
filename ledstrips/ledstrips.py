import urllib.request
import asyncio
import json
import flet
from flet import (
    Column,
    Container,
    Page,
    Row,
    Text,
    UserControl,
    border_radius,
    colors,
)
# https://pypi.org/project/flet-contrib/
# https://github.com/flet-dev/flet-contrib/blob/main/flet_contrib/color_picker/README.md
# https://github.com/flet-dev/flet-contrib/blob/main/flet_contrib/color_picker/src/color_picker.py
from flet_contrib.color_picker import ColorPicker
from typing import List


#---------------------------


class App():
    def __init__(self):
        self._ledstrips: List[LedStrip] = list()

    def addStrip(self):
#        self._ledstrips.append(LedStrip(name="Luna", endpoint="http://192.168.5.12:8888/light/Luna"))
#        self._ledstrips.append(LedStrip(name="Bedroom", endpoint="http://192.168.5.10:8888/light/Bedroom"))
        self._ledstrips.append(LedStrip(name="Loft", endpoint="http://192.168.5.11:8888/light/Loft"))

    def list(self):
        for strip in self._ledstrips:
            print(strip)

    def GUI(self, page: Page):
        page.title="Ledstrips"
        page.window_width=400
        page.window_height=440
        ledstripsGUI=LedstripsGUI()
        page.add(ledstripsGUI)


#---------------------------


class LedStrip():
    _Name: str = ""
    _API_endpoint: str = ""
    _Status: bool = False
    _LedCount: int = 0
    _RedValue: int = 0
    _GreenValue: int = 0
    _BlueValue: int = 0
    _WhiteValue: int = 0
    _BrightnessValue: int = 1
    def __init__(self, name: str, endpoint: str):
        self._Name=name
        self._API_endpoint=endpoint
        asyncio.run(self.getMetadata())

    def __str__(self) -> str:
        return f"Name: {self._Name} (led_count:{self._LedCount}, status:{self._Status})"

    async def getMetadata(self):
        # Get the status of the ledstrip:
        try:
            req=urllib.request.urlopen(self._API_endpoint)
            res=req.read()
            contents = json.loads(res.decode("utf-8"))
            print(str(contents))
            self._Status=contents["light"]["state"]
            self._LedCount=contents["light"]["led-count"]
            self._BrightnessValue=contents["light"]["brightness"]
            self._RedValue=contents["light"]["color"]["red"]
            self._GreenValue=contents["light"]["color"]["green"]
            self._BlueValue=contents["light"]["color"]["blue"]
            self._WhiteValue=contents["light"]["color"]["white"]
        except Exception as e:
            print(str(e))

    def _sendData(self, toggle: bool):
        _behavior = "Default"   # "Default" or "Christmass"
        try:
            data={"action": "update",
                "toggle": toggle,
                "behavior": _behavior,
                "led-count": self._LedCount,
                "brightness": self._BrightnessValue,
                "color": {
                    "red": self._RedValue,
                    "green": self._GreenValue,
                    "blue": self._BlueValue,
                    "white": self._WhiteValue
                }
            }
            data=json.dumps(data)
            data=data.encode('utf-8')
            req=urllib.request.Request(self._API_endpoint, data=data)
            req.add_header("Content-Type", "application/json")
            contents = urllib.request.urlopen(req).read()
            print(str(contents))
        except Exception as e:
            print(str(e))

    def toggle(self):
        self._sendData(toggle=True)

    def setColor(self, red: int = 0, green: int = 0, blue: int = 0):
        self._RedValue = red
        self._GreenValue = green
        self._BlueValue = blue
        self._sendData(toggle=False)

    def setBrightness(self, value: int):
        self._BrightnessValue = value
        self._sendData(toggle=False)


#---------------------------


class LedstripsGUI(UserControl):
    def build(self):
        self.result = Text(value="0", color=colors.WHITE, size=20)

        # application's root control (i.e. "view") containing all other controls
        return Container(
            width=400,
            bgcolor=colors.BLACK,
            border_radius=border_radius.all(10),
            padding=20,
            content=Column(
                controls=[
                    Row(controls=[self.result], alignment="end"),
                    Row(controls=[self.ColorPickerWidget()],),
                ],
            ),
        )


    def ColorPickerWidget(self):
        color_picker = ColorPicker(color="#c8df6f")

        def select_color(e):
            self.result.value=color_picker.color
            self.result.update()

        return flet.Column(
            [
                color_picker,
                flet.FilledButton("Select", on_click=select_color),
            ]
        )


#---------------------------


if __name__ == '__main__':
    app = App()
    app.addStrip()
    app.list()
    flet.app(target=app.GUI)
