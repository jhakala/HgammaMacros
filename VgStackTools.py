from os import path, makedirs, getcwd
from ROOT import TFile

def closeAllFiles(files):
  for f in files:
    f.Close()
    del f

def getHistsDir(cutName, withBtag, analysis, useScaleFactors, vgMC, windowEdges, sideband):
  if cutName in [ "nMinus1" ]:
    if withBtag:
      histsDir = "%s/%s_weightedMCbgHists_%s_withBtag"%(getcwd(), analysis, cutName )
    if not withBtag:
      histsDir = "%s/%s_weightedMCbgHists_%s_noBtag"%(getcwd(), analysis, cutName )
  else:
    histsDir = "%s/%s_weightedMCbgHists_%s"%(getcwd(), analysis, cutName)
  if sideband:
    if not cutName in "preselection":
      histsDir += "_sideband%i%i" % (windowEdges[0], windowEdges[1])
  if useScaleFactors:
    histsDir += "_SF"
  if vgMC:
    histsDir += "_vgMC"
  return histsDir

def getDirName(analysis, cutName, withBtag, useScaleFactors, vgMC):
  dirName = "%s_weightedMCbgHists_%s" % (analysis, cutName)
  if cutName in "nMinus1":
    if withBtag:
      dirName += "_withBtag"
    else:
      dirName += "_noBtag"
  if useScaleFactors:
    dirName += "_SF"
  if vgMC:
    dirName += "_vgMC"
  return dirName

def getOutFile(cutName, withBtag, analysis, windowEdges, useScaleFactors, vgMC, varkey, indexLabel, sideband):
  if cutName in "nMinus1":
    if withBtag:
      outDirName = "%s_stackplots_softdrop_%s_withBtag" % (analysis, cutName)
    else:
      outDirName = "%s_stackplots_softdrop_%s_noBtag" % (analysis, cutName)
  else:
    outDirName = "%s_stackplots_softdrop_%s" % (analysis, cutName)
  if sideband:
    if not cutName in "preselection":
      outDirName +="_sideband%i%i" %(windowEdges[0], windowEdges[1])
  if useScaleFactors:
    outDirName += "_SF"
  if vgMC:
    outDirName += "_vgMC"
  if not path.exists(outDirName):
    makedirs(outDirName)
  outFileName = "%s/%s_stack_%s%s.root"%(outDirName, cutName, varkey, indexLabel)
  return TFile.Open(outFileName, "RECREATE")

