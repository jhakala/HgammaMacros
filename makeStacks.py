from argparse import ArgumentParser
from copy import deepcopy

# new script to make all stackplots.
# John Hakala 7/14/16



if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument("-c", "--cutName", dest="cutName", required=True,
                    help="the set of cuts to apply"                                      )
  parser.add_argument("-a", dest="analysis"  , required=True,
                    help="the analysis in question, either 'Hg' or 'Zg'"                 )
  parser.add_argument("-w", action="store_true", dest="withBtag"  , default=False,
                    help="if -w is used, then apply the btag cut"                        )
  parser.add_argument("-r", action="store_false", dest="showSigs" , default=True,
                    help="if -r is used, then do not show signals overlaid."             )
  parser.add_argument("-s", action="store_true", dest="sideband"  , default=False,
                    help="if -s is used, then look in sideband, not signal window."       )
  parser.add_argument("-f", action="store_true", dest="useScaleFactors" , default=False,
                    help = "use Btagging scalefactors"                                   )
  parser.add_argument("-l", action="store_false", dest="addLines"     , default=True,
                    help = "if -l is used, then do not draw a line at 1 in the ratios"   )
  parser.add_argument("-g", action="store_true", dest="graphics"     , default=False,
                    help = "turn off batch mode"                                         )
  parser.add_argument("-e", dest="edges",     
                    help = "the signal mass window edges: either 100110, 5070, or 80100"  )
  parser.add_argument("-v", action="store_true", dest="vgMC", default=False,     
                    help = "if -v is used, make a stackplot for MC BG limits"            )
  options = parser.parse_args()
  
  
  from pyrootTools import isOrIsNot
  from VgParameters import getDebugVar
  from VgPlotTools import makeAllHists
  dinkoMethod = False
  
  higgsSigBand = [110.0, 140.0]
  zSigBand = [80.0, 100.0] # TODO: double check this against 2016 Zg
  if "Hg" in options.analysis:
    sigBand = higgsSigBand
  elif "Zg" in options.analysis:
    sigBand = zSigBand
  else:
    print "invalid analysis, either 'Hg' or 'Zg'"
    exit(1)
  
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
    #elif options.edges in "80100":
    #  windowEdges = [80.0,100.0]
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
  
  print "Making stackplots for %s cuts." % options.cutName
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
    print "%s being shown in the signal region:" % isOrIsNot(True, "plural"), str(sigBand)
  
  if windowEdges[0] == windowEdges[1]:
    print "something is funny with the windowEdges", windowEdges
    #print "exiting"
    #exit(1)


  if options.vgMC and (not options.useScaleFactors or options.sideband or not options.cutName in ["btag", "antibtag"] ):
    print "vgMC was requested, but something is wrong... you must use scaleFactors, no sideband, and a cut of either 'btag' or 'antibtag'"
    exit(1)
  nonEmptyFilesDict = makeAllHists(options.analysis, options.cutName, options.withBtag, options.sideband, options.useScaleFactors, windowEdges, options.vgMC, options.vgMC, getDebugVar())
  print "done making all histograms. \n"

  print "calling makeStack(%r, %r, %r, %r, %r, %r, %r, %r, %r)" % (options.sideband, options.showSigs, options.addLines, options.useScaleFactors, options.vgMC, options.cutName, options.withBtag, options.analysis, windowEdges)
  from ROOT import gROOT, TColor
  gROOT.SetBatch()
  TColor.SetColorThreshold(0.1)

  from VgStackTools import makeStack
  makeStack(nonEmptyFilesDict, options.sideband, options.showSigs, options.addLines, options.useScaleFactors, options.vgMC, options.cutName, options.withBtag, options.analysis, windowEdges)

  print "done with makeStacks!"
