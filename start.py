from flask import Flask, request, abort
from api_actions import *
from html2text import html2text as htmlToText
from random import shuffle

line = init_line_client()
handler = init_line_webhook()
evernote = init_evernote_client()
parser = init_line_parser()

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
    print('=> handling event')
    print(event)
    print('message')
    print(event.message)

    tags = "".join((char if char.isalpha() else " ") for char in event.message.text).split()
    print('extracted tags')
    print(tags)

    notes = get_notes_by_tags(evernote, tags)
    print('retrieved',len(notes),'notes')

    if len(notes) == 0:
        send_message(line, "Please select an existing tag")
    else:
        shuffle(notes)
        print('picked note')
        print(str(notes[0])[:30])
        reply_text = note_to_text(notes[0])
        print('text in note')
        print(reply_text[:30])
        send_message(line, reply_text)

@app.route("/", methods=['GET'])
def home():
    return 'Welcome Home'

@app.route("/webhook", methods=['GET', 'POST'])
def webhook():
    if request.method == 'POST':
        return 'OK'

# @handler.add(MessageEvent, message=TextMessage)
# def handle_message(event):
#     print('=> handling event')
#     print(event)
#     print('message')
#     print(event.message)
#     reply_text = 'Papuanewgini'
#     tags = event.message.text.replace(' ','').split(',')
#     notes = get_notes_by_tags(evernote, tags)
#     print('retrieved',len(notes),'notes')
# 
    # if len(notes) == 0:
    #     reply_text = 'There is no note with tag ' + str(tags)
    # else:
    #     shuffle(notes)
    #     print('after shuffle')
    #     print('first note')
    #     print(str(notes[0])[:30])
    #     reply_text = note_to_text(notes[0])
    #     print('text in note')
    #     print(reply_text[:30])
# 
    # send_message(line, reply_text)
# 
    # print('handler returning OK')
    # return 'OK'
if __name__ == "__main__":
    send_message(line, "Bot server has started")
    app.run()