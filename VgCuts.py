import copy
from ROOT import TCut
# functions to define the selection cuts for H(bb)Gamma 
# John Hakala 7/13/16

def getTagger(analysis):
  if "Hg" in analysis:
    return "akx_HbbvsQCD"
  elif "Zg" in analysis:
    return "akx_ZvsQCD"

def getTaggerWPs():
  #TODO TODO find good cut values
  return {
      "DDB"            : 0.9,
      "decDDB"         : 0.9,
      "akx_HbbvsQCD"   : 0.9,
      "akx_ZvsQCD"     : 0.9
      }

def getSDmassWindow(analysis):
  if "Zg" in analysis:
    return [80.0, 100.0]
  elif "Hg" in analysis:
    return [110.0, 140.0]
  else:
    print "invalid analysis in VgCuts.getSDmassWindow."
    exit(1)

def getCutValues(analysis):
  tagger = getTagger(analysis)
  cutValues = {}
  cutValues["minInvMass"]     = 700.0
  #cutValues["minInvMass"]     = 500.0
  cutValues["phEta"]          = 1.4442
  cutValues["phPt"]           = 200.0
  cutValues["jetAbsEta"]      = 2.2
  cutValues["deltaR"]         = 1.1
  cutValues["ptOverM"]        = 0.35
  cutValues[tagger]            = getTaggerWPs()[tagger]
  if "Hg" in analysis:
    cutValues["jetPt"]          = 250.0
  elif "Zg" in analysis:
    cutValues["jetPt"]          = 225.0
  else:
    print "invalid analysis for HgCuts, either 'Hg' or 'Zg'"
    exit(1)
  #cutValues["higgsWindow"]    = [110.0, 140.0]
  #cutValues["sidebandWindow"] = [100.0, 110.0]
  #cutValues["sideband5070Window"] = [50.0, 70.0]
  #cutValues["sideband80100Window"] = [80.0, 100.0]
  #cutValues["preselectionWindow"] = [30.0, 99999.9]
  return cutValues


def combineCuts(cutDict):
  combinedCut = TCut()
  for cut in cutDict.keys():
    combinedCut += cutDict[cut]
  return combinedCut

def getVarKeys():
  varKeys = {}
  varKeys["bJett2t1"]                = "t2t1"
  varKeys["bJet_DDBtag"]             = "unused"
  varKeys["bJet_decDDBtag"]          = "unused"
  varKeys["bJet_csvbb"]              = "unused"
  varKeys["bJet_akx_probHbb"]        = "unused"
  varKeys["bJet_akx_HbbvsQCD"]       = "btagHolder"
  varKeys["bJet_akx_H4qvsQCD"]       = "unused"
  varKeys["bJet_akx_probZbb"]        = "unused"
  varKeys["bJet_akx_probZcc"]        = "unused"
  varKeys["bJet_akx_probZqq"]        = "unused"
  varKeys["bJet_akx_ZvsQCD"]         = "btagHolder"
  varKeys["bJet_akx_ZbbvsQCD"]       = "unused"
  varKeys["bJet_akx_probWcq"]        = "unused"
  varKeys["bJet_akx_probWqq"]        = "unused"
  varKeys["bJet_akx_WvsQCD"]         = "unused"
  varKeys["bJet_akxDec_H4qvsQCD"]    = "unused"
  varKeys["bJet_akxDec_HbbvsQCD"]    = "unused"
  varKeys["bJet_akxDec_WvsQCD"]      = "unused"
  varKeys["bJet_akxDec_ZHbbvsQCD"]   = "unused"
  varKeys["bJet_akxDec_ZHccvsQCD"]   = "unused"
  varKeys["bJet_akxDec_ZbbvsQCD"]    = "unused"
  varKeys["bJet_akxDec_ZvsQCD"]      = "unused"
  varKeys["bJet_akxDec_bbvsLight"]   = "unused"
  varKeys["bJet_akxDec_probHbb"]     = "unused"
  varKeys["bJet_akxDec_probHcc"]     = "unused"
  varKeys["bJet_akxDec_probHqqqq"]   = "unused"
  varKeys["bJet_akxDec_probWcq"]     = "unused"
  varKeys["bJet_akxDec_probWqq"]     = "unused"
  varKeys["bJet_akxDec_probZbb"]     = "unused"
  varKeys["bJet_akxDec_probZcc"]     = "unused"
  varKeys["bJet_akxDec_probZqq"]     = "unused"
  varKeys["cosThetaStar"]            = "cosThetaStar"
  varKeys["phPtOverMgammaj"]         = "ptOverM"
  varKeys["leadingPhEta"]            = "phEta"
  varKeys["leadingPhPhi"]            = "phPhi"
  varKeys["leadingPhPt"]             = "phPt"
  varKeys["leadingPhAbsEta"]         = "phEta"
  varKeys["phJetInvMass_softdrop"]   = "turnon"
  varKeys["phJetDeltaR"]             = "deltaR"
  varKeys["bJet_abseta"]             = "jetAbsEta"
  varKeys["bJet_eta"]                = "jetEta"
  varKeys["bJet_phi"]                = "jetPhi"
  varKeys["bJet_pt"]                 = "jetPt"
  varKeys["softdropJetCorrMass"]     = "higgsWindow"
  return varKeys

def makeHiggsWindow(analysis, sideband=False, windowEdges=[100.0,110.0]):
    #print "makeHiggsWindow got sideband =", sideband, "and windowEdges =", windowEdges
    cutValues = getCutValues(analysis)
    cuts = {}
    cuts["higgsWindowLow"] = TCut( "softdropJetCorrMass>%f"   % windowEdges[0] )
    cuts["higgsWindowHi"]  = TCut( "softdropJetCorrMass<%f"   % windowEdges[1] )
    #print "will return combineCuts(cuts)=", combineCuts(cuts)
    return combineCuts(cuts)

