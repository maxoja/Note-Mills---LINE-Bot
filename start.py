from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

import hashlib
import binascii
import evernote.edam.userstore.constants as UserStoreConstants
import evernote.edam.type.ttypes as Types
import os
import sys
from evernote.api.client import EvernoteClient
import argparse

import configs

def test_line_api():
    print('== Begin testing LINE API')
    line = LineBotApi(configs.CHANNEL_ACCESS_TOKEN)
    line.push_message(to=configs.USER_ID, messages=TextSendMessage(text='Hello World!'))
    print('Push message to chat')
    print('== Finish testing LINE API')

def test_evernote_api():
    print('== Begin testing Evernote API')
    client = EvernoteClient(token=configs.EVERNOTE_SANDBOX_ACCESS_TOKEN, sandbox=True,china=False)
    user_store = client.get_user_store()
    version_ok = user_store.checkVersion(
        "Evernote EDAMTest (Python)",
        UserStoreConstants.EDAM_VERSION_MAJOR,
        UserStoreConstants.EDAM_VERSION_MINOR
    )
    
    print("Is my Evernote API version up to date? ", str(version_ok),'\n')

    note_store = client.get_note_store()
    notebooks = note_store.listNotebooks()
    print("Found ", len(notebooks), " notebooks:")
    for notebook in notebooks:
        print("  * ", notebook.name)
    print('== Finish testing Evernote API')

        
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
    
