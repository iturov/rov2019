# -*- coding: utf-8 -*-
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.properties import NumericProperty
from kivy.properties import StringProperty
from kivy.clock import Clock
from pymavlink import mavutil

Window.clearcolor = (.15, .15, .15, 1)
Window.size = (1366, 768)
# Window.fullscreen = 'auto'


class Axis(object):
    def __init__(self):
        self.axis = {
            "X": 0,
            "Y": 0,
        }
        self.dead_zone = 1.0

    def updateAxis(self, axis, value, range=32767.0, offset=0):
        self.axis[axis] = value * 1000.0 / range + offset

        if abs(self.axis[axis]) < self.dead_zone:
            self.axis[axis] = 0


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
        print("x", self.X)
        print("SQ", self.SQUARE)
        print("CIRCLE", self.CIRCLE)
        print("triangle",  self.TRIANGLE)
        print("l1", self.L1)
        print("r1", self.R1)

    def printHats(self):
        print("up", self.UP)
        print("down", self.DOWN)
        print("right", self.RIGHT)
        print("left", self.LEFT)

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

    angle = NumericProperty(0)
    tempLabel = StringProperty('23')
    barLabel = StringProperty('1.2')
    konttempLabel = StringProperty('23')

    def __init__(self, **kwargs):
        super(myGui, self).__init__(**kwargs)
        Window.bind(on_joy_hat=self.on_joy_hat)
        Window.bind(on_joy_axis=self.on_joy_axis)
        Window.bind(on_joy_button_down=self.on_joy_button_down)
        Window.bind(on_joy_button_up=self.on_button_release)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self.controller = Controller()
        Clock.schedule_interval(self.sendAxis, 0.2)
        Clock.schedule_interval(self.pullValues, 0.02)
        self.master = mavutil.mavlink_connection('udp:192.168.2.1:14550')
        self.master.wait_heartbeat()

    def modeChange(self, modeName):
        print("** Mode changed to: {} **".format(modeName))
        mode_id = self.master.mode_mapping()[modeName]
        self.master.set_mode(mode_id)
        # Change the mode to 'modeName'

    def armVehicle(self):
        self.master.mav.command_long_send(
            self.master.target_system,
            self.master.target_component,
            mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
            0,
            1, 0, 0, 0, 0, 0, 0)
        print('Vehicle Armed')

    def disarmVehicle(self):
        self.master.mav.command_long_send(
            self.master.target_system,
            self.master.target_component,
            mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
            0,
            0, 0, 0, 0, 0, 0, 0)
        print('Vehicle Disarmed')

    def on_joy_axis(self, win, stickid, axisid, value):

        if(axisid == 1):
            self.controller.LEFT_AXIS.updateAxis("Y", value, range=32767.0, offset=50)
            print('sa')

        if (axisid == 3):
            self.controller.RIGHT_AXIS.updateAxis("X", value, range=32767.0, offset=50)

        if (axisid == 4):
            self.controller.RIGHT_AXIS.updateAxis("Y", value, range=32767.0, offset=50)


    def on_joy_button_down(self, win, stickid, buttonid):
        self.controller.resetButtons()
        if buttonid == 0:
            self.controller.SQUARE = True
            self.armVehicle()
        if buttonid == 1:
            self.controller.X = True
            self.disarmVehicle()
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

    def sendAxis(self, *args):
        self.master.mav.heartbeat_send(6, 8, 192, 0, 4, 3)
        self.master.mav.manual_control_send(self.master.target_system, -(int(self.controller.LEFT_AXIS.axis['Y'])-50), 0, int(500 + int(self.controller.RIGHT_AXIS.axis['Y'])/2)-25, int(self.controller.RIGHT_AXIS.axis['X'])-50, 1)

    def pullValues(self, *args):
        msg = self.master.recv_match()
        if msg.get_type() == 'SCALED_PRESSURE':
            self.barLabel = str(int(msg.press_abs))
            self.konttempLabel = str(msg.temperature/100)
        if msg.get_type() == 'SCALED_PRESSURE2':
            self.tempLabel = str(msg.temperature/100)
        if msg.get_type() == 'SCALED_IMU2':
            print(msg)

class GuiTestApp(App):

    def build(self):
        return myGui()




if __name__== "__main__":
    GuiTestApp().run()