def makeStack(nonEmptyFilesDict, sideband, showSigs, addLines, useScaleFactors, vgMC, cutName, withBtag, analysis, windowEdges):
  from ROOT import gROOT, gStyle, TColor, TCanvas, TPad, THStack, kCyan, kOrange, kMagenta, kRed, kBlack, TLine, kFALSE
  from pyrootTools import getSortedDictKeys, drawInNewCanvas
  from VgParameters import getSamplesDirs, getVariableDict, getRangesDict, getHiggsRangesDict, getDebugVar
  from VgCuts import shouldBlind
  from getMCbgWeights import getWeightsDict, getMCbgWeightsDict, getMCbgColors, getMCbgOrderedList, getMCbgLabels
  from tcanvasTDR import TDRify

  TColor.SetColorThreshold(0.1)
  gROOT.SetBatch()

  debugOneVar = getDebugVar()
  doStack = True
  doBottomPad = (True and doStack)

  printNonempties = False
  printFileNames  = False
  blindData = shouldBlind(cutName, sideband, windowEdges)
  sampleDirs = getSamplesDirs(analysis)
  rangesDict = getRangesDict(vgMC)
  higgsRangesDict = getHiggsRangesDict(vgMC)
  mcBgWeights = getMCbgWeightsDict(analysis, sampleDirs["bkgSmall3sDir"])

  treekey="ddboost"
  dinkoMethod = False
  histsDir = getHistsDir(cutName, withBtag, analysis, useScaleFactors, vgMC, windowEdges, sideband)
  
  tfiles=[]
  datafiles=[]
  sigfiles=[]
  cans=[]
  pads=[]
  thstacks=[]
  thstackCopies=[]
  hists=[]
  datahists=[]
  datahistsCopies=[]
  sighists=[]
  lines=[]
  legendLabels = getMCbgLabels()
  varDict = getVariableDict()
  
  print "now making all stackplots."
  #for varkey in [higgsRangesDict.keys()[0]]:
  if "antibtag" in cutName and not useScaleFactors:
    for varkey in higgsRangesDict.keys():
      if "SF" in varkey or "mcWeight" in varkey:
        #print "about to get rid of ", varkey, "from the higgsRangesDict"
        higgsRangesDict.pop(varkey)

  for varkey in higgsRangesDict.keys():
    if debugOneVar:
      if debugOneVar in varkey:
        pass
      else:
        continue

    iRange = 1
    first = True
    for rng in higgsRangesDict[varkey]:
      print "  -> working on range", rng, "for varkey", varkey
      if "btagSF" in varkey:
        continue;
      indexLabel = ""
      outFile = getOutFile(cutName, withBtag, analysis, windowEdges, useScaleFactors, vgMC, varkey, indexLabel, sideband)
      if not first:
        indexLabel +="_%i" % iRange
      cans.append(TCanvas())
      pads.append(TPad("stack_%s_%s%s"%(cutName, varkey, indexLabel), "stack_%s_%s%s"%(cutName, varkey, indexLabel), 0, 0.3, 1, 1.0))
      cans[-1].cd()
      pads[-1].Draw()
      pads[-1].cd()
  
      #### Build the stackplot
      cans[-1].cd()
      pads[-1].Draw()
      if not "SF" in varkey:
        pads[-1].SetLogy()
      if doStack:
        thstacks.append(THStack("thstack_%s_%s%s"%(cutName, varkey, indexLabel),""))
        thstackCopies.append(THStack("thstackCopy_%s_%s%s"%(cutName, varkey, indexLabel),""))
        integralsDict={}
        namesDict={}
        iFile = -1
        for filekey in mcBgWeights.keys():
          iFile += 1
          if iFile == -1:
            break
          filenameDefault = varkey+"_"+treekey+"_"+filekey
          filename = varkey+"_"+treekey+"_"+filekey.replace(".root", "%s.root"%indexLabel)
          if printNonempties:
            print "The nonempty files dict is:"
            print nonEmptyFilesDict
          dirName = getDirName(analysis, cutName, withBtag, useScaleFactors, vgMC)
          thisFileName = "%s/%s" % (dirName, filename)
          thisFileNameDefault = "%s/%s" % (dirName, filenameDefault)

          #HACKHACKHACK:
          if nonEmptyFilesDict[thisFileNameDefault] == "nonempty" and path.exists(thisFileName):
            tfiles.append(TFile.Open(thisFileName))
            hists.append(tfiles[-1].Get("hist_%s" % filename))
            hists[-1].SetFillColor(getMCbgColors()[filekey])
            drawInNewCanvas(hists[-1], "HIST")
            integralsDict[hists[-1].Integral()] = hists[-1] 
            namesDict[hists[-1].GetName()] = hists[-1]

        for mcBG in getMCbgOrderedList():
          for key in namesDict:
            if mcBG in key:
              thstacks[-1].Add(namesDict[key])
              thstackCopies[-1].Add(namesDict[key])
  

        pads[-1].cd()
        thstacks[-1].Draw("hist")
        thstacks[-1].SetMinimum(0.08)
        thstacks[-1].SetMaximum(thstacks[-1].GetMaximum()*45)
        #print thstacks[-1]
        hasAxis = False
        if thstacks[-1].GetXaxis():
          hasAxis = True
        if varkey in varDict.keys() and hasAxis:
          thstacks[-1].GetXaxis().SetTitle(varDict[varkey])
          thstacks[-1].GetYaxis().SetTitle("Events/%g"%thstacks[-1].GetXaxis().GetBinWidth(1))
          thstacks[-1].GetYaxis().SetLabelSize(0.04)
          thstacks[-1].GetYaxis().SetTitleSize(0.04)
          thstacks[-1].GetYaxis().SetTitleOffset(1.2)
  
      dName = getDirName(analysis, cutName, withBtag, False, False)
      if sideband:
        if not cutName in "preselection":
          dName += "_sideband%i%i" % (windowEdges[0], windowEdges[1])
      if not blindData:
        dataFileName = varkey+"_"+treekey+"_data_2017%s.root" % indexLabel
        #print "going to use data file",  dataFileName, "for the plot"
        datafiles.append(TFile.Open("%s/%s"%(dName, dataFileName)))
        datahists.append(datafiles[-1].Get("hist_%s"%dataFileName))
        #print datahists[-1]
        if doStack:
          datahists[-1].Draw("PE SAME")
        else:
          pads[-1].cd()
          datahists[-1].Draw("PE")
        datahists[-1].SetMarkerStyle(20)
        datahists[-1].SetMarkerSize(datahists[-1].GetMarkerSize()*.7)
        if doBottomPad:
          datahistsCopies.append(datahists[-1].Clone())
      #for sigMass in [650, 750, 1000, 1250, 1500, 1750, 2000, 2500, 3000, 3500, 4000]:
      rName = getDirName(analysis, cutName, withBtag, useScaleFactors, vgMC)
      if showSigs:
        colors={}
        colors[800]=kCyan-6
        colors[1000]=kOrange
        colors[2000]=kMagenta
        colors[3000]=kRed
        for sigMass in [800, 1000, 2000, 3000]:
          sigFileName = varkey+"_"+treekey+"_%s-%i%s.root"%(analysis, sigMass, indexLabel)
          outDirName = "%s_stackplots_softdrop_%s" % (analysis, rName)
          sigfiles.append(TFile.Open("%s/%s"%(rName, sigFileName)))
          #print "adding signal file", sigfiles[-1].GetName(), "to the plot"
          sighists.append(sigfiles[-1].Get("hist_%s"%sigFileName))
          sighists[-1].SetLineStyle(3)
          sighists[-1].SetLineWidth(2)
          sighists[-1].SetLineColor(colors[sigMass])
          sighists[-1].SetTitle("%s#gamma(%r TeV)"%(analysis[0],sigMass/float(1000)))
          #sighists[-1].SetMarkerSize(0)
          sighists[-1].Draw("hist SAME")
  
      pads[-1].SetBottomMargin(0)
      pads[-1].BuildLegend()
      cans[-1].cd()
      pads[-1].Draw()
      if showSigs:
        TDRify(pads[-1], False, "cpad_%s_%s"%(rName, sigFileName))
      for prim in pads[-1].GetListOfPrimitives():
        if "TLegend" in prim.IsA().GetName():
          prim.SetX1NDC(0.753)
          prim.SetY1NDC(0.703)
          prim.SetX2NDC(0.946)
          prim.SetY2NDC(0.911)
     #### WHAT THE HELL #### TODO TODO ####
