#!/bin/python
# *- coding: utf8 -*

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

import fileinput

#############################################################################
# Latex formatting
#############################################################################

class Latex:
    def section(self, heading):
        print("\\section{%s}" % (heading))
        #print("\\twocolumn")

    def end_section(self, heading):
        #print("\\onecolumn")
        print("\\newpage") # Try \pagebreak

    def subsection(self, heading):
        print("\\subsection{%s}" % (heading))

    def line(self, text):
        print("%s\\\\" % (text))

    def header (self, title, author):
        print("\\documentclass[10pt,draft,twocolumn]{article}")
        print("\\usepackage[latin1]{inputenc}")
        print("\\usepackage{geometry}")
        print("\\geometry{a4paper}")
        print("\\usepackage{sectsty}")
#        print("\\usepackage{draftwatermark}")
#        print("\\SetWatermarkText{Confidential}")
#        print("\\SetWatermarkScale{5}")
        print("\\title{%s}" % (title))
        print("\\author{%s}" % (author))
        print("\\date{}")
        print("\\begin{document}")
        

    def trailer (self):
        print("\\end{document}")
        
#############################################################################
# Format input as TSV
#############################################################################

def format_tsv (formatter):
    "Format a TSV file read from stdin and a latex document"
    formatter.header ("Conjugations (DRAFT)", "...")
    count=0
    last_section=None
    last_subsection=None
    for line in fileinput.input():
        # TODO Currently this is only set up to wotk with 'conjugation.py'
        columns=line.split ('\t')
        section=columns[0] + " (" + columns[1] + ")"
        subsection=columns[2]
        value=columns[3]
        if count > 0:
            if section != last_section:
                if section is not None:
                    formatter.end_section(section)
                formatter.section(section)
                last_section=section
                last_subsection=None
            if subsection != last_subsection:
                formatter.subsection(subsection)
                last_subsection=subsection
            formatter.line(value)
        count=count+1
    formatter.trailer ()

format_tsv(Latex())
