# -*- coding: utf-8 -*-
"""
TA7291Pモータドライバを表すクラスを提供する。

TA7291Pは、PWMピンによる制御をおこなうことで速度調整が可能である。
TA7291Pは、Vref ピンを10kΩ抵抗経由でVcc(Pi:5V)に接続し、IN1/IN2ピンをPWM化して
速度調整を行うことができる。
しかし本クラスでは、IN1、IN2はそれぞれ通常のGPIOピン、Vrefと接続したGPIOピンを
疑似PWM化して使用する前提とする。
"""

import pigpio

class MotorDriverWithoutVref:
    '''
    TA7219Pに接続されたモータを駆動させるためのドライバクラス。
    VrefにVccより低い一定電圧をかけ、IN1/IN2をPWM化して速度調節する場合は
    こちらのクラスを使用する。
    消費するGPIOピン数を減らしたい場合に使用する(更に減らしたい場合はI2C化)。
    指定するPWM値の範囲は0～100であるが、マイナス値を指定した場合は逆転動作を
    実行する。
    '''
    def __init__(self, pi, gpio_in1, gpio_in2, pwm_range=255, pwm_freq=50):
        '''
        TA7219Pと接続されたGPIO番号をセットし、各ピンを使用可能な状態にする。
        引数：
            pi              pigpioパッケージのpiインスタンス
            gpio_in1        IN1と結線されているGPIOの番号
            gpio_in2        IN2と結線されているGPIOの番号
            pwm_range       PWM1周期を構成するクロックの個数(デフォルト255)
            pwm_freq        PWM 周波数(単位:Hz, 0以上を指定、デフォルト50Hz)
        戻り値：
            なし
        '''
        self.gpio_in1 = gpio_in1
        self.gpio_in2 = gpio_in2
        self.pi = pi
        self.pi.set_mode(self.gpio_in1,  pigpio.OUTPUT)
        self.pi.set_mode(self.gpio_in2,  pigpio.OUTPUT)
        # PWMの周波数(Hz:1秒に何回か)
        self.pwm_freq = pwm_freq
        self.pi.set_PWM_frequency(self.gpio_in1, self.pwm_freq)
        self.pi.set_PWM_frequency(self.gpio_in2, self.pwm_freq)
        # PWM1周期を構成するクロックの個数
        self.pwm_range = pwm_range
        self.pi.set_PWM_range(self.gpio_in1, self.pwm_range)
        self.pi.set_PWM_range(self.gpio_in2, self.pwm_range)
        # 初期状態、動力なし(free)にする
        self.pi.set_PWM_dutycycle(self.gpio_in1, 0)
        self.pi.set_PWM_dutycycle(self.gpio_in2, 0)
    
    def free(self):
        '''
        動力なし状態にする。
        引数：
            なし
        戻り値：なし
        '''
        self.pi.set_PWM_dutycycle(self.gpio_in1, 0)
        self.pi.set_PWM_dutycycle(self.gpio_in2, 0)
    
    def brake(self):
        '''
        制動停止状態にする。
        引数：
            なし
        戻り値：
            なし
        '''
        self.pi.set_PWM_dutycycle(self.gpio_in1, self.pwm_range)
        self.pi.set_PWM_dutycycle(self.gpio_in2, self.pwm_range)

    def move(self, input_value):
        """
        Controller/AutoPilotから入力されたアナログ値(範囲[-1.0, 1.0])に
        従ってモータを動かす。
        引数：
            input_value   float([0.0, 1.0])     DCモータへの入力値
        戻り値：
            なし
        """
        if input_value > 0:
            self._forward(self._to_duty_cycle(input_value))
        elif input_value < 0:
            self._back(self._to_duty_cycle(abs(input_value)))
        else:
            self.free()

    def _forward(self, pwm_duty_cycle):
        '''
        引数で指定された正値でモータを正転させる。
        引数：
            pwm_duty_cycle  float([0.0, 1.0])   DCモータへの入力値
        戻り値：
            なし
        '''
        self.pi.set_PWM_dutycycle(self.gpio_in1, pwm_duty_cycle)
        self.pi.set_PWM_dutycycle(self.gpio_in2, 0)

    def _back(self, pwm_duty_cycle):
        '''
        引数で指定された正値でモータを逆転させる。
        引数：
            pwm_duty_cycle  float([0.0, 1.0])   DCモータへの入力値
        戻り値：
            なし
        '''
        self.pi.set_PWM_dutycycle(self.gpio_in1, 0)
        self.pi.set_PWM_dutycycle(self.gpio_in2, pwm_duty_cycle)

    def _to_duty_cycle(self, input_value):
        """
        input_value値をduty_cycle値に変換する。
        引数：
            input_value     float([-1.0, 1.0])      DCモータへの入力値
        戻り値：
            duty_cycle      int(0～self.range)      PWM Duty Cycle値
        """
        return int(float(self.pwm_range) * float(abs(input_value)))

