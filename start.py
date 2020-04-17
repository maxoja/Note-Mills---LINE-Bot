from flask import Flask, request, abort
from api_actions import *
from html2text import html2text as htmlToText

line = init_line_client()
handler = init_line_webhook()
evernote = init_evernote_client()

def note_to_text(note):
    return htmlToText(note.content)

app = Flask(__name__)

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
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))

if __name__ == "__main__":    
    tagged_notes = get_notes_by_tags(evernote, ['try'])
    for note in tagged_notes:
        text_in_note = note_to_text(note)
        send_message(line, text_in_note)

    app.run()