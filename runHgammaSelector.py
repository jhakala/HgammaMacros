# Macro to analyze a VgammaTuplizer flatTuple
# This macro takes three options
# The option "i" is the input file, containing the tree named "ntuplizer/tree" 
# The "-o" option is the output filename
# The optional "-l" will ask to load the macro from a compiled library, rather than compiling it from source
# Example: 
# python runTreeChecker.py -i myVgammaNtuple.root -o myOutputFile.root -l
# John Hakala 1/15/2016

import os


from ROOT import *
from getMCbgWeights import getMCbgWeightsDict
from HgParameters import getSamplesDirs

def deleteLibs(macroName):
  # remove the previously compiled libraries
  if os.path.exists(macroName+"_C_ACLiC_dict_rdict.pcm"):
     os.remove(macroName+"_C_ACLiC_dict_rdict.pcm")
  if os.path.exists(macroName+"_C.d"):
     os.remove(macroName+"_C.d")
  if os.path.exists(macroName+"_C.so"):
     os.remove(macroName+"_C.so")

def processHg(analysis, inputFileName, outputFileName, load, loopMode = False, btagVariation=0, phSFvariation=0):
  if inputFileName is None:
    print "\nPlease specify the input file with the -i option."
    exit(1)
  elif outputFileName is None:
    print "\nPlease specify the output filename with the -o option."
    exit(1)
  elif not os.path.isfile(inputFileName):
    print "\nThe input file specified was not found: %s" % inputfileName
    exit(1)
  
  
  print "\nInput file is %s\n" % inputFileName
  presentTense = "load" if load else "compile"
  pastTense  = "loaded" if load else "compiled"
  print "\nAttempting to %s HgammaSelector.\n" % presentTense
  
  # call the compiling function to compile the HgammaSelector, then run its Loop() method
  if presentTense=="compile" and not loopMode:
     deleteLibs("HgammaSelector")
     # compile the macro using g++ and check compilation status
     exitCode = gSystem.CompileMacro("HgammaSelector.C", "gOck")
     success=(exitCode==1)
  elif presentTense=="load" and not loopMode:
     exitCode = gSystem.Load('HgammaSelector_C')
     success=(exitCode>=-1)
  if not loopMode:
    if not success:
       print "\nError... HgammaSelector failed to %s. :-("%presentTense
       print "Make sure you're using an up-to-date version of ROOT by running cmsenv in a 7_4_X>=16 CMSSW area."
       exit(1)
  
  print "\nHgammaSelector %s successfully."%pastTense
  if presentTense=="compile" and not loopMode:
     gSystem.Load('HgammaSelector_C')
  inputFile = TFile(inputFileName)
  
  print "testing"
  from pprint import pprint
  from os.path import basename
  sampleDirs = getSamplesDirs()
  weights = getMCbgWeightsDict(sampleDirs["bkgSmall3sDir"])
  pprint(weights)
  shortName = basename(inputFile.GetName()).replace("smallified_", "")
  print shortName
  weight = 1.
  if shortName in weights.keys():
    weight = weights[shortName][0]
  print "weight for this sample:", weight
  
  pdgCodeForBoson = None
  if "Hg" in analysis:
    pdgCodeForBoson = 25
  elif "Zg" in analysis:
    pdgCodeForBoson = 23
  else:
    print "invalid analysis, either 'Zg' or 'Hg'"
    exit(1)
  # get the ntuplizer/tree tree from the file specified by argument 1
  tree = inputFile.Get("ntuplizer/tree")
  instance = HgammaSelector(tree)
  # run the HgammaSelector::Loop method
  instance.Loop(pdgCodeForBoson, outputFileName, btagVariation, phSFvariation, weight)

if __name__=="__main__":
  from argparse import ArgumentParser
  parser = ArgumentParser()
  parser.add_argument("-l", dest="load", action="store_true", default=False,
                    help="use this if you want to load the macro from a compiled library"  )
  parser.add_argument("-i",  dest="inputFileName",
                    help="the input file name"                                             )
  parser.add_argument("-o",  dest="outputFileName",
                    help="the output file name"                                            )
  parser.add_argument("-b",  type=int, dest="btagVariation", default=0,
                    help="vary the b-tagging SFs, 1 to vary up and -1 to vary down"        )
  parser.add_argument("-p",  type=int, dest="phSFVariation", default=0,
                    help="vary the photon SFs, 1 to vary up and -1 to vary down"        )
  parser.add_argument("-a",  dest="analysis", required=True,
                    help="the analysis, either 'Hg' or 'Zg'"        )
  options = parser.parse_args()
  processHg(analysis, options.inputFileName, options.outputFileName, options.load, options.btagVariation, options.phSFvariation)
