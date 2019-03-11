# -*- coding: utf-8 -*-
"""
DCMotorクラスをパーツとして登録するサンプルコード。
"""
import pigpio
import donkeycar as dk

from donkeycar.parts.clock import Timestamp
from donkeycar.parts.camera import PiCamera
from donkeycar.parts.datastore import TubWriter

def drive(cfg):
    V = dk.vehicle.Vehicle()

    clock = Timestamp()
    V.add(clock, outputs=['timestamp'])

    cam = PiCamera(resolution=cfg.CAMERA_RESOLUTION)
    V.add(cam, outputs=['cam/image_array'], threaded=True)

    # 略
    V.mem['recording'] = True

    # JoyStickやWebControllerを改変し、以下の値をVehicleフレームワークの
    # メモリ上に格納する
    # .../value -1.0～1.0までの入力値→DCモータに加わる電圧になる
    # .../status 'move':前後動 'free':動力なし 'brake':制動停止

    # 以下両モータ半速前進する入力値をダミーとして投入
    V.mem['user/left/value'] = 0.5
    V.mem['user/left/status'] = 'move' # 'free' 'brake'
    V.mem['user/right/value'] = 0.5
    V.mem['user/right/status'] = 'move' # 'free' 'brake'


    # 対象Raspberry Pi上のpigpiodと通信するオブジェクト
    # 複数モータを使用する場合は、同じオブジェクトをそれぞれコンストラクタへ渡す
    # 但し、GPIOピンは重複させることはできない
    pi = pigpio.pi()

    # DCモータ1基ごとに1つのDCMotorインスタンスとして管理
    from donkeypart_dc130ra import DCMotor
    left_motor = DCMotor(pi, cfg.LEFT_MOTOR_IN1_GPIO, cfg.LEFT_MOTOR_IN2_GPIO)
    right_motor = DCMotor(pi, cfg.RIGHT_MOTOR_IN1_GPIO, cfg.RIGHT_MOTOR_IN2_GPIO)

    # Vehicleフレームワークへ登録
    V.add(left_motor,
          inputs=['user/left/value', 'user/left/status'])
    V.add(right_motor,
          inputs=['user/right/value', 'user/right/status'])


    # Tubデータ・フォーマットも変更しなくてはならない
    inputs = ['cam/image_array', 'user/left/value', 'user/left/status', 
        'user/right/status', 'user/right/status', 'timestamp']
    types = ['image_array', 'float', 'str',  'float', 'str', 'str']


    # single tub
    tub = TubWriter(path=cfg.TUB_PATH, inputs=inputs, types=types)
    V.add(tub, inputs=inputs, run_condition='recording')

    # run the vehicle
    V.start(rate_hz=cfg.DRIVE_LOOP_HZ,
            max_loop_count=cfg.MAX_LOOPS)

if __name__ == '__main__':
    cfg = dk.load_config()
    drive(cfg)