#!/bin/python
# *- coding: utf8 -*

import re

#############################################################################
# Conjugation rules
#############################################################################

pronouns=('je','tu', 'elle/il', 'nous', 'vous', 'ils/elles')
vowels=['a','â','e','ê', 'é','á','i','í','o','ó','u','ú']

def startsWithVowel(word): return word[:1] in vowels

class rule ():
    def __init__ (self, pattern, suffix, present, perfect, pluperfect, imparfait, futur, conditional, present_subjunctive, perfect_subjunctive):
        #  plus_que_parfait, futur, futur_anterior, passe_simple
        self.pattern = pattern
        self.suffix = suffix
        self.present = present
        self.perfect = perfect   # Passé composé
        self.imparfait = imparfait
        self.pluperfect = pluperfect
        self.futur = futur
        self.conditional = conditional
        self.present_subjunctive = present_subjunctive
        self.perfect_subjunctive = perfect_subjunctive

    def match (self, infinitive):
        return re.match(self.pattern, infinitive)

    def conjugate (self, infinitive, english):
        #section(infinitive + " (" + english + ")")
        yield self.conjugate_tense (infinitive, english, 'Present', self.present)
        yield self.conjugate_tense (infinitive, english, 'Passé composé', self.perfect)

        yield self.conjugate_tense (infinitive, english, 'Imparfait', self.imparfait)
        yield self.conjugate_tense (infinitive, english,  'Pluperfect', self.pluperfect)

        yield self.conjugate_tense (infinitive, english,  'Futur', self.futur)
        #self.conjugate_tense (infinitive, english,  'Futur perfect', self.futur)

        yield self.conjugate_tense (infinitive, english,  'Conditional', self.conditional)
        #self.conjugate_tense (infinitive, english,  'Conditional perfect', self.conditional)
        
        yield self.conjugate_tense (infinitive, english,  'Present subjunctive', self.present_subjunctive)
        yield self.conjugate_tense (infinitive, english,  'Perfect subjunctive', self.perfect_subjunctive)

    def conjugate_tense (self, infinitive, english, tense_name, endings):
        #subsection(tense_name)
        stem=infinitive[:-len(self.suffix.replace('-','').replace('+',''))]
        for xx in range(0,len(pronouns)):
            pronoun=pronouns[xx]
            conjugation=endings[xx].replace('-', stem).replace('+',infinitive)
            pronoun = "j'" if pronoun == 'je' and startsWithVowel(stem) else pronoun + " "
            expression=pronoun + conjugation
            yield (infinitive, english, tense_name, expression)
            #yield pronouns + " " + verb + ending
            #line(pronoun + conjugation)
            #print('')

#############################################################################
# Conjugation rules
#############################################################################

etre_present        = ('suis',     'es',       'est',      'etes',       'sommes',     'sont')
etre_subjunctive    = ('sois que', 'sois que', 'soit que', 'soyez que',  'soyons que', 'soient que')
avoir_present       = ('ai',       'as',       'a',        'avez',       'avons',      'ont')
avoir_imperfect     = ('ai',       'as',       'a',        'avez',       'avons',      'ont')
avoir_subjunctive   = ('aie que',  'aies que', 'ait que',  'ayons que',  'ayez que',   'aient que')
imparfait           = ('-ais',     '-ais',     '-ait',     '-iez',       '-ions',      '-aient')
futur               = ('+ai',      '+as',      '+a',       '+ez',        '+ons',       '+ont')
conditional         = ('+ais',     '+ais',     '+ait',     '+iez',       '+ions',      '+aiont')
present_subjunctive = ('-e que',    '-es que', '-e que',   '-iez que',   '-ions que',  '-ent que')

def use_stem (stem, endings):
    "Conjugations constructed from a stem with different endings for each pronoun"
    return [ending.replace('-', stem).replace('+', stem) for ending in endings]
    
def use_participle(participle, verb_present=avoir_present):
    "Conjugations based on a composite of a verb and a partiple"
    return tuple([avoir + ' ' + participle for avoir in verb_present])

