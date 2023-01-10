from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage
)

from subprocess import PIPE

import subprocess #pythonからコマンドを実行するモジュール


app = Flask(__name__)

line_bot_api = LineBotApi('99AI37RnTd/R0Ia28yMiqf1ckAHGsOxO0eT224nX8igQ78WuSNExnQCzsRqTCBeSP3MzNm4fyxxoLmJHvXGcumQSeT49uRtfcW7BtLhuO2N4dYWqreyVMCxVxDiBYf3GZRaH7ALrt65uYXUPUWbMTAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('812710815b916263bee08e22e4231866')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'



@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
        lineRes = event.message.text
        print(lineRes)
        botRes ='LEDを点けたり消したりします'
        print(botRes)

        if lineRes == '温度測定':
            exec(open("./sensor-of-HAT.py").read())
        elif lineRes == '再開':
            subprocess.run('/home/pi/Desktop/raspi-factory/start.sh',shell=True,check=True)
            print("再開")
        elif lineRes == '停止':
            subprocess.run('/home/pi/Desktop/raspi-factory/stop.sh',shell=True,check=True)
            print("停止")

        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=botRes))

if __name__ == "__main__":
    app.run()