import csv
import enchant
from enchant.checker import SpellChecker
from sys import argv, stderr

class TranscriptLine:

	def __init__(self, time, speaker, speech):
		self.time = time
		self.speaker = speaker
		self.speech = speech


def spellcheck(sentence):
	checker = SpellChecker("en_US")
	checker.set_text(sentence)
	for error in checker:
		for suggestion in error.suggest():
			if error.word.replace(' ','') == suggestion.replace(' ',''):
				error.replace(suggestion)
				break
	return checker.get_text()


def gettranscript(txtfile):
	lines = [line.rstrip('\n') for line in open(txtfile, "r")]
	transcriptlist = []
	for x in range((len(lines)+1)/4):
		time = lines[x*4]
		speaker = lines[(x*4)+1]
		speech = spellcheck(lines[(x*4)+2])
		tl = TranscriptLine(time, speaker, speech)
		transcriptlist.append(tl)
	return transcriptlist

def createcsv(transcriptlist, csvfile):
	with open(csvfile, "w") as fl:
		wr = csv.writer(fl)
		for line in transcriptlist:
			row = []
			row.append(line.time)
			row.append(line.speaker)
			row.append(line.speech)
			wr.writerow(row)



def converttocsv(txtfile, csvfile):
	transcriptlist = gettranscript(txtfile)
	createcsv(transcriptlist, csvfile)


if __name__ == "__main__":

    if len(argv) == 3:

        converttocsv(argv[1], argv[2])

    else:

        stderr.write("Usage: python %s <inputtxt> <outputcsv>\n" % (argv[0]))
