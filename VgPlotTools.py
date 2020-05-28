from ROOT import *
from pyrootTools import *
from getMCbgWeights import *
from VgParameters import *
from VgCuts import *
from os import path

# John Hakala, 12/1/2016
# churns out all the possible histograms from DDtrees

printCuts = False
TColor.SetColorThreshold(0.1)

def makeAllHists(analysis, cutName, withBtag=True, sideband=False, useScaleFactors=False, windowEdges=[100,110], fineBinning=False, useReweighting=False, debugOneVar=""):
  print "entering HgPlotTools.makeAllHists for analysis", analysis
  if fineBinning != useReweighting:
    print "there was something funny happening... fineBinning and useReweighting were different..."
    exit(1)
  sampleDirs = getSamplesDirs(analysis)
  weightsDict = getWeightsDict(analysis, sampleDirs["bkgSmall3sDir"])
  rangesDict = getRangesDict(fineBinning)
  nonEmptyFilesDict={}
  thingsToProcess = getWeightsDict(analysis, getSamplesDirs(analysis)["bkgSmall3sDir"]).keys()
  if windowEdges == "signalRegion":
    thingsToProcess.remove("data_2017.root")
  for key in thingsToProcess:
    print "  -> working on sample", key
    sampleType = getWeightsDict(analysis, getSamplesDirs(analysis)["bkgSmall3sDir"])[key][1]
    useTrigger = True
    #if sampleType == "sig":
    #  useTrigger = False
    #print "making all histograms for: %s" % key
    #print "useTrigger is %r since sampleType is %s" % (useTrigger, sampleType)
    pre = getDDPrefix()
    print "      -> opening file:", path.join(sampleDirs["%sDDdir" % sampleType], pre+key)
    tfile = TFile.Open(path.join(sampleDirs["%sDDdir" % sampleType], pre+key))
    #print "tfile is: ", tfile.GetName(), tfile
    tree = tfile.Get("ddboost")
    varNames = []
    for branch in tree.GetListOfBranches():
      if not "csvValues" in branch.GetName() and not "subjetCut" in branch.GetName() and not "triggerFired" in branch.GetName():
        varNames.append(branch.GetName())
    for var in varNames:
      if debugOneVar:
        print "debugOneVar found"
        if debugOneVar in var:
          pass
        else:
          continue
      else:
        print "debugOneVar is false"
      print "    -> working on var:", var
      iRange = 1
      firstRange = True
      for rng in rangesDict[var]:
        histName = "hist_%s_%s_%s"%(var, "ddboost", key)
        if not firstRange:
          histName = histName.replace(".root","")+"_%i.root"%iRange
        if fineBinning == True:
          nBins = 4000
        else:
          nBins = 100
        hist = TH1F(histName,histName,nBins,rng[0],rng[1])
        if sampleType == "bkg":
          #print "setting bkg", key, "fill color to", getMCbgColors()[key]
          hist.SetFillColor(getMCbgColors()[key])
        #if var == "bJet_DDBtag":
        #  hist.Rebin(5)
        #print "cutName is:", cutName
        if   cutName in "btag":
          cut = getBtagComboCut(analysis, "ddboost", useTrigger, sideband, useScaleFactors, windowEdges)
          print "\n\n"
          print cut
        elif cutName in "antibtag":
          cut = getAntiBtagComboCut(analysis, "ddboost", useTrigger, sideband, useScaleFactors, windowEdges)
        elif cutName in "nobtag":
          print "going to pass getNoBtagComboCut windowEdges", windowEdges 
          cut = getNoBtagComboCut(analysis, "ddboost", useTrigger, sideband, windowEdges)
        elif cutName in "nMinus1":
          print "going to pass getNminus1ComboCut windowEdges", windowEdges 
          cut = getNminus1ComboCut(analysis, "ddboost", var, withBtag, useTrigger, sideband, windowEdges)
          print cut
        elif cutName in "preselection":
          cut = getPreselectionComboCut(analysis, "ddboost", useTrigger, sideband, [30.0, 99999.9])
        else:
          print "Invalid category: %s" % cutName
          print "Must be btag, antibtag, nMinus1, or preselection."
          exit(1)
        if useTrigger:
          cut += makeTrigger(analysis)
        #print "cut is now", cut
          
        #if cutName is "preselection":
        #  nEntries = tree.Draw("%s>> hist_preselection_%s_%s_%s"%(var, var, region, key), cut)
        #  filename = "weightedMCbgHists_%s/%s_%s_%s"%("preselection", var, region, key)
        #elif not preselection:
        #histName = "hist_%s_%s_%s"%(var, region, key)
        #print "cut is: " 
        #print cut
        if useScaleFactors:
          if cutName in ["antibtag", "btag"]:
            cutString = "%sSF*(%s)" % (cutName, cut.GetTitle())
            if useReweighting:
              cutString = "weightFactor*(%s)"%cutString
          else:
            cutString = "1*(%s)" % (cut.GetTitle())
        else:
          if cutName in "preselection":
            cutString = "1*(%s)" % cut.GetTitle()
          else:
            cutString = "1*(%s)" % (cut.GetTitle())
        print "      -> cuts:", cutString
        nEntries = tree.Draw("%s>> %s"%(var, histName), cutString, "HIST")
        directory = ""
        bareDirectory = ""
        if cutName in "nMinus1":
          if withBtag:
              directory = "%s_weightedMCbgHists_%s_withBtag"%(analysis, cutName)
              bareDirectory = directory
          else:
              directory = "%s_weightedMCbgHists_%s_noBtag"%(analysis, cutName)
              bareDirectory = directory
        else:
          if useScaleFactors:
            directory = "%s_weightedMCbgHists_%s"%(analysis, cutName)
            bareDirectory = directory
          else:
            directory = "%s_weightedMCbgHists_%s"%(analysis, cutName)
            bareDirectory = directory
        if sideband:
          if not cutName in "preselection":
            directory += "_sideband%i%i" % (windowEdges[0], windowEdges[1])
        if useScaleFactors:
          directory += "_SF"
          bareDirectory += "_SF"
        if fineBinning and useReweighting:
          directory += "_vgMC"
          bareDirectory += "_vgMC"
        filename = "%s/%s_%s_%s"%(directory, var, "ddboost", key)
        hackFilename = "%s/%s_%s_%s"%(bareDirectory, var, "ddboost", key)
        if not os.path.exists(directory):
          os.makedirs(directory)
        if not nEntries == 0:
          if firstRange:
            outFile = TFile.Open(filename, "RECREATE")
          else:
            outFile = TFile.Open(filename.replace(".root","")+"_%i.root"%iRange, "RECREATE")
          outFile.cd()
          print "    -> output file is:", outFile.GetName()
          #print "applying weight %s to sample %s" % (weightsDict[key][0], filename )
          #print " weightsDict has keys: " 
          #print weightsDict.keys()
          for histBin in range(0,hist.GetXaxis().GetNbins()):
            hist.SetBinContent(histBin, hist.GetBinContent(histBin)*weightsDict[key][0])  
          hist.Write()
          outFile.Close()
          del outFile
          #print "closed outFile" , outFile.GetName()
          nonEmptyFilesDict[filename]="nonempty"
          nonEmptyFilesDict[hackFilename]="nonempty"
        else:
          nonEmptyFilesDict[filename]="empty"
          nonEmptyFilesDict[hackFilename]="empty"
          print "      the histogram %s was empty for" % histName, filename
        iRange += 1
        firstRange = False;
    tfile.Close()
    del tfile
  return nonEmptyFilesDict
