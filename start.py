from actions import *

line = None
evernote = None

if __name__ == "__main__":
    line = init_line_client()
    evernote = init_evernote_client()
    
    tagged_notes = get_notes_by_tags(evernote, ['try'])