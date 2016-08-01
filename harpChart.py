# -*- coding: utf-8 -*-
from abjad import *
from itertools import product
from presentation import *

def intListToPitchClasses(intList):
	pitchClasses = []
	masterStrings = ['d', 'c', 'b', 'e', 'f', 'g', 'a'] 
	masterPitchClasses = [pitchtools.NamedPitchClass(x) for x in masterStrings]
	deviationDict = {-1:'s', 0:'', 1:'f'}
	for pitchClass, deviation in zip(masterPitchClasses, intList): 
		pitchClass = pitchClass.apply_accidental(deviationDict[deviation])
		pitchClasses.append(pitchClass)
	return pitchClasses
				
def sortPitchClasses(unsorted):
	return [unsorted[1], unsorted[0], unsorted[3], unsorted[4], unsorted[5], unsorted[6], unsorted[2] ]

def classesToPitches(classList):
	pitches = [pitchtools.NamedPitch(x, 4) for x in classList]
	return pitches

def pitchesToNotes(pitchList):
	return [Note(x, (1,4)) for x in pitchList]

def intListToString(intList):
	outString = ""
	conversionDict = {-1:'v', 0:'-', 1:'^'}
	for c in intList:
		outString += conversionDict[c]
	outString = outString[:3] + "|" + outString[3:]
	return outString

def makePedalMarkup(intList, measure):
	pString = intListToString(intList)
	scheme = schemetools.Scheme(pString, force_quotes=True)
	markup = markuptools.Markup(markuptools.MarkupCommand('harp-pedal', scheme))
	return markup
	
def intListToMeasure(intList):
	pitchClasses = intListToPitchClasses(intList)	
	sortedClasses = sortPitchClasses(pitchClasses)
	pitches = classesToPitches(sortedClasses)
	notes = pitchesToNotes(pitches)
	measure = Measure((7,4), notes)
	setMarkup = makeSetMarkup(measure)
	pedalMarkup = makePedalMarkup(intList, measure)
	markup = Markup.center_column([pedalMarkup, setMarkup], Down)
	attach(markup, measure[0])
	return measure
	
def makeChart():
	staff = Staff([])
	voice = Voice([])
	intLists = list(product([-1,0,1],repeat=7))
	for n,x in enumerate(intLists):
		voice.append(intListToMeasure(x))
		print("rendering list", n)
	staff.append(voice)
	return staff
		



staff = makeChart() 
score = Score([staff])
lily = make_sketch_lilypond_file(score)
show(lily)
