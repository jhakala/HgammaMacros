from os.path import join, basename
from glob import glob
from ROOT import *
from makeVgHists import getVgShortName

gROOT.SetBatch()

def getSignalEfficiencies(inDir):
  response = {}
  print glob(join(inDir, "*"))
  for inDir in glob(join(inDir, "*")):
    category = basename(inDir)
    response[category] = {}
    for inFileName in glob(join(inDir, "*sig*")):
      mass = basename(inFileName).split("_m")[-1].split(".root")[0]
      inFile = TFile(inFileName, "READ")
      print "determining efficiency for file: ", inFile.GetName()
      #print inFile.Get("distribs_X").GetSumOfWeights()
      response[category][mass] = inFile.Get("distribs_X").GetSumOfWeights()
      inFile.Close()
  return response
      

if __name__ == "__main__":
  print getSignalEfficiencies(getVgShortName())
  
