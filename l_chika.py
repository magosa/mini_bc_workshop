#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time
import pigpio  # pigpioライブラリをインポートする

# 18はGPIO18の18番です。
PIN = 18


def main():
    pi = pigpio.pi()  # GPIOにアクセスするためのインスタンスを作成します
    pi.set_mode(PIN, pigpio.OUTPUT)  # GPIOのモードを設定します他にINPUTとかある。

    while True:
        pi.write(PIN, 1)  # GPIO18番のレベルをHIGHにします
        time.sleep(0.5)
        pi.write(PIN, 0)  # GPIO18番のレベルをLOWにします
        time.sleep(0.5)


if __name__ == '__main__':          # importされないときだけmain()を呼ぶ
    main()    # メイン関数を呼び出す
