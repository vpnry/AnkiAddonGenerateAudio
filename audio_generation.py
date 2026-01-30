# audio_generation.py

from anki.notes import Note
from aqt.qt import QMessageBox
from aqt import mw
from anki.hooks import addHook
from aqt.utils import askUser, showInfo, html_to_text
import os
import subprocess
import re
from bs4 import BeautifulSoup
import html

def generate_audio_for_note(note: Note, replace_existing=False):
    import time
    raw_term = note["term"] if "term" in note else ""
    print("📦 RAW TERM:", repr(raw_term))
    unescaped = html.unescape(raw_term)
    soup = BeautifulSoup(unescaped, "html.parser")
    term = soup.get_text().strip()
    print("🧽 CLEANED TERM:", repr(term))
    term = term.replace('\u00A0', ' ').replace('\xa0', ' ').replace('&nbsp;', ' ')  # Normalize all nbsp variants
    if not term:
        showInfo("⚠️ Skipped a note because the 'term' field was empty.")
        return

    sanitized_term = re.sub(r"[^\w\-]", "_", term)
    filename = f"{sanitized_term}.mp3"
    media_dir = mw.col.media.dir()
    media_path = os.path.join(media_dir, filename)
    temp_aiff_path = os.path.join(media_dir, f"{sanitized_term}_{int(time.time())}.aiff")

    if os.path.exists(media_path) and not replace_existing:
        return

    try:
        print(f"🔊 Using say command for: {term}")
        subprocess.run(['say', '-v', 'Alice', '-o', temp_aiff_path, '--data-format=LEF32@22050', term], check=True)

        print(f"🎧 Converting to mp3 with ffmpeg")
        subprocess.run(['/opt/homebrew/bin/ffmpeg', '-y', '-i', temp_aiff_path, '-codec:a', 'libmp3lame', '-qscale:a', '2', media_path], check=True)
    except subprocess.CalledProcessError as e:
        showInfo(f"❌ Error generating audio for '{term}': {e}")
    finally:
        if os.path.exists(temp_aiff_path):
            os.remove(temp_aiff_path)

    note["Audio"] = f"[sound:{filename}]"
    note.flush()

def run_audio_generation():
    replace = askUser("Do you want to replace existing audio files?", defaultno=True)
    if not replace:
        return

    media_dir = mw.col.media.dir()
    print(f"Media directory: {media_dir}")

    for note in mw.col.notes():
        generate_audio_for_note(note, replace)

addHook("profileLoaded", run_audio_generation)
