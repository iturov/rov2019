from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.properties import NumericProperty
from kivy.properties import StringProperty
from kivy.clock import Clock

Window.clearcolor = (.15, .15, .15, 1)
Window.size = (1366, 768)
#Window.fullscreen = 'auto'

class myGui(GridLayout):

    tempLabel = StringProperty('23')
    barLabel = StringProperty('1.2')

    def __init__(self, **kwargs):
        super(myGui, self).__init__(**kwargs)
        Window.bind(on_joy_hat=self.on_joy_hat)
        Window.bind(on_joy_axis=self.on_joy_axis)
        Window.bind(on_joy_button_down=self.on_joy_button_down)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def on_joy_axis(self, win, stickid, axisid, value):
        if(axisid == 0):
            print(value)
            #XaxisSend(value) '-32768,32768'
        if(axisid == 1):
            print("Y ekseni")
            #YaxisSend(value) '-32768,32768'
        if (axisid == 3):
            print("Ek ekseni")
            #XaxisSend(value) '-32768,32768'
        if (axisid == 4):
            print("Z ekseni")
            #YaxisSend(value) '-32768,32768'

    def on_joy_button_down(self, win, stickid, buttonid):
        if buttonid == 0:
            print('A')
        if buttonid == 1:
            print('B')
        if buttonid == 2:
            print('X')
        if buttonid == 3:
            print('Y')
        if buttonid == 4:
            print('LB')
        if buttonid == 5:
            print('RB')
        if buttonid == 6:
            print('BACK')
        if buttonid == 7:
            print('START')

    def on_joy_hat(self, win, stickid, hatid, value):
        if value[0] == 1:
            print("sağ")
        if value[0] == -1:
            print("sol")
        if value[1] == 1:
            print("yukarı")
        if value[1] == -1:
            print("aşağı")

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if(keycode[1] == 'right'):
            #self.ids.anchor.rotation.angle += 1*0
            print(self.ids.cursorButton.angle)
        if(keycode[1] == 'left'):
            self.ids.relative.ids.anchor1.ids.anchor2.rotation.angle += 1

class GuiTestApp(App):
    angle = NumericProperty(0)

    def build(self):
        Clock.schedule_interval(self.update_angle, 0)
        return myGui()

    def update_angle(self, dt, *args):
        self.angle += dt * 100

if __name__=="__main__":
    GuiTestApp().run()