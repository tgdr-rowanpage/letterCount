#! /usr/bin/python3

# count the counts of each letter in the file given and provide an output list
# optionally, output to a csv file the stats for each letter and word

import argparse
import time
import nltk

parser = argparse.ArgumentParser()
parser.add_argument("-i","--inputFile",help="inuput file")
parser.add_argument("-o","--outputFile",help="output file")

args = parser.parse_args()
if not (args.inputFile):
  exit("No input file specified")

# create dictionary
letterDict = {}
wordDict = {}
noWords = 0
noChars = 0

# vars for timing...
lastTimeCheck = time.time()

def since(last):
	# seconds since the last time check
	return (time.time() - lastTimeCheck)

#open the file etc
with open (args.inputFile) as iFile:
	linesProcessed = 0
	lines = iFile.readlines()
	updateType = 0
	if (len(lines) > 1000):
		updateType = 1
	print("Read {} lines from {} in {} seconds".format(len(lines),args.inputFile,int(since(lastTimeCheck))),flush=True)
	lastTimeCheck = time.time()
	print("Processing lines",end='',flush=True)
	if updateType > 0:
		print("")
	for line in lines:
		
		tokens = nltk.word_tokenize(line.lower())
		for token in tokens:
			noWords += 1
			wordDict[token] = wordDict.get(token,0) + 1
		for char in line:
			noChars += 1
			letterDict[char] = letterDict.get(char,0) + 1
		
		linesProcessed +=1 
		if updateType == 1:
			if linesProcessed % 1000 == 0:
				linesLeft = len(lines) - linesProcessed
				timeFor1000 = since(lastTimeCheck)
				timeLeft = int(timeFor1000 * linesLeft / 1000)
				print("Processed {} of {} lines in {} seconds (about {} seconds left)".format(linesProcessed,len(lines),int(since(lastTimeCheck)),timeLeft),flush=True)
				lastTimeCheck = time.time()
		else:
			print(".",end='',flush=True)


print("Finished reading {}".format(args.inputFile))

# do the output...

lastTimeCheck = time.time()
sortedWords = sorted(wordDict.items(), key=lambda x:x[1])
#print("Sorted words in {} seconds".format(int(since(lastTimeCheck))))
lastTimeCheck = time.time()
#print("Reversing words")
sortedWords.reverse()
#print("Reversed words in {} seconds".format(int(since(lastTimeCheck))))
lastTimeCheck = time.time()
#print("Sorting letters")
sortedLetters = sorted(letterDict.items(), key=lambda x:x[1])
#print("Sorted letters in {} seconds".format(int(since(lastTimeCheck))))
#print("Reversing letters")
lastTimeCheck = time.time()
sortedLetters.reverse()
#print("Reversed letters in {} seconds".format(int(since(lastTimeCheck))))
print("{} letters counted:".format(noChars))
print("{} different letters used".format(len(sortedLetters)))
for char in sortedLetters:
	print("{}: {}".format(char[0],char[1]))
print("\n\n{} words counted:".format(noWords))
print("{} different words in the file".format(len(sortedWords)))
counter = 0
while counter < 20:
	print("{}: {}".format(sortedWords[counter][0],sortedWords[counter][1]))
	counter += 1
#for word in sortedWords:
	#print("{}: {}".format(word[0],word[1]))

if args.outputFile:
	# do output of stats to a file...
	with open(args.outputFile,"w") as of:
		for char in sortedLetters:
			of.write("letter,\"{}\",{}\n".format(char[0],char[1]))
		for word in sortedWords:
			of.write("word,\"{}\",{}\n".format(word[0],word[1]))