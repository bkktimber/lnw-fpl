import os
import pytz
from datetime import datetime
from flask import Flask, request
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookHandler
from linebot.models import TextSendMessage
from linebot.exceptions import InvalidSignatureError

from utils.read_fpl_data import get_match_deadlines, read_json_file

load_dotenv()

CHANNEL_ACCESS_TOKEN = os.getenv('CHANNEL_ACCESS_TOKEN')
CHANNEL_SECRET = os.getenv('CHANNEL_SECRET')
FPL_DATA_FILE = os.getenv('FPL_DATA_FILE')

app = Flask(__name__)

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

data = read_json_file(FPL_DATA_FILE)

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    # Not applicable for Dialogflow
    # signature = request.headers['User-Agent']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # print(body)

    r = request.get_json(silent=True, force=True)
    intent_name = r["queryResult"]["intent"]["displayName"]
    text = r['originalDetectIntentRequest']['payload']['data']['message']['text']
    reply_token = r['originalDetectIntentRequest']['payload']['data']['replyToken']
    user_id = r['originalDetectIntentRequest']['payload']['data']['source']['userId']
    user_display_name = line_bot_api.get_profile(user_id).display_name
    
    print('id = ' + user_id)
    print('name = ' + user_display_name)
    print('text = ' + text)
    print('intent = ' + intent_name)
    print('reply_token = ' + reply_token)

    reply(intent_name, text, reply_token, user_id, user_display_name)
    return 'OK'


def reply(intent, text, reply_token, id, disname):
    if intent == 'deadline-alert':
        gw_deadlines = get_match_deadlines(data)
        bkk_tz = pytz.timezone('Asia/Bangkok')
        dt_deadline = datetime.fromtimestamp(gw_deadlines[0][1], tz=pytz.utc)
        deadline = dt_deadline.astimezone(bkk_tz).strftime('%d %b %Y %I:%M %p')
        message_body = f'Next deadline is on {deadline}'
        text_message = TextSendMessage(text=message_body)
        line_bot_api.reply_message(reply_token, text_message)


def push_message(message_body=''):
    text_message = TextSendMessage(text=message_body)
    line_bot_api.push_message(id, text_message)

if __name__ == "__main__":
    app.run(debug=True)

