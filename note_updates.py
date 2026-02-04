# note_updates.py

from aqt import mw
from aqt.utils import showInfo
from .select_deck import is_note_in_selected_decks

def process_notes(replace, generate_audio_for_note, selected_decks=None):
    mw.checkpoint("Generate Audio")
    note_ids = mw.col.db.list("SELECT id FROM notes")
    _process_note_ids(note_ids, replace, generate_audio_for_note, selected_decks)

def process_selected_notes(note_ids, replace, generate_audio_for_note):
    mw.checkpoint("Generate Audio for Selected")
    _process_note_ids(note_ids, replace, generate_audio_for_note)

from aqt.operations import QueryOp

def _process_note_ids(note_ids, replace, generate_audio_for_note, selected_decks=None):
    def background_op(col):
        updated = 0
        total = len(note_ids)
        
        # We process notes one by one to provide progress updates
        for i, nid in enumerate(note_ids):
            # Update progress dialog
            mw.taskman.run_on_main(
                lambda: mw.progress.update(
                    label=f"Processing audio: {i+1}/{total}",
                    value=i,
                    max=total
                )
            )
            
            note = col.get_note(nid)
            if selected_decks and not is_note_in_selected_decks(note, selected_decks):
                continue
            
            if "term" in note and ("Audio" not in note or not note["Audio"].strip() or replace):
                # Note: generate_audio_for_note should be thread-safe
                generate_audio_for_note(note, replace_existing=replace)
                updated += 1
                
        return updated

    def on_success(updated):
        showInfo(f"✅ Audio generated for {updated} notes.")

    QueryOp(
        parent=mw,
        op=background_op,
        success=on_success,
    ).with_progress("Generating Audio...").run_in_background()
