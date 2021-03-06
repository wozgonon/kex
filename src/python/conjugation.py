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

import re
import fileinput
import collections

#############################################################################
# Conjugation rules
#############################################################################

consonants="bcdfghjklmnpqrstvwxyz"
def isVowel (char):
    return char not in consonants

for vowel in ['a','â','e','ê','é','é','á','i','í','o','ó','u','ú']:
    assert(isVowel(vowel))

def startsWithVowel(word): return word[:1] not in consonants

assert(startsWithVowel('abc'))
assert(startsWithVowel('é'))
assert(not startsWithVowel('bc'))
assert(startsWithVowel('été'))
assert(startsWithVowel('étre'))

def make_stem_from_infinitive(suffix, infinitive):
    return infinitive[:-len(suffix.replace('-','').replace('+',''))]

assert(make_stem_from_infinitive('-re', 'apprendre') == 'apprend')
assert(make_stem_from_infinitive('', 'aller') == '')
assert(make_stem_from_infinitive('+er', 'donner') == 'donn')

def make_conjugation(ending, stem, infinitive):
    return ending.replace('-', stem).replace('+',infinitive)

assert(make_conjugation('-ons', 'pass', 'passer')=='passons')
assert(make_conjugation('+ai', 'pass', 'passer')=='passerai')


class Rule ():
    def __init__ (self, language, pattern, suffix, tenses): #present, perfect, imparfait, pluperfect, futur, future_perfect, conditional, present_subjunctive, perfect_subjunctive):
        # TODO plus_que_parfait, futur_anterior
        self.language = language
        self.pattern = pattern
        self.suffix = suffix
        self.tenses = tenses
        #self.present = present
        #self.perfect = perfect   # Passé composé
        #self.imparfait = imparfait
        #self.pluperfect = pluperfect
        #self.futur = futur
        #self.future_perfect = future_perfect
        #self.conditional = conditional
        #self.present_subjunctive = present_subjunctive
        #self.perfect_subjunctive = perfect_subjunctive

    def match (self, infinitive):
        return re.match(self.pattern, infinitive)

    def conjugate (self, infinitive, english):
        for name in self.tenses.keys():
            tense = self.tenses[name]
            yield self.conjugate_tense (infinitive, english, name, tense)

        # TODO  'Conditional perfect'
        # TODO  'Conditional future'
        # TODO  'Perfect subjunctive'

    def conjugate_tense (self, infinitive, english, tense_name, endings):
        #       stem=infinitive[:-len(self.suffix.replace('-','').replace('+',''))]
        stem=make_stem_from_infinitive(self.suffix, infinitive)
        for xx in range(0,len(self.language.pronouns)):
            conjugation = make_conjugation(endings[xx], stem, infinitive)
            pronoun = self.language.make_pronoun (self.language.pronouns[xx], conjugation)
            expression=pronoun + conjugation
            yield (infinitive, english, tense_name, expression)

def match_rules(rules, verb, english):
    "Match a verb against a list of rules and conjugate it using the first matching rule"
    for rule in rules:
        if rule.match(verb):
            for lines in rule.conjugate(verb, english):
                for line in lines:
                    yield line
            break

#############################################################################

languages = collections.OrderedDict()
        
#############################################################################
# Conjugation rules for the French language
#############################################################################

class French:
    def __init__(self):
        self.pronouns=('je','tu', 'elle/il', 'nous', 'vous', 'ils/elles')
        self.rules = []
        
    def make_pronoun (self, pronoun, conjugation):
        return "j'" if pronoun == 'je' and startsWithVowel(conjugation) else pronoun + " "

    def rule (self, pattern, suffix, present, perfect, imparfait, pluperfect, future, future_perfect, conditional, present_subjunctive, perfect_subjunctive):
        tenses = collections.OrderedDict()
        tenses ["Present"] = present
        tenses ["Perfect"] = perfect
        tenses ["Imparfait"] = imparfait
        tenses ["Pluperfect"] = pluperfect
        tenses ["Future"] = future
        tenses ["Future perfect"] = future_perfect
        tenses ["Conditional"] = conditional
        tenses ["Present subjunctive"] = present_subjunctive
        tenses ["Perfect subjunctive"] = perfect_subjunctive
        self.rules.append(Rule (self, pattern, suffix, tenses))
    
french = French()
languages["French"] = french
                          
assert(french.make_pronoun('je', 'étre') == "j'")
assert(french.make_pronoun('je', 'ai fait') == "j'")
assert(french.make_pronoun('tu', 'étre') == 'tu ')
assert(french.make_pronoun('je', 'crois') == 'je ')
assert(french.make_pronoun('nous', 'crois') == 'nous ')