rules = [
    rule('être', '',
         etre_present,
         use_participle('été'),
         use_stem('ét', imparfait),
         use_participle('été', avoir_imperfect), # pluperfect
         use_stem('ser', futur),
         use_stem('ser', conditional),
         etre_subjunctive,
         use_participle('été', avoir_subjunctive)),
    rule('aller', '',
         ('vais', 'va', 'va',  'allez', 'allons', 'vont'),
         use_participle('allé', etre_present),
         use_stem('all', imparfait),
         use_participle('allé', avoir_imperfect),  # pluperfect
         use_participle('ir', futur),
         use_participle('ir', conditional),
         ('aille', 'ailles', 'aille',  'alliez', 'allions', 'aillent'),
         use_participle('allé', avoir_subjunctive)),
    rule('avoir', '',
         avoir_present,
         use_participle('eu'),
         use_stem('av', imparfait),
         use_participle('eu', avoir_imperfect),  # pluperfect
         use_stem('aur', futur),
         use_stem('aur', conditional),
         avoir_subjunctive,
         use_participle('eu', avoir_subjunctive)),
    rule('faire', '',
        ('fais',   'fais', 'fait',   'faissez',  'faisson',  'font'),
         use_participle('fait'),
         use_stem('fais', imparfait),
         use_participle('fait', avoir_imperfect),  # pluperfect
         use_stem('fer', futur),  # pluperfect
         use_stem('fer', conditional),
         use_participle('fas', present_subjunctive),
         use_participle('fait', avoir_subjunctive)),
    rule('.*re', '-re',
        ('-e','-es','-e','-ons','-ez','-ent'),
         use_participle('-u'),
         imparfait,
         use_participle('-u', avoir_imperfect),  # pluperfect
         ('-rai', '-ras', '-ra', '-rez', '-rons', '-ront'),
         conditional,
         present_subjunctive,
         use_participle('-u', avoir_subjunctive)),
    rule('.*er', '-er',
         ('-e','-es','-e','-ons','-ez','-ent'),
#         ('-s','-s','','-ons','-ez','-ent'),
         use_participle('-é'),
         imparfait,
         use_participle('-é', avoir_imperfect),  # pluperfect
         futur,
         conditional,
         present_subjunctive,
         use_participle('-é', avoir_subjunctive)),
    rule('.*ir', '-ir',   # -mir, -tir, or -vir
        ('-is','-is','-it','-issons','-issez','-issent'),
         use_participle('-i'),
         imparfait,
         use_participle('-i', avoir_imperfect),  # pluperfect
         futur,
         conditional,
         present_subjunctive,
         use_participle('-i', avoir_subjunctive))
]

#############################################################################
#  Verbs
############################################################################

verbs=[
    ('être',  'to be'),
    ('avoir', 'to have'),
    ('aller', 'to go'),
    ('faire', 'to do'),

    ('aimer',   'to like'),
    ('parler',  'to speak'),
    ('visiter', 'to visit'),
    ('donner',  'to give'),

    ('attendre',  'to wait (for)'),
    ('défendre',  'to defend'),
    ('descendre', 'to descend'),
    ('entendre',  'to hear'),
    ('étendre',   'to stretch'),
    ('fondre',    'to melt'),
    ('pendre',    'to hang, suspend'),
    ('perdre',    'to lose'),
    ('prétendre', 'to claim'),
    ('rendre',    'to give back, return'),
    ('répandre',  'to spread, scatter'),
    ('répondre',  'to answer'),
    ('vendre',    'to sell'),

    ('abolir',    'to abolish'),
    ('agir',      'to act'),
    ('avertir',   'to warn'),
    ('bâtir',     'to build'),
    ('bénir',     'to bless'),
    ('choisir',   'to choose'),
    ('établir',   'to establish'),
    ('étourdir',  'to stun, deafen, make dizzy'),
    ('finir',     'to finish'),
    ('grossir',   'to gain weight, get fat'),
    ('guérir',    'to cure, heal, recover'),
    ('maigrir',   'to lose weight, get thin'),
    ('nourrir',   'to feed, nourish'),
    ('obé ir',    'to obey'),
    ('punir',     'to punish'),
    ('réfléchir', 'to reflect, think'),
    ('remplir',   'to fill'),
    ('réussir',   'to succeed'),
    ('rougir',    'to blush, turn red'),
    ('vieillir'   'to grow old')
]

#############################################################################
#  Generate a TSV conjugation table
#############################################################################

def tsv_conjugation_table (verbs, rules):
    "Generate a table of conjugations in Tab Separated File (TSV) format."
    print ("French\tEnglish\tTense\tConjugation")
    for verb in verbs:
        french = verb[0]
        english = verb[1]
        for rule in rules:
            if rule.match(french):
                for lines in rule.conjugate(french, english):
                    for line in lines:
                        print '\t'.join(line)
                break

            

tsv_conjugation_table (verbs, rules)
