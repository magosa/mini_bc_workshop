#!usr/bin/env python
# -*- coding: utf-8 -*-

import paho.mqtt.client as mqtt     # MQTTのライブラリをインポート
import pigpio
import json
import time

TOPIC = "test/001"
SENSOR = 18


def onConnect(client, userdata, flag, rc):  # ブローカーに接続できたときの処理
    print("Connected with result code " + str(rc))


def onDisconnect(client, userdata, flag, rc):  # ブローカーが切断したときの処理
    if rc != 0:
        print("Unexpected disconnection.")


def onPublish(client, userdata, mid):  # publishが完了したときの処理
    print("publish: {0}".format(mid))


def main():  # メイン関数   この関数は末尾のif文から呼び出される
    client = mqtt.Client()                 # クラスのインスタンス(実体)の作成
    client.on_connect = onConnect         # 接続時のコールバック関数を登録
    client.on_disconnect = onDisconnect   # 切断時のコールバックを登録
    client.on_publish = onPublish         # メッセージ送信時のコールバック

    client.connect("localhost", 1883, 60)  # 接続先は自分自身

    pi = pigpio.pi()
    pi.set_mode(SENSOR, pigpio.INPUT)
    pi.set_pull_up_down(SENSOR, pigpio.PUD_DOWN)

    # 通信処理スタート
    client.loop_start()    # subはloop_forever()だが，pubはloop_start()で起動だけさせる

    json_str = {}
    # 永久に繰り返す
    while True:
        json_str['value'] = pi.read(SENSOR)
        json_str['datetime'] = time.time()
        json_str['publisher'] = "infrared01"
        payload = json.dumps(json_str, ensure_ascii=False, indent=4)
        client.publish(TOPIC, payload)    # トピック名とメッセージを決めて送信
        time.sleep(5)   # 5秒待つ


if __name__ == '__main__':          # importされないときだけmain()を呼ぶ
    main()    # メイン関数を呼び出す
