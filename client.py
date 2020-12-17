#!/usr/bin/python
# -*- coding:utf-8 -*-
from frontend import DISPLAYS
from frontend.tracking import TrackingScreen
from remote import RemoteControlThread
from client import SocketClient
from threading import Thread
import time
import sys, signal
import config

import waveshare
from pi import ButtonSensor

output_property = config.properties.output_type
remote_properties = getattr(config.properties, 'remote', None) 
pi_properties = getattr(config.properties, 'pi_gpio', None) 

debug = len(sys.argv) > 1 and sys.argv[1] == 'debug'

if __name__ == "__main__":
    socket_client = SocketClient()
    output = DISPLAYS[output_property]
    tracking_screen = TrackingScreen(socket_client, output=output)

    def signal_handler(sig, frame):
        sys.exit(0)

    signal.signal(signal.SIGTERM, signal_handler)

    while True:
        try:
            print('connect')
            socket_client.start()
            break
        except Exception as e:
            print(e)
            pass
        time.sleep(1)

    def reset_exercise():
            socket_client.emit('reset_exercise')
        
    def toggle_pause_exercise():
        socket_client.emit('toggle_pause')

    def wake():
        output.switch_backlight(True)
            
        def delay_and_switch_off():
            time.sleep(10)
            if not tracking_screen.is_idle:
                output.switch_backlight(False)

        Thread(daemon=True, target=delay_and_switch_off)

    def button_name_to_lambda(button_name):
        if button_name == 'reset_button':
            return reset_exercise
        elif button_name == 'pause_button':
            return toggle_pause_exercise
        elif button_name == 'wake_button':
            return wake

    if remote_properties:
        button_to_action = {}

        for key, value in vars(remote_properties.buttons).items():
            button_to_action[value] = button_name_to_lambda(key)

        def on_button_clicked(button, state):
            if debug:
                print(button, state)
            
            action = button_to_action.get(button)

            if action and state == 0:
                action()
                
        RemoteControlThread(remote_properties.device_id, on_button_clicked, debug=debug).start()

    if pi_properties:
        pin_to_action = {}

        for key, value in vars(pi_properties.buttons).items():
            pin_to_action[value.pin] = button_name_to_lambda(key)

        def on_pin(pin: int):
            action = pin_to_action.get(pin)
            if action:
                action()

        ButtonSensor(vars(pi_properties.buttons).values(), on_pin=on_pin)
