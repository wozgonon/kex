# Kex

Some simple example programs.


## chords.py

Generates a table of [Musical Chords](https://en.wikipedia.org/wiki/Chord_(music)).
This is generated as [TSV](https://en.wikipedia.org/wiki/Tab-separated_values) which
can then be formatted by importing into a Spreadsheet or by piping into another programming.

```
$ ./Chords.py > Chords.tsv
$ ./Chords.py | tsvhtml > Chords.html
```

## conjugation.py

Generates a table of French verb conjugations:

```
$ ./conjugation.py > conjugation.tsv
$ ./conjugation.py | ./tsv2latex.py > conjugation.tex
$ ./conjugation.py | ./tsv2latex.py | pdflatex > conjugation.pdf
```

## tsv2latex.py

A program that converts a TSV file to a latex document.
Latex can be converted directly into PDF, so this provides
a simple tool to generate PDF files.

To create a .tex file from a TSV file:

```
$ ./conjugation.py | ./tsv2latex.py > conjugation.tex
```

To create a PDF file directly from a TSV file:

```
$ ./conjugation.py | ./tsv2latex.py | pdflatex > conjugation.pdf
```
