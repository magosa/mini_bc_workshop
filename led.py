#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
# GPIOのライブラリをインポート
import pigpio
# MQTTのライブラリをインポート
import paho.mqtt.client as mqtt

TOPIC = "test/001"
HOST = "localhost"


# RGBのポート番号の設定
GPIO = [17, 27, 22]

# ホワイトバランスの設定
FREQ = 100
RANGE = 255
TARGET_COLOR = [255, 255, 255]
color = [0, 0, 0]


def initLighting():
    light = pigpio.pi()
    for index, pin in enumerate(GPIO):
        # 周波数の設定
        light.set_PWM_frequency(pin, FREQ)
        # 周波数の設定
        light.set_PWM_range(pin, TARGET_COLOR[index])
        # PWMの設定(色設定)
        light.set_PWM_dutycycle(pin, TARGET_COLOR[index])
    return light


def runLighting():
    # pigpioの初期化
    light = initLighting()
    flag = True
    counter = 0
    while counter < 5:
        counter = counter + 1
        time.sleep(0.005)
        for index, pin in enumerate(GPIO):
            # PWMの設定(色の設定)
            light.set_PWM_dutycycle(pin, color[index])
            # PWMの設定(明るさ設定)
            if flag:
                if color[index] < TARGET_COLOR[index]:
                    color[index] = color[index] + 1
            else:
                if color[index] > 0:
                    color[index] = color[index] - 1
            # PWMの設定(明るさ強弱フラグの切替)
            if color == TARGET_COLOR:
                flag = False
            elif color == [0, 0, 0]:
                flag = True


def onConnect(client, userdata, flag, rc):  # ブローカーに接続できたときの処理
    print("Connected with result code " + str(rc))  # 接続できた旨表示
    client.subscribe(TOPIC)  # subするトピックを設定


def onDisconnect(client, userdata, flag, rc):  # ブローカーが切断したときの処理
    if rc != 0:
        print("Unexpected disconnection.")


def onMessage(client, userdata, msg):  # メッセージが届いたときの処理
    # msg.topicにトピック名が，msg.payloadに届いたデータ本体が入っている
    if msg.payload.value == "1":
        runLighting()
    else:
        print("Received message '" + str(msg.payload) +
              "' on topic '" + msg.topic + "' with QoS " + str(msg.qos))


def main():
    # MQTTの接続設定
    client = mqtt.Client()                 # クラスのインスタンス(実体)の作成
    client.on_connect = onConnect         # 接続時のコールバック関数を登録
    client.on_disconnect = onDisconnect   # 切断時のコールバックを登録
    client.on_message = onMessage         # メッセージ到着時のコールバック
    client.connect(HOST, 1883, 60)         # 接続先は自分自身
    client.loop_forever()                  # 永久ループして待ち続ける


if __name__ == '__main__':
    main()
