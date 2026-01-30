Modified:

- Remove all language and voice selection to use the default language and voice of the system.

---

# Anki Generate Audio for Terms

This Anki add-on automatically generates audio files for vocabulary terms using your macOS system's built-in `say` command, then converts the audio to MP3 using `ffmpeg`. It's designed to make it quick and easy to add pronunciation audio to your flashcards without leaving Anki.

---

## 🔧 Requirements

- Anki 2.1.65+ (compatible with Qt6)
- macOS with the `say` command available (default on macOS)
- `ffmpeg` installed and accessible at `/opt/homebrew/bin/ffmpeg` (typically installed via Homebrew)

---

## 🚀 What It Does

- Scans selected decks in your collection for notes containing a `term` field.
- Uses macOS's `say` command to generate AIFF audio for each term.
- Converts the AIFF to MP3 using `ffmpeg`.
- Attaches the MP3 as an `[sound:filename.mp3]` reference in the note's `Audio` field.
- Skips notes with missing or empty terms.
- Optionally replaces existing audio files if desired.

---

## 🧭 How to Use

1. **Open Anki** and go to the `Tools` menu.
2. Click on **"🔊 Generate Audio for Notes"**.
3. Select one or more decks you want to scan.
4. Choose whether to replace existing audio.
5. Choose a language and voice for audio synthesis.
6. The add-on will process the notes and attach the audio automatically.

---

## 🗂 Field Requirements

Your notes should have:
- A `term` field (the word or phrase to pronounce)
- An `Audio` field (where the sound tag will be inserted)

---

## 🛠 Troubleshooting

- Make sure `ffmpeg` is installed:
  ```bash
  brew install ffmpeg
  ```
- If `say` or `ffmpeg` fails, you may see a popup with the error. Ensure both tools are installed and accessible in your system PATH.

---

## 🙏 Credits

- App designer: Frank Valenziano
- Developer: ChatGPT
- Source URL: https://github.com/frankvalenziano/AnkiAddonGenerateAudio
- Anki Package: 1056834290
---

## 📄 License

This project is licensed under the GNU General Public License v3.0.  
See the [LICENSE](LICENSE) file for full details.
