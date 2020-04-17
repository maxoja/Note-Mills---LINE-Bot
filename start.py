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

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    print(len(events), 'events detected')

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        print('is Message Event', isinstance(event, MessageEvent))
        print('has Text Message', isinstance(event.message, TextMessage))
        print('type:', type(event))
        print()
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        # handle webhook body
        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            print("Invalid signature. Please check your channel access token/channel secret.")
            abort(400)

    print('returning OK')
    return 'OK'

@app.route("/", methods=['GET'])
def home():
    return 'Welcome Home'

@app.route("/webhook", methods=['GET', 'POST'])
def webhook():
    if request.method == 'POST':
        return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print('handling event')
    print(event)
    print('message')
    print(event.message)

    reply_text = ''
    tags = event.message.text.replace(' ','').split(',')
    notes = get_notes_by_tags(evernote, tags)

    # if len(notes) == 0:
    #     reply_text = 'There is no note with tag ' + str(tags)
    # else:
    #     shuffle(notes)
    #     reply_text = note_to_text(notes[0])

    # send_message(line, reply_text)

    print('handler returning OK')
    return 'OK'
if __name__ == "__main__":
    send_message("Bot server has started")
    app.run()