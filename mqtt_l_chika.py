#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time
import pigpio  # pigpioライブラリをインポートする
import paho.mqtt.client as mqtt  # MQTTのライブラリをインポート
import json  # JSONのライブラリをインポート

TOPIC = "test/001"
HOST = "localhost"
PIN = 18  # 18はGPIO18の18番です。


def runChika(interval):
    pi = pigpio.pi()  # GPIOにアクセスするためのインスタンスを作成します
    pi.set_mode(PIN, pigpio.OUTPUT)  # GPIOのモードを設定します他にINPUTとかある。
    counter = 0
    while counter < 10:
        pi.write(PIN, 1)  # GPIO18番のレベルをHIGHにします
        time.sleep(interval)
        pi.write(PIN, 0)  # GPIO18番のレベルをLOWにします
        time.sleep(interval)
        counter = counter + 1


def onConnect(client, userdata, flag, rc):  # ブローカーに接続できたときの処理
    print("Connected with result code " + str(rc))  # 接続できた旨表示
    client.subscribe(TOPIC)  # subするトピックを設定


def onDisconnect(client, userdata, flag, rc):  # ブローカーが切断したときの処理
    if rc != 0:
        print("Unexpected disconnection.")


def onMessage(client, userdata, msg):  # メッセージが届いたときの処理
    # msg.topicにトピック名が，msg.payloadに届いたデータ本体が入っている
    mq_value = json.loads(msg.payload)["value"]
    if mq_value > 0:
        runChika(mq_value)
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


if __name__ == '__main__':          # importされないときだけmain()を呼ぶ
    main()    # メイン関数を呼び出す