etre_present        = ('suis',     'es',       'est',      'etes',       'sommes',     'sont')
etre_subjunctive    = ('sois que', 'sois que', 'soit que', 'soyez que',  'soyons que', 'soient que')
avoir_present       = ('ai',       'as',       'a',        'avez',       'avons',      'ont')
avoir_future        = ('aurai',    'auras',    'aura',     'aurez',      'aurons',     'auront')
avoir_imperfect     = ('avais',    'avais',    'avait',    'aviez',      'avions',     'avaient')
avoir_subjunctive   = ('aie que',  'aies que', 'ait que',  'ayons que',  'ayez que',   'aient que')
imparfait           = ('-ais',     '-ais',     '-ait',     '-iez',       '-ions',      '-aient')
futur               = ('+ai',      '+as',      '+a',       '+ez',        '+ons',       '+ont')
conditional         = ('+ais',     '+ais',     '+ait',     '+iez',       '+ions',      '+aiont')
present_subjunctive = ('-e que',    '-es que', '-e que',   '-iez que',   '-ions que',  '-ent que')

def use_stem (stem, endings):
    "Conjugations constructed from a stem with different endings for each pronoun"
    return [ending.replace('-', stem).replace('+', stem) for ending in endings]
    
def use_auxiliary(participle, auxillary_verb_conjugations=avoir_present):
    "Conjugations based on a composite of an auxiliary verb and a partiple"
    return [auxillary + ' ' + participle for auxillary in auxillary_verb_conjugations]

french.rule('être', '',
         etre_present,
         use_auxiliary('été'),
         use_stem('ét', imparfait),
         use_auxiliary('été', avoir_imperfect), # pluperfect
         use_stem('ser', futur),
         use_auxiliary('été', avoir_future),
         use_stem('ser', conditional),
         etre_subjunctive,
         use_auxiliary('été', avoir_subjunctive))
french.rule('aller', '',
         ('vais', 'va', 'va',  'allez', 'allons', 'vont'),
         use_auxiliary('allé', etre_present),
         use_stem('all', imparfait),
         use_auxiliary('allé', avoir_imperfect),  # pluperfect
         use_stem('ir', futur),
         use_auxiliary('allé', avoir_future),
         use_stem('ir', conditional),
         ('aille', 'ailles', 'aille',  'alliez', 'allions', 'aillent'),
         use_auxiliary('allé', avoir_subjunctive))
french.rule('avoir', '',
         avoir_present,
         use_auxiliary('eu'),
         use_stem('av', imparfait),
         use_auxiliary('eu', avoir_imperfect),  # pluperfect
         use_stem('aur', futur),
         use_auxiliary('eu', avoir_future),
         use_stem('aur', conditional),
         avoir_subjunctive,
         use_auxiliary('eu', avoir_subjunctive))
french.rule('faire', '',
        ('fais',   'fais', 'fait',   'faissez',  'faisson',  'font'),
         use_auxiliary('fait'),
         use_stem('fais', imparfait),
         use_auxiliary('fait', avoir_imperfect),  # pluperfect
         use_stem('fer', futur),  # pluperfect
         use_auxiliary('fait', avoir_future),
         use_stem('fer', conditional),
         use_auxiliary('fas', present_subjunctive),
         use_auxiliary('fait', avoir_subjunctive))
french.rule('.*re', '-re',
        ('-e','-es','-e','-ons','-ez','-ent'),
         use_auxiliary('-u'),
         imparfait,
         use_auxiliary('-u', avoir_imperfect),  # pluperfect
         ('-rai', '-ras', '-ra', '-rez', '-rons', '-ront'),
         use_auxiliary('-u', avoir_future),
         conditional,
         present_subjunctive,
         use_auxiliary('-u', avoir_subjunctive))
french.rule('.*er', '-er',
         ('-e','-es','-e','-ons','-ez','-ent'),
#         ('-s','-s','','-ons','-ez','-ent'),
         use_auxiliary('-é'),
         imparfait,
         use_auxiliary('-é', avoir_imperfect),  # pluperfect
         futur,
         use_auxiliary('-é', avoir_future),
         conditional,
         present_subjunctive,
         use_auxiliary('-é', avoir_subjunctive))
french.rule('.*ir', '-ir',   # -mir, -tir, or -vir
        ('-is','-is','-it','-issons','-issez','-issent'),
         use_auxiliary('-i'),
         imparfait,
         use_auxiliary('-i', avoir_imperfect),  # pluperfect
         futur,
         use_auxiliary('-i', avoir_future),
         conditional,
         present_subjunctive,
         use_auxiliary('-i', avoir_subjunctive))


#############################################################################
# Conjugation rules for the Dutch language
#
# tense - wijs
# Infinitive - Onbepaalde wijs: zijn; wezen
# Present participle - Tegenwoordig deelwoord: zijnd
# Past participle - Verleden deelwoord: geweest
# Imperative - Gebiedende wijs
# Present - Onvoltooid tegenwoordige tijd [o t t
# Present Perfect - Voltooid tegenwoordige tijd
# Past - Onvoltooid verleden tijd
# Past Perfect - Voltooid verleden tijd
# Future - Onvoltooid tegenwoordige toekomende tijd
# Future Perfect - Voltooid tegenwoordige toekomende tijd
# Imperfect - Onvoltooid verleden toekomende tijd
# Perfect - Voltooid verleden toekomende tijd
#############################################################################

