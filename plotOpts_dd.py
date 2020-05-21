# John Hakala, 12/1/2016
# Makes optimization plots by sliding cuts over N-1 stackplots from makeStacks.py


from optTools import *

def makeOpt(analysis, var, inFileName_sideband, inFileName_higgswindow, upDown, withBtag, srCans, srPads, sbCans, sbPads, stacks, sidebands, i, windowEdges, isTagger, useMC=False, omitData = False):
  
  debug=True
  inFile_higgswindow     = TFile.Open(inFileName_higgswindow)
  if debug:
    print "inFile_higgswindow is: %s" % inFile_higgswindow.GetName()
  inFile_sideband     = TFile.Open(inFileName_sideband)
  if debug:
    print "inFile_sideband is: %s" % inFile_sideband.GetName()

  can_higgswindow = getCanvas(inFile_higgswindow, i)
  srCans.append(can_higgswindow)

  pad_higgswindow = getTopPad(inFile_higgswindow.GetName(), i, can_higgswindow)
  srPads.append(pad_higgswindow)

  bottomPad_higgswindow = getRatioPad(inFile_higgswindow.GetName(), i, can_higgswindow)
  srPads.append(bottomPad_higgswindow)
  bottomPad_ratio=srPads[-1]
  can_higgswindow.Draw()

  can_sideband = getCanvas(inFile_sideband, i, True)
  sbCans.append(can_sideband)

  pad_sideband = getTopPad(inFile_sideband.GetName(), i, can_sideband, True)
  sbPads.append(pad_sideband)

  for prim in can_sideband.GetListOfPrimitives():
    if "ratio" in prim.GetName():
      bottomPad_sideband = prim
      for primitive in bottomPad_sideband.GetListOfPrimitives():
        if not ("TLine" in primitive.IsA().GetName() or "TFrame" in primitive.IsA().GetName()):
          primitive.SetName("%s_%s_sideband" % (inFileName_sideband, primitive.GetName()))
      SetOwnership(bottomPad_sideband, False)
      sbPads.append(bottomPad_sideband)
      bottomPad_ratio = sbPads[-1]


  for subprim in pad_higgswindow.GetListOfPrimitives():
    #print "pad_higgswindow has primitive: %s" % subprim.GetName()
    if "-800" in subprim.GetName():
      name800 = subprim.GetName()
    if "-1000" in subprim.GetName():
      name1000 = subprim.GetName()
    if "-2000" in subprim.GetName():
      name2000 = subprim.GetName()
    if "-3000" in subprim.GetName():
      name3000 = subprim.GetName()
    #if "m4000" in subprim.GetName():
    #  name4000 = subprim.GetName()
    if "THStack" in subprim.IsA().GetName():
      subprim.SetName("%i_theStack_%s" % ( i, inFileName_higgswindow))
      stack = subprim
      SetOwnership(stack, False)
      stacks.append(stack)
    if "SilverJson" in subprim.GetName():
      print "this is screwy, some SilverJson crap"
      exit(1)
      subprim.SetName("garbage_%i_%s_%s" % (i, inFileName_higgswindow, subprim.GetName()))
      subprim.Delete()

  for subprim in pad_sideband.GetListOfPrimitives():
    if debug:
      print "pad_sideband has primitive:", subprim.GetName()
    if "data" in subprim.GetName():
      subprim.SetName("%i_theSideband_%s" % (i, inFileName_sideband))
      sideband = subprim
      if omitData:
        sideband.Reset()
      SetOwnership(sideband, False)
      sidebands.append(sideband)
    elif "THStack" in subprim.IsA().GetName() or "THist" in subprim.IsA().GetName():
      subprim.SetName("garbage_%i_%s_%s" % (i, inFileName_sideband, subprim.GetName()))
      subprim.Delete()

  if not omitData:
    sbNorm = getSbNorm(stack, sideband, omitData)
    if debug:
      print "number of entries in stack is   : %f" % stack.GetStack().Last().GetSumOfWeights()
      print "number of entries in sideband is: %f" % sideband.GetSumOfWeights()
      print "                       sbNorm is: %f" % sbNorm 
    for sbBin in range (1, sideband.GetXaxis().GetNbins()+1):
      sideband.SetBinContent(sbBin, sideband.GetBinContent(sbBin)*sbNorm)
  #stack = stacks[-1]
  #theSideband = sidebands[-1]
  #print stack

  ## HERE?  can_higgswindow.Draw()
  m800 = pad_higgswindow.GetPrimitive(name800)
  color800 = kTeal
  m800.SetLineColor(color800)
  m800.SetLineStyle(2)
  m800.SetLineWidth(3)
  m1000 = pad_higgswindow.GetPrimitive(name1000)
  color1000  = kOrange-3
  m1000.SetLineColor(color1000)
  m1000.SetLineStyle(2)
  m1000.SetLineWidth(3)
  m2000 = pad_higgswindow.GetPrimitive(name2000)
  color2000 = kPink-3
  m2000.SetLineColor(color2000)
  m2000.SetLineStyle(2)
  m2000.SetLineWidth(3)
  m3000 = pad_higgswindow.GetPrimitive(name3000)
  color3000 = kRed+2
  m3000.SetLineColor(color3000)
  m3000.SetLineStyle(2)
  m3000.SetLineWidth(3)

  #m4000 = pad.GetPrimitive(name4000)
  if useMC:
    total = stack.GetStack().Last()
  else:
    total = sideband

  if not m800.GetNbinsX() == total.GetNbinsX():
    #print "nonmatching histograms!"
    quit()

  graphPoints800 = []
  graphPoints1000 = []
  graphPoints2000 = []
  graphPoints3000 = []
  #graphPoints4000 = []
  nSteps = total.GetNbinsX()
  # HACK HACK
  lowerBound = getRangesDict(analysis)[whichVarAmI(inFileName_higgswindow)][0][0]
  upperBound = getRangesDict(analysis)[whichVarAmI(inFileName_higgswindow)][0][1]
  # END HACK HACK
  stepSize = (upperBound-lowerBound)/nSteps
  for i in range(-1, total.GetNbinsX()):
    slideValue = lowerBound+i*stepSize
    if i==-1:
      if upDown in "down":
        sOverRootB800 = "b=0"
        sOverRootB1000 = "b=0"
        sOverRootB2000 = "b=0"
        sOverRootB3000 = "b=0"
      elif upDown in "up":
        sOverRootB800 = m800.GetSumOfWeights()/sqrt(total.GetSumOfWeights()), [m800.GetSumOfWeights(), total.GetSumOfWeights()]
        sOverRootB1000 = m1000.GetSumOfWeights()/sqrt(total.GetSumOfWeights()), [m1000.GetSumOfWeights(), total.GetSumOfWeights()]
        sOverRootB2000 = m2000.GetSumOfWeights()/sqrt(total.GetSumOfWeights()), [m2000.GetSumOfWeights(), total.GetSumOfWeights()]
        sOverRootB3000 = m3000.GetSumOfWeights()/sqrt(total.GetSumOfWeights()), [m3000.GetSumOfWeights(), total.GetSumOfWeights()]
    if i>=0:
      sOverRootB800  = getSoverRootB(total,  m800, slideValue, upDown, withBtag, useMC)
      sOverRootB1000 = getSoverRootB(total, m1000, slideValue, upDown, withBtag, useMC)
      sOverRootB2000 = getSoverRootB(total, m2000, slideValue, upDown, withBtag, useMC)
      sOverRootB3000 = getSoverRootB(total, m3000, slideValue, upDown, withBtag, useMC)
    if type(sOverRootB800[0]) is float : 
      graphPoints800.append([slideValue, sOverRootB800])
      #print "filled point %f %f into graphPoints800 direction %s" % ( slideValue, sOverRootB800[0], upDown)
    if type(sOverRootB1000[0]) is float : 
      graphPoints1000.append([slideValue, sOverRootB1000])
      #print "filled point %f %f into graphPoints1000 direction %s" % ( slideValue, sOverRootB1000[0], upDown)
    if type(sOverRootB2000[0]) is float : 
      graphPoints2000.append([slideValue, sOverRootB2000])
      #print "filled point %f %f into graphPoints2000 direction %s" % ( slideValue, sOverRootB2000[0], upDown)
    if type(sOverRootB3000[0]) is float : 
      graphPoints3000.append([slideValue, sOverRootB3000])
      #print "filled point %f %f into graphPoints3000 direction %s" % ( slideValue, sOverRootB3000[0], upDown)
    #if type(sOverRootB4000) is float : 
    #  graphPoints4000.append([slideValue, sOverRootB2000])

  #  print graphPoints
  #graph4000 = TGraph()
  #for graphPoint4000 in graphPoints4000:
  #  graph4000.SetPoint(graph4000.GetN(), graphPoint4000[0], graphPoint4000[1])
  #  #print "set point in graph4000"
  if isTagger and upDown == "up":
    graphData = {"graphPoints3000": graphPoints3000, "graphPoints2000": graphPoints2000, "graphPoints1000":graphPoints1000, "graphPoints800":graphPoints800}
    if useMC:
      pickle.dump(graphData, open("tagOpt_mcBG_%s/tagOpt_%s.pkl" % (analysis, var), "wb"))
    else:
      pickle.dump(graphData, open("tagOpt_%s/tagOpt_%s.pkl" % (analysis, var), "wb"))
  #  print graph[0], graph[1]
  graph3000 = TGraph()
  graph3000.SetName("optGraph_%s"%name3000)
  for graphPoint3000 in graphPoints3000:
    graph3000.SetPoint(graph3000.GetN(), graphPoint3000[0], graphPoint3000[1][0])
    #print "set point in graph3000"

  graph2000 = TGraph()
  graph2000.SetName("optGraph_%s"%name2000)
  for graphPoint2000 in graphPoints2000:
    graph2000.SetPoint(graph2000.GetN(), graphPoint2000[0], graphPoint2000[1][0])
    #print "set point in graph2000"

  graph1000 = TGraph()
  graph1000.SetName("optGraph_%s"%name1000)
  for graphPoint1000 in graphPoints1000:
    graph1000.SetPoint(graph1000.GetN(), graphPoint1000[0], graphPoint1000[1][0])
    #print "set point in graph1000"

  graph800 = TGraph()
  graph800.SetName("optGraph_%s"%name800)
  for graphPoint800 in graphPoints800:
    graph800.SetPoint(graph800.GetN(), graphPoint800[0], graphPoint800[1][0])
    #print "set point in graph800"

  #bottomPad_higgswindow.cd()
  #bottomPad_higgswindow.Clear()
  bottomPad_ratio.cd()
  bottomPad_ratio.Clear()
  graph2000.Draw()
  graph2000.GetXaxis().SetLimits(lowerBound, upperBound)
  #graph1000.Draw()
  #graph1000.GetXaxis().SetLimits(lowerBound, upperBound)
  #bottomPad_higgswindow.SetBottomMargin(0.18)
  #bottomPad_higgswindow.SetBorderSize(0)
  #bottomPad_higgswindow.Draw()
  bottomPad_ratio.SetBottomMargin(0.18)
  bottomPad_ratio.SetBorderSize(0)
  bottomPad_ratio.Draw()
  pad_higgswindow.SetBottomMargin(0.15)
  can_higgswindow.cd()
  #pad.SetBBoxY1(-2)
  #pad.SetBBoxY2(105)
  pad_higgswindow.Draw()
  pad_higgswindow.cd()
  sideband.SetMarkerStyle(20)
  sideband.SetMarkerColor(kBlack)
  sideband.SetLineColor(kBlack)
  sideband.Draw("SAME PE")
  for prim in pad_higgswindow.GetListOfPrimitives():
    if "TLegend" in prim.IsA().GetName():
      prim.InsertEntry(sideband.GetName(), "Sideband %i GeV < m_{j} < %i GeV" % (windowEdges[0], windowEdges[1]))

  #bottomPad_higgswindow.cd()
  bottomPad_ratio.cd()
  graph2000.GetYaxis().SetTitle("S/#sqrt{B} (a.u.)")
  #graph2000.GetYaxis().SetLabelSize(0)
  graph2000.GetXaxis().SetLabelSize(0.1)
  graph2000.GetYaxis().SetTitleSize(0.12)
  graph2000.GetYaxis().SetTitleOffset(.3)
  graph2000.GetXaxis().SetTitle("cut value")
  graph2000.GetXaxis().SetTitleSize(0.12)
  graph2000.GetXaxis().SetTitleOffset(0.65)
  graph2000.SetLineStyle(2)
  graph2000.SetLineWidth(2)
  graph2000.SetLineColor(color2000)
  graph2000.SetFillColor(kWhite)
  graph2000.SetMarkerStyle(20)
  graph2000.SetMarkerSize(0)
  graph3000.Draw("SAME")
  graph3000.SetLineStyle(2)
  graph3000.SetLineWidth(2)
  graph3000.SetLineColor(color3000)
  graph3000.SetFillColor(kWhite)
  graph1000.Draw("SAME")
  graph1000.SetLineStyle(2)
  graph1000.SetLineWidth(2)
  graph1000.SetLineColor(color1000)
  graph1000.SetFillColor(kWhite)
  graph800.Draw("SAME")
  graph800.SetLineStyle(2)
  graph800.SetLineWidth(2)
  graph800.SetLineColor(color800)
  graph800.SetFillColor(kWhite)
  #bottomPad_higgswindow.BuildLegend()
  bottomPad_ratio.BuildLegend()
  legendLabels = getMCbgLabels()
  #for prim in bottomPad_higgswindow.GetListOfPrimitives():
  for prim in bottomPad_ratio.GetListOfPrimitives():
    if "TLegend" in prim.IsA().GetName():
      prim.SetX1NDC(0.753)
      prim.SetY1NDC(0.703)
      prim.SetX2NDC(0.946)
      prim.SetY2NDC(0.911)
      for subprim in prim.GetListOfPrimitives():
        for mass in ["800", "1000", "2000", "3000"]:
          if mass in subprim.GetLabel():
            subprim.SetLabel("%s#gamma(%r TeV)"%(arguments.analysis[0], (float(mass)/float(1000))))
            subprim.SetOption("lf")
  can_higgswindow.cd()
  #bottomPad_higgswindow.Draw()
  bottomPad_ratio.Draw()
  pad_higgswindow.SetBorderSize(0)

  
  outDirName = None
  if withBtag:
    if useMC:
      outDirName = "%s_optplots_nMinus1_withBtag_dd_sb%i%i_mcBG" % (analysis, windowEdges[0], windowEdges[1])
    else:
      outDirName = "%s_optplots_nMinus1_withBtag_dd_sb%i%i" % (analysis, windowEdges[0], windowEdges[1])
    outFileName="%s/%s"%(outDirName, inFileName_higgswindow.split("/")[1])
  else:
    if useMC:
      outDirName =  "%s_optplots_nMinus1_noBtag_dd_sb%i%i_mcBG" % (analysis, windowEdges[0], windowEdges[1])
    else:
      outDirName =  "%s_optplots_nMinus1_noBtag_dd_sb%i%i" % (analysis, windowEdges[0], windowEdges[1])
    outFileName="%s/%s"%(outDirName, inFileName_higgswindow.split("/")[1])
  if not path.exists(outDirName):
    makedirs(outDirName)
  outFileName=outFileName.split(".")[0]
  outFile = TFile.Open("%s_%r.root"%(outFileName, upDown), "RECREATE")
  print outFile.GetName()
  outFile.cd()
  can_higgswindow.Write()
  can_higgswindow.Print("%s_%r.pdf"%(outFileName, upDown))
  outFile.Close()
  inFile_higgswindow.Close()
  del inFile_higgswindow
  inFile_sideband.Close()
  del inFile_sideband

