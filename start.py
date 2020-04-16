from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
import gkeepapi
import configs

def test_line_api():
    line = LineBotApi(configs.CHANNEL_ACCESS_TOKEN)
    line.push_message(to=configs.USER_ID, messages=TextSendMessage(text='Hello World!'))

if __name__ == "__main__":
    test_line_api()