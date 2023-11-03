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


class ColorSelectorApp(UserControl):
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


def main(page: Page):
    page.title="Color Selector App"
    page.window_width=400
    page.window_height=440
    colorSelector=ColorSelectorApp()
    page.add(colorSelector)


flet.app(target=main)