if __name__ == "__main__":
  from argparse import ArgumentParser
  parser = ArgumentParser()

  parser.add_argument("-b", "--tagoption", required=True,
                      dest="tagoption", help="either 'withBtag' or 'noBtag'")
  parser.add_argument("-s", "--sideband", required=True,
                      dest="sideband", help="either 100110, 5070, or 80100")
  parser.add_argument("-a", "--analysis", required=True,
                      dest="analysis", help="either 'Hg' or 'Zg'")
  parser.add_argument("-m", "--useMC", action="store_true",
                      dest="useMC", help="use MC background rather than sideband")
  parser.add_argument("-o", "--omitData", action="store_true",
                      dest="omitData", help="don't bother with data, only do MC bg stuff")
  arguments = parser.parse_args()
  if not arguments.tagoption in ["withBtag", "noBtag"] :
    print "invalid first argument: either 'withBtag' or 'noBtag'"
    exit(1)
  withBtag = arguments.tagoption
  if arguments.sideband in "100110":
    windowEdges = [100.0, 110.0]
  elif arguments.sideband in "5070":
    windowEdges = [50.0, 70.0]
  elif arguments.sideband in "80100":
    windowEdges = [80.0, 100.0]
    print "this is a weird sideband:", arguments.sideband
    exit(1)
  else: 
    print "bad sideband:", arguments.sideband
    exit(1)
  
  from os import path, makedirs
  from math import sqrt
  import pickle
  from ROOT import *
  from VgParameters import getRangesDict, getHiggsRangesDict, isVarTagger
  from getMCbgWeights import getMCbgLabels
  from pyrootTools import isOrIsNot

  #gROOT.SetBatch()
  debugOneVar = False

  #for direction in ["up", "down", "spacer"]:
  for direction in ["up", "down"]:
    if "spacer" in direction:
      print "exiting"
      from time import sleep
      sleep(3)
      exit()
    srCans =  []
    srPads =  []
    sbCans =  []
    sbPads =  []
    stacks = []
    sidebands = []
    i=0
    for key in getHiggsRangesDict().keys():
      print "working on key:", key
      isTagger = isVarTagger(key)
      print "  -> this variable", isOrIsNot(isTagger, "singular"), "a b-tagger"
      if debugOneVar and not key=="phPtOverMgammaj":
        continue
      if "btagSF" in key or key=="mcWeight":
        continue
      sideband_varName    = "%s_stackplots_softdrop_nMinus1_%s_sideband%i%i/nMinus1_stack_%s.root"%( arguments.analysis, withBtag, windowEdges[0], windowEdges[1], key)
      higgswindow_varName = "%s_stackplots_softdrop_nMinus1_%s/nMinus1_stack_%s.root"%(arguments.analysis, withBtag, key)
      makeOpt(arguments.analysis, key, sideband_varName, higgswindow_varName, direction, withBtag == "withBtag", srCans, srPads, sbCans, sbPads, stacks, sidebands, i, windowEdges, isTagger, arguments.useMC, arguments.omitData)
      i+=1
  #for direction in ["up", "down"]:
  #  srCans =  []
  #  srPads =  []
  #  sbCans =  []
  #  sbPads =  []
  #  stacks = []
  #  sidebands = []
  #  i=0
  #  for key in getHiggsRangesDict().keys():
  #    sideband_varName = "stackplots_softdrop_nMinus1_noBtag_sideband/nMinus1_stack_%s.root"%key
  #    higgswindow_varName = "stackplots_softdrop_nMinus1_noBtag/nMinus1_stack_%s.root"%key
  #    makeOpt(sideband_varName, higgswindow_varName, direction, False, srCans, srPads, sbCans, sbPads, stacks, sidebands, i)
  #    i+=1
  #  if direction is direction[-1]:
  #    exit(0)
