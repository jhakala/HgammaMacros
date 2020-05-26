from os import path, makedirs
from ROOT import TFile


def makeStack(nonEmptyFilesDict, sideband, showSigs, addLines, useScaleFactors, vgMC, cutName, withBtag, analysis, windowEdges):
  from ROOT import gROOT, gStyle, TColor, TCanvas, TPad, THStack, kCyan, kOrange, kMagenta, kRed, kBlack, TLine, kFALSE
  from pyrootTools import getSortedDictKeys, drawInNewCanvas
  from VgParameters import getSamplesDirs, getVariableDict, getRangesDict, getHiggsRangesDict, getDebugVar
  from VgCuts import shouldBlind
  from VgStackOrg import getHistsDir, getDirName 
  from tcanvasTDR import TDRify

  TColor.SetColorThreshold(0.1)
  gROOT.SetBatch()

  debugOneVar = getDebugVar()
  doStack = False
  doBottomPad = (False and doStack)

  printNonempties = False
  printFileNames  = False
  blindData = shouldBlind(cutName, sideband, windowEdges)
  sampleDirs = getSamplesDirs(analysis)
  rangesDict = getRangesDict(vgMC)

  treekey="ddboost"
  histsDir = getHistsDir(cutName, withBtag, analysis, useScaleFactors, vgMC, windowEdges, sideband)
  
  cans=[]
  pads=[]
  hists=[]
  tfiles=[]
  datahists=[]
  datahistsCopies=[]
  datafiles=[]
  varDict = getVariableDict()
  

  rng = [0., 1.]
  outFile = TFile.Open("debug.root", "RECREATE")
  cans.append(TCanvas())
  pads.append(TPad("topPad", "top pad", 0, 0.3, 1, 1.0))
  cans[-1].cd()
  pads[-1].Draw()
  
  #### Build the stackplot
  cans[-1].cd()
  pads[-1].Draw()
  pads[-1].SetLogy()
  
  dName = getDirName(analysis, cutName, withBtag, False, False)
  dName += "_sideband%i%i" % (windowEdges[0], windowEdges[1])
  dataFileName = "bJet_akxDec_bbvsLight"+"_"+treekey+"_data_2017.root" 
  print "going to use data file",  dataFileName, "for the plot"
  datafiles.append(TFile.Open("%s/%s"%(dName, dataFileName)))
  datahists.append(datafiles[-1].Get("hist_%s"%dataFileName))
  pads[-1].cd()
  datahists[-1].Draw("PE")
  datahists[-1].SetMarkerStyle(20)
  datahists[-1].SetMarkerSize(datahists[-1].GetMarkerSize()*.7)
  if doBottomPad:
    datahistsCopies.append(datahists[-1].Clone())
  #for sigMass in [650, 750, 1000, 1250, 1500, 1750, 2000, 2500, 3000, 3500, 4000]:
  rName = getDirName(analysis, cutName, withBtag, useScaleFactors, vgMC)
  
  pads[-1].SetBottomMargin(0)
  pads[-1].BuildLegend()
  cans[-1].cd()
  pads[-1].Draw()
  for prim in pads[-1].GetListOfPrimitives():
    if "TLegend" in prim.IsA().GetName():
      prim.SetX1NDC(0.753)
      prim.SetY1NDC(0.703)
      prim.SetX2NDC(0.946)
      prim.SetY2NDC(0.911)
  ### WHAT THE HELL #### TODO TODO ####
#      for subprim in prim.GetListOfPrimitives():
#         pass
#        print "subprim has label:", subprim.GetLabel()
#        for key in legendLabels:
#          if key in subprim.GetLabel():
#            subprim.SetLabel("myLabel")
#            subprim.SetOption("lf")
#          elif "data" in subprim.GetLabel():
#            #print "found something named SinglePhoton"
#            subprim.SetLabel("data")
#            subprim.SetOption("pe")
  outFile.cd()
  cans[-1].Write()
  outFile.Close()
