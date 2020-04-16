from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

import evernote.edam.userstore.constants as UserStoreConstants
import evernote.edam.type.ttypes as Types
from evernote.api.client import EvernoteClient
import hashlib, binascii

import os, sys, argparse
import configs

line = None
evernote = None
def init_line_client():
    global line
    line = LineBotApi(configs.CHANNEL_ACCESS_TOKEN)
    
def init_evernote_client():
    global evernote
    evernote = EvernoteClient(token=configs.EVERNOTE_SANDBOX_ACCESS_TOKEN, sandbox=True,china=False)
    user_store = evernote.get_user_store()
    version_ok = user_store.checkVersion(
        "Python 3.x Application",
        UserStoreConstants.EDAM_VERSION_MAJOR,
        UserStoreConstants.EDAM_VERSION_MINOR
    )
    if not version_ok:
        print('Incompatible protocol, terminate application')
        exit(1)

def test_line_api():
    print('== Begin testing LINE API')
    init_line_client()
    line.push_message(to=configs.USER_ID, messages=TextSendMessage(text='Hello World!'))
    print('Push message to chat')
    print('== Finish testing LINE API')

def test_evernote_api():
    print('== Begin testing Evernote API')
    init_evernote_client()
    note_store = evernote.get_note_store()
    notebooks = note_store.listNotebooks()
    print("Found ", len(notebooks), " notebooks:")

def test():
    test_line_api()
    test_evernote_api()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--test', action='store_true')
    options = parser.parse_args()

    if options.test:
        test()
        exit(0)
    

