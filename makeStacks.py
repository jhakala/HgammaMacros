from os import path, makedirs
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
parser.add_option("-l", action="store_false", dest="addLines"     , default=True,
                  help = "if -l is used, then do not draw a line at 1 in the ratios"   )
parser.add_option("-b", action="store_true", dest="batch"     , default=False,
                  help = "turn on batch mode"                                          )
(options, args) = parser.parse_args()
print "options: ",
print options
print "args: ",
print args

from ROOT import *
if options.batch:
  gROOT.SetBatch()

from pyrootTools import getSortedDictKeys, drawInNewCanvas
from testpy import getRangesDict, getHiggsRangesDict, makeAllHists
from HgParameters import getSamplesDirs, getVariableDict
from getMCbgWeights import getWeightsDict, getMCbgWeightsDict, getMCbgColors, getMCbgOrderedList, getMCbgLabels
from tcanvasTDR import TDRify
#for withBtag in [True, False]:
sideband = options.sideband
showSigs = options.showSigs
addLines = options.addLines
for withBtag in [options.withBtag]:
  print "withBtag is %r" % withBtag
  printNonempties = False
  printFileNames  = False

  if options.cutName=="preselection" or sideband:
    blindData       = False
  else:
    blindData    = True

  sampleDirs = getSamplesDirs()

  rangesDict = getRangesDict()
  print ""
  print "getRangesDict:"
  print rangesDict

  higgsRangesDict = getHiggsRangesDict()
  print ""
  print "getHiggsRangesDict:"
  print higgsRangesDict

  #for sideband in ['100110','5070']:
  #  SidebandRangesDict = getSidebandRangesDict(sideband)
  #  print ""
  #  print "getSidebandRangesDict('%s')" % sideband
  #  print SidebandRangesDict


  print ""
  print ""
  print "getMCbgWeights(): "
  mcBgWeights = getMCbgWeightsDict(sampleDirs["small3sDir"])
  print mcBgWeights
  treekey="higgs"
  for cutName in [options.cutName]:
    if cutName in [ "nMinus1" ]:
      if withBtag:
        histsDir = "~/WZgammaMacros/weightedMCbgHists_%s_withBtag"%cutName 
      if not withBtag:
        histsDir = "~/WZgammaMacros/weightedMCbgHists_%s_noBtag"%cutName 
    else:
      histsDir = "~/WZgammaMacros/weightedMCbgHists_%s"%cutName
    if sideband:
      histsDir += "_sideband"
    nonEmptyFilesDict = makeAllHists(cutName, withBtag, sideband)
    print "done making all histograms."
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
    for varkey in higgsRangesDict.keys():
      cans.append(TCanvas())
      pads.append(TPad("stack_%s_%s"%(cutName, varkey), "stack_%s_%s"%(cutName, varkey), 0, 0.3, 1, 1.0))
      cans[-1].cd()
      pads[-1].Draw()
      pads[-1].cd()

      #### Build the stackplot
      thstacks.append(THStack("thstack_%s_%s"%(cutName, varkey),""))
      thstackCopies.append(THStack("thstackCopy_%s_%s"%(cutName, varkey),""))
      integralsDict={}
      namesDict={}
      for filekey in mcBgWeights.keys():
        filename = varkey+"_"+treekey+"_"+filekey
        if printNonempties:
          print "The nonempty files dict is:"
          print nonEmptyFilesDict
        dirName = "weightedMCbgHists_%s" % cutName
        if cutName in "nMinus1":
          if withBtag:
            dirName += "_withBtag"
          else:
            dirName += "_noBtag"
        if sideband:
          dirName += "_sideband"
        thisFileName = "%s/%s" % (dirName, filename)
        print "going to use the hist from file %s in building THStack " % thisFileName
        if nonEmptyFilesDict[thisFileName] == "nonempty":
          #if printFileNames:
          #  print thisFileName
          tfiles.append(TFile(path.join(histsDir , filename)))
          hists.append(tfiles[-1].Get("hist_%s" % filename))
          hists[-1].SetFillColor(getMCbgColors()[filekey])
          drawInNewCanvas(hists[-1])
          integralsDict[hists[-1].Integral()] = hists[-1] 
          namesDict[hists[-1].GetName()] = hists[-1]
      for mcBG in getMCbgOrderedList():
        for key in namesDict:
          if mcBG in key:
            #print "adding %s to stackplot; it has integral %f" % (integralsDict[key], key)
            thstacks[-1].Add(namesDict[key])
            thstackCopies[-1].Add(namesDict[key])

      #### Get the signal histograms
      

      if cutName in "nMinus1":
        if withBtag:
          outDirName = "stackplots_%s_withBtag" % cutName
        else:
          outDirName = "stackplots_%s_noBtag" % cutName
      else:
        outDirName = "stackplots_%s" % cutName
      if sideband:
        outDirName +="_sideband"
      if not path.exists(outDirName):
        makedirs(outDirName)
      outfileName = "%s/%s_stack_%s.root"%(outDirName, cutName, varkey)
      outfile=TFile(outfileName, "RECREATE")
      cans[-1].cd()
      pads[-1].Draw()
      pads[-1].cd()
      thstacks[-1].Draw()
      thstacks[-1].SetMinimum(0.08)
      thstacks[-1].SetMaximum(thstacks[-1].GetMaximum()*45)
      print thstacks[-1]
      if varkey in varDict.keys():
        print "going to set title for thstacks[-1] to %s " % varkey
        thstacks[-1].GetXaxis().SetTitle(varDict[varkey])
      thstacks[-1].GetYaxis().SetTitle("Events/%g"%thstacks[-1].GetXaxis().GetBinWidth(1))
      thstacks[-1].GetYaxis().SetLabelSize(0.04)
      thstacks[-1].GetYaxis().SetTitleSize(0.04)
      thstacks[-1].GetYaxis().SetTitleOffset(1.2)

      dataFileName = varkey+"_"+treekey+"_SilverJson.root"
      dName = "weightedMCbgHists_%s" % cutName
      if cutName in "nMinus1":
        if withBtag:
          dName += "_withBtag"
        else:
          dName += "_noBtag"
      if sideband:
        dName += "_sideband"
      datafiles.append(TFile("%s/%s"%(dName, dataFileName)))
      print datafiles[-1]
      datahists.append(datafiles[-1].Get("hist_%s"%dataFileName))
      print datahists[-1]
      if not blindData:
        datahists[-1].Draw("PE SAME")
      datahists[-1].SetMarkerStyle(20)
      datahistsCopies.append(datahists[-1].Clone())
      #for sigMass in [650, 750, 1000, 1250, 1500, 1750, 2000, 2500, 3000, 3500, 4000]:
      if showSigs:
        colors={}
        colors[750]=kCyan-6
        colors[1000]=kOrange
        colors[2050]=kMagenta
        colors[3250]=kRed
        for sigMass in [750, 1000, 2050, 3250]:
          sigFileName = varkey+"_"+treekey+"_signal_m%i.root"%sigMass
          rName = "weightedMCbgHists_%s" % cutName
          if cutName in "nMinus1":
            if withBtag:
              rName += "_withBtag"
            else:
              rName += "_noBtag"
          if sideband:
            rName += "_sideband"
          outDirName = "stackplots_%s" % rName
          sigfiles.append(TFile("%s/%s"%(rName, sigFileName)))
          sighists.append(sigfiles[-1].Get("hist_%s"%sigFileName))
          sighists[-1].SetLineStyle(3)
          sighists[-1].SetLineWidth(2)
          sighists[-1].SetLineColor(colors[sigMass])
          sighists[-1].SetTitle("H#gamma(%r TeV)"%(sigMass/float(1000)))
          sighists[-1].SetMarkerSize(0)
          sighists[-1].Draw("SAME")

      pads[-1].SetBottomMargin(0)
      pads[-1].BuildLegend()
      cans[-1].cd()
      pads[-1].Draw()

      TDRify(pads[-1])
      for prim in pads[-1].GetListOfPrimitives():
        if "TLegend" in prim.IsA().GetName():
          prim.SetX1NDC(0.753)
          prim.SetY1NDC(0.703)
          prim.SetX2NDC(0.946)
          prim.SetY2NDC(0.911)
          for subprim in prim.GetListOfPrimitives():
            for key in legendLabels:
              if key in subprim.GetLabel():
                subprim.SetLabel(legendLabels[key])
                subprim.SetOption("lf")
              elif "SilverJson" in subprim.GetLabel():
                subprim.SetLabel("data")
                subprim.SetOption("pe")

      pads.append(TPad("ratio_%s_%s"%(cutName, varkey), "ratio_%s_%s"%(cutName, varkey), 0, 0.05, 1, 0.3))
      pads[-1].SetTopMargin(0)
      pads[-1].SetBottomMargin(0.15)
      pads[-1].cd()

      fullStack = thstackCopies[-1].GetStack().Last()
      fullStack.Sumw2()
      if varkey in varDict.keys():
        fullStack.GetXaxis().SetTitle(varDict[varkey])
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
      TDRify(pads[-1], True)
      outfile.cd()
      cans[-1].Write()
      outfile.Close()

