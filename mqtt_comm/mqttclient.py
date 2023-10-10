#! /bin/python3
# coding=utf-8

import paho.mqtt.client as mqtt
from pb import net2_pb2


def on_connect(client, userdata, flags, rc):
    print("Connectied with result code: " + str(rc))


def on_message(client, userdata, msg):
    data = net2_pb2.CarData()
    data.ParseFromString(msg.payload)
    print(msg.topic + " " + str(data))


# 订阅回调
def on_subscribe(client, userdata, mid, granted_qos):
    print("On Subscribed: qos = %d" % granted_qos)
    pass


# 取消订阅回调
def on_unsubscribe(client, userdata, mid):
    print("取消订阅")
    print("On unSubscribed: qos = %d" % mid)
    pass


# 发布消息回调
def on_publish(client, userdata, mid):
    print("发布消息")
    print("On onPublish: qos = %d" % mid)
    pass


# 断开链接回调
def on_disconnect(client, userdata, rc):
    print("断开链接")
    print("Unexpected disconnection rc = " + str(rc))
    pass


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish
client.on_disconnect = on_disconnect
client.on_unsubscribe = on_unsubscribe
client.on_subscribe = on_subscribe
client.connect('192.168.19.97', 1883, 600)
client.subscribe('/udi/backend/45/adv-gt-69', qos=2)
client.loop_forever()