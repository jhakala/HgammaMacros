from os.path import join, basename
from glob import glob
from ROOT import *
from makeVgHists import getVgShortName

gROOT.SetBatch()

def getSignalEfficiencies(inDir):
  response = {}
  print inDir
  print glob(join(inDir, "*"))
  for inDir in glob(join(inDir, "*")):
    category = basename(inDir)
    response[category] = {}
    print "HERE HERE"
    print category
    print join(inDir, "*sig*")
    print glob(join(inDir, "*sig*"))
    for inFileName in glob(join(inDir, "*sig*")):
      mass = basename(inFileName).split("_m")[-1].split(".root")[0]
      inFile = TFile(inFileName, "READ")
      print "determining efficiency for file: ", inFile.GetName()
      #print inFile.Get("distribs_X").GetSumOfWeights()
      print inFile.Get("distribs_X").GetSumOfWeights()
      response[category][mass] = inFile.Get("distribs_X").GetSumOfWeights()
      inFile.Close()
  return response
      

if __name__ == "__main__":
  responses = {}
  for var in ["up", "down", "nom"]:
    responses[var] = getSignalEfficiencies("vgHists_lowerBound720_btag-nom_phSF-%s" % (var))
  
  from pprint import pprint
  pprint(responses)