class MotorDriverWithVref:
    '''
    TA7219Pに接続されたモータを駆動させるためのドライバクラス。
    IN1,IN2はデジタルOUTPUTピンとし、VrefをPWM OUTPUTピンとして結線する場合
    こちらのクラスを使用する。
    PWM消費数を最小限にする場合などで使用する。
    指定するPWM値の範囲は0～100であるが、マイナス値を指定した場合は逆転動作を
    実行する。
    '''
    def __init__(self, pi, gpio_in1, gpio_in2, gpio_vref, pwm_range=255, pwm_freq=50):
        '''
        TA7219Pと接続されたGPIO番号をセットし、各ピンを使用可能な状態にする。
        引数：
            pi              pigpioパッケージのpiインスタンス
            gpio_in1        IN1と結線されているGPIOの番号(Digital OUTPUT)
            gpio_in2        IN2と結線されているGPIOの番号(Digital OUTPUT)
            gpio_vref       Vrefと結線されているGPIOの番号(PWM OUTPUT)
            pwm_range       PWM1周期を構成するクロックの個数(デフォルト255)
            pwm_freq        PWM 周波数(単位:Hz, 0以上を指定、デフォルト50Hz)
        戻り値：
            なし
        '''
        self.gpio_in1 = gpio_in1
        self.gpio_in2 = gpio_in2
        self.gpio_vref = gpio_vref
        self.pi = pi
        self.pi.set_mode(self.gpio_in1,  pigpio.OUTPUT)
        self.pi.set_mode(self.gpio_in2,  pigpio.OUTPUT)
        self.pi.set_mode(self.gpio_vref,  pigpio.OUTPUT)
        # PWMの周波数(Hz:1秒に何回か)
        self.pwm_freq = pwm_freq
        self.pi.set_PWM_frequency(self.gpio_vref, self.pwm_freq)
        # PWM1周期を構成するクロックの個数
        self.pwm_range = pwm_range
        self.pi.set_PWM_range(self.gpio_vref, self.pwm_range)
        self.pi.set_PWM_range(self.gpio_in2, self.pwm_range)
        # 初期状態、動力なし(free)にする
        self.pi.write(self.gpio_in1, 0)
        self.pi.write(self.gpio_in2, 0)
        self.pi.set_PWM_dutycycle(self.gpio_vref, 0)
    
    def free(self):
        '''
        動力なし状態にする。
        引数：
            なし
        戻り値：なし
        '''
        self.pi.write(self.gpio_in1, 0)
        self.pi.write(self.gpio_in2, 0)
        self.pi.set_PWM_dutycycle(self.gpio_vref, 0)
    
    def brake(self):
        '''
        制動停止状態にする。
        引数：
            なし
        戻り値：
            なし
        '''
        self.pi.write(self.gpio_in1, 1)
        self.pi.write(self.gpio_in2, 1)
        self.pi.set_PWM_dutycycle(self.gpio_vref, 0)

    def move(self, input_value):
        """
        Controller/AutoPilotから入力されたアナログ値(範囲[-1.0, 1.0])に
        従ってモータを動かす。
        引数：
            input_value   float([0.0, 1.0])     DCモータへの入力値
        戻り値：
            なし
        """
        if input_value > 0:
            self._forward(self._to_duty_cycle(input_value))
        elif input_value < 0:
            self._back(self._to_duty_cycle(abs(input_value)))
        else:
            self.free()

    def _forward(self, pwm_duty_cycle):
        '''
        引数で指定された正値でモータを正転させる。
        引数：
            pwm_duty_cycle  float([0.0, 1.0])   DCモータへの入力値
        戻り値：
            なし
        '''
        self.pi.write(self.gpio_in1, 1)
        self.pi.write(self.gpio_in2, 0)
        self.pi.set_PWM_dutycycle(self.gpio_vref, pwm_duty_cycle)

    def _back(self, pwm_duty_cycle):
        '''
        引数で指定された正値でモータを逆転させる。
        引数：
            pwm_duty_cycle  float([0.0, 1.0])   DCモータへの入力値
        戻り値：
            なし
        '''
        self.pi.write(self.gpio_in1, 0)
        self.pi.write(self.gpio_in2, 1)
        self.pi.set_PWM_dutycycle(self.gpio_vref, pwm_duty_cycle)

    def _to_duty_cycle(self, input_value):
        """
        input_value値をduty_cycle値に変換する。
        引数：
            input_value     float([-1.0, 1.0])      DCモータへの入力値
        戻り値：
            duty_cycle      int(0～self.range)      PWM Duty Cycle値
        """
        return int(float(self.pwm_range) * float(abs(input_value)))
