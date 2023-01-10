#coding: utf-8
from sense_hat import SenseHat
import subprocess #pythonからコマンドを実行するモジュール
import RPi.GPIO as GPIO
import dht11
import time
import datetime
from datetime import datetime
import requests
import json
import sys
from time import sleep



#ウェザーAPIキー
API_KEY = "2837135fe1e908836e35450970c54d6d"
api = "http://api.openweathermap.org/data/2.5/weather?q={city}&APPID={key}"



#部屋の状態-----------------------------------------------------------------------------------------------

fukai85 = "今の部屋の状態は、暑くてたまらない状態です。クーラーを付けるか、クーラーの温度を下げた方が良いです。"
fukai80 = "今の部屋の状態は、暑くて汗が出る状態です。クーラーを付けるか、クーラーの温度を下げた方が良いです。"
fukai75 = "今の部屋の状態は、少しだけ暑い状態です。"
fukai70 = "今の部屋の状態は、暑くはない状態です。"
fukai65 = "今の部屋の状態は、非常に心地よい状態です。"
fukai60 = "今の部屋の状態は、寒くはない状態です。"
fukai55 = "今の部屋の状態は、肌寒い状態です。"
fukai50 = "今の部屋の状態は、寒い状態です。"
fukai45 = "今の部屋の状態は、非常に寒い状態です。"
fukai40 = "今の部屋の状態は、寒くてたまらない状態です。"
humi_low = "部屋が、非常に乾燥しています。"

#温湿度センサーをインスタンス化
#instance = dht11.DHT11(pin=2)

#senseHATで温湿度を取得
sense = SenseHat()
# 色の設定
red = (255, 0, 0)
green = (0, 255, 0)
yellow = (255, 255, 0)
blue = (0, 0, 255)

yellow = (255, 255, 0)
lightgreen= (180, 230, 0)
vividgreen=(2, 230, 0)
white=(255, 255, 255)


r = (255, 0, 0)     # red
y = (255, 255, 0)   # yelloy
g = (0, 255, 0)     # gyeen
w= (255, 255, 255) # white
b=(0,0,0)

happy = [
g, g, g, g, g, g, g, g,
g, g, g, g, g, g, g, g,
g, g, b, g, g, b, g, g,
g, g, g, g, g, g, g, g,
g, g, g, g, g, g, g, g,
g, b, g, g, g, g, b, g,
g, g, b, b, b, b, g, g,
g, g, g, g, g, g, g, g
]

sad = [
r, r, r, r, r, r, r, r,
r, r, r, r, r, r, r, r,
r, r, b, r, r, b, r, r,
r, r, r, r, r, r, r, r,
r, r, r, r, r, r, r, r,
r, r, b, b, b, b, r, r,
r, b, r, r, r, r, b, r,
r, r, r, r, r, r, r, r
]

normal = [
y, y, y, y, y, y, y, y,
y, y, y, y, y, y, y, y,
y, y, b, y, y, b, y, y,
y, y, y, y, y, y, y, y,
y, y, y, y, y, y, y, y,
y, b, b, b, b, b, b, y,
y, y, y, y, y, y, y, y,
y, y, y, y, y, y, y, y
]


#一度のみ実行させる
i = 0
try:
    while i < 1:
      # セ温度と湿度、気圧を測定
        t = sense.get_temperature()
        p = sense.get_pressure()
        h = sense.get_humidity()
        # 小数点以下第1位に四捨五入
        t = round(t, 1)-12
        p = round(p, 1)
        h = round(h, 1)

        #不快指数を求める
        fukai = 0.81 * t + 0.01 * h * (0.99 * t -14.3) + 46.3
        print(fukai)
        i += 1
except KeyboardInterrupt:
      sense.clear() 

#取得した値をテキスト化
temp_say = str(t)
humi_say = str(h)
#不快指数を四捨五入
fukai_say_round = round(fukai,1)
#不快指数をテキスト化
fukai_room = str(fukai_say_round)

roomTempText = "只今の部屋の温度は" + temp_say + "度,"
roomHumiText = "湿度" + humi_say + "パーセントです。"
#say = str(roomTempText + roomHumiText)
fukai_roomText = "不快指数は、" + fukai_room + "です。"
print(roomTempText)
print(roomHumiText)
print(fukai_roomText)

