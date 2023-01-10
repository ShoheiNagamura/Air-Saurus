#coding: utf-8
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

#ブレッドボードのLEDを定義
Gr_LED = 14
Y_LED = 15
R_LED = 18

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()
GPIO.setup(Gr_LED, GPIO.OUT)
GPIO.setup(Y_LED, GPIO.OUT)
GPIO.setup(R_LED, GPIO.OUT)

#GPIO.output(Gr_LED, GPIO.LOW)
#GPIO.output(Y_LED, GPIO.LOW)
#GPIO.output(R_LED, GPIO.LOW)

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
instance = dht11.DHT11(pin=2)

#取得した値を読み込み
while True:

    for i in range(2):
        result = instance.read()
        time.sleep(0.5)
        temp = result.temperature
        time.sleep(0.5)
        humi = result.humidity
        #不快指数の計算
        fukai = 0.81 * temp + 0.01 * humi * (0.99 * temp -14.3) + 46.3
        time.sleep(1)
        if result.is_valid():
            print("Temperature: %d C" % result.temperature)
            print("Humidity: %d %%" % result.humidity)

    if humi == 0:
        continue
    else:
        break

time.sleep(2)

#取得した値をテキスト化
temp_say = str(temp)
humi_say = str(humi)
fukai_say_round = round(fukai,1)
fukai_say = str(fukai_say_round)

say1 = "只今の部屋の温度は" + temp_say + "度,"
say2 = "湿度" + humi_say + "パーセントです。"
say = str(say1 + say2)
say3 = "不快指数は、" + fukai_say + "です。"
print(say1)
print(say2)
print(say3)


#条件によってシェルスクリプトを実行
if fukai_say_round > 85:
    subprocess.call('./thTalk-room/talking85.sh',shell=True)
elif fukai_say_round > 80:
    subprocess.call('./thTalk-room/talking80.sh',shell=True)
elif fukai_say_round > 75:
    subprocess.call('./thTalk-room/talking75.sh',shell=True)
elif fukai_say_round > 70:
    subprocess.call('./thTalk-room/talking70.sh',shell=True)
    GPIO.output(R_LED, GPIO.HIGH)
elif fukai_say_round > 65:
    subprocess.call('./thTalk-room/talking65.sh',shell=True)
    GPIO.output(R_LED, GPIO.HIGH)
elif fukai_say_round > 61:
    subprocess.call('./thTalk-room/talking60.sh',shell=True)
elif fukai_say_round > 56:
    subprocess.call('./thTalk-room/talking55.sh',shell=True)
elif fukai_say_round > 51:
    subprocess.call('./thTalk-room/talking50.sh',shell=True)
elif fukai_say_round > 46:
    subprocess.call('./thTalk-room/talking45.sh',shell=True)

else:
    subprocess.call('./thTalk-room/talking40.sh',shell=True)
    print("fuga")
if humi < 40:
    subprocess.call('./thTalk-room/talkingHumiLow.sh',shell=True)



#外気温-----------------------------------------------------------------------------------------
city_name = "Fukuoka-shi"
url = api.format(city = city_name, key = API_KEY)
response = requests.get(url)
data = json.loads(response.text)
k2c = lambda k: k - 273.15

temp = k2c(data["main"]["temp"])
hum = data["main"]["humidity"]
round_temp = round(temp,1)

fukai = 0.81 * temp + 0.01 * hum * (0.99 * temp -14.3) + 46.3
round_fukai = round(fukai)

time.sleep(2)

say_temp = "只今の外の気温は、"+ str(round_temp)+ "度"
say_hum = "湿度" + str(hum)+ "パーセント"
say_fukai = "不快指数は、" + str(round_fukai)+ "です。"

print(say_temp)
print(say_hum)
print(say_fukai)


if round_fukai > 80:
    subprocess.call('./thTalk-other/talking80.sh',shell=True)

elif round_fukai > 76:
    subprocess.call('./thTalk-other/talking70.sh',shell=True)

elif round_fukai > 61:
    subprocess.call('./thTalk-other/talking65.sh',shell=True)

elif round_fukai > 49:
    subprocess.call('./thTalk-other/talking60.sh',shell=True)

else:
    subprocess.call('./thTalk-other/talking50.sh',shell=True)


x = float(temp_say)
y = float(round_temp)
roomTemperature = round(x)#室温
outsideTemperature = round(y)#外気温
print(roomTemperature)
print(outsideTemperature)

#室温と外気温の差を求める
difference = roomTemperature - outsideTemperature
print(difference)

#室温と外気温の差が１０度以上あれば黄色が点灯、以下であれば緑が点灯
if difference > 10:
    GPIO.output(Y_LED, GPIO.HIGH)
else:
    GPIO.output(Gr_LED, GPIO.HIGH)

#３秒後処理を止める
sleep(3)
#指定時間経過後、LEDを消灯させる
GPIO.output(R_LED, GPIO.LOW)
GPIO.output(Y_LED, GPIO.LOW)

