import pickle
import glob
from sys import argv
from pprint import pprint
from copy import deepcopy


analysis = None
if len(argv) != 3:
  print "invalid arguments, [Zg or Hg] [SB or MC]"
  exit(1)
if "Hg" in argv[1]:
  analysis = "Hg"
elif "Zg" in argv[1]:
  analysis = "Zg"
else:
  print "invalid analysis, either 'Hg' or 'Zg'"
  exit(1)
if "SB" in argv[2]:
  bg = "SB"
elif "MC" in argv[2]:
  bg = "MC"
else:
  print "invalid background, either 'SB' or 'MC'"
  exit(1)

tagOpts = {}
dirPrefix = "tagOpt"
if "MC" in bg:
  dirPrefix += "_mcBG" 
inFiles=glob.glob("%s_%s/*"%(dirPrefix, analysis))
for inFile in inFiles:
  tagOpts[inFile.replace("%s_%s/tagOpt_bJet_"%(dirPrefix, analysis), "").replace(".pkl", "")]=pickle.load(open(inFile, "rb"))

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
  optTaggers[mass] = [bestTagger, secondBestTagger, thirdBestTagger, fourthBestTagger]
  print "final best taggers for mass", mass, ":", optTaggers

#pprint(optTaggers)

#{'DDBtag': {'graphPoints1000': [[-1.0,
#                                 (27.733815937074006,
#                                  [3004.0, 11732.230823516846])],

from ROOT import TGraph, TCanvas, kRed, gROOT
rocCurves = {}
gROOT.SetBatch()
for tagger in tagOpts.keys():
  #rocCurves[tagger+"_all"] = TGraph()
  can = TCanvas()
  can.cd()
  first = True
  for mass in tagOpts[tagger].keys():
    cName = tagger+"_m%s"%mass.replace("graphPoints","")
    rocCurves[cName] = TGraph()
    print "totalB, totalS"
    totalB = tagOpts[tagger][mass][0][1][1][1]
    totalS = tagOpts[tagger][mass][0][1][1][0]
    print totalB, totalS
    print "point"
    iColor = -2
    for point in tagOpts[tagger][mass]:
      rocCurves[cName].SetPoint(rocCurves[cName].GetN(), point[1][1][1]/totalB, point[1][1][0]/totalS)
    rocCurves[cName].SetLineColor(kRed+iColor)
    rocCurves[cName].SetTitle("%s M%s" % (tagger, mass.replace("graphPoints", "")))
    if first:
      rocCurves[cName].Draw()
      rocCurves[cName].GetXaxis().SetRangeUser(0,1)
      rocCurves[cName].GetXaxis().SetTitle("Background eff")
      rocCurves[cName].GetYaxis().SetRangeUser(0,1)
      rocCurves[cName].GetYaxis().SetTitle("Signal eff")
      first = False
    else:
      rocCurves[cName].Draw("SAME")
    iColor += 2

  can.BuildLegend()
  can.Print("rocCurves_%s/rocCurve_%s.pdf"%(argv[1],tagger))

      