#部屋の温度
roomTemp = round(t)
#部屋の湿度
roomHumi = round(h)

if fukai_say_round >= 70 & roomHumi > 60:
    subprocess.run('/home/pi/Desktop/raspi-factory/thTalk-room/talkingRoomScript1.sh',shell=True,check=True)
    res = subprocess.run('/home/pi/Desktop/raspi-factory/line/lineScript1.sh',shell=True,check=True)
    print(res)
    sense.set_pixels(sad)

elif fukai_say_round >= 70 & roomHumi <= 60:
    subprocess.run('/home/pi/Desktop/raspi-factory/thTalk-room/talkingRoomScript2.sh',shell=True,check=True)
    res = subprocess.run('/home/pi/Desktop/raspi-factory/line/lineScript2.sh',shell=True,check=True)
    print(res)
    sense.set_pixels(normal)

elif fukai_say_round < 70 & roomTemp < 18 :
    subprocess.run('./thTalk-room/talkingRoomScript3.sh',shell=True,check=True)
    res = subprocess.run('/home/pi/Desktop/raspi-factory/line/lineScript3.sh',shell=True,check=True)
    print(res)
    sense.set_pixels(sad)

else:
    sense.set_pixels(happy)



#外気温-----------------------------------------------------------------------------------------

#APIで外気温を取得
city_name = "Fukuoka-shi"
url = api.format(city = city_name, key = API_KEY)
response = requests.get(url)
data = json.loads(response.text)
k2c = lambda k: k - 273.15

temp = k2c(data["main"]["temp"])
hum = data["main"]["humidity"]
round_temp = round(temp,1)

#外の不快指数を求める
fukai = 0.81 * temp + 0.01 * hum * (0.99 * temp -14.3) + 46.3
round_fukai = round(fukai)

time.sleep(2)

otherTempText = "只今の外の気温は、"+ str(round_temp)+ "度"
otherHumiText = "湿度" + str(hum)+ "パーセント"
fukai_otherText = "不快指数は、" + str(round_fukai)+ "です。"

print(otherTempText)
print(otherHumiText)
print(fukai_otherText)


if round_fukai > 80:
    res = subprocess.run('/home/pi/Desktop/raspi-factory/thTalk-other/talking80.sh',shell=True,check=True)
    print(res)
elif round_fukai > 76:
    res = subprocess.run('/home/pi/Desktop/raspi-factory/thTalk-other/talking70.sh',shell=True,check=True)
    print(res)
elif round_fukai > 61:
    res = subprocess.run('/home/pi/Desktop/raspi-factory/thTalk-other/talking65.sh',shell=True,check=True)
    print(res)
elif round_fukai > 49:
    res = subprocess.run('/home/pi/Desktop/raspi-factory/thTalk-other/talking60.sh',shell=True)
    print(res)
else:
    res = subprocess.run('/home/pi/Desktop/raspi-factory/thTalk-other/talking50.sh',shell=True,check=True)
    print(res)

x = float(temp_say)
y = float(round_temp)
roomTemperature = round(t)#室温
outsideTemperature = round(y)#外気温
#print(roomTemperature)
#print(outsideTemperature)

#室温と外気温の差を求める
difference = roomTemperature - outsideTemperature
#差分をテキスト化
strDifference = str(difference)

print("室内と外の気温差は" + strDifference + "以上あります。" )

intDifference = int(strDifference)

print(type(intDifference))

#室温と外気温の差が１０度以上あれば赤が点灯、以下であれば緑が点灯
if intDifference > 10:
    sense.show_message("Caution!", text_colour=white, back_colour=red, scroll_speed=0.05)
    res = subprocess.run('/home/pi/Desktop/raspi-factory/line/line-alert.sh',shell=True,check=True)
    print(res)

    sleep(1)
    sense.clear()
    
else:
    sense.show_message("OK!", text_colour=white, back_colour=blue, scroll_speed=0.05)
    res = subprocess.run('/home/pi/Desktop/raspi-factory/line/line-alert-under10.sh',shell=True,check=True)
    print(res)
    sleep(1)
    sense.clear()


#３秒後処理を止める
sleep(3)
