import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

# 從環境變數讀取憑證（重要！安全做法）
line_bot_api = LineBotApi(os.environ.get('LINE_CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.environ.get('LINE_CHANNEL_SECRET'))

@app.route("/")
def home():
    return "🍜 美食達人琳琳服務運行中！"

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text.lower()
    
    # 琳琳的回覆邏輯
    if any(keyword in user_message for keyword in ['推薦', '美食', '餐廳', '吃什麼']):
        reply_text = "🍜 美食達人琳琳推薦：\n\n• 中式：鼎泰豐小籠包\n• 日式：瞞著爹壽司\n• 西式：教父牛排\n• 甜點：Lady M千層蛋糕\n\n想找哪種類型呢？"
    
    elif any(keyword in user_message for keyword in ['你好', '嗨', 'hello']):
        reply_text = "👋 你好！我是美食達人琳琳～\n專門推薦各種美味餐廳！\n問我『推薦美食』吧！"
    
    elif '中式' in user_message:
        reply_text = "🥢 中式推薦：鼎泰豐、鼎王、欣葉台菜"
    
    elif '日式' in user_message:
        reply_text = "🍣 日式推薦：瞞著爹、一蘭拉麵、杏子豬排"
    
    elif '甜點' in user_message:
        reply_text = "🍰 甜點推薦：Lady M、深夜裡的法國手工甜點"
    
    else:
        reply_text = "😊 我是美食達人琳琳！可以問我：\n• 推薦美食\n• 中式/日式餐廳\n• 甜點推薦"
    
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text)
    )

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
