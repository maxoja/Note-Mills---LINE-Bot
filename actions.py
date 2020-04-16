from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

import evernote.edam.userstore.constants as UserStoreConstants
import evernote.edam.type.ttypes as Types
from evernote.api.client import EvernoteClient
import hashlib, binascii
import configs

def init_line_client():
    return LineBotApi(configs.CHANNEL_ACCESS_TOKEN)
    
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