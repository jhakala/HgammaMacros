from os import listdir, makedirs
from os.path import isfile, join, exists, basename
from shutil import rmtree
from argparse import ArgumentParser


parser = ArgumentParser()
parser.add_argument("-i", "--inDir", dest="inDir",
                  help = "the input directory", required=True)
parser.add_argument("-b", action="store_true", dest="batch", default=False, 
                  help = "turn on batch mode")
options = parser.parse_args()

from tcanvasTDR import TDRify
from ROOT import *
if options.batch:
  gROOT.SetBatch()

inFiles=[]
for inF in listdir(options.inDir):
  if isfile(join(options.inDir, inF)):
    inFiles.append(TFile(join(options.inDir, inF)))
print inFiles
print " "

outCans = {}
for inFile in inFiles:
  for key in inFile.GetListOfKeys():
    print key
    fileObj = inFile.Get(key.GetName())
    print fileObj 
    if fileObj.IsA().GetName() == "TCanvas":
      outCans[inFile.GetName()]=fileObj

if exists("pdf_tdr_%s" % options.inDir):
  rmtree("pdf_tdr_%s" % options.inDir)
makedirs("pdf_tdr_%s" % options.inDir)


for canKey in outCans.keys():
  outName = "%s.pdf"%basename(canKey).replace(".root","")
  outCans[canKey].Print(join("pdf_tdr_%s" % options.inDir, outName))
