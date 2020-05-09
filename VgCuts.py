import copy
from ROOT import TCut
# functions to define the selection cuts for H(bb)Gamma 
# John Hakala 7/13/16

def getTaggerWPs():
  return {
      "DDB"   : 0.9,
      "decDDB": 0.9
      }

def getSDmassWindow(analysis):
  if "Zg" in analysis:
    return [80.0, 100.0]
  elif "Hg" in analysis:
    return [110.0, 140.0]
  else:
    print "invalid analysis in VgCuts.getSDmassWindow."
    exit(1)

def getCutValues(analysis, tagger="DDB"):
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
    cutValues["jetPt"]          = 180.0
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
  varKeys["bJet_DDBtag"]             = "btagHolder"
  varKeys["bJet_decDDBtag"]          = "btagHolder"
  varKeys["bJet_csvbb"]              = "btagHolder"
  varKeys["bJet_akx_probHbb"]        = "btagHolder"
  varKeys["bJet_akx_HbbvsQCD"]       = "btagHolder"
  varKeys["bJet_akx_H4qvsQCD"]       = "btagHolder"
  varKeys["bJet_akx_probZbb"]        = "btagHolder"
  varKeys["bJet_akx_probZcc"]        = "btagHolder"
  varKeys["bJet_akx_probZqq"]        = "btagHolder"
  varKeys["bJet_akx_ZvsQCD"]         = "btagHolder"
  varKeys["bJet_akx_ZbbvsQCD"]       = "btagHolder"
  varKeys["bJet_akx_probWcq"]        = "btagHolder"
  varKeys["bJet_akx_probWqq"]        = "btagHolder"
  varKeys["bJet_akx_WvsQCD"]         = "btagHolder"
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
    #window = "higgsWindow"
    #if sideband:
    #  if windowEdges == [100.0,110.0]:
    #    window = "sidebandWindow"
    #  elif windowEdges == [50.0,70.0]:
    #    window = "sideband5070Window"
    #  elif windowEdges == [80.0,100.0]:
    #    window = "sideband80100Window"
    #  elif windowEdges == [30.0,99999.9]:
    #    window = "preselectionWindow"
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

    cuts = {} 
    cuts["phEta"]           = TCut( "leadingPhAbsEta<%f"           % cutValues["phEta"]      )
    cuts["ptOverM"]         = TCut( "phPtOverMgammaj>%f"           % cutValues["ptOverM"]    )
    cuts ["phPt"]           = TCut("leadingPhPt>%f"                % cutValues["phPt"]       )
    cuts ["phPhi"]          = TCut()
    cuts ["t2t1"]           = TCut()
    cuts ["jetPhi"]         = TCut()
    cuts ["jetEta"]         = TCut()
    cuts ["btagHolder"]     = TCut()
    cuts ["cosThetaStar"]   = TCut()
    if useTrigger: 
      cuts["trigger"]         = makeTrigger(analysis)
    if region is "ddboost":
      cuts["turnon"]   = TCut( "phJetInvMass_softdrop>%f"      % cutValues["minInvMass"]     )
      cuts["deltaR"]   = TCut( "phJetDeltaR>%f"              % cutValues["deltaR"]         )
      cuts["jetAbsEta"]       = TCut( "bJet_abseta<%f"         % cutValues["jetAbsEta"]      )
      cuts["btag"]     = TCut( "bJet_DDBtag>%f"                % cutValues["DDB"]            )
      cuts["antibtag"] = TCut( "bJet_DDBtag<%f"                % cutValues["DDB"]            )
      cuts ["jetPt"]          = TCut("bJet_pt>%f"          % cutValues["jetPt"]      )
      #cuts["higgsWindowLow"] = TCut( "higgsPuppi_softdropJetCorrMass>%f"   % cutValues["higgsWindow"][0] )
      #cuts["higgsWindowHi"]  = TCut( "higgsPuppi_softdropJetCorrMass<%f"   % cutValues["higgsWindow"][1] )
      cuts["higgsWindow"]     = makeHiggsWindow(analysis, sideband, windowEdges)
    #elif region is "side5070" or region is "side100110":
    #  if region is "side5070":
    #    index = "Three"
    #  else:
    #    index = "Four"
    #  cuts["turnon"]   = TCut( "phJetInvMass_softdrop_sideLow%s>%f" % (index, cutValues["minInvMass"] ))
    #  cuts["deltaR"]   = TCut( "phJetDeltaR_sideLow%s>%f"         % (index, cutValues["deltaR"]     ))
    #  cuts["jetEta"]   = TCut( "sideLow%sJet_abseta<%f"    % (index, cutValues["jetEta"]     ))
    #  cuts["btag"]     = TCut( "sideLow%sJet_DDBtag>%f"           % (index, cutValues["DDB"]        ))
    #  cuts["antibtag"] = TCut( "sideLow%sJet_DDBtag<%f"           % (index, cutValues["DDB"]        ))
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

