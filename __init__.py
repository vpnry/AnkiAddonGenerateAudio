# __init__.py

# This file serves as the entry point for the Anki add-on that generates audio for note fields
# using macOS's built-in 'say' command and ffmpeg for conversion.

import os
import html
from bs4 import BeautifulSoup
from aqt import mw
from aqt.qt import QAction, qconnect
from aqt.utils import showInfo
from anki.notes import Note

# Importing helper utilities and modules
from .audio_utils import normalize_term, get_output_paths, synthesize_audio, convert_to_mp3
from .audio_generation_mode import get_generation_mode
from .note_updates import process_notes, process_selected_notes
from .select_deck import select_decks
from aqt import gui_hooks

def generate_audio_for_note(note: Note, replace_existing=False):
    """Generate audio for a single Anki note's 'term' field using the system default voice."""
    term = note["term"].strip() if "term" in note else ""
    unescaped = html.unescape(term)
    soup = BeautifulSoup(unescaped, "html.parser")
    term = soup.get_text().strip()

    if not term:
        showInfo("⚠️ Skipped a note because the 'term' field was empty.")
        return

    media_dir = mw.col.media.dir()
    temp_aiff_path, media_path, filename = get_output_paths(term, media_dir)

    if os.path.exists(media_path) and not replace_existing:
        return

    try:
        synthesize_audio(term, temp_aiff_path)
        convert_to_mp3(temp_aiff_path, media_path)
    except Exception as e:
        showInfo(f"❌ Error generating audio for '{term}': {e}")
    finally:
        if os.path.exists(temp_aiff_path):
            os.remove(temp_aiff_path)

    note["Audio"] = f"[sound:{filename}]"
    note.flush()

def run_audio_generation():
    """Initiate the audio generation process by walking the user through options."""
    selected_decks = select_decks()
    if not selected_decks:
        return

    replace = get_generation_mode()
    if replace is None:
        return

    process_notes(replace, generate_audio_for_note, selected_decks)

def generate_audio_for_selected_browser_notes(browser):
    """Generate audio for notes selected in the browser."""
    note_ids = browser.selected_notes()
    if not note_ids:
        showInfo("Please select at least one note.")
        return

    replace = get_generation_mode()
    if replace is None:
        return

    process_selected_notes(note_ids, replace, generate_audio_for_note)

def on_browser_menus_did_init(browser):
    """Add a menu item to the Browser's Edit menu."""
    action = QAction("🔊 Generate Audio for Selected Notes", browser)
    qconnect(action.triggered, lambda: generate_audio_for_selected_browser_notes(browser))
    browser.form.menuEdit.addAction(action)

# Register callbacks
gui_hooks.browser_menus_did_init.append(on_browser_menus_did_init)

# Register a menu item in Anki's Tools menu
action = QAction("🔊 Generate Audio for Notes", mw)
qconnect(action.triggered, run_audio_generation)
mw.form.menuTools.addAction(action)