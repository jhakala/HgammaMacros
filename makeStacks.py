from os import path, makedirs, getcwd
from optparse import OptionParser
from copy import deepcopy

# new script to make all stackplots.
# John Hakala 7/14/16

parser = OptionParser()
parser.add_option("-c", "--cutName", dest="cutName",
                  help="the set of cuts to apply"                                      )
parser.add_option("-w", action="store_true", dest="withBtag"  , default=False,
                  help="if -w is used, then apply the btag cut"                        )
parser.add_option("-r", action="store_false", dest="showSigs" , default=True,
                  help="if -r is used, then do not show signals overlaid."             )
parser.add_option("-s", action="store_true", dest="sideband"  , default=False,
                  help="if -s is used, then look in sideband, not Higgs window."       )
parser.add_option("-f", action="store_true", dest="useScaleFactors" , default=False,
                  help = "use Btagging scalefactors"                                   )
parser.add_option("-l", action="store_false", dest="addLines"     , default=True,
                  help = "if -l is used, then do not draw a line at 1 in the ratios"   )
parser.add_option("-g", action="store_true", dest="graphics"     , default=False,
                  help = "turn off batch mode"                                         )
parser.add_option("-e", dest="edges",     
                  help = "the higgs mass window edges: either 100110, 5070, or 80100"  )
parser.add_option("-v", action="store_true", dest="vgMC", default=False,     
                  help = "if -v is used, make a stackplot for MC BG limits"            )
(options, args) = parser.parse_args()


from pyrootTools import isOrIsNot
dinkoMethod = False

if options.sideband is False:
  windowEdges="signalRegion"
if options.edges is not None and options.sideband is False:
  print "cannot specify a sideband window without the -s option."
  exit(1)
if options.edges is None and options.sideband is True:
  options.edges = "100110"
if options.sideband is True:
  if options.edges in "100110":
    windowEdges = [100.0,110.0]
  elif options.edges in "5070":
    windowEdges = [50.0,70.0]
  elif options.edges in "80100":
    windowEdges = [80.0,100.0]
  else:
    print "invalid higgs mass window supplied."
    exit(1)
if options.cutName=="preselection":
  windowEdges=[30.0, 99999.9]
  options.sideband=True

validCutNames = ["preselection", "nobtag", "btag", "antibtag", "nMinus1"]
if not options.cutName in validCutNames:
  print "please select a cutName with the -c option, options are: %s" % str(validCutNames )
  exit(1)

print "Making stackplots for %s cuts." % options.cutName,
if options.cutName != "preselection":
  print "The btagging cut %s being applied%s" % (
         isOrIsNot(options.withBtag, "singular"), 
         "and btagging scalefactors %s being used."%isOrIsNot(options.useScaleFactors, "plural") if options.withBtag else "."
        ),
  if options.sideband:
    print "Data %s shown in the mass window." % isOrIsNot(True, "singular"), windowEdges,
  print "MC backgrounds",
  if options.showSigs:
    print "and signals",
  print "%s being shown in the signal region [110.0, 140.0]." % isOrIsNot(True, "plural")

if windowEdges[0] == windowEdges[1]:
  print "something is funny with the windowEdges", windowEdges
  #print "exiting"
  #exit(1)

from ROOT import *
TColor.SetColorThreshold(0.1)
if not options.graphics:
  gROOT.SetBatch()

from pyrootTools import getSortedDictKeys, drawInNewCanvas
from HgPlotTools import getRangesDict, getHiggsRangesDict, makeAllHists
from HgParameters import getSamplesDirs, getVariableDict
from getMCbgWeights import getWeightsDict, getMCbgWeightsDict, getMCbgColors, getMCbgOrderedList, getMCbgLabels
from tcanvasTDR import TDRify
#for withBtag in [True, False]:
sideband = options.sideband
showSigs = options.showSigs
addLines = options.addLines
useScaleFactors = options.useScaleFactors
vgMC = options.vgMC
if vgMC and (not useScaleFactors or sideband or not options.cutName in ["btag", "antibtag"] ):
  print "vgMC was requested, but something is wrong... you must use scaleFactors, no sideband, and a cut of either 'btag' or 'antibtag'"
  exit(1)
