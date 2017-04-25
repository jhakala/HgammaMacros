from ROOT import *
from pyrootTools import *
from getMCbgWeights import *
from HgParameters import *
from HgCuts import *

# John Hakala, 12/1/2016
# A poorly-named collection of functions that churns out all the possible histograms from DDtrees

printCuts = True


def getHiggsRangesDict():
  rangesDict = {}
  rangesDict["cosThetaStar"] = [0., 1.]
  rangesDict["phPtOverMgammaj"]=[0., 1.2]
  rangesDict["leadingPhPhi"]=[-3.5, 3.5]
  rangesDict["leadingPhPt"]=[0., 2000.]
  rangesDict["leadingPhAbsEta"]=[0.,2.5]
  rangesDict["leadingPhEta"]=[-2.8,2.8]
  label = "higgs"
  rangesDict["%sJet_HbbTag"%label]=[-1. , 1.]
  rangesDict["%sJet_pruned_abseta"%label]=[0., 3]
  rangesDict["%sJett2t1"%label]=[0, 1]
  rangesDict["%sPrunedJetCorrMass"%label]=[0,200]
  rangesDict["phJetDeltaR_%s"%label]=[0,6]
  rangesDict["phJetInvMass_pruned_%s"%label]=[0,4000]
  return rangesDict

## this is for making stackplots from the ddTrees
#def getSidebandRangesDict(sideband):
#  rangesDict = {}
#  if sideband == "100110":
#    index="Four"
#  elif sideband == "5070":
#    index="Three"
#  else:
#    print "Invalid sideband! Either 100110 or 5070."
#    quit()
#  label="sideLow%s"%index
#  rangesDict["cosThetaStar"] = [0., 1.]
#  rangesDict["phPtOverMgammaj"]=[0., 2.]
#  rangesDict["leadingPhPhi"]=[-3.5, 3.5]
#  rangesDict["leadingPhPt"]=[0., 2000.]
#  rangesDict["leadingPhAbsEta"]=[0.,2.5]
#  rangesDict["leadingPhEta"]=[-2.8,2.8]
#  rangesDict["%sJet_HbbTag"%label]=[-1. , 1.]
#  rangesDict["%sJet_pruned_abseta"%label]=[0., 3]
#  rangesDict["%sJett2t1"%label]=[0, 1]
#  rangesDict["%sPrunedJetCorrMass"%label]=[0, 4000]
#  rangesDict["phJetDeltaR_%s"%label]=[0,6]
#  rangesDict["phJetInvMass_pruned_%s"%label]=[0,4000]
#  return rangesDict

def getRangesDict():
  rangesDict = {}
  higgsRangesDict = getHiggsRangesDict()
  for key in higgsRangesDict.keys():
    rangesDict[key]=higgsRangesDict[key]
  #lowFourRangesDict = getSidebandRangesDict("100110")
  #for key in lowFourRangesDict.keys():
  #  rangesDict[key]=lowFourRangesDict[key]
  #lowThreeRangesDict = getSidebandRangesDict("5070")
  ##print lowThreeRangesDict
  #for key in lowThreeRangesDict.keys():
  #  rangesDict[key]=lowThreeRangesDict[key]
  #print rangesDict
  return rangesDict

#def makeHist(tree, hist, var, key, region):
#  nEntries = tree.Draw("%s>> hist"%var, getAntiBtagComboCut(region))
#  if nEntries == 0:
#    return False
#  else:
#    outFile = TFile("weightedMCbgHists/%s_%s_%s"%(key, region, var), "RECREATE")
#    outFile.cd()
#    for histBin in range (0,hist.GetXaxis().GetNbins()):
#      hist.SetBinContent(histBin, hist.GetBinContent(histBin)*weightsDict[key])
#    hist.Draw()
#    hist.Write()
#    outFile.Close()
#    return True

def makeAllHists(cutName, withBtag=True, sideband=False):
  sampleDirs = getSamplesDirs()
  weightsDict = getWeightsDict(sampleDirs["small3sDir"])
  #regions = ["higgs", "side100110", "side5070"]
  regions = ["higgs"]
  rangesDict = getRangesDict()
  nonEmptyFilesDict={}
  for key in getWeightsDict(getSamplesDirs()["small3sDir"]).keys():
    print "making all histograms for: %s" % key
    for region in regions:
      pre = getFilePrefix()
      tfile = TFile(sampleDirs["ddDir"]+pre+key)
      tree = tfile.Get(region)
      varNames = []
      for branch in tree.GetListOfBranches():
        if not "csvValues" in branch.GetName() and not "subjetCut" in branch.GetName() and not "triggerFired" in branch.GetName():
          varNames.append(branch.GetName())
      for var in varNames:
        hist = TH1F("hist_%s_%s_%s"%(var, region, key),"hist_%s_%s_%s"%(var, region, key),100,rangesDict[var][0],rangesDict[var][1])
        if var == "higgsJet_HbbTag":
          hist.Rebin(5)
        if   cutName in "btag":
          cut = getBtagComboCut(region, sideband)
        elif cutName in "antibtag":
          cut = getAntiBtagComboCut(region, sideband)
        elif cutName in "nobtag":
          cut = getNoBtagComboCut(region, sideband)
        elif cutName in "nMinus1":
          cut = getNminus1ComboCut(region, var, withBtag, sideband)
          print "The cut is:"
          print cut
        elif cutName == "preselection":
          cut = TCut()
        else:
          print "Invalid category! Must be btag, antibtag, nMinus1, or preselection."
        if printCuts:
          print "got cutName %s, the cuts are:" % cutName
          print cut
        #if cutName is "preselection":
        #  nEntries = tree.Draw("%s>> hist_preselection_%s_%s_%s"%(var, var, region, key), cut)
        #  filename = "weightedMCbgHists_%s/%s_%s_%s"%("preselection", var, region, key)
        #elif not preselection:
        histName = "hist_%s_%s_%s"%(var, region, key)
        print "cut is: " 
        print cut
        nEntries = tree.Draw("%s>> %s"%(var, histName), cut)
        directory = ""
        if cutName in "nMinus1":
          if withBtag:
              directory = "weightedMCbgHists_%s_withBtag"%cutName
          else:
              directory = "weightedMCbgHists_%s_noBtag"%cutName
        else:
          directory = "weightedMCbgHists_%s"%cutName
        if sideband:
          directory += "_sideband"
        filename = "%s/%s_%s_%s"%(directory, var, region, key)
        if not os.path.exists(directory):
          os.makedirs(directory)
        if not nEntries == 0:
          outFile = TFile(filename, "RECREATE")
          outFile.cd()
          print "applying weight %s to sample %s" % (weightsDict[key], filename )
          print " weightsDict has keys: " 
          print weightsDict.keys()
          for histBin in range(0,hist.GetXaxis().GetNbins()):
            hist.SetBinContent(histBin, hist.GetBinContent(histBin)*weightsDict[key])  
          hist.Write()
          outFile.Close()
          nonEmptyFilesDict[filename]="nonempty"
        else:
          nonEmptyFilesDict[filename]="empty"
  return nonEmptyFilesDict
