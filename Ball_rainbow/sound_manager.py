import mido
import pygame.midi
import time
from random import randint

class SoundManager:

    def __init__(self):
        pygame.midi.init()
        self.player = pygame.midi.Output(0)
        self.player.set_instrument(0)

        self.notes = []
        self.index = 0
        self.active_notes = []  # [(note, time_started)]

        self.music_file = f"Sounds/Musics/music{randint(1, 4)}.mid"
        #self.music_file = f"Sounds/Musics/music4.mid"
        self._extract_notes(self.music_file)

    def _extract_notes(self, midi_file_path):
        mid = mido.MidiFile(midi_file_path)
        for msg in mid:
            if not msg.is_meta and msg.type == 'note_on' and msg.velocity > 0:
                self.notes.append(msg.note)

    def note(self):
        if self.index >= len(self.notes):
            self.index = 0
        note = self.notes[self.index]
        self.player.note_on(note, velocity=100)
        self.active_notes.append((note, time.time()))
        self.index += 1

    def update(self):
        now = time.time()
        to_stop = []
        for note, start_time in self.active_notes:
            if now - start_time > 0.5:
                self.player.note_off(note, velocity=100)
                to_stop.append((note, start_time))
        for note in to_stop:
            self.active_notes.remove(note)

    def reset(self):
        self.index = 0
        self.active_notes.clear()

    def close(self):
        self.player.close()
        pygame.midi.quit()