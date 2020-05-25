from ROOT import SetOwnership
from VgParameters import getRangesDict
from math import sqrt

def whichVarAmI(inFileName):
  for key in getRangesDict().keys():
    if key in inFileName:
      iAm = key
  return iAm

def getSoverRootB(bkg, sig, start, goUpOrDown, withBtag, useMC=False):
  bb=0.
  ss=0.
  if goUpOrDown in "up":
    for iBin in range(bkg.FindBin(start), bkg.GetNbinsX()+1):
      bb+=bkg.GetBinContent(iBin)
      ss+=sig.GetBinContent(iBin)
  elif goUpOrDown in "down":
    for iBin in range(0, bkg.FindBin(start)):
      bb+=bkg.GetBinContent(iBin)
      ss+=sig.GetBinContent(iBin)
  if bb != 0:
    return (ss/sqrt(bb), [ss, bb])
  else:
    return "b=0"

def getSbNorm(stack, sideband, omitData, mode="matchMCsig"):
  if omitData:
    return 1.
  if mode=="matchMCsig":
    return stack.GetStack().Last().GetSumOfWeights()/float(sideband.GetSumOfWeights())

def getLabel(sideband):
  if sideband:
    return "sideband"
  else:
    return "higgswindow"
  

def getCanvas(inFile, i, sideband=False, debug=False):
  label = getLabel(sideband)
  if debug:
    print "inFile.GetName()", inFile.GetName()
  for key in inFile.GetListOfKeys():
    if debug:
      print "can_%s has key:", (label, key.GetName())
    if "c1" in key.GetName():
      #can = inFile.Get(key.GetName()).DrawClone()
      can = inFile.Get(key.GetName())
      can.SetName("%i_%s_c1_%s" % (i, inFile.GetName(), label))
      for prim in can.GetListOfPrimitives():
        if debug:
          print "  can_%s has primitive: %s" % (label, prim.GetName())
        newPrimName = "%i_%s_%s" % (i, prim.GetName(), label)
        prim.SetName(newPrimName)
        if debug:
          print "  -> new name is: ", prim.GetName()
      SetOwnership(can, False)
      return can

def getTopPad(inFileName, i, can, sideband=False, debug=False):
  label = getLabel(sideband)
  for prim in can.GetListOfPrimitives():
    if sideband:
      prim.SetName("%i_%s_sideband" % (i, prim.GetName()))

    if "stack" in prim.GetName():
      pad = prim
      for primitive in pad.GetListOfPrimitives():
        if not ("TLine" in primitive.IsA().GetName() or "TFrame" in primitive.IsA().GetName()):
          primitive.SetName("%s_%s_%s" % (inFileName, primitive.GetName(), label))
      SetOwnership(pad, False)
      return pad

def getRatioPad(inFileName, i, can, sideband=False, debug=False):
  label = getLabel(sideband)
  for prim in can.GetListOfPrimitives():
    if "ratio" in prim.GetName():
      pad_ratio = prim
      for primitive in pad_ratio.GetListOfPrimitives():
        if not ("TLine" in primitive.IsA().GetName() or "TFrame" in primitive.IsA().GetName()):
          primitive.SetName("%s_%s_%s" % (inFileName, primitive.GetName(), label))
      SetOwnership(pad_ratio, False)
      return pad_ratio

def getPlots(higgsWindowFile, sidebandFile, i, debug=False):
  can_higgswindow = getCanvas(higgsWindowFile , i, False , debug)
  can_sideband    = getCanvas(sidebandFile    , i, True  , debug)

  pad_higgswindow = getTopPad(higgsWindowFile.GetName() , i, can_higgswindow, debug)
  pad_sideband    = getTopPad(sidebandFile.GetName()    , i, can_sideband   , debug)

  bottomPad_sideband = getRatioPad(sidebandFile.GetName(), i, can_sideband, debug)
  return can_higgswindow, pad_higgswindow, can_sideband, pad_sideband, bottomPad_sideband
