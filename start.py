from flask import Flask, request, abort
from api_actions import *
from html2text import html2text as htmlToText
from random import shuffle

line = init_line_client()
handler = init_line_webhook()
evernote = init_evernote_client()
parser = init_line_parser()

def note_to_text(note):
    body_text = htmlToText(note.content)
    body_text = body_text.replace('\n\n\n','\n')
    body_text = body_text.replace('\n\n','\n')
    body_text = body_text.replace('\n','\n\n')
    title_text = f'[ {note.title} ]'
    result = title_text + '\n\n' + body_text
    return result.strip()

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
    print('========>')
    print('Handling Event:')
    print(event)
    print()

    print('Attached Message:')
    print(event.message)
    print()

    tags =event.message.text.split(',')
    tags = [ tag.strip() for tag in tags ]
    print('Extracted Note Tags:')
    print(tags)
    print()

    notes = get_notes_by_tags(evernote, tags)
    print('Retrieved',len(notes),' Notes')
    print()

    if len(notes) == 0:
        send_message(line, "Please select an existing tag from the following")
        send_message(line, str('\n'.join(get_all_tags(evernote))))
    else:
        print('Shuffling retrieved notes ...')
        shuffle(notes)
        picked_note = notes[0]
        reply_text = note_to_text(picked_note)
        print('Picked note has content =',reply_text[:30],'...')
        send_message(line, reply_text)
    
    print('<========')

@app.route("/", methods=['GET'])
def home():
    return 'Welcome to the Home of Note Mills'

@app.route("/webhook", methods=['GET', 'POST'])
def webhook():
    if request.method == 'POST':
        return 'OK'

if __name__ == "__main__":
    send_message(line, "Bot server has started")
    app.run()