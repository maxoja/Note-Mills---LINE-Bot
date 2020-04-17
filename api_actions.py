from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

import evernote.edam.userstore.constants as UserStoreConstants
import evernote.edam.type.ttypes as Types
from evernote.edam.notestore import NoteStore
from evernote.api.client import EvernoteClient
import hashlib, binascii
import configs

import math

VERY_LARGE_INT = 999999999

def init_line_client():
    return LineBotApi(configs.CHANNEL_ACCESS_TOKEN)
    
def init_line_webhook():
    return WebhookHandler(configs.CHANNEL_SECRET)
    
def init_evernote_client():
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
    return evernote

def send_message(client, text):
    client.push_message(to=configs.USER_ID, messages=TextSendMessage(text=text))

def get_notes_by_tags(client, tags=[]):
    note_store = client.get_note_store()

    tag_objs = note_store.listTags(configs.EVERNOTE_SANDBOX_ACCESS_TOKEN)

    search_filter = NoteStore.NoteFilter()
    search_filter.inactive = False
    search_filter.tagGuids = []
    [search_filter.tagGuids.append(tag.guid) for tag in tag_objs if tag.name in tags]
    
    result = note_store.findNotes(configs.EVERNOTE_SANDBOX_ACCESS_TOKEN, search_filter, 0, VERY_LARGE_INT)
    notes = result.notes
    return [note_store.getNote(configs.EVERNOTE_SANDBOX_ACCESS_TOKEN,meta.guid, True, True, True, True) for meta in notes]