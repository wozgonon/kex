OPTS=-enable-enctex

all:	chords.tsv esperanto-conjugations.pdf french-conjugations.pdf dutch-conjugations.pdf

tex:	french-conjugations.tex dutch-conjugations.tex esperanto-conjugations.tex

chords.tsv: chords.py
	 ./chords.py  > $@

chords.html: chords.tsv
	 cat $< | tsvhtml > $@

french-conjugations.tex: ../test/french-verbs.tsv ./conjugation.py
	cat $< | ./conjugation.py | ./tsv2latex.py > $@

french-conjugations.pdf: french-conjugations.tex
	xelatex $(OPTS) $<

dutch-conjugations.tex: ../test/dutch-verbs.tsv ./conjugation.py
	cat $< | ./conjugation.py | ./tsv2latex.py > $@

dutch-conjugations.pdf: dutch-conjugations.tex
	xelatex $(OPTS) $<

esperanto-conjugations.tex: ../test/esperanto-verbs.tsv ./conjugation.py
	cat $< | ./conjugation.py | ./tsv2latex.py > $@

esperanto-conjugations.pdf: esperanto-conjugations.tex
	xelatex $(OPTS) $<

clean:
	rm -f *-conjugations.*chords.tsv chords.html *.log *.aux *.tex *.pdf

