# -*- coding: utf-8 -*-
"""
pigpioパッケージを使用しないpytestモジュール。
"""
import pytest
from donkeypart_dcmotor import DCMotor
#import pigpio
from pigpio import pi




def test_constructor():
    _pi = pi()
    actual_in1 = 1
    actual_in2 = 2
    motor = DCMotor(_pi, actual_in1, actual_in2)
    assert(_pi.get_mode(actual_in1) == 1)
    assert(_pi.get_mode(actual_in2) == 1)
    assert(_pi.get_PWM_range(actual_in1) == 255)
    assert(_pi.get_PWM_range(actual_in2) == 255)
    assert(_pi.get_PWM_frequency(actual_in1) == 50)
    assert(_pi.get_PWM_frequency(actual_in2) == 50)
    assert(_pi.get_PWM_dutycycle(actual_in1) == 0)
    assert(_pi.get_PWM_dutycycle(actual_in2) == 0)

def test_run_upper_limit():
    _pi = pi()
    actual_in1 = 1
    actual_in2 = 2
    motor = DCMotor(_pi, actual_in1, actual_in2)
    motor.run(1.0, 'move')
    assert(_pi.get_PWM_dutycycle(actual_in1)==255)
    assert(_pi.get_PWM_dutycycle(actual_in2)==0)

def test_run_lower_limit():
    _pi = pi()
    actual_in1 = 1
    actual_in2 = 2
    motor = DCMotor(_pi, actual_in1, actual_in2)
    motor.run(-1.0, 'move')
    print(_pi.pins)
    assert(_pi.get_PWM_dutycycle(actual_in1)==0)
    assert(_pi.get_PWM_dutycycle(actual_in2)==255)

def test_run_zero():
    _pi = pi()
    actual_in1 = 1
    actual_in2 = 2
    motor = DCMotor(_pi, actual_in1, actual_in2)
    motor.run(0.0, 'move')
    assert(_pi.get_PWM_dutycycle(actual_in1)==0)
    assert(_pi.get_PWM_dutycycle(actual_in2)==0)

def test_run_zero_upper_limit():
    _pi = pi()
    actual_in1 = 1
    actual_in2 = 2
    motor = DCMotor(_pi, actual_in1, actual_in2)
    motor.run(0.09, 'move')
    assert(_pi.get_PWM_dutycycle(actual_in1)==0)
    assert(_pi.get_PWM_dutycycle(actual_in2)==0)

def test_run_zero_lower_limit():
    _pi = pi()
    actual_in1 = 1
    actual_in2 = 2
    motor = DCMotor(_pi, actual_in1, actual_in2)
    motor.run(-0.09, 'move')
    assert(_pi.get_PWM_dutycycle(actual_in1)==0)
    assert(_pi.get_PWM_dutycycle(actual_in2)==0)

def test_run_zero_upper_limit_in():
    _pi = pi()
    actual_in1 = 1
    actual_in2 = 2
    motor = DCMotor(_pi, actual_in1, actual_in2)
    motor.run(0.1, 'move')
    assert(_pi.get_PWM_dutycycle(actual_in1)==int(0.1*255.0))
    assert(_pi.get_PWM_dutycycle(actual_in2)==0)

def test_run_zero_lower_limit_in():
    _pi = pi()
    actual_in1 = 1
    actual_in2 = 2
    motor = DCMotor(_pi, actual_in1, actual_in2)
    motor.run(-0.1, 'move')
    assert(_pi.get_PWM_dutycycle(actual_in1)==0)
    assert(_pi.get_PWM_dutycycle(actual_in2)==int(0.1*255.0))

if __name__ == '__main__':
    test_constructor()
    test_run_lower_limit()
    test_run_upper_limit()
    test_run_zero()
    test_run_zero_lower_limit()
    test_run_zero_lower_limit_in()
    test_run_zero_upper_limit()
    test_run_zero_upper_limit_in()