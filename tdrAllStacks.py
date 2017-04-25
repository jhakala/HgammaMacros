from os import listdir, makedirs
from os.path import isfile, join, exists, basename
from optparse import OptionParser


parser = OptionParser()
parser.add_option("-i", "--inDir", dest="inDir",
                  help = "the input directory")
parser.add_option("-o", "--outDir", dest="outDir", 
                  help = "the output directory")
parser.add_option("-b", action="store_true", dest="batch", default=False, 
                  help = "turn on batch mode")
(options, args) = parser.parse_args()
if options.inDir is None:  
    parser.error('Input dir not given')
if options.outDir is None:  
    parser.error('Output dir not given')

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
  if fileObj.IsA().GetName() == "TCanvas":
    outCans[inFile.GetName()]=fileObj

if not exists(options.outDir):
  makedirs(options.outDir)

for canKey in outCans.keys():
  outCans[canKey].Print(join(options.outDir, "%s.pdf"%basename(canKey)))


