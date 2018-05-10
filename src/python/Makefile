
all:	chords.tsv french-conjugations.pdf dutch-conjugations.pdf

chords.tsv: chords.py
	 ./chords.py  > $@

chords.html: chords.tsv
	 cat $< | tsvhtml > $@

french-conjugations.tex: ../test/french-verbs.tsv
	cat $< | ./conjugation.py | ./tsv2latex.py > $@

french-conjugations.pdf: french-conjugations.tex
	pdflatex $<

dutch-conjugations.tex: ../test/dutch-verbs.tsv
	cat $< | ./conjugation.py | ./tsv2latex.py > $@

dutch-conjugations.pdf: dutch-conjugations.tex
	pdflatex $<

clean:
	rm -f dutch-conjugations.* french-conjugations.* chords.tsv chords.html *.log *.aux *.tex *.pdf

