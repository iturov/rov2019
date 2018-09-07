# -*- coding: utf-8 -*-
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.properties import NumericProperty
from kivy.properties import StringProperty
from kivy.clock import Clock

Window.clearcolor = (.15, .15, .15, 1)
Window.size = (1366, 768)
#Window.fullscreen = 'auto'

class Axis():
    def __init__(self):
        self.axis = {
            "X": 0,
            "Y": 0
        }
        self.dead_zone = 1.0


    def updateAxis(self, axis, value, invert=False, range=32767., offset=0):
        self.axis[axis] = value * 100.0 / range + offset
        if invert:
            self.axis[axis] *= -1

        if abs(self.axis[axis]) < self.dead_zone:
            self.axis[axis] = 0.


class Controller():
    def __init__(self):
        self.X = False
        self.SQUARE = False
        self.CIRCLE = False
        self.TRIANGLE = False

        self.L1 = False
        self.R1 = False

        self.UP = False
        self.DOWN = False
        self.RIGHT = False
        self.LEFT = False

        self.LEFT_AXIS = Axis()
        self.RIGHT_AXIS = Axis()
        self.R3L3 = Axis()

    def printButtons(self):
        print "x", self.X
        print "SQ", self.SQUARE
        print "CIRCLE", self.CIRCLE
        print "triangle",  self.TRIANGLE
        print "l1", self.L1
        print "r1", self.R1

    def printHats(self):
        print "up", self.UP
        print "down", self.DOWN
        print "right", self.RIGHT
        print "left", self.LEFT

    def resetButtons(self):
        self.X = False
        self.SQUARE = False
        self.CIRCLE = False
        self.TRIANGLE = False

        self.L1 = False
        self.R1 = False

    def resetHats(self):
        self.UP = False
        self.DOWN = False
        self.RIGHT = False
        self.LEFT = False

class myGui(GridLayout):

    tempLabel = StringProperty('23')
    barLabel = StringProperty('1.2')

    def __init__(self, **kwargs):
        super(myGui, self).__init__(**kwargs)
        Window.bind(on_joy_hat=self.on_joy_hat)
        Window.bind(on_joy_axis=self.on_joy_axis)
        Window.bind(on_joy_button_down=self.on_joy_button_down)
        Window.bind(on_joy_button_up=self.on_button_release)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self.controller = Controller()
    def on_joy_axis(self, win, stickid, axisid, value):
        if(axisid == 0):
            self.controller.LEFT_AXIS.updateAxis("X", value, True)

        if(axisid == 1):
            self.controller.LEFT_AXIS.updateAxis("Y", value, True)

        if (axisid == 3):
            self.controller.R3L3.updateAxis("X", value, range=32767.0*2, offset=50)

        if (axisid == 4):
            self.controller.R3L3.updateAxis("Y", value, range=32767.0*2, offset=50)

        if (axisid == 5):
            self.controller.RIGHT_AXIS.updateAxis("Y", value, True)

        if (axisid == 2):
            self.controller.RIGHT_AXIS.updateAxis("X", value)


    def on_joy_button_down(self, win, stickid, buttonid):
        self.controller.resetButtons()
        if buttonid == 0:
            self.controller.SQUARE = True
        if buttonid == 1:
            self.controller.X = True
        if buttonid == 2:
            self.controller.CIRCLE = True
        if buttonid == 3:
            self.controller.TRIANGLE = True
        if buttonid == 4:
            self.controller.L1 = True
        if buttonid == 5:
            self.controller.R1 = True
        if buttonid == 6:
            print('BACK')
        if buttonid == 7:
            print('START')

        self.controller.printButtons()

    def on_button_release(self, win, stickid, buttonid):
        self.controller.resetButtons()
        self.controller.printButtons()


    def on_joy_hat(self, win, stickid, hatid, value):
        # Reset the controller
        self.controller.resetHats()

        if value[0] == 1:
            self.controller.RIGHT = True
        if value[0] == -1:
            self.controller.LEFT = True
        if value[1] == 1:
            self.controller.UP = True
        if value[1] == -1:
            self.controller.DOWN = True

        self.controller.printHats()

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
