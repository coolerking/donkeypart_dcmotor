# -*- coding: utf-8 -*-
"""
DCモータをあらわすパーツクラス。
"""

from .ta7291p import MotorDriverWithoutVref

class DCMotor:
    '''
    DCモータを管理するパーツクラス。Threaded対応していないので通常のパーツとして
    扱うこと。
    '''
    def __init__(self, pi, gpio_in1, gpio_in2, gpio_vref=None, epsilone=0.1):
        '''
        TA7291P DCモータドライバと接続しているIN1,IN2およびVrefに接続されたGPIOピンを
        引数に与える。また範囲(-epsilone ～ epsilone)をゼロ値として扱う。
        引数：
            pi          pigpioパッケージのpiオブジェクト
            pu_gpios    パワーユニット用GPIO番号が格納された２次元配列
        '''
        self.pi = pi
        self.epsilone = epsilone
        self.motor = MotorDriverWithoutVref(pi, gpio_in1, gpio_in2)
        #self.motor =   .ta7291p.MotorDriverWithoutVref(pi, gpio_in1, gpio_in2, gpio_vref)

    def run(self, motor_value, motor_status):
        '''
        それぞれのモータに指示を出す。
        引数：
            motor_value      モータ動作レベル(-1.0～1.0)
            motor_status     モータステータス(move, free, brake)
        戻り値：
            なし
        '''
        # 未入力状態の場合、何もしない
        if motor_value is None:
            return

        if motor_status == 'brake':
            self.motor.brake()
        elif motor_status == 'free':
            self.motor.free()
        else:
            self.motor.move(self._add_idle(motor_value))
    
    def shutdown(self):
        '''
        シャットダウン時、各モータの動力がない状態にする。
        引数：
            なし
        戻り値：
            なし
        '''
        self.motor.free()

    def _add_idle(self, input_value):
        """
        ゼロの前後あそび(epsilone)範囲内の値をゼロとして扱う補正を加え返却する。
        引数：
            input_value     float([-1.0,1.0])   入力された値
        戻り値：
            idled_value     float([-1.0,1.0])   0近傍補正された入力値
        """
        if input_value < -1.0:
            idled_value = -1.0
        elif 1.0 < input_value:
            idled_value = 1.0
        elif self.epsilone > abs(input_value):
            idled_value = 0.0
        else:
            idled_value = input_value
        return idled_value

