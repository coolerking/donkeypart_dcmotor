# -*- coding: utf-8 -*-
"""
テスト用ダミークラス
"""
OUTPUT = 1

class pi:
    def __init__(self):
        self.pins = {}
    def set_mode(self, pin, value):
        self.pins[str(pin) + '_mode'] = value
        print('set {} mode at gpio[{}]'.format(str(value), str(pin)))
    def get_mode(self, pin):
        return self.pins[str(pin) + '_mode']
    def set_PWM_range(self, pin, range_size):
        self.pins[str(pin) + '_range'] = range_size
        print('set pwm {} Hz at gpio[{}]'.format(str(range_size), str(pin)))
    def get_PWM_range(self, pin):
        return self.pins[str(pin) + '_range']
    def set_PWM_frequency(self, pin, freq):
        self.pins[str(pin) + '_freq'] = freq
        print('set pwm {} freq at gpio[{}]'.format(str(freq), str(pin)))
    def get_PWM_frequency(self, pin):
        return self.pins[str(pin) + '_freq']
    def set_PWM_dutycycle(self, pin, dutycycle):
        self.pins[str(pin) + '_dutycycle'] = dutycycle
        print('set pwm dity cycle {} at gpio[{}]'.format(str(dutycycle), str(pin)))
    def get_PWM_dutycycle(self, pin):
        return self.pins[str(pin) + '_dutycycle']
    def write(self, pin, value):
        self.pins[str(pin) + '_value'] = value
        print('set {} value at gpio[{}]'.format(str(value), str(pin)))
    def read(self, pin):
        return self.pins[str(pin) + '_value']
    def stop(self):
        self.pins = {}
        print('stop called')