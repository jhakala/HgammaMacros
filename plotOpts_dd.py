from math import sqrt
from ROOT import *
from testpy import getRangesDict, getHiggsRangesDict
from getMCbgWeights import getMCbgLabels
from os import path, makedirs

# John Hakala, 12/1/2016
# Makes optimization plots by sliding cuts over N-1 stackplots from makeStacks.py

gROOT.SetBatch()
debugOneVar = True

def whichVarAmI(inFileName):
  for key in getRangesDict().keys():
    if key in inFileName:
      iAm = key
  return iAm

def getSoverRootB(bkg, sig, start, goUpOrDown, withBtag):
  bb=0.
  ss=0.
  if goUpOrDown in "up":
    for iBin in range(bkg.FindBin(start), bkg.GetNbinsX()):
      bb+=bkg.GetBinContent(iBin)
      ss+=sig.GetBinContent(iBin)
  elif goUpOrDown in "down":
    for iBin in range(0, bkg.FindBin(start)):
      bb+=bkg.GetBinContent(iBin)
      ss+=sig.GetBinContent(iBin)
  if bb != 0:
    return ss/sqrt(bb)
  else:
    return "b=0"

def makeOpt(inFileName_sideband, inFileName_higgswindow, upDown, withBtag, srCans, srPads, sbCans, sbPads, stacks, sidebands, i, windowEdges):
  
  debug=True
  inFile_higgswindow     = TFile(inFileName_higgswindow)
  if debug:
    print "inFile_higgswindow is: %s" % inFile_higgswindow.GetName()
  inFile_sideband     = TFile(inFileName_sideband)
  if debug:
    print "inFile_sideband is: %s" % inFile_sideband.GetName()

  for key in inFile_higgswindow.GetListOfKeys():
    #print key.GetName()
    if "c1" in key.GetName():
      can_higgswindow = inFile_higgswindow.Get(key.GetName()).DrawClone()
      can_higgswindow.SetName("%i_%s_c1_higgswindow" % (i, inFileName_higgswindow))
      #print "can_higgswindow: ",
      #print can_higgswindow
      SetOwnership(can_higgswindow, False)
      srCans.append(can_higgswindow)
      #canName_higgswindow = "c1_higgswindow"
        
  for key in inFile_higgswindow.GetListOfKeys():
    if debug:
      print "inFile_higgswindow is: %s" % inFile_higgswindow.GetName()
      print "inFile_higgswindow has key: ", 
      print key.GetName()
  #print "canName_higgswindow: %s" % canName_higgswindow 
  if debug:
    print can_higgswindow
  for prim in can_higgswindow.GetListOfPrimitives():
    if debug:
      print "can_higgswindow has primitive: %s" % prim.GetName()
    prim.SetName("%i_%s_higgswindow" % (i, prim.GetName()))
    #print "can_higgswindow has renamed primitive: %s" % prim.GetName()
    if "stack" in prim.GetName():
      pad_higgswindow = prim
      for primitive in pad_higgswindow.GetListOfPrimitives():
        if not ("TLine" in primitive.IsA().GetName() or "TFrame" in primitive.IsA().GetName()):
          primitive.SetName("%s_%s_higgswindow" % (inFileName_higgswindow, primitive.GetName()))
      #print "pad_higgswindow: ",
      #print  pad_higgswindow
      SetOwnership(pad_higgswindow, False)
      srPads.append(pad_higgswindow)
      #print "using higgswindow stack: %s" % padName_higgswindow
    if debug:
      print "prim.GetName()", prim.GetName()
    if "ratio" in prim.GetName():
      bottomPad_higgswindow = prim
      for primitive in bottomPad_higgswindow.GetListOfPrimitives():
        if not ("TLine" in primitive.IsA().GetName() or "TFrame" in primitive.IsA().GetName()):
          primitive.SetName("%s_%s_higgswindow" % (inFileName_higgswindow, primitive.GetName()))
      SetOwnership(bottomPad_higgswindow, False)
      srPads.append(bottomPad_higgswindow)
      bottomPad_ratio=srPads[-1]
      


  for key in inFile_sideband.GetListOfKeys():
    #print key.GetName()
    #print "inFile_sideband is: %s" % inFile_sideband.GetName()
    if "c1" in key.GetName():
      can_sideband = inFile_sideband.Get(key.GetName()).DrawClone()
      can_sideband.SetName("%i_%s_c1_sideband" % (i, inFileName_sideband))
      SetOwnership(can_sideband, False)
      sbCans.append(can_sideband)
  can_higgswindow.Draw()
  for prim in can_sideband.GetListOfPrimitives():
    if debug:
      print "can_sideband has primitive: %s" % prim.GetName()
    prim.SetName("%i_%s_sideband" % (i, prim.GetName()))
    #print "can_sideband has renamed primitive: %s" % prim.GetName()
    if "stack" in prim.GetName():
      pad_sideband = prim
      for primitive in pad_sideband.GetListOfPrimitives():
        if not ("TLine" in primitive.IsA().GetName() or "TFrame" in primitive.IsA().GetName()):
          primitive.SetName("%s_%s_sideband" % (inFileName_sideband, primitive.GetName()))
      SetOwnership(pad_sideband, False)
      sbPads.append(pad_sideband)
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
    if "m750" in subprim.GetName():
      name750 = subprim.GetName()
    if "m1000" in subprim.GetName():
      name1000 = subprim.GetName()
    if "m2050" in subprim.GetName():
      name2050 = subprim.GetName()
    if "m3250" in subprim.GetName():
      name3250 = subprim.GetName()
    #if "m4000" in subprim.GetName():
    #  name4000 = subprim.GetName()
    if "THStack" in subprim.IsA().GetName():
      subprim.SetName("%i_theStack_%s" % ( i, inFileName_higgswindow))
      stack = subprim
      SetOwnership(stack, False)
      stacks.append(stack)
    if "SilverJson" in subprim.GetName():
      subprim.SetName("garbage_%i_%s_%s" % (i, inFileName_higgswindow, subprim.GetName()))
      subprim.Delete()

  for subprim in pad_sideband.GetListOfPrimitives():
    if "SinglePhoton" in subprim.GetName():
      subprim.SetName("%i_theSideband_%s" % (i, inFileName_sideband))
      sideband = subprim
      SetOwnership(sideband, False)
      sidebands.append(sideband)
    elif "THStack" in subprim.IsA().GetName() or "THist" in subprim.IsA().GetName():
      subprim.SetName("garbage_%i_%s_%s" % (i, inFileName_sideband, subprim.GetName()))
      subprim.Delete()


  def getSbNorm(stack, sideband, mode="matchMCsig"):
    if mode=="matchMCsig":
      return stack.GetStack().Last().GetSumOfWeights()/float(sideband.GetSumOfWeights())

  sbNorm = getSbNorm(stack, sideband)
  #sbNorm = stack.GetStack().Last().GetSumOfWeights()/float(sideband.GetSumOfWeights())

  print "number of entries in stack is   : %f" % stack.GetStack().Last().GetSumOfWeights()
  print "number of entries in sideband is: %f" % sideband.GetSumOfWeights()
  print "                       sbNorm is: %f" % sbNorm 
  for sbBin in range (1, sideband.GetXaxis().GetNbins()+1):
    sideband.SetBinContent(sbBin, sideband.GetBinContent(sbBin)*sbNorm)
  #stack = stacks[-1]
  #theSideband = sidebands[-1]
  #print stack

  ## HERE?  can_higgswindow.Draw()
  m750 = pad_higgswindow.GetPrimitive(name750)
  color750 = kTeal
  m750.SetLineColor(color750)
  m750.SetLineStyle(2)
  m750.SetLineWidth(3)
  m1000 = pad_higgswindow.GetPrimitive(name1000)
  color1000  = kOrange-3
  m1000.SetLineColor(color1000)
  m1000.SetLineStyle(2)
  m1000.SetLineWidth(3)
  m2050 = pad_higgswindow.GetPrimitive(name2050)
  color2050 = kPink-3
  m2050.SetLineColor(color2050)
  m2050.SetLineStyle(2)
  m2050.SetLineWidth(3)
  m3250 = pad_higgswindow.GetPrimitive(name3250)
  color3250 = kRed+2
  m3250.SetLineColor(color3250)
  m3250.SetLineStyle(2)
  m3250.SetLineWidth(3)

  #m4000 = pad.GetPrimitive(name4000)
  total = sideband
  if not m750.GetNbinsX() == total.GetNbinsX():
    #print "nonmatching histograms!"
    quit()

  graphPoints750 = []
  graphPoints1000 = []
  graphPoints2050 = []
  graphPoints3250 = []
  #graphPoints4000 = []
  nSteps = total.GetNbinsX()
  # HACK HACK
  lowerBound = getRangesDict()[whichVarAmI(inFileName_higgswindow)][0][0]
  upperBound = getRangesDict()[whichVarAmI(inFileName_higgswindow)][0][1]
  # END HACK HACK
  stepSize = (upperBound-lowerBound)/nSteps
  for i in range(0, total.GetNbinsX()):
    slideValue = lowerBound+i*stepSize
    sOverRootB750= getSoverRootB(total, m750, slideValue, upDown, withBtag)
    sOverRootB1000= getSoverRootB(total, m1000, slideValue, upDown, withBtag)
    sOverRootB2050= getSoverRootB(total, m2050, slideValue, upDown, withBtag)
    sOverRootB3250= getSoverRootB(total, m3250, slideValue, upDown, withBtag)
    if type(sOverRootB750) is float : 
      graphPoints750.append([slideValue, sOverRootB750])
      #print "filled point %f %f into graphPoints750" % ( slideValue, sOverRootB750)
    if type(sOverRootB1000) is float : 
      graphPoints1000.append([slideValue, sOverRootB1000])
      #print "filled point %f %f into graphPoints1000" % ( slideValue, sOverRootB1000)
    if type(sOverRootB2050) is float : 
      graphPoints2050.append([slideValue, sOverRootB2050])
      #print "filled point %f %f into graphPoints2050" % ( slideValue, sOverRootB2050)
    if type(sOverRootB3250) is float : 
      graphPoints3250.append([slideValue, sOverRootB3250])
    #if type(sOverRootB4000) is float : 
    #  graphPoints4000.append([slideValue, sOverRootB2050])

  #  print graphPoints
  #graph4000 = TGraph()
  #for graphPoint4000 in graphPoints4000:
  #  graph4000.SetPoint(graph4000.GetN(), graphPoint4000[0], graphPoint4000[1])
  #  #print "set point in graph4000"

  graph3250 = TGraph()
  graph3250.SetName("optGraph_%s"%name3250)
  for graphPoint3250 in graphPoints3250:
    graph3250.SetPoint(graph3250.GetN(), graphPoint3250[0], graphPoint3250[1])
    #print "set point in graph3250"

  graph2050 = TGraph()
  graph2050.SetName("optGraph_%s"%name2050)
  for graphPoint2050 in graphPoints2050:
    graph2050.SetPoint(graph2050.GetN(), graphPoint2050[0], graphPoint2050[1])
    #print "set point in graph2050"

  graph1000 = TGraph()
  graph1000.SetName("optGraph_%s"%name1000)
  for graphPoint1000 in graphPoints1000:
    graph1000.SetPoint(graph1000.GetN(), graphPoint1000[0], graphPoint1000[1])
    #print "set point in graph1000"

  graph750 = TGraph()
  graph750.SetName("optGraph_%s"%name750)
  for graphPoint750 in graphPoints750:
    graph750.SetPoint(graph750.GetN(), graphPoint750[0], graphPoint750[1])
    #print "set point in graph750"

  #bottomPad_higgswindow.cd()
  #bottomPad_higgswindow.Clear()
  bottomPad_ratio.cd()
  bottomPad_ratio.Clear()
  graph1000.Draw()
  graph1000.GetXaxis().SetLimits(lowerBound, upperBound)
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
  graph1000.GetYaxis().SetTitle("S/#sqrt{B} (a.u.)")
  graph1000.GetYaxis().SetLabelSize(0)
  graph1000.GetXaxis().SetLabelSize(0.1)
  graph1000.GetYaxis().SetTitleSize(0.12)
  graph1000.GetYaxis().SetTitleOffset(.3)
  graph1000.GetXaxis().SetTitle("cut value")
  graph1000.GetXaxis().SetTitleSize(0.12)
  graph1000.GetXaxis().SetTitleOffset(0.65)
  graph1000.SetLineStyle(2)
  graph1000.SetLineWidth(2)
  graph1000.SetLineColor(color1000)
  graph1000.SetFillColor(kWhite)
  graph1000.SetMarkerStyle(20)
  graph1000.SetMarkerSize(0)
  graph2050.Draw("SAME")
  graph2050.SetLineStyle(2)
  graph2050.SetLineWidth(2)
  graph2050.SetLineColor(color2050)
  graph2050.SetFillColor(kWhite)
  graph3250.Draw("SAME")
  graph3250.SetLineStyle(2)
  graph3250.SetLineWidth(2)
  graph3250.SetLineColor(color3250)
  graph3250.SetFillColor(kWhite)
  graph750.Draw("SAME")
  graph750.SetLineStyle(2)
  graph750.SetLineWidth(2)
  graph750.SetLineColor(color750)
  graph750.SetFillColor(kWhite)
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
        for mass in ["750", "1000", "2050", "3250"]:
          if mass in subprim.GetLabel():
            subprim.SetLabel("H#gamma(%r TeV)"%(float(mass)/float(1000)))
            subprim.SetOption("lf")
  can_higgswindow.cd()
  #bottomPad_higgswindow.Draw()
  bottomPad_ratio.Draw()
  pad_higgswindow.SetBorderSize(0)

  
  if withBtag:
    outDirName = "optplots_nMinus1_withBtag_dd_sb%i%i" % (windowEdges[0], windowEdges[1])
    outFileName="%s/%s"%(outDirName, inFileName_higgswindow.split("/")[1])
  else:
    outDirName =  "optplots_nMinus1_noBtag_dd_sb%i%i" % (windowEdges[0], windowEdges[1])
    outFileName="%s/%s"%(outDirName, inFileName_higgswindow.split("/")[1])
  if not path.exists(outDirName):
    makedirs(outDirName)
  outFileName=outFileName.split(".")[0]
  outFile = TFile("%s_%r.root"%(outFileName, upDown), "RECREATE")
  outFile.cd()
  can_higgswindow.Write()
  can_higgswindow.Print("%s_%r.pdf"%(outFileName, upDown))
  outFile.Close()


