import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

# 設定您的 LINE Bot 憑證
line_bot_api = LineBotApi('hPj2PfOSrL3RK2dmUEYJdgVuCbo88bS9hqSsfdWbE8E+CVOz+y1Z4qz/aN21SY6L7pO1TDItFpuu6a0gQ9X7VXnWvyxUheOi4F4Wo/+/PRaP0yaJ9vXlO6jbhLTFHFIqKpIwPgd4+hbg0VAXMnymxQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('45947b4a028c6879ec530ba9ea5fef9c')

@app.route("/")
def home():
    return "美食達人琳琳 LINE Bot 運行中！🍜"

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
    
    # 美食達人琳琳的回覆邏輯
    if any(keyword in user_message for keyword in ['推薦', '美食', '餐廳', '吃什麼']):
        reply_text = "🍜 美食達人琳琳推薦：\n\n• 中式：鼎泰豐、鼎王麻辣鍋\n• 日式：瞞著爹、三味食堂\n• 西式：Smith & Wollensky\n• 甜點：Lady M、深夜裡的法國手工甜點\n\n想找哪種類型呢？"
    
    elif any(keyword in user_message for keyword in ['你好', '嗨', 'hello', '嗨嗨']):
        reply_text = "👋 你好呀！我是美食達人琳琳～\n專門推薦各種美味餐廳和隱藏版小吃！\n問我『推薦美食』或『吃什麼』吧！"
    
    elif any(keyword in user_message for keyword in ['中式', '中餐', '台灣小吃']):
        reply_text = "🥢 中式美食推薦：\n• 鼎泰豐 - 小籠包\n• 鼎王 - 麻辣鍋\n• 欣葉 - 台菜\n• 鬍鬚張 - 滷肉飯\n• 永康牛肉麵"
    
    elif any(keyword in user_message for keyword in ['日式', '日本', '壽司', '拉麵']):
        reply_text = "🍣 日式美食推薦：\n• 瞞著爹 - 壽司\n• 一蘭 - 拉麵\n• 三味食堂 - CP值高\n• 杏子豬排\n• 鳥喜居酒屋"
    
    elif any(keyword in user_message for keyword in ['西式', '牛排', '義大利麵']):
        reply_text = "🍝 西式美食推薦：\n• Smith & Wollensky - 牛排\n• 教父牛排\n• 橘色 - 涮涮鍋\n• RAW - 創意料理"
    
    elif any(keyword in user_message for keyword in ['甜點', '蛋糕', '下午茶']):
        reply_text = "🍰 甜點推薦：\n• Lady M - 千層蛋糕\n• 深夜裡的法國手工甜點\n• 時飴 - 千層蛋糕\n• 米朗琪 - 鬆餅\n• COVA - 下午茶"
    
    else:
        reply_text = "😊 我是美食達人琳琳！可以問我：\n• 推薦美食\n• 中式/日式/西式餐廳\n• 甜點推薦\n• 吃什麼好\n\n我會給你最棒的美食建議！"
    
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text)
    )

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
