from os import path, makedirs, getcwd
from sys import argv
from glob import glob
from runVgammaSelector import processVg
from pprint import pprint

debug = False
first = True

argvGood = False
if len(argv) == 2:
  if argv[1] == "Hg" or argv[1] == "Zg":
    argvGood = True

if not argvGood:
  print "must supply the analysis, either 'Hg' or 'Zg'"
  exit(1)

if argvGood:
  print"""  -----------------------------  
|  making all ddTrees for %s" |
 -----------------------------"""% argv[1] 

#for variation in [("nom", 0), ("up", 1), ("down", -1)]:
for btagVariation in [("nom", 0)]:
  #for phSFvariation in [("nom", 0), ("up", 1), ("down", -1)]:
  for phSFvariation in [("nom", 0)]:
    baseDir = path.join(getcwd(), "organize_smallifications")
    categories = ["backgrounds", "signals", "data"]
    #categories = ["signals"]
    catDirs = {}
    for category in categories:
      catDirs[category] = path.join(baseDir, category)
    #pprint(catDirs)
    
    outDir = baseDir.replace("smallifications", "%s_DDs_btag-%s_phSF-%s" % (argv[1], btagVariation[0], phSFvariation[0]))
    if not path.exists(outDir):
      makedirs(outDir)
    #print "catDirs", catDirs

    for catDir in catDirs:
      catOutDir = path.join(outDir, catDir)
      if "signals" in catDir:
        inputFiles = glob("%s/%s/*%s*.root" % (baseDir, catDir, argv[1]))
      else: 
        inputFiles = glob("%s/%s/*.root" % (baseDir, catDir))
      
      #print "inputFiles: ", inputFiles
      if not path.exists(catOutDir):
        makedirs(catOutDir)
      for inputFile in inputFiles:
        if first:
          print "  about to call the first processVg" 
          processVg(argv[1], inputFile, inputFile.replace("smallified", "ddTree").replace("smallifications", "DDs_btag-%s_phSF-%s" % (btagVariation[0], phSFvariation[0])), False, False, btagVariation[1], phSFvariation[1])
          first = False
        elif not debug:
          processVg(argv[1], inputFile, inputFile.replace("smallified", "ddTree").replace("smallifications", "DDs_btag-%s_phSF-%s" % (btagVariation[0], phSFvariation[0])), True, True, btagVariation[1], phSFvariation[1])

print "\n\ndone making all ddTrees for %s\n---------------------------------------" % argv[1]
