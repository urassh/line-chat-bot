from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('1KEXCm11CDNYf+NpkVPFD5Vx68bE44mi4ZtaazDY4ZGcL5ViY24flQvlgMv61IkJH3sBsfTG+r2SxqDEtG7DXmUoMfvTHrurfoeeDuwV+hzImgNGp5dOazwnKoaqIkaLd0pLC/N6B6bfcd4iKUw69wdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('5098b31cb3363ab438d328ce91f3ec19')

@app.route("/")
def test():
    return "OK"

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

from time import time
users = {}
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    userId = event.source.user_id
    if event.message.text == "勉強開始":
        reply_message = "計測を開始しました。"
        if not userId in users:
            users[userId] = {}
            users[userId]["total"] = 0
        users[userId]["start"] = time()
    elif event.message.text == "勉強終了":
        end = time()
        difference = int(end - users[userId]["start"])
        users[userId]["total"] += difference
        hour = difference // 3600
        minute = (difference % 3600) // 60
        secound = difference % 60
        reply_message = f"ただいまの勉強時間は{hour}時間{minute}分{secound}秒です。お疲れ様でした。本日は合計で{users[userId]['total']}秒勉強しています。"
    else:
        reply_message = event.message.text

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_message))


if __name__ == "__main__":
    app.run()