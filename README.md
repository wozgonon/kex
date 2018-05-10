# Kex

Some simple example programs in python.

## To build

```
$ cd src/python
$ make
```


## chords.py

Generates a table of [Musical Chords](https://en.wikipedia.org/wiki/Chord_(music)).
This is generated as [TSV](https://en.wikipedia.org/wiki/Tab-separated_values) which
can then be formatted by importing into a Spreadsheet or by piping into another programming.

```
$ ./chords.py > Chords.tsv
$ ./chords.py | tsvhtml > Chords.html
```

## conjugation.py

Generates a table of verb conjugations for French and Dutch:

```
$ cat ../test/french-verbs.tsv | ./conjugation.py > french-conjugations.tsv
$ cat ../test/french-verbs.tsv | ./conjugation.py | ./tsv2latex.py > french-conjugations.tsv && pdflatex french-conjugations.tsv
```

Generates a table of French verb conjugations:

```
$ cat ../test/dutch-verbs.tsv | ./conjugation.py > dutch-conjugations.tsv
$ cat ../test/dutch-verbs.tsv | ./conjugation.py | ./tsv2latex.py > dutch-conjugations.tex && pdflatex dutch-conjugations.tsv
```

## tsv2latex.py

A program that converts a TSV file to a latex document.
Latex can be converted directly into PDF, so this provides
a simple tool to generate PDF files.

To create a .tex file from a TSV file:

```
$ cat ../test/dutch-verbs.tsv | ./conjugation.py | ./tsv2latex.py > dutch-conjugations.tex
```

To create a PDF file directly from a TSV file:

```
$ cat ../test/french.tsv | ./conjugation.py | ./tsv2latex.py | pdflatex > conjugation.pdf
```

To create a .tex file from a TSV file, then create a PDF.

```
$ cat ../test/french.tsv | ./conjugation.py | ./tsv2latex.py > conjugation.tex && pdflatex conjugation.tex
```