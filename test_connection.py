from api_actions import *
import configs

def test_line_api():
    print('== Begin testing LINE API')
    line = init_line_client()
    line.push_message(to=configs.USER_ID, messages=TextSendMessage(text='Hello World!'))
    print('Push message to chat')
    print('== Finish testing LINE API')

def test_evernote_api():
    print('== Begin testing Evernote API')
    evernote = init_evernote_client()
    note_store = evernote.get_note_store()
    notebooks = note_store.listNotebooks()
    print("Found ", len(notebooks), " notebooks:")

def test_connection():
    test_line_api()
    test_evernote_api()

if __name__ == "__main__":
    test_connection()