for withBtag in [options.withBtag]:
  #print "withBtag is %r" % withBtag
  printNonempties = False
  printFileNames  = False

  if options.cutName=="preselection" or sideband:
    blindData       = False
  else:
    blindData    = True

  if windowEdges == "signalRegion":
    blindData = True

  sampleDirs = getSamplesDirs()

  rangesDict = getRangesDict(vgMC)
  #print ""
  #print "getRangesDict:"
  #print rangesDict

  higgsRangesDict = getHiggsRangesDict(vgMC)
  #print ""
  #print "getHiggsRangesDict:"
  #print higgsRangesDict

  #for sideband in ['100110','5070']:
  #  SidebandRangesDict = getSidebandRangesDict(sideband)
  #  print ""
  #  print "getSidebandRangesDict('%s')" % sideband
  #  print SidebandRangesDict


  #print ""
  #print ""
  #print "getMCbgWeights(): "
  mcBgWeights = getMCbgWeightsDict(sampleDirs["bkgSmall3sDir"])
  #print mcBgWeights
  treekey="higgs"
  for cutName in [options.cutName]:
    if cutName in [ "nMinus1" ]:
      if withBtag:
        histsDir = "%s/weightedMCbgHists_%s_withBtag"%(getcwd(), cutName )
      if not withBtag:
        histsDir = "%s/weightedMCbgHists_%s_noBtag"%(getcwd(), cutName )
    else:
      histsDir = "%s/weightedMCbgHists_%s"%(getcwd(), cutName)
    if sideband:
      if not cutName in "preselection":
        histsDir += "_sideband%i%i" % (windowEdges[0], windowEdges[1])
    if useScaleFactors:
      histsDir += "_SF"
    if vgMC:
      histsDir += "_vgMC"

    #print "going to pass makeAllHists windowEdges", windowEdges
    print "calling makeAllHists(" + str(cutName)  + ", " +  str(withBtag) + ", " + str(sideband) + ", " + str(useScaleFactors) + ", " + str(windowEdges) +", " + str(vgMC) + ",  " + str(vgMC) + ")"
    nonEmptyFilesDict = makeAllHists(cutName, withBtag, sideband, useScaleFactors, windowEdges, vgMC, vgMC)
    #print "done making all histograms."
    thstacks=[]
    thstackCopies=[]
    cans=[]
    pads=[]
    hists=[]
    tfiles=[]
    datahists=[]
    datahistsCopies=[]
    datafiles=[]
    sighists=[]
    sigfiles=[]
    lines=[]
    legendLabels = getMCbgLabels()
    varDict = getVariableDict()

    #for varkey in [higgsRangesDict.keys()[0]]:
    if "antibtag" in cutName and not useScaleFactors:
      for varkey in higgsRangesDict.keys():
        if "SF" in varkey:
          #print "about to get rid of ", varkey, "from the higgsRangesDict"
          higgsRangesDict.pop(varkey)
    for varkey in higgsRangesDict.keys():
      if "mcWeight" in varkey:
        continue;
      iRange = 1
      first = True
      for rng in higgsRangesDict[varkey]:
        print "working on range", rng, "for varkey", varkey
        if "btagSF" in varkey:
          continue;
        indexLabel = ""
        if not first:
          indexLabel +="_%i" % iRange
        cans.append(TCanvas())
        pads.append(TPad("stack_%s_%s%s"%(cutName, varkey, indexLabel), "stack_%s_%s%s"%(cutName, varkey, indexLabel), 0, 0.3, 1, 1.0))
        cans[-1].cd()
        pads[-1].Draw()
        pads[-1].cd()

        #### Build the stackplot
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
          dirName = "weightedMCbgHists_%s" % cutName
          if cutName in "nMinus1":
            if withBtag:
              dirName += "_withBtag"
            else:
              dirName += "_noBtag"
          #if sideband:
          #  dirName += "_sideband%i%i" % (windowEdges[0], windowEdges[1])
          if useScaleFactors:
            dirName += "_SF"
          if vgMC:
            dirName += "_vgMC"
          thisFileName = "%s/%s" % (dirName, filename)
          thisFileNameDefault = "%s/%s" % (dirName, filenameDefault)
          #print "going to use the MC background hist from file %s in building THStack " % thisFileName
          #HACKHACKHACK:
          if nonEmptyFilesDict[thisFileNameDefault] == "nonempty" and path.exists(thisFileName):
            #if printFileNames:
            #  print thisFileName
            #print "tfiles.append(TFile(path.join(", histsDir " ,", filename, ")))"
            #tfiles.append(TFile(path.join(histsDir , filename)))
            tfiles.append(TFile(thisFileName))
            #print "tfiles[-1]:", tfiles[-1].GetName()
            hists.append(tfiles[-1].Get("hist_%s" % filename))
            hists[-1].SetFillColor(getMCbgColors()[filekey])
            drawInNewCanvas(hists[-1], "HIST")
            integralsDict[hists[-1].Integral()] = hists[-1] 
            namesDict[hists[-1].GetName()] = hists[-1]
        for mcBG in getMCbgOrderedList():
          for key in namesDict:
            #print "key", key
            #print "namesDict[key]", namesDict[key]
            if mcBG in key:
              #print "mcBG found in namesDict[key]"
              #print "adding %s to stackplot; it has integral %f" % (integralsDict[key], key)
              thstacks[-1].Add(namesDict[key])
              thstackCopies[-1].Add(namesDict[key])

        #### Get the signal histograms
        

        if cutName in "nMinus1":
          if withBtag:
            outDirName = "stackplots_softdrop_%s_withBtag" % cutName
          else:
            outDirName = "stackplots_softdrop_%s_noBtag" % cutName
        else:
          outDirName = "stackplots_softdrop_%s" % cutName
        if sideband:
          if not cutName in "preselection":
            outDirName +="_sideband%i%i" %(windowEdges[0], windowEdges[1])
        if useScaleFactors:
          outDirName += "_SF"
        if vgMC:
          outDirName += "_vgMC"
        if not path.exists(outDirName):
          makedirs(outDirName)
        outfileName = "%s/%s_stack_%s%s.root"%(outDirName, cutName, varkey, indexLabel)
        outfile=TFile(outfileName, "RECREATE")
        cans[-1].cd()
        pads[-1].Draw()
        if not "SF" in varkey:
          pads[-1].SetLogy()
        pads[-1].cd()
        thstacks[-1].Draw("hist")
        thstacks[-1].SetMinimum(0.08)
        thstacks[-1].SetMaximum(thstacks[-1].GetMaximum()*45)
        #print thstacks[-1]
        hasAxis = False
        if thstacks[-1].GetXaxis():
          hasAxis = True
        if varkey in varDict.keys() and hasAxis:
          print "going to set title for thstacks[-1] to %s " % varkey
          print "varkey:", varkey
          print "varDict:", varDict
          print "varDict[varkey]:", varDict[varkey]
          print "thstacks[-1]", thstacks[-1]
          print "thstacks[-1].GetXaxis()", thstacks[-1].GetXaxis()
          #print "working on thstack with name: ", thstacks[-1].GetName()
          #print type(thstacks[-1].GetXaxis().GetTitle())
          thstacks[-1].GetXaxis().SetTitle(varDict[varkey])
          thstacks[-1].GetYaxis().SetTitle("Events/%g"%thstacks[-1].GetXaxis().GetBinWidth(1))
          thstacks[-1].GetYaxis().SetLabelSize(0.04)
          thstacks[-1].GetYaxis().SetTitleSize(0.04)
          thstacks[-1].GetYaxis().SetTitleOffset(1.2)

        dName = "weightedMCbgHists_%s" % cutName
        if cutName in "nMinus1":
          if withBtag:
            dName += "_withBtag"
          else:
            dName += "_noBtag"
        if sideband:
          if not cutName in "preselection":
            dName += "_sideband%i%i" % (windowEdges[0], windowEdges[1])
        if not blindData:
          dataFileName = varkey+"_"+treekey+"_data_2017%s.root" % indexLabel
          print "going to use data file",  dataFileName, "for the plot"
          datafiles.append(TFile("%s/%s"%(dName, dataFileName)))
          datahists.append(datafiles[-1].Get("hist_%s"%dataFileName))
          #print datahists[-1]
          datahists[-1].Draw("PE SAME")
          datahists[-1].SetMarkerStyle(20)
          datahists[-1].SetMarkerSize(datahists[-1].GetMarkerSize()*.7)
          datahistsCopies.append(datahists[-1].Clone())
        #for sigMass in [650, 750, 1000, 1250, 1500, 1750, 2000, 2500, 3000, 3500, 4000]:
        if showSigs:
          colors={}
          colors[700]=kCyan-6
          colors[1000]=kOrange
          colors[2000]=kMagenta
          colors[3000]=kRed
          for sigMass in [700, 1000, 2000, 3000]:
            sigFileName = varkey+"_"+treekey+"_Hg-%i%s.root"%(sigMass, indexLabel)
            rName = "weightedMCbgHists_%s" % cutName
            if cutName in "nMinus1":
              if withBtag:
                rName += "_withBtag"
              else:
                rName += "_noBtag"
            #if sideband:
            #  rName += "_sideband%i%i" % (windowEdges[0], windowEdges[1])
            if useScaleFactors:
              rName += "_SF"
            if vgMC:
              rName += "_vgMC"
            outDirName = "stackplots_softdrop_%s" % rName
            sigfiles.append(TFile("%s/%s"%(rName, sigFileName)))
            #print "adding signal file", sigfiles[-1].GetName(), "to the plot"
            sighists.append(sigfiles[-1].Get("hist_%s"%sigFileName))
            sighists[-1].SetLineStyle(3)
            sighists[-1].SetLineWidth(2)
            sighists[-1].SetLineColor(colors[sigMass])
            sighists[-1].SetTitle("H#gamma(%r TeV)"%(sigMass/float(1000)))
            #sighists[-1].SetMarkerSize(0)
            sighists[-1].Draw("hist SAME")

        pads[-1].SetBottomMargin(0)
        pads[-1].BuildLegend()
        cans[-1].cd()
        pads[-1].Draw()

        TDRify(pads[-1], False, "cpad_%s_%s"%(rName, sigFileName))
        for prim in pads[-1].GetListOfPrimitives():
          if "TLegend" in prim.IsA().GetName():
            prim.SetX1NDC(0.753)
            prim.SetY1NDC(0.703)
            prim.SetX2NDC(0.946)
            prim.SetY2NDC(0.911)
            for subprim in prim.GetListOfPrimitives():
              #print "subprim has label:", subprim.GetLabel()
              for key in legendLabels:
                if key in subprim.GetLabel():
                  subprim.SetLabel(legendLabels[key])
                  subprim.SetOption("lf")
                elif "data" in subprim.GetLabel():
                  #print "found something named SinglePhoton"
                  subprim.SetLabel("data")
                  subprim.SetOption("pe")
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
              print "sbscale is: ", sbScale
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
          TDRify(pads[-1], True, "cpad_%s_%s"%(rName, sigFileName))
        outfile.cd()
        cans[-1].Write()
        outfile.Close()
        iRange += 1
        first = False
print "done with makeStacks!"
exit(0)
