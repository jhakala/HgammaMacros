import pickle
import glob
from sys import argv
from pprint import pprint
from copy import deepcopy


analysis = None
if len(argv) != 2:
  print "please specify analysis, either 'Zg' or 'Hg'"
  exit(1)
if "Hg" in argv[1]:
  analysis = "Hg"
elif "Zg" in argv[1]:
  analysis = "Zg"
else:
  print "invalid analysis, either 'Hg' or 'Zg'"
  exit(1)

tagOpts = {}
inFiles=glob.glob("tagOpt_%s/*"%analysis)
for inFile in inFiles:
  tagOpts[inFile.replace("tagOpt_%s/tagOpt_bJet_"%analysis, "").replace(".pkl", "")]=pickle.load(open(inFile, "rb"))

print "\n---------------------"
print "tagOpts:"
pprint(tagOpts)
print "---------------------\n"
optPoints = {}
for tagger in tagOpts.keys():
  optPoints[tagger] = {}
  maxPoint = [-10., -1.]
  for mass in tagOpts[tagger].keys():
    for graphPoint in tagOpts[tagger][mass]:
      if graphPoint[1] > maxPoint[1]: # and graphPoint[0] <= .9001:
        maxPoint = graphPoint
    optPoints[tagger][mass] = maxPoint
#pprint(optPoints)

optTaggers = {}
for mass in optPoints["decDDBtag"].keys():
  bestTagger = ["error", [-10., -1.]]
  secondBestTagger = ["error", [-10., -1.]]
  thirdBestTagger = ["error", [-10., -1.]]
  fourthBestTagger = ["error", [-10., -1.]]
  print "working on mass", mass
  for tagger in optPoints.keys():
    if "prob" in tagger or not (analysis[0] in tagger or "DDB" in tagger):
      continue
    print "working on tagger", tagger, optPoints[tagger][mass]
    if optPoints[tagger][mass][1] > bestTagger[1][1]:
      #print "found best tagger", tagger
      fourthBestTagger = deepcopy(thirdBestTagger)
      thirdBestTagger = deepcopy(secondBestTagger)
      secondBestTagger = deepcopy(bestTagger)
      bestTagger = [tagger, optPoints[tagger][mass]]
    elif optPoints[tagger][mass][1] > secondBestTagger[1][1]:
      #print "found second best tagger", tagger
      fourthBestTagger = deepcopy(thirdBestTagger)
      thirdBestTagger = deepcopy(secondBestTagger)
      secondBestTagger = [tagger, optPoints[tagger][mass]]
    elif optPoints[tagger][mass][1] > thirdBestTagger[1][1]:
      #print "found second best tagger", tagger
      fourthBestTagger = deepcopy(thirdBestTagger)
      thirdBestTagger = [tagger, optPoints[tagger][mass]]
    elif optPoints[tagger][mass][1] > fourthBestTagger[1][1]:
      #print "found second best tagger", tagger
      fourthBestTagger = [tagger, optPoints[tagger][mass]]
  print "final best taggers for mass", mass, ":", bestTagger, secondBestTagger
  optTaggers[mass] = [bestTagger, secondBestTagger, thirdBestTagger, fourthBestTagger]

#pprint(optTaggers)

#{'DDBtag': {'graphPoints1000': [[-1.0,
#                                 (27.733815937074006,
#                                  [3004.0, 11732.230823516846])],

from ROOT import TGraph
rocCurves = {}
for tagger in tagOpts.keys():
  rocCurves[tagger+"_all"] = TGraph()
  for mass in tagOpts[tagger].keys():
    rocCurves[tagger+"_m%s"%mass.replace("graphPoints","")] = TGraph()
    totalB = tagOpts[tagger][mass][0][1][1]
    totalS = tagOpts[tagger][mass][0][1][0]
    print tagger, mass, totalB, totalS
    exit(1)
    #[3109.0, 11678.490283966064]