def makeTrigger(analysis, which = "OR"):
  # TODO TODO fix this "which = OR" business
  cutValues = getCutValues(analysis)
  cuts = {}
  if which == "OR":
    #cuts["trigger"] = TCut( "triggerFired_175 > 0.5 || triggerFired_165HE10 > 0.5" )
    cuts["trigger"] = TCut( "triggerFired_200 > 0.5" )
  return combineCuts(cuts)
    

def getDefaultCuts(analysis, region, useTrigger, sideband=False, windowEdges=[100.0,110.0]):
    cutValues = getCutValues(analysis)
    tagger = getTagger(analysis)

    cuts = {} 
    cuts["phEta"]           = TCut( "leadingPhAbsEta<%f"           % cutValues["phEta"]      )
    cuts["ptOverM"]         = TCut( "phPtOverMgammaj>%f"           % cutValues["ptOverM"]    )
    cuts ["phPt"]           = TCut("leadingPhPt>%f"                % cutValues["phPt"]       )
    cuts ["phPhi"]          = TCut()
    cuts ["t2t1"]           = TCut()
    cuts ["jetPhi"]         = TCut()
    cuts ["jetEta"]         = TCut()
    cuts ["btagHolder"]     = TCut()
    cuts ["unused"]         = TCut()
    cuts ["cosThetaStar"]   = TCut()
    if useTrigger: 
      cuts["trigger"]         = makeTrigger(analysis)
    if region is "ddboost":
      cuts["turnon"]   = TCut( "phJetInvMass_softdrop>%f"      % cutValues["minInvMass"]     )
      cuts["deltaR"]   = TCut( "phJetDeltaR>%f"              % cutValues["deltaR"]         )
      cuts["jetAbsEta"]       = TCut( "bJet_abseta<%f"         % cutValues["jetAbsEta"]      )
      cuts["btag"]     = TCut( "bJet_%s>%f"                % (getTagger(analysis), cutValues[tagger]) )
      cuts["antibtag"] = TCut( "bJet_%s<%f"                % (getTagger(analysis), cutValues[tagger]) )
      #if "Zg" in analysis:
      #  cuts["btag"]     = TCut( "bJet_%s>%f"                % cutValues[tagger]            )
      #  cuts["antibtag"] = TCut( "bJet_%s<%f"                % cutValues[tagger]            )
      cuts ["jetPt"]          = TCut("bJet_pt>%f"          % cutValues["jetPt"]      )
      cuts["higgsWindow"]     = makeHiggsWindow(analysis, sideband, windowEdges)
    else:
      print "Invalid region!!!"
      quit()
    return cuts
    
def getBtagComboCut(analysis, region, useTrigger, sideband=False, scaleFactors=False, windowEdges=[100,110]):
    if windowEdges == "signalRegion":
      windowEdges = getSDmassWindow(analysis)
    btagCuts = copy.deepcopy(getDefaultCuts(analysis, region, useTrigger, sideband, windowEdges))
    btagCuts.pop("antibtag")
    if scaleFactors:
      btagCuts.pop("btag")
    return combineCuts(btagCuts)

def getAntiBtagComboCut(analysis, region, useTrigger, sideband=False, scaleFactors=False, windowEdges=[100.0,110.0]):
    if windowEdges == "signalRegion":
      windowEdges = getSDmassWindow(analysis)
    antibtagCuts = copy.deepcopy(getDefaultCuts(analysis, region, useTrigger, sideband, windowEdges))
    antibtagCuts.pop("btag")
    if scaleFactors:
      antibtagCuts.pop("antibtag")
    return combineCuts(antibtagCuts)

def getNoBtagComboCut(analysis, region, useTrigger, sideband=False, windowEdges=[100.0,110.0]):
    if windowEdges == "signalRegion":
      windowEdges = getSDmassWindow(analysis)
    nobtagCuts = copy.deepcopy(getDefaultCuts(analysis, region, useTrigger, sideband, windowEdges))
    nobtagCuts.pop("btag")
    nobtagCuts.pop("antibtag")
    return combineCuts(nobtagCuts)

def getNminus1ComboCut(analysis, region, popVar, withBtag, useTrigger, sideband=False, windowEdges=[100.0,110.0]):
    if windowEdges == "signalRegion":
      windowEdges = getSDmassWindow(analysis)
    nobtagCuts = copy.deepcopy(getDefaultCuts(analysis, region, useTrigger, sideband, windowEdges))
    nobtagCuts.pop("antibtag")
    if not withBtag:
      nobtagCuts.pop("btag")
    if not "SF" in popVar and not "weightFactor" in popVar and not "mcWeight" in popVar:
      nobtagCuts.pop(getVarKeys()[popVar])
    return combineCuts(nobtagCuts)

def getPreselectionComboCut(analysis, region, useTrigger, sideband=False, windowEdges=[30.0,99999.9] ):
    preselectionCuts = copy.deepcopy(getDefaultCuts(analysis, region, useTrigger, sideband, windowEdges))
    preselectionCuts.pop("phEta")
    preselectionCuts.pop("ptOverM")
    preselectionCuts.pop("turnon")
    preselectionCuts.pop("btag")
    preselectionCuts.pop("antibtag")
    preselectionCuts.pop("jetAbsEta")
    return combineCuts(preselectionCuts)

def shouldBlind(cutName, sideband, windowEdges):
  blindData = True

  if cutName=="preselection" or sideband:
    blindData       = False
  else:
    blindData    = True
  
  if windowEdges == "signalRegion":
    blindData = True

  return blindData
