from flask import Flask, request
from linebot import LineBotApi, WebhookHandler
from linebot.models import (MessageEvent,
                            TextMessage,
                            TextSendMessage)

import openai
openai.api_key = "sk-proj-M3IumUoTgIFWedBGyI2WT3BlbkFJk4MT3mLGAJX9Yo8Gwtct"
model_use = "text-davinci-003"

channel_secret = "2da0ccca9798f48c1b212bf81b59ff4f"
channel_access_token = "XPglkMEPmfyyNp9VXgBoHHZPQ4chxX1tQwtfrLWLBFBWpJP2ReopfnagW+F3VchYs5Av+dZB9vHr+EgZElA99JfCqewF09iHF9nhogPRWbQYx27B9l9MG5LmQo8aA1Jenn2qA4n1382s2kWKz6D30QdB04t89/1O/w1cDnyilFU="

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def home():
    try:
        signature = request.headers["X-Line-Signature"]
        body = request.get_data(as_text=True)
        handler.handle(body, signature)
    except:
        pass
    
    return "Hello Line Chatbot"

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    text = event.message.text
    print(text)

    prompt_text = text

    response = openai.Completion.create(
        model=model_use,
        prompt=prompt_text,  
        max_tokens=1024) # max 4096

    text_out = response.choices[0].text 
    line_bot_api.reply_message(event.reply_token,
                               TextSendMessage(text=text_out))

if __name__ == "__main__":          
    app.run()