from sys import argv
if not 3 is len(argv) :
  print "please supply two arguments, with/without btag and the sideband name." 
  exit(1)
if not argv[1] in ["withBtag", "noBtag"] :
  print "invalid first argument: either 'withBtag' or 'noBtag'"
  exit(1)
if not argv[2] in ["100110", "5070", "80100"]:
  print 'invalid second argument, either "100110", "5070", or "80100"'
  exit(1)
withBtag = argv[1]
if argv[2] in "100110":
  windowEdges = [100.0, 110.0]
elif argv[2] in "5070":
  windowEdges = [50.0, 70.0]
elif argv[2] in "80100":
  windowEdges = [80.0, 100.0]

for direction in ["up", "down"]:
  srCans =  []
  srPads =  []
  sbCans =  []
  sbPads =  []
  stacks = []
  sidebands = []
  i=0
  for key in getHiggsRangesDict().keys():
    print "key:", key
    if debugOneVar and not key=="phPtOverMgammaj":
      continue
    # for withBtag / noBtag you need to change the next THREE lines
    sideband_varName    = "stackplots_puppiSoftdrop_nMinus1_%s_sideband%i%i/nMinus1_stack_%s.root"%( withBtag, windowEdges[0], windowEdges[1], key)
    higgswindow_varName = "stackplots_puppiSoftdrop_nMinus1_%s/nMinus1_stack_%s.root"%(withBtag, key)
    makeOpt(sideband_varName, higgswindow_varName, direction, withBtag == "withBtag", srCans, srPads, sbCans, sbPads, stacks, sidebands, i, windowEdges)
    i+=1
  if direction is direction[-1]:
    exit(0)
#for direction in ["up", "down"]:
#  srCans =  []
#  srPads =  []
#  sbCans =  []
#  sbPads =  []
#  stacks = []
#  sidebands = []
#  i=0
#  for key in getHiggsRangesDict().keys():
#    sideband_varName = "stackplots_puppiSoftdrop_nMinus1_noBtag_sideband/nMinus1_stack_%s.root"%key
#    higgswindow_varName = "stackplots_puppiSoftdrop_nMinus1_noBtag/nMinus1_stack_%s.root"%key
#    makeOpt(sideband_varName, higgswindow_varName, direction, False, srCans, srPads, sbCans, sbPads, stacks, sidebands, i)
#    i+=1
#  if direction is direction[-1]:
#    exit(0)
