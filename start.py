from api_actions import *
from html2text import html2text as htmlToText

line = None
evernote = None

def note_to_text(note):
    return htmlToText(note.content)

if __name__ == "__main__":
    line = init_line_client()
    evernote = init_evernote_client()
    
    tagged_notes = get_notes_by_tags(evernote, ['try'])
    for note in tagged_notes:
        text_in_note = note_to_text(note)
        send_message(line, text_in_note)
        