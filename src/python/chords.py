#! python

#    chords.py - Generates a table of musical chords in TSV format.
#    Copyright (C) 2018  Wozgonon
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

solfege=('la', 'la#', 'si', 'do', 'do#', 're', 're#', 'me', 'fa', 'fa#', 'sol', 'sol#')
notes=('A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#')

def chords (notes, type, offsets):
    "Generates a table of notes for each chord."
    len1=len(notes)
    for chord in range(0,len1):
        notes_in_chord=[notes[(chord+offset)%len1] for offset in offsets]
        yield [notes[chord],type] + [note if note in notes_in_chord else '' for note in notes]
        
def common_chords (notes):
    "Generates tables for the common chords."
    yield [['Note', "Chord"] + list(notes)]
    yield chords(notes, "major",      [0,4,7])
    yield chords(notes, "minor",      [0,3,7])
    yield chords(notes, "per.5th",      [0,7])    # perfect 5th
    yield chords(notes, "dim.",       [0,3,6])    # diminshed
    yield chords(notes, "aug.",       [0,4,8])    # augmented
    yield chords(notes, "maj.7th",    [0,4,7,11]) # Major 7th
    yield chords(notes, "min.7th",    [0,3,7,10]) # Minor 7th
    yield chords(notes, "dom.7th",    [0,4,7,10]) # Dominant  7th
    yield chords(notes, "sus2",       [0,2,7])    # Suspended 2
    yield chords(notes, "sus4",       [0,5,7])    # Suspended 4

def tsv_chord_table ():
    "Generate a chord tables in Tab Separated File (TSV) format"
    for row in common_chords (notes):
        print("\n".join (["\t".join([str(s) for s in r]) for r in row]))

# Generate a chord table
tsv_chord_table()