#          for subprim in prim.GetListOfPrimitives():
#             pass
#            print "subprim has label:", subprim.GetLabel()
#            for key in legendLabels:
#              if key in subprim.GetLabel():
#                subprim.SetLabel(legendLabels[key])
#                subprim.SetOption("lf")
#              elif "data" in subprim.GetLabel():
#                #print "found something named SinglePhoton"
#                subprim.SetLabel("data")
#                subprim.SetOption("pe")
      if doBottomPad:
        if not blindData:
          pads.append(TPad("ratio_%s_%s%s"%(cutName, varkey, indexLabel), "ratio_%s_%s%s"%(cutName, varkey, indexLabel), 0, 0.05, 1, 0.3))
          pads[-1].SetTopMargin(0)
          pads[-1].SetBottomMargin(0.15)
          pads[-1].cd()
   
          fullStack = thstackCopies[-1].GetStack().Last()
          fullStack.Sumw2()
          if varkey in varDict.keys():
            fullStack.GetXaxis().SetTitle(varDict[varkey])
          ### HEREHERE
          if sideband:
            if dinkoMethod or cutName=="preselection":
              sbScale = 1
            else:
              sbScale = fullStack.GetSumOfWeights()/datahists[-1].GetSumOfWeights()
              #print "sbscale is: ", sbScale
            for iBin in range(0, datahists[-1].GetNbinsX()):
              #print "sbScale", sbScale 
              #print "old bin content", datahists[-1].GetBinContent(iBin)
              #print "new bin content", datahists[-1].GetBinContent(iBin)*sbScale
              datahists[-1].SetBinContent(iBin, datahists[-1].GetBinContent(iBin)*sbScale)
              datahistsCopies[-1].SetBinContent(iBin, datahistsCopies[-1].GetBinContent(iBin)*sbScale)
          pads[-2].Update()
          pads[-1].Update()
          ### HEREHERE
          fullStack.GetXaxis().SetLabelSize(0.10)
          fullStack.GetXaxis().SetTitleSize(0.13)
          fullStack.GetXaxis().SetTitleOffset(2)
          gStyle.SetOptStat(0)
          datahistsCopies[-1].Sumw2()
          datahistsCopies[-1].Divide(fullStack)
          datahistsCopies[-1].Draw("PE")
          if addLines:
            lines.append(TLine(fullStack.GetXaxis().GetBinLowEdge(1) , 1, fullStack.GetXaxis().GetBinUpEdge(fullStack.GetXaxis().GetNbins()) ,1))
            lines[-1].SetLineStyle(2)
            lines[-1].Draw("SAME")
          datahistsCopies[-1].SetTitle("")
          datahistsCopies[-1].GetYaxis().SetRangeUser(0,2)
          datahistsCopies[-1].SetLineColor(kBlack)
          datahistsCopies[-1].SetStats(kFALSE)
          datahistsCopies[-1].GetXaxis().SetLabelSize(0.10)
          datahistsCopies[-1].GetXaxis().SetTitleSize(0.13)
          datahistsCopies[-1].GetXaxis().SetTitleOffset(2)
   
          pads[-1].cd()
          gStyle.SetOptStat(0)
          cans[-1].cd()
          if not blindData:
            pads[-1].Draw()
          #for prim in pads[-1].GetListOfPrimitives():
          #  if "Text" in prim.IsA().GetName():
          #    prim.Delete()
          #  if "Stats" in prim.IsA().GetName():
          #    prim.Delete()
          datahistsCopies[-1].GetYaxis().SetTitle("data/MC")
          datahistsCopies[-1].GetYaxis().SetTitleSize(0.13)
          datahistsCopies[-1].GetYaxis().SetTitleOffset(0.24)
          datahistsCopies[-1].GetYaxis().SetLabelSize(0.08)
          if showSigs:
            TDRify(pads[-1], True, "cpad_%s_%s"%(rName, sigFileName))
      outFile.cd()
      cans[-1].Write()
      outFile.Close()
      for f in [tfiles, datafiles, sigfiles]:
        closeAllFiles(f)
