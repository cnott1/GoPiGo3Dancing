#!/usr/bin/env python

"""
GoPiGo3 for the Raspberry Pi: an open source robotics platform for the Raspberry Pi.
Copyright (C) 2017  Dexter Industries

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/gpl-3.0.txt>.
"""

import random
import easygopigo3 as easy
import threading
from time import sleep

class GoPiGo3WithKeyboard(object):
    """
    Class for interfacing with the GoPiGo3.
    It's functionality is to map different keys
    of the keyboard to different commands of the GoPiGo3.
    """

    KEY_DESCRIPTION = 0
    KEY_FUNC_SUFFIX = 1

    left_blinker_on = False
    right_blinker_on = False

    left_eye_on = False
    right_eye_on = False

    def __init__(self):
        """
        Instantiates the key-bindings between the GoPiGo3 and the keyboard's keys.
        Sets the order of the keys in the menu.
        """
        self.gopigo3 = easy.EasyGoPiGo3()
        self.keybindings = {
        "w" : ["Move the GoPiGo3 forward", "forward"],
        "s" : ["Move the GoPiGo3 backward", "backward"],
        "a" : ["Turn the GoPiGo3 to the left", "left"],
        "d" : ["Turn the GoPiGo3 to the right", "right"],
        "<SPACE>" : ["Stop the GoPiGo3 from moving", "stop"],

        "<F1>" : ["Drive forward for 10 centimeters", "forward10cm"],
        "<F2>" : ["Drive forward for 10 inches", "forward10in"],
        "<F3>" : ["Drive forward for 360 degrees (aka 1 wheel rotation)", "forwardturn"],

        "1" : ["Turn ON/OFF left blinker of the GoPiGo3", "leftblinker"],
        "2" : ["Turn ON/OFF right blinker of the GoPiGo3", "rightblinker"],
        "3" : ["Turn ON/OFF both blinkers of the GoPiGo3", "blinkers"],
        "5" : ["Do a little boogie woogie", "activatedance"],
        "7" : ["Deliver altoids from kitchen to computer", "deliveraltoids"],

        "8" : ["Turn ON/OFF left eye of the GoPiGo3", "lefteye"],
        "9" : ["Turn ON/OFF right eye of the GoPiGo3", "righteye"],
        "0" : ["Turn ON/OFF both eyes of the GoPiGo3", "eyes"],

        "e" : ["Change the eyes' color on the go", "eyescolor"],

        "<ESC>" : ["Exit", "exit"],
        }
        self.order_of_keys = ["w", "s", "a", "d", "<SPACE>", "<F1>", "<F2>", "<F3>", "1", "2", "3", "5", "7", "8", "9", "0", "e", "<ESC>"]

    def executeKeyboardJob(self, argument):
        """
        Argument can be any of the strings stored in self.keybindings list.

        For instance: if argument is "w", then the algorithm looks inside self.keybinds dict and finds
        the "forward" value, which in turn calls the "_gopigo3_command_forward" method
        for driving the gopigo3 forward.

        The return values are:
        * "nothing" - when no method could be found for the given argument.
        * "moving" - when the robot has to move forward, backward, to the left or to the right for indefinite time.
        * "path" - when the robot has to move in a direction for a certain amount of time/distance.
        * "static" - when the robot doesn't move in any direction, but instead does static things, such as turning the LEDs ON.
        * "exit" - when the key for exiting the program is pressed.
        """
        method_prefix = "_gopigo3_command_"
        try:
            method_suffix = str(self.keybindings[argument][self.KEY_FUNC_SUFFIX])
        except KeyError:
            method_suffix = ""
        method_name = method_prefix + method_suffix

        method = getattr(self, method_name, lambda : "nothing")

        return method()

    def drawLogo(self):
        """
        Draws the name of the GoPiGo3.
        """
        print("   _____       _____ _  _____         ____  ")
        print("  / ____|     |  __ (_)/ ____|       |___ \ ")
        print(" | |  __  ___ | |__) || |  __  ___     __) |")
        print(" | | |_ |/ _ \|  ___/ | | |_ |/ _ \   |__ < ")
        print(" | |__| | (_) | |   | | |__| | (_) |  ___) |")
        print("  \_____|\___/|_|   |_|\_____|\___/  |____/ ")
        print("                                            ")

    def drawDescription(self):
        """
        Prints details related on how to operate the GoPiGo3.
        """
        print("\nPress the following keys to run the features of the GoPiGo3.")
        print("To move the motors, make sure you have a fresh set of batteries powering the GoPiGo3.\n")

    def drawMenu(self):
        """
        Prints all the key-bindings between the keys and the GoPiGo3's commands on the screen.
        """
        try:
            for key in self.order_of_keys:
                print("\r[key {:8}] :  {}".format(key, self.keybindings[key][self.KEY_DESCRIPTION]))
        except KeyError:
            print("Error: Keys found GoPiGo3WithKeyboard.order_of_keys don't match with those in GoPiGo3WithKeyboard.keybindings.")

    def _gopigo3_command_forward(self):
        self.gopigo3.forward()

        return "moving"

    def _gopigo3_command_backward(self):
        self.gopigo3.backward()

        return "moving"

    def _gopigo3_command_left(self):
        self.gopigo3.left()

        return "moving"

    def _gopigo3_command_right(self):
        self.gopigo3.right()

        return "moving"

    def _gopigo3_command_stop(self):
        self.gopigo3.stop()

        return "moving"

    def _gopigo3_command_forward10cm(self):
        self.gopigo3.drive_cm(10)

        return "path"

    def _gopigo3_command_forward10in(self):
        self.gopigo3.drive_inches(10)

        return "path"

    def _gopigo3_command_forwardturn(self):
        self.gopigo3.drive_degrees(360)

        return "path"

    def _gopigo3_command_leftblinker(self):
        if self.left_blinker_on is False:
            self.gopigo3.led_on(1)
            self.left_blinker_on = True
        else:
            self.gopigo3.led_off(1)
            self.left_blinker_on = False

        return "static"

    def _gopigo3_command_rightblinker(self):
        if self.right_blinker_on is False:
            self.gopigo3.led_on(0)
            self.right_blinker_on = True
        else:
            self.gopigo3.led_off(0)
            self.right_blinker_on = False

        return "static"

    def _gopigo3_command_blinkers(self):
        if self.left_blinker_on is False and self.right_blinker_on is False:
            self.gopigo3.led_on(0)
            self.gopigo3.led_on(1)
            self.left_blinker_on = self.right_blinker_on = True
        else:
            self.gopigo3.led_off(0)
            self.gopigo3.led_off(1)
            self.left_blinker_on = self.right_blinker_on = False

        return "static"

    def _gopigo3_command_lefteye(self):
        if self.left_eye_on is False:
            self.gopigo3.open_left_eye()
            self.left_eye_on = True
        else:
            self.gopigo3.close_left_eye()
            self.left_eye_on = False

        return "static"

    def _gopigo3_command_righteye(self):
        if self.right_eye_on is False:
            self.gopigo3.open_right_eye()
            self.right_eye_on = True
        else:
            self.gopigo3.close_right_eye()
            self.right_eye_on = False

        return "static"

    def _gopigo3_command_eyes(self):
        if self.left_eye_on is False and self.right_eye_on is False:
            self.gopigo3.open_eyes()
            self.left_eye_on = self.right_eye_on = True
        else:
            self.gopigo3.close_eyes()
            self.left_eye_on = self.right_eye_on = False

        return "static"

    def _gopigo3_command_eyescolor(self):
        red = random.randint(0, 255)
        green = random.randint(0, 255)
        blue = random.randint(0, 255)

        self.gopigo3.set_eye_color((red, green, blue))
        if self.left_eye_on is True:
            self.gopigo3.open_left_eye()
        if self.right_eye_on is True:
            self.gopigo3.open_right_eye()

        return "static"

    def _gopigo3_command_exit(self):
        return "exit"
    
    def _gopigo3_command_activatedance(self):
        beat = 60/128
        self.gopigo3.set_speed(300)
        turn90Deg = 310
        self.gopigo3.close_eyes()
            
        """
        self.gopigo3.set_speed(1000)
        self.gopigo3.forward()
        sleep(beat*4)
        
        self.gopigo3.stop()
        self.gopigo3.set_speed(300)
        return "static"
        """
        
        
        
        
        
        
        
        """beat 0"""
        self.gopigo3.steer(100, 100)
        sleep(beat * 2)
        self.gopigo3.stop()
        sleep(beat * 2)
        
        self.gopigo3.steer(100, 100)
        sleep(beat * 2)
        self.gopigo3.stop()
        sleep(beat * 2)
        
        """
        self.gopigo3.set_speed(300)
        self.gopigo3.orbit(180, 15)
        """
        self.gopigo3.set_speed(300)
        self.gopigo3.steer(100, 13.5)
        sleep(beat*8)
        
        
        """beat 16"""
        self.gopigo3.set_speed(300)
        self.gopigo3.steer(100, 100)
        sleep(beat / 2)
        self.gopigo3.stop()
        sleep(beat / 2)
        self.gopigo3.steer(100, 100)
        sleep(beat / 2)
        self.gopigo3.stop()
        sleep(beat / 2)
        self.gopigo3.steer(100, 100)
        sleep(beat / 2)
        self.gopigo3.stop()
        sleep(beat / 2)
        self.gopigo3.steer(100, 100)
        sleep(beat / 2)
        self.gopigo3.stop()
        sleep(beat / 2)
        
        self.gopigo3.steer(100, 100)
        sleep(beat / 2)
        self.gopigo3.stop()
        sleep(beat / 2)
        self.gopigo3.steer(100, 100)
        sleep(beat / 2)
        self.gopigo3.stop()
        sleep(beat / 2)
        self.gopigo3.steer(100, 100)
        sleep(beat / 2)
        self.gopigo3.stop()
        sleep(beat / 2)
        self.gopigo3.steer(100, 100)
        sleep(beat / 2)
        self.gopigo3.stop()
        sleep(beat / 2)
        
        """beat 24"""
        
        starDriveDiameter = 380
        starDriveHypotenuse = starDriveDiameter / 2 * 1.141
        
        starTurnSpeed135 = 243
        self.gopigo3.set_speed(starDriveDiameter)
        self.gopigo3.steer(100, 100)
        sleep(beat * 2)
        self.gopigo3.set_speed(starTurnSpeed135)
        self.gopigo3.steer(-100, 100)
        sleep(beat * 2)
        
        self.gopigo3.set_speed(starDriveHypotenuse)
        self.gopigo3.steer(100, 100)
        sleep(beat * 2)
        self.gopigo3.set_speed(starTurnSpeed135 * (90/135))
        self.gopigo3.steer(-100, 100)
        sleep(beat * 2)
        
        self.gopigo3.set_speed((starDriveHypotenuse))
        self.gopigo3.steer(100, 100)
        sleep(beat * 2)
        self.gopigo3.set_speed(starTurnSpeed135 * (90/135))
        self.gopigo3.steer(-100, 100)
        sleep(beat * 2)
        
        self.gopigo3.set_speed(starDriveHypotenuse)
        self.gopigo3.steer(100, 100)
        sleep(beat * 2)
        self.gopigo3.set_speed(starTurnSpeed135)
        self.gopigo3.steer(-100, 100)
        sleep(beat * 2)
        
        self.gopigo3.set_speed(starDriveDiameter)
        self.gopigo3.steer(100, 100)
        sleep(beat * 2)
        
        """Beat 42"""
        self.gopigo3.set_speed(turn90Deg)
        self.gopigo3.steer(100, -100)
        sleep(beat)
        
        self.gopigo3.set_speed(250)
        slowCounter = 12
        while slowCounter > 0:
            self.gopigo3.set_speed(slowCounter * 25)
            self.gopigo3.steer(100, 100)
            slowCounter -= 1
            sleep(beat)
        
        """Beat 55"""
        self.gopigo3.set_speed(turn90Deg)
        self.gopigo3.steer(100, -100)
        sleep(beat)
        
        self.gopigo3.set_speed(300)
        self.gopigo3.steer(100, 100)
        sleep(beat / 2)
        self.gopigo3.stop()
        sleep(beat / 2)
        self.gopigo3.steer(100, 100)
        sleep(beat / 2)
        self.gopigo3.stop()
        sleep(beat / 2)
        self.gopigo3.steer(100, 100)
        sleep(beat / 2)
        self.gopigo3.stop()
        sleep(beat / 2)
        self.gopigo3.steer(100, 100)
        sleep(beat / 2)
        self.gopigo3.stop()
        sleep(beat / 2)
        
        self.gopigo3.steer(100, 100)
        sleep(beat / 2)
        self.gopigo3.stop()
        sleep(beat / 2)
        self.gopigo3.steer(100, 100)
        sleep(beat / 2)
        self.gopigo3.stop()
        sleep(beat / 2)
        self.gopigo3.steer(100, 100)
        sleep(beat / 2)
        self.gopigo3.stop()
        sleep(beat / 2)
        self.gopigo3.steer(100, 100)
        sleep(beat / 2)
        self.gopigo3.stop()
        sleep(beat / 2)
        
        """Beat 64"""
        walkSpeed = 250
        self.gopigo3.set_speed(turn90Deg)
        self.gopigo3.steer(100, -100)
        sleep(beat)
        
        self.gopigo3.set_speed(walkSpeed)
        self.gopigo3.forward()
        sleep(beat * 2)
        
        self.gopigo3.steer(100, -100)
        sleep(beat/2)
        self.gopigo3.steer(-100, 100)
        sleep(beat/2)
        
        self.gopigo3.set_speed(walkSpeed)
        self.gopigo3.forward()
        sleep(beat * 2)
        
        """Beat 70"""
        self.gopigo3.steer(100, -100)
        sleep(beat/2)
        self.gopigo3.steer(-100, 100)
        sleep(beat/2)
        
        self.gopigo3.set_speed(turn90Deg)
        self.gopigo3.steer(-100, 100)
        sleep(beat)
        
        self.gopigo3.set_speed(walkSpeed)
        self.gopigo3.forward()
        sleep(beat * 2)
        
        self.gopigo3.steer(100, -100)
        sleep(beat/2)
        self.gopigo3.steer(-100, 100)
        sleep(beat/2)
        
        self.gopigo3.set_speed(walkSpeed)
        self.gopigo3.forward()
        sleep(beat * 2)
        
        self.gopigo3.steer(100, -100)
        sleep(beat/2)
        self.gopigo3.steer(-100, 100)
        sleep(beat/2)
        
        """Beat 78"""
        
        self.gopigo3.set_speed(turn90Deg)
        self.gopigo3.steer(-100, 100)
        sleep(beat)
        
        self.gopigo3.set_speed(walkSpeed)
        self.gopigo3.forward()
        sleep(beat * 1)
        
        self.gopigo3.open_eyes()
        self.gopigo3.blinker_on(0)
        self.gopigo3.blinker_on(1)
        self.gopigo3.set_speed(walkSpeed)
        self.gopigo3.forward()
        sleep(beat * 1)
        
        self.gopigo3.steer(100, -100)
        sleep(beat/2)
        self.gopigo3.steer(-100, 100)
        sleep(beat/2)
        
        self.gopigo3.set_speed(walkSpeed)
        self.gopigo3.forward()
        sleep(beat * 2)
        
        self.gopigo3.steer(100, -100)
        sleep(beat/2)
        self.gopigo3.steer(-100, 100)
        sleep(beat/2)
                
        self.gopigo3.set_speed(turn90Deg)
        self.gopigo3.steer(100, -100)
        sleep(beat)
        
        """Beat 86"""
        self.gopigo3.set_speed(walkSpeed)
        self.gopigo3.forward();
        sleep(beat * 4)
        self.gopigo3.set_speed(turn90Deg)
        self.gopigo3.steer(100, -100);
        sleep(beat * 1)
        self.gopigo3.set_speed(walkSpeed)
        self.gopigo3.forward();
        sleep(beat * 3)
        
        """Beat 94"""
        
        
        figure8speed = 320;
        
        self.gopigo3.set_speed(figure8speed)
        self.gopigo3.steer(100, 20)
        sleep(beat * 4)
        self.gopigo3.set_speed(figure8speed)
        self.gopigo3.steer(20, 100)
        sleep(beat * 4)
        
        """Beat 102"""
        self.gopigo3.set_speed(turn90Deg)
        self.gopigo3.steer(-100, 100)
        sleep(beat*8)
                
        self.gopigo3.set_speed(turn90Deg)
        self.gopigo3.steer(100, -100)
        sleep(beat*2)
        
        """Beat 112"""
        self.gopigo3.set_speed(figure8speed)
        self.gopigo3.steer(20, 100)
        sleep(beat * 4)
        self.gopigo3.set_speed(figure8speed)
        self.gopigo3.steer(100, 20)
        sleep(beat * 4)
        
        """Beat 120"""
        self.gopigo3.set_speed(turn90Deg)
        self.gopigo3.steer(-100, 100)
 

        self.gopigo3.set_right_eye_color((255,0,0))
        self.gopigo3.set_left_eye_color((0,0,255))
        self.gopigo3.close_eyes()
        self.gopigo3.open_eyes()
        sleep(beat)
        self.gopigo3.set_right_eye_color((0,255,0))
        self.gopigo3.set_left_eye_color((255,0,0))
        self.gopigo3.close_eyes()
        self.gopigo3.open_eyes()
        sleep(beat)
        self.gopigo3.set_right_eye_color((0,0,255))
        self.gopigo3.set_left_eye_color((0,255,0))
        self.gopigo3.close_eyes()
        self.gopigo3.open_eyes()
        sleep(beat)
        self.gopigo3.set_right_eye_color((255,255,255))
        self.gopigo3.set_left_eye_color((255,255,255))
        self.gopigo3.close_eyes()
        self.gopigo3.open_eyes()
        sleep(beat)
            
        finishCounter = 0
        self.gopigo3.set_speed(turn90Deg)
        self.gopigo3.steer(100, -100)
        
        
        self.gopigo3.set_right_eye_color((255,0,0))
        self.gopigo3.set_left_eye_color((0,0,255))
        self.gopigo3.close_eyes()
        self.gopigo3.open_eyes()
        sleep(beat)
        self.gopigo3.set_right_eye_color((0,255,0))
        self.gopigo3.set_left_eye_color((255,0,0))
        self.gopigo3.close_eyes()
        self.gopigo3.open_eyes()
        sleep(beat)
        self.gopigo3.set_right_eye_color((0,0,255))
        self.gopigo3.set_left_eye_color((0,255,0))
        self.gopigo3.close_eyes()
        self.gopigo3.open_eyes()
        sleep(beat)
        self.gopigo3.set_right_eye_color((255,255,255))
        self.gopigo3.set_left_eye_color((255,255,255))
        self.gopigo3.close_eyes()
        self.gopigo3.open_eyes()
        sleep(beat)
        
        

        self.gopigo3.close_eyes()
        self.gopigo3.blinker_off(0)
        self.gopigo3.blinker_off(1)
        
        self.gopigo3.stop()
        self.gopigo3.set_speed(500)
        return "static"
        
        
        
        
        
        
        
        
        
        
        
        
    def _gopigo3_command_deliveraltoids(self):
        
        self.gopigo3.set_speed(300)
        
        servo = self.gopigo3.init_servo()
        
        """
        servo.rotate_servo(-160)
        sleep(2)
        servo.rotate_servo(160)
        sleep(2)
        """
        
        turn90 = 84
        
        #waypoint 1 -> 2
        self.gopigo3.drive_inches(49)
        self.gopigo3.turn_degrees(turn90)  
        
        #waypoint 2 -> 3
        self.gopigo3.drive_inches(76)
        self.gopigo3.turn_degrees(turn90-2)
        
        #waypoint 3 -> 4
        self.gopigo3.drive_inches(40)
        
        self.gopigo3.turn_degrees(turn90*2)
        self.gopigo3.drive_inches(-36)
        
        #waypoint 4 -> 5
        self.gopigo3.set_speed(100)
        self.gopigo3.drive_inches(-48)
        self.gopigo3.set_speed(300)
        self.gopigo3.turn_degrees(-turn90+2)
                
        #waypoint 5 -> 6
        self.gopigo3.drive_inches(80)
        self.gopigo3.turn_degrees(-turn90)
        
        self.gopigo3.stop()
        return "static"
