from optparse import OptionParser
from glob import glob
from natsort import natsorted
from ROOT import TFile, TGraph, TCanvas
from HgParameters import getNormalizations
from checkSignalEfficiency import getSignalEfficiencies
from makeVgHists import getVgShortName

massWindowToCheck = [110, 140]

#for variation in ["btag-up", "btag-down"]:
for variation in ["btag-nom_phSF-nom", "btag-nom_phSF-up", "btag-nom_phSF-down"]:
  outfile = TFile("%s_efficienciesGraphs_masswindow_%r-%r.root"%(variation, massWindowToCheck[0], massWindowToCheck[1]), "RECREATE")
  outfile.cd()
  
  #def getSignalEfficiencies(category):
  #  if not (category == "btag" or category == "antibtag"):
  #    exit("something went wrong with the categories!")
  #  signalEfficiencies={}
  #  fileNames = glob("sigHists_Dec31/%s/histos_flatTuple_m*.root" % category)
  #  fileNames = natsorted(fileNames)
  #  for histFileName in fileNames:
  #    histFile = TFile(histFileName)
  #    histMass = histFileName.replace("sigHists_Dec31/%s/histos_flatTuple_m" % category,"").replace(".root", "")
  #    numberFound = 0
  #    print " >> checking file %s for a matching histogram..." % histFile.GetName()
  #    for key in histFile.GetListOfKeys():
  #      if "distribs" in key.GetName() and "_0" == key.GetName()[-2:]:
  #        print "   >>>> this one seems to match: %s " % key.GetName()
  #        numberFound += 1
  #        signalEfficiencies[histMass] = histFile.Get(key.GetName()).GetSumOfWeights()
  #    if numberFound != 1:
  #      exit("found more than one histogram that seems to be the right one!!!!")
  #      
  #  return signalEfficiencies
  
  
  graphs   = []
  
  #for category in ['btag', 'antibtag']:
  sigEffs = getSignalEfficiencies("%s_%s" % (getVgShortName(), variation))
  for category in ['btag', 'antibtag']:
    #canvases.append(TCanvas())
    graphs.append(TGraph())
    graphs[-1].SetNameTitle("SigEff_%s" % category, "Signal efficiency, %s category" % category)
    graphs[-1].Draw()
    masses = getNormalizations()  
    print sigEffs
    for mass in masses.keys():
      print "%r: %f" % (float(mass), sigEffs[category][str(mass)])
      graphs[-1].SetPoint(graphs[-1].GetN(), float(mass), sigEffs[category][str(mass)])
    graphs[-1].GetXaxis().SetTitle("Signal mass (GeV)")
    graphs[-1].GetYaxis().SetTitle("#varepsilon")
    graphs[-1].SetMarkerStyle(2)
    outfile.cd()
    graphs[-1].Write() 
  
