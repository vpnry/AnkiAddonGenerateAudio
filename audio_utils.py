import os
import re
import subprocess
import html
from bs4 import BeautifulSoup

def normalize_term(term):
    """
    Clean and standardize the term text for consistent audio file generation.
    Strips HTML tags/entities and replaces non-breaking spaces.
    """
    unescaped = html.unescape(term)
    soup = BeautifulSoup(unescaped, "html.parser")
    cleaned = soup.get_text().replace('\u00A0', ' ').replace('\xa0', ' ').replace('&nbsp;', ' ').strip()
    return cleaned

def get_output_paths(term, media_dir):
    """
    Generate consistent AIFF and MP3 file paths based on a sanitized version of the term.
    Returns:
        temp_aiff_path, final_mp3_path, mp3_filename
    """
    sanitized = re.sub(r"[^\w\-]", "_", term)
    filename = f"{sanitized}.mp3"
    aiff_path = os.path.join(media_dir, f"{sanitized}.aiff")
    mp3_path = os.path.join(media_dir, filename)
    return aiff_path, mp3_path, filename

def synthesize_audio(term, aiff_path):
    """
    Use macOS 'say' command to synthesize speech into an AIFF file.
    """
    subprocess.run(['say', '-o', aiff_path, term], check=True)

def convert_to_mp3(aiff_path, mp3_path):
    """
    Use ffmpeg to convert AIFF to MP3 format for Anki compatibility.
    """
    subprocess.run([
        '/opt/homebrew/bin/ffmpeg',
        '-y',
        '-i', aiff_path,
        '-codec:a', 'libmp3lame',
        '-qscale:a', '2',
        mp3_path
    ], check=True)
