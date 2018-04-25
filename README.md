# Kex

Some simple example programs.


## Chords.py

Generates a table of [Musical Chords](https://en.wikipedia.org/wiki/Chord_(music)).
This is generated as [TSV](https://en.wikipedia.org/wiki/Tab-separated_values) which
can then be formatted by importing into a Spreadsheet or by piping into another programming.

```
$ ./Chords.py > Chords.tsv
$ ./Chords.py | tsvhtml > Chords.html
```