zijn_present        = ('ben',     'bent',       'is',      'zijn',       'zijn',     'zijn')
zijn_imperfect      = ('was',     'was',        'was',     'waren',      'waren',    'waren')
zijn_future         = ('zal',     'zult',       'zal',     'zullen',     'zullen',   'zullen')
zijn_conditional    = ('zou',     'zou',        'zou',     'zouden',     'zouden',   'zouden')
hebben_present      = ('heb',     'heb',        'heeft',   'hebben',     'hebben',   'hebben')
hebben_imperfect    = ('had',     'had',        'had',     'hadden',     'hadden',   'hadden')

class Dutch:
    def __init__(self):
        self.pronouns=('ik','jij', 'hij/zij', 'wij', 'jullie', 'zij')
        self.rules = []

    def make_pronoun (self, pronoun, conjugation):
        return pronoun + ' '

    def rule (self, pattern, suffix, present, perfect, imparfait, pluperfect, future, future_perfect, conditional):
        tenses = collections.OrderedDict()
        tenses["Present"]        = present
        tenses["Perfect"]        = perfect
        tenses["Imparfait"]      = imparfait
        tenses["Pluperfect"]     = pluperfect
        tenses["future"]         = future
        tenses["Future perfect"] = future_perfect
        tenses["Conditional"]    = conditional
        self.rules.append(Rule (self, pattern, suffix, tenses))

dutch = Dutch()
languages["Dutch"] = dutch

dutch.rule('zijn', '',
         zijn_present,
         use_auxiliary('geweest', zijn_present),
         zijn_imperfect,
         use_auxiliary('geweest', zijn_imperfect), # pluperfect
         zijn_future,
         use_auxiliary('geweest', zijn_future),
         zijn_conditional)          # TODO use_auxiliary('geweest', zijn_conditional),

dutch.rule('hebben', '',
         hebben_present,
         use_auxiliary('ge-d', hebben_present),
         hebben_imperfect,
         use_auxiliary('ge-d', hebben_imperfect),
         use_auxiliary('-', zijn_future),
         use_auxiliary('ge-d', zijn_future),
         use_auxiliary('-', zijn_conditional))

dutch.rule('.*nen', '-nen',
         ('-','-t','-t','-nen','-nen','-nen'),
         use_auxiliary('ge-d', hebben_present),
         ('-de','-de','-de','-den','-den','-den'),
         use_auxiliary('ge-d', hebben_imperfect),
         use_auxiliary('-', zijn_future),
         use_auxiliary('ge-d', zijn_future),
         use_auxiliary('-', zijn_conditional))

dutch.rule('.*ben', '-ben',
         ('-','-t','-t','-ben','-ben','-ben'),
         use_auxiliary('ge-d', hebben_present),
         ('-de','-de','-de','-den','-den','-den'),
         use_auxiliary('ge-d', hebben_imperfect),
         use_auxiliary('-', zijn_future),
         use_auxiliary('ge-d', zijn_future),
         use_auxiliary('-', zijn_conditional))

dutch.rule('.*en', '-en',
         ('-','-t','-t','-en','-en','-en'),
         use_auxiliary('ge-d', hebben_present),
         ('-e','-e','-e','-en','-en','-en'),
         use_auxiliary('ge-d', hebben_imperfect),
         use_auxiliary('-', zijn_future),
         use_auxiliary('ge-d', zijn_future),
         use_auxiliary('-', zijn_conditional))
                                

#############################################################################
# Conjugation rules for the Esperanto language.
#
# mi (I), vi (you) ,li (he), ŝi (she), ni (we), ili (they)
#############################################################################

class Esperanto:
    def __init__(self):
        self.pronouns=('mi/vi/li/ŝi/ni/ili'),
        # Infinitive -i
        tenses = collections.OrderedDict()
        tenses["Indicative present"] = ['-as']
        tenses["Indicative past"]    = ['-is']
        tenses["Indicative future"]  = ['-os']
        tenses["Conditional"]        = ['-us']
        self.rules = [(Rule(self, '.*i', '-i', tenses))]

    def make_pronoun (self, pronoun, conjugation):
        return pronoun + ' '

esperanto = Esperanto()
languages["Esperanto"] = esperanto

#############################################################################
#  Generate a TSV conjugation table
#############################################################################

def conjugate_tsv_from_stdin ():
    "Generate a table of conjugations in Tab Separated File (TSV) format given a list of verbs in TSV format."
    count = 0
    for line in fileinput.input():
        line=line.replace('\n', '').replace('\r', '')
        words=line.split('\t')
        assert(len(words)>=2)
        verb=words[0]
        english=words[1]
        if count == 0:
            language=languages[verb]
            if language is None:
                raise Error("Language %s unknown" % (verb))
            print("%s\tEnglish\tTense\tExpression" % (verb))
        else:
            for line in match_rules(language.rules, verb, english):
                    print '\t'.join(line)
                
        count = count+1

conjugate_tsv_from_stdin()
