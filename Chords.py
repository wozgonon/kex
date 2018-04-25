#! python

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
    yield chords(notes, "dim.", [0,3,6])
    yield chords(notes, "aug.",  [0,4,8])
#    yield chords(notes, "maj.7th",  [0,4,8])
#    yield chords(notes, "min.7th",  [0,4,8])

def tsv_chord_table ():
    "Generate a chord tables in Tab Separated File (TSV) format"
    for row in common_chords (notes):
        print "\n".join (["\t".join([str(s) for s in r]) for r in row])

# Generate a chord table
tsv_chord_